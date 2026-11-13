import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
EXE = "build_game/ResistanceFoMGame.exe"
PDB = "build_game/ResistanceFoMGame.pdb"
BACKUP = "backup-mod-menu-v2"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def closed():
    output = subprocess.check_output(["tasklist.exe", "/FO", "CSV", "/NH"], text=True, errors="replace")
    if any(f'"{name}"' in output.lower() for name in ("resistancefom.exe", "resistancefomgame.exe", "launcher.exe")):
        raise ValueError("Feche o Resistance e o Launcher antes de continuar.")


def prepare(port, stage):
    patch = json.loads((PACKAGE / "patch.json").read_text(encoding="utf-8"))
    if (port / "VERSION").read_text().strip() != "0.2.3-beta":
        raise ValueError("Esta versão do mod requer o porte Windows 0.2.3-beta.")
    if sha((port / "game/game.elf").read_bytes()) != patch["game_elf_sha256"]:
        raise ValueError("A edição do jogo não corresponde a BCUS98107 v1.00.")
    manifest = {EXE: sha((port / EXE).read_bytes())}
    added = []
    for name, spec in patch["files"].items():
        src = port / name
        dst = stage / "modified" / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        if "new" in spec:
            if src.exists():
                raise ValueError(f"Já existe outro mod ou instalação em {name}.")
            data = spec["new"].encode("utf-8")
            added.append(name)
        else:
            current = src.read_bytes()
            source = current.decode("utf-8").replace("\r\n", "\n")
            if sha(source.encode("utf-8")) != spec["base_sha256"]:
                raise ValueError(f"Arquivo incompatível ou já modificado: {name}.")
            lines = source.splitlines()
            for start, count, insertion in reversed(spec["edits"]):
                lines[start:start + count] = insertion
            data = ("\n".join(lines) + "\n").encode("utf-8")
            manifest[name] = sha(current)
        if sha(data) != spec["final_sha256"]:
            raise ValueError(f"O pacote não reproduziu a versão esperada de {name}.")
        dst.write_bytes(data)
    (stage / "installed-sha256.json").write_text(json.dumps(manifest), encoding="utf-8")
    return manifest, added


def restore(port, backup, entries):
    for name, existed in entries.items():
        dst = port / name
        if existed:
            shutil.copy2(backup / name, dst)
        else:
            dst.unlink(missing_ok=True)


def install(port):
    backup = port / BACKUP
    if backup.exists():
        raise ValueError("Já existe uma instalação ou cópia de segurança. Execute Remover.cmd primeiro.")
    with tempfile.TemporaryDirectory(prefix="rfom-mod-menu-") as work:
        stage = Path(work)
        manifest, added = prepare(port, stage)
        closed()
        print("Compilando os arquivos alterados. Aguarde a conclusão.", flush=True)
        subprocess.run([str(PACKAGE / "build-staged.cmd"), str(port), str(stage)], check=True)
        closed()
        for name, expected in manifest.items():
            if sha((port / name).read_bytes()) != expected:
                raise ValueError(f"Arquivo alterado durante a compilação: {name}.")
        if any((port / name).exists() for name in added):
            raise ValueError("Um arquivo do mod apareceu durante a compilação.")
        paths = [name for name in manifest if name != EXE] + added + [PDB, EXE]
        entries = {name: (port / name).is_file() for name in paths}
        backup.mkdir()
        try:
            for name, existed in entries.items():
                if existed:
                    dst = backup / name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(port / name, dst)
            (backup / "files.json").write_text(json.dumps(entries), encoding="utf-8")
        except Exception:
            shutil.rmtree(backup)
            raise
        try:
            for name in paths:
                source = stage / (name if name in (EXE, PDB) else "modified/" + name)
                shutil.copy2(source, port / name)
                if sha(source.read_bytes()) != sha((port / name).read_bytes()):
                    raise ValueError(f"Falha na cópia de {name}.")
        except Exception:
            restore(port, backup, entries)
            shutil.rmtree(backup)
            raise
    print("Mod menu v2 instalado. Abra a campanha e pressione Ctrl + F2.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--remover", action="store_true")
    parser.add_argument("pasta", nargs="?")
    args = parser.parse_args()
    folder = args.pasta or input("Cole o caminho da pasta do porte (onde fica Launcher.exe): ")
    if not folder.strip():
        raise ValueError("Informe a pasta do porte.")
    port = Path(folder.strip().strip('"')).resolve(strict=True)
    if not (port / "Launcher.exe").is_file():
        raise ValueError("Selecione a pasta principal do porte, onde fica Launcher.exe.")
    closed()
    if args.remover:
        backup = port / BACKUP
        entries = json.loads((backup / "files.json").read_text(encoding="utf-8"))
        patch = json.loads((PACKAGE / "patch.json").read_text(encoding="utf-8"))
        if set(entries) != set(patch["files"]) | {EXE, PDB}:
            raise ValueError("O manifesto da cópia de segurança é incompatível.")
        restore(port, backup, entries)
        shutil.rmtree(backup)
        print("Arquivos originais restaurados.")
    else:
        install(port)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Falha: {error}", file=sys.stderr)
        sys.exit(1)

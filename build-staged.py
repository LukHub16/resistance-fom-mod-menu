import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def run(tool, args, cwd):
    subprocess.run([str(tool), *args], cwd=cwd, check=True,
                   creationflags=subprocess.BELOW_NORMAL_PRIORITY_CLASS)


def ninja_attributes(lines, start):
    attrs = {}
    for line in lines[start + 1:]:
        if not line.startswith("  "):
            break
        key, value = line.strip().split(" = ", 1)
        attrs[key] = value
    return attrs


def build_staged(port, stage, reuse):
    manifest = json.loads((stage / "installed-sha256.json").read_text(encoding="utf-8"))
    for name, expected in manifest.items():
        if hashlib.sha256((port / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"The installed version changed: {name}")

    active = port / "build_game"
    build = (active / "build.ninja").read_text(encoding="utf-8").splitlines()
    llvm = Path(r"C:\Program Files\LLVM\bin")
    result = stage / "build_game"
    result.mkdir(exist_ok=True)
    replacements = {}
    for source in manifest:
        if not source.endswith(".cpp"):
            continue
        source_file = stage / "modified" / source
        name = source_file.name
        i = next(i for i, line in enumerate(build)
                 if line.startswith("build CMakeFiles\\ResistanceFoMGame.dir\\")
                 and f"\\{name}.obj: CXX_COMPILER__" in line)
        obj = build[i].split(": ", 1)[0].removeprefix("build ")
        settings = ninja_attributes(build, i)
        dest = result / f"{name}.obj"
        matched = next((prior for prior in reuse if (prior / "modified" / source).is_file()
                        and (prior / "build_game" / f"{name}.obj").is_file()
                        and source_file.read_bytes() == (prior / "modified" / source).read_bytes()
                        and all((prior / "modified/project" / header.name).is_file()
                                and header.read_bytes() == (prior / "modified/project" / header.name).read_bytes()
                                for header in (stage / "modified/project").glob("*.h")
                                if f'"{header.name}"' in source_file.read_text(encoding="utf-8"))), None)
        if matched:
            replacements[obj] = matched / "build_game" / f"{name}.obj"
            continue
        flags = settings["FLAGS"].split()
        flags[flags.index("/Zi")] = "/Z7"
        print(f"Compiling {name}", flush=True)
        run(llvm / "clang-cl.exe", ["/nologo", "/TP", *settings.get("DEFINES", "").split(),
            *settings["INCLUDES"].split(), *flags, "/c", f"/Fo{dest}", str(source_file)], result)
        replacements[obj] = dest

    i = next(i for i, line in enumerate(build) if line.startswith("build ResistanceFoMGame.exe:"))
    objects = build[i].split(" | ", 1)[0].split()[3:]
    if not set(replacements).issubset(objects):
        raise ValueError("The linker input is missing one or more changed objects")
    settings = ninja_attributes(build, i)
    flags = [flag for flag in settings["LINK_FLAGS"].split() if flag != "/INCREMENTAL"]
    libs = [str(active / item) if item.startswith("ps3recomp_sdk\\") else item
            for item in settings["LINK_LIBRARIES"].split()]
    original_manifest = active / settings["OBJECT_DIR"] / "embed.manifest"
    response = result / "link.rsp"
    args = ["/nologo", *flags, "/MANIFEST:EMBED", f"/MANIFESTINPUT:{original_manifest}",
            f"/out:{result / 'ResistanceFoMGame.exe'}", f"/pdb:{result / 'ResistanceFoMGame.pdb'}",
            *(str(replacements.get(obj, active / obj)) for obj in objects), *libs]
    response.write_text(subprocess.list2cmdline(args), encoding="utf-8")
    print("Linking the staged executable", flush=True)
    run(llvm / "lld-link.exe", [f"@{response}"], result)
    data = (result / "ResistanceFoMGame.exe").read_bytes()
    for label in ("Sem recarga", "Arc Charger sem aquecer"):
        if label.encode("utf-16-le") + b"\x00\x00" not in data:
            raise ValueError(f"Missing menu entry in the staged executable: {label}")
    if not any(label.encode("utf-16-le") + b"\x00\x00" in data
               for label in ("Salto prolongado", "Salto prolongado (teste)")):
        raise ValueError("Missing longer jump menu entry")
    if not any(label.encode("utf-16-le") + b"\x00\x00" in data
               for label in ("Cadência do tiro", "Tiro rápido")):
        raise ValueError("Missing cadence menu entry")
    (result / "ResistanceFoMGame.sha256").write_text(hashlib.sha256(data).hexdigest() + "\n", encoding="ascii")
    print("Staged executable verified", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=Path)
    parser.add_argument("stage", type=Path)
    parser.add_argument("reuse", type=Path, nargs="*")
    args = parser.parse_args()
    build_staged(args.port.resolve(), args.stage.resolve(), [path.resolve() for path in args.reuse])

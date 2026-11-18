# Resistance: Fall of Man Mod Menu v2

Mod menu em PT-BR para a campanha de **Resistance: Fall of Man Recomp** no Windows. Inclui noclip, câmera livre, hit kill, voo ao segurar o pulo, salto prolongado, velocidade de caminhada e cadência ajustáveis, além do seletor de armas e dos controles de vida e munição.

## Downloads

- [Baixar o mod menu v2 em ZIP](https://github.com/LukHub16/resistance-fom-mod-menu/archive/refs/heads/main.zip)
- [Baixar o instalador do porte Windows 0.2.3-beta](https://github.com/miroslavdanutalexandru-alt/Resistance-Fall-of-Man-Recomp/releases/download/v0.2.3-beta/ResistancePort-Setup-0.2.3-beta.exe)
- [Ver os arquivos e instruções do porte compatível](https://github.com/miroslavdanutalexandru-alt/Resistance-Fall-of-Man-Recomp/releases/tag/v0.2.3-beta)

O ZIP do mod contém o instalador, o removedor e o patch de código. Para instalar, você precisa preparar sua própria cópia **BCUS98107 v1.00** com o Setup do porte e concluir a compilação original. O jogo e os arquivos gerados são fornecidos pela sua instalação local.

## Compatibilidade

- Porte Windows **0.2.3-beta** de **miroslavdanutalexandru-alt**, instalado e compilado pelo Setup do próprio porte. [Projeto original](https://github.com/miroslavdanutalexandru-alt/Resistance-Fall-of-Man-Recomp)
- Cópia americana do jogo **BCUS98107 v1.00**. O instalador confere o jogo e os arquivos do porte antes de alterar a instalação.
- O pacote inclui scripts e alterações de código. A compilação acontece no seu PC e usa o Python e as ferramentas de compilação do porte.
- O instalador usa o Python 3.9 ou superior disponível como `python`, o Visual Studio Build Tools com as ferramentas C++ x64 e o LLVM em `C:\Program Files\LLVM\bin`. O Setup do porte deve gerar a pasta `build_game`, incluindo `build.ninja` e os arquivos de compilação. Mantenha essas ferramentas disponíveis até terminar a instalação do mod.

## Como baixar e instalar

1. Baixe o ZIP pelo link **Baixar o mod menu v2** acima, ou clique no botão verde **Code** e depois em **Download ZIP**.
2. No Explorador do Windows, clique com o botão direito no ZIP e escolha **Extrair tudo**.
3. Salve a partida e feche o jogo e o **Launcher.exe**.
4. Abra a pasta extraída e dê dois cliques em **Instalar.cmd**.
5. Quando aparecer o pedido, cole o caminho da pasta onde está **Launcher.exe** e pressione **Enter**. Exemplo `C:\Games\ResistancePort`.
6. Espere aparecer **Mod menu v2 instalado**. Em seguida, abra o jogo, entre na campanha e pressione **Ctrl + F2**.

Se aparecer **Arquivo incompatível ou já modificado**, use uma instalação original da versão indicada. Se o Windows indicar que o Python ou as ferramentas de compilação estão faltando, conclua primeiro o Setup do porte.

## Funções e testes

- Vida infinita, munição do carregador, reserva, tiro secundário e granadas.
- Cadência de tiro ajustável e controles das armas, incluindo seletor e tratamento de aquecimento da Arc Charger.
- Velocidade de caminhada ajustável, voo ao segurar o pulo e salto prolongado.
- Noclip, câmera livre e hit kill.

O autor relatou funcionamento dessas mecânicas durante os testes de sua campanha. A instalação foi conferida por compilação e comparação dos arquivos, e a restauração foi verificada em uma instalação simulada. A compatibilidade é limitada à combinação de porte e edição indicada acima. As armas Arc Charger e Reapers podem apresentar limitações na troca pela roda de armas em certos trechos da campanha.

## Controles

| Função | Como usar |
| --- | --- |
| Menu | **Ctrl + F2** na campanha |
| Noclip | **Home** liga e **End** desliga no local atual. **WASD** move, **Espaço** sobe e **C** desce. Ao desligar no ar, a gravidade volta a agir. |
| Câmera livre | Ative no menu. **WASD** move, **mouse** ou **setas** giram, **Espaço** sobe, **C** desce e **Shift** acelera. |
| Voo ao segurar o pulo | Ative no menu e segure o botão de pulo no ar. |
| Hit kill | Ative no menu. O dano elevado também pode atingir aliados ou objetos que recebem dano. |

## Como remover

1. Feche o jogo e o Launcher.
2. Abra **Remover.cmd** na pasta extraída e informe o mesmo caminho do porte.
3. O script restaura os arquivos da pasta **backup-mod-menu-v2**. Preserve essa pasta enquanto usar o mod.

## Créditos

Porte de Windows por **miroslavdanutalexandru-alt**, a partir da recompilação original de **Psyykosis**. Os pontos de vida e munição aproveitam a pesquisa de **bungholio** e **hyper2k**, publicada no [projeto ArtemisPS3](https://github.com/bucanero/ArtemisPS3). [Proposta do mod menu no repositório do porte](https://github.com/miroslavdanutalexandru-alt/Resistance-Fall-of-Man-Recomp/issues/6).

---
date:
  created: 2026-07-07
readtime: 6
categories:
  - Tecnologia
tags:
  - opencode
  - termux
  - proot-distro
  - linux
  - celular
authors:
  - luciodias
slug: usando-opencode-no-celular-com-termux
---

# Usando o OpenCode no celular com Termux

O OpenCode é um assistente de programação via terminal que roda direto no CLI. E sim, ele funciona no celular.

<!-- more -->

## O que é o Termux

Termux é um emulador de terminal para Android que também fornece um ambiente Linux mínimo. Ele não precisa de root e dá acesso a um gerenciador de pacotes (APT), shell Bash, Python, Git, SSH e centenas de outras ferramentas nativas. Basicamente, transforma seu celular num ambiente de desenvolvimento portátil.

A instalação é simples: baixe o APK pelo [F-Droid](https://f-droid.org/packages/com.termux/) (recomendado, versão mais atualizada) ou pelo GitHub. Depois de abrir, rode:

```bash
pkg update && pkg upgrade
pkg install python git
```

Pronto. Você já tem Python e Git funcionando.

## Por que o proot-distro é necessário

O Termux tem uma limitação importante: por questões de segurança do Android (SELinux, isolamento de processos), ele não consegue acessar certas chamadas de sistema que programas comuns esperam. Isso significa que algumas ferramentas podem falhar ou se comportar de forma inesperada.

O **proot-distro** resolve isso. Ele usa `proot` para simular um ambiente chroot sem precisar de root. Com ele, você instala distribuições Linux completas (Ubuntu, Debian, Arch) dentro do Termux, com acesso a chamadas de sistema reais e um sistema de arquivos isolado.

Para instalar:

```bash
pkg install proot-distro
proot-distro install ubuntu
proot-distro login ubuntu
```

Dentro da distro, você tem um ambiente Ubuntu praticamente completo. É lá que o OpenCode roda sem problemas.

## Instalando o OpenCode

Dentro do Ubuntu via proot-distro:

```bash
apt update && apt upgrade -y
apt install python3 python3-pip git -y
pip install opencode
```

Depois é só usar:

```bash
opencode
```

## Como é a experiência no dia a dia

A session típica funciona assim:

1. Abra o Termux
2. Rode `proot-distro login ubuntu`
3. Navegue até seu projeto com `cd`
4. Execute `opencode` e comece a programar

O teclado virtual do celular é o ponto mais desconfortável — um teclado físico Bluetooth ou um cliente SSH do computador ajuda muito. Fora isso, a performance é surpreendentemente boa em dispositivos com 4 GB de RAM ou mais.

## Considerações finais

Usar o OpenCode no celular com Termux + proot-distro é uma forma prática de ter um ambiente de desenvolvimento completo no bolso. Não substitui um desktop para trabalho pesado, mas é excelente para experimentos, correções rápidas e aprendizado em qualquer lugar.

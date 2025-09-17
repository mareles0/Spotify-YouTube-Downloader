# 🎵 Spotify & 🎬 YouTube Downloader

Aplicação **desktop em Python** com interface moderna (**CustomTkinter**) para baixar músicas do **Spotify** (via YouTube) e vídeos do **YouTube** (com suporte a **upscaling até 4K 60fps**).

---

## ✨ Funcionalidades

- **Spotify**
  - Baixe **músicas individuais** ou **playlists inteiras**.
  - Progresso detalhado: mostra **i/total** e **porcentagem**.
  - Arquivos exportados em **MP3** (192 kbps).
  - Playlists podem ser exportadas como `.zip`.

- **YouTube**
  - Baixe vídeos ou playlists inteiras.
  - Escolha entre **MP3** (áudio) ou **MP4** (vídeo).
  - Resoluções disponíveis:
    - 240p, 360p, 480p, 720p, 720p 60fps, 1080p, 1080p 60fps, 4K, 4K 60fps
  - **Upscaling automático** via FFmpeg.
  - Progresso detalhado: **i/total** e **porcentagem**.
  - Áudio convertido para **AAC** (corrige bug com OPUS).

- **Interface**
  - Moderna e amigável com **CustomTkinter**.
  - Botão **Parar** funciona tanto em downloads quanto em upscaling.
  - Botões de **procurar pasta** para salvar arquivos.

---

## 🚀 Instalação

### Pré-requisitos

- [Python 3.9+](https://www.python.org/downloads/)
- [FFmpeg](https://ffmpeg.org/download.html) instalado e disponível no **PATH**
- Conta Spotify Developer (para gerar **Client ID** e **Client Secret**)

### Clonar o repositório

```bash
git clone https://github.com/mareles0/Spotify-YouTube-Downloader/blob/main/README.md
cd Spotify-YouTube-Downloader

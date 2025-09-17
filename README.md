# 🎵 Spotify & 🎬 YouTube Downloader

Aplicação **desktop em Python** com interface moderna (**CustomTkinter**) para baixar músicas do **Spotify** (via YouTube) e vídeos do **YouTube** (com suporte a **upscaling até 4K 60fps**).

## ✨ Funcionalidades

### Spotify
- Baixe **músicas individuais** ou **playlists inteiras**
- Progresso detalhado: mostra **i/total** e **porcentagem**
- Arquivos exportados em **MP3** (192 kbps)
- Playlists podem ser exportadas como `.zip`

### YouTube
- Baixe vídeos ou playlists inteiras
- Escolha entre **MP3** (áudio) ou **MP4** (vídeo)
- Resoluções disponíveis:
  - 240p, 360p, 480p
  - 720p, 720p 60fps
  - 1080p, 1080p 60fps
  - 4K, 4K 60fps
- **Upscaling automático** via FFmpeg
- Progresso detalhado: **i/total** e **porcentagem**
- Áudio convertido para **AAC** (corrige bug com OPUS)

### Interface
- Moderna e amigável com **CustomTkinter**
- Botão **Parar** funciona tanto em downloads quanto em upscaling
- Botões de **procurar pasta** para salvar arquivos

## 🚀 Instalação

### Pré-requisitos
- [Python 3.9+](https://www.python.org/downloads/)
- [FFmpeg](https://ffmpeg.org/download.html) instalado e disponível no **PATH**
- Conta Spotify Developer (para gerar **Client ID** e **Client Secret**)

### Passos de Instalação

1. Clone o repositório
```bash
git clone https://github.com/mareles0/Spotify-YouTube-Downloader.git
cd Spotify-YouTube-Downloader
```

2. Crie um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 🔑 Configuração das Credenciais Spotify

1. Acesse o [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Crie um App e copie o Client ID e Client Secret
3. Na raiz do projeto, crie um arquivo `.env`:
```bash
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
```

## ▶️ Uso

1. Inicie a aplicação:
```bash
python app.py
```

2. A interface gráfica será aberta com duas abas:
   - **Spotify**: inserir link de playlist ou música
   - **YouTube**: inserir link de vídeo ou playlist, selecionar formato e resolução

## ⚡ Tecnologias Utilizadas

- **Python**: linguagem de programação base
- **yt-dlp**: download de vídeos/áudios
- **Spotipy**: integração com Spotify API
- **FFmpeg**: conversão e upscaling de vídeos
- **CustomTkinter**: UI moderna
- **python-dotenv**: variáveis de ambiente

## 📜 Licença

Este projeto é de uso livre para fins educacionais e pessoais.
Não deve ser utilizado para violar os termos de serviço do Spotify/YouTube.
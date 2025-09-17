import os
import shutil
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from tkinter import messagebox
import core.utils as utils


def get_spotify_client():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise Exception("Credenciais Spotify não encontradas. Configure SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET.")

    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def get_track_info(track_url):
    sp = get_spotify_client()
    track_id = track_url.split('/')[-1].split('?')[0]
    track = sp.track(track_id)
    return f"{track['name']} - {track['artists'][0]['name']}"


def get_playlist_tracks(playlist_url):
    sp = get_spotify_client()
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    while results:
        for item in results['items']:
            track = item['track']
            if track:
                tracks.append(f"{track['name']} - {track['artists'][0]['name']}")
        results = sp.next(results) if results.get('next') else None
    return tracks


def spotify_download_playlist(url, download_path, prog_bar, prog_label):
    os.makedirs(download_path, exist_ok=True)
    try:
        tracks = get_playlist_tracks(url)
    except Exception as e:
        messagebox.showerror("Erro", f"Spotify: Não foi possível obter a playlist. {e}")
        return

    total = len(tracks)
    if total == 0:
        messagebox.showwarning("Aviso", "Spotify: Nenhuma música encontrada na playlist.")
        return

    for i, track in enumerate(tracks, start=1):
        if utils.is_stop():
            messagebox.showinfo("Interrompido", "Spotify: Download interrompido pelo usuário.")
            return

        # hook que calcula porcentagem geral (i de total)
        def hook(progress, prog_bar_local=prog_bar, prog_label_local=prog_label, idx=i, total_local=total):
            if utils.is_stop():
                raise RuntimeError("Cancelado pelo usuário")
            if progress.get('status') == 'downloading':
                downloaded = progress.get('downloaded_bytes', 0)
                total_bytes = progress.get('total_bytes') or progress.get('total_bytes_estimate') or 1
                track_fraction = downloaded / total_bytes
                overall_fraction = ((idx - 1) + track_fraction) / total_local
                overall_percent = overall_fraction * 100
                try:
                    if prog_bar_local:
                        prog_bar_local.set(overall_percent / 100)
                    if prog_label_local:
                        prog_label_local.configure(text=f"Spotify: baixando {idx}/{total_local} - {overall_percent:.2f}%")
                except Exception:
                    pass
            elif progress.get('status') == 'finished':
                try:
                    if prog_bar_local:
                        prog_bar_local.set(idx / total_local)
                    if prog_label_local:
                        prog_label_local.configure(text=f"Spotify: baixou {idx}/{total_local} (100%)")
                except Exception:
                    pass

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'progress_hooks': [hook]
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch:{track}"])
        except RuntimeError:  # abortado pelo hook
            messagebox.showinfo("Interrompido", "Spotify: Download interrompido pelo usuário.")
            return
        except Exception as e:
            # mostra no console, pula a música
            print(f"Spotify: Erro ao baixar '{track}': {e}")
   
    try:
        shutil.make_archive(os.path.join(download_path, "playlist_download"), 'zip', download_path)
    except Exception:
        pass

    messagebox.showinfo("Concluído", "Spotify: Download da playlist concluído!")


def spotify_download_single(url, download_path, prog_bar, prog_label):
    os.makedirs(download_path, exist_ok=True)
    try:
        track_name = get_track_info(url)
    except Exception as e:
        messagebox.showerror("Erro", f"Spotify: Não foi possível obter a música. {e}")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'progress_hooks': [lambda p: utils.yt_progress_hook(p, prog_bar, prog_label, "Spotify")]
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch:{track_name}"])
    except RuntimeError:
        messagebox.showinfo("Interrompido", "Spotify: Download interrompido pelo usuário.")
        return
    except Exception as e:
        messagebox.showerror("Erro", f"Spotify: Erro ao baixar: {e}")
        return

    if prog_bar:
        prog_bar.set(1)
    if prog_label:
        prog_label.configure(text=f"Spotify: '{track_name}' concluído (100%)")
    messagebox.showinfo("Concluído", f"Spotify: Download da música '{track_name}' concluído!")

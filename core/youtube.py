# core/youtube.py
import os
import yt_dlp
from tkinter import messagebox
import core.utils as utils
from core.ffmpeg_utils import upscale_video_with_progress


def download_youtube_video(url, download_path, fmt, res, dl_prog_bar, dl_prog_label, up_prog_bar, up_prog_label):
    os.makedirs(download_path, exist_ok=True)

    # mapeamento de escala + fps
    scale_mapping = {
        "240p": "scale=426:240",
        "360p": "scale=640:360",
        "480p": "scale=854:480",
        "720p": "scale=1280:720",
        "720p 60fps": "scale=1280:720,fps=60",
        "1080p": "scale=1920:1080",
        "1080p 60fps": "scale=1920:1080,fps=60",
        "4K": "scale=3840:2160",
        "4K 60fps": "scale=3840:2160,fps=60"
    }

    # Detecta se é playlist antes de baixar (obter entradas)
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl_top:
            info_top = ydl_top.extract_info(url, download=False)
    except Exception as e:
        messagebox.showerror("Erro", f"YouTube: Não foi possível analisar a URL: {e}")
        return

    entries = []
    if info_top.get('_type') == 'playlist' or 'entries' in info_top:
        # coleta URLs das entradas
        raw_entries = info_top.get('entries') or []
        for e in raw_entries:
            # pode vir parcial; tente extrair id/webpage_url
            entry_url = e.get('webpage_url') or (f"https://www.youtube.com/watch?v={e.get('id')}") if e.get('id') else None
            if entry_url:
                entries.append(entry_url)
    else:
        # é um vídeo único
        entries = [url]

    total = len(entries)

    for idx, entry_url in enumerate(entries, start=1):
        if utils.is_stop():
            messagebox.showinfo("Interrompido", "YouTube: Download interrompido pelo usuário.")
            return

        # hook: atualiza porcentagem global com base no progresso do item atual
        def hook(progress, prog_bar_local=dl_prog_bar, prog_label_local=dl_prog_label, index=idx, total_local=total, prefix="YouTube"):
            if utils.is_stop():
                raise RuntimeError("Cancelado pelo usuário")
            if progress.get('status') == 'downloading':
                downloaded = progress.get('downloaded_bytes', 0)
                total_bytes = progress.get('total_bytes') or progress.get('total_bytes_estimate') or 1
                item_fraction = downloaded / total_bytes
                overall_fraction = ((index - 1) + item_fraction) / total_local
                overall_percent = overall_fraction * 100
                try:
                    if prog_bar_local:
                        prog_bar_local.set(overall_percent / 100)
                    if prog_label_local:
                        prog_label_local.configure(text=f"YouTube: baixando {index}/{total_local} - {overall_percent:.2f}%")
                except Exception:
                    pass
            elif progress.get('status') == 'finished':
                try:
                    if prog_bar_local:
                        prog_bar_local.set(index / total_local)
                    if prog_label_local:
                        prog_label_local.configure(text=f"YouTube: baixou {index}/{total_local} (100%)")
                except Exception:
                    pass

        # options dependendo do formato
        if fmt == "mp3":
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
        else:  # mp4
            ydl_opts = {
                # tenta pegar melhor video + melhor audio; a seguir forçamos o ffmpeg a transcodificar áudio para AAC
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'quiet': True,
                'progress_hooks': [hook],
                # forçar transcodificação do áudio para aac para evitar "opus" incompatível em alguns players
                'postprocessor_args': ['-c:a', 'aac', '-b:a', '192k'],
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }]
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # usamos extract_info(download=True) pra obter info e nome do arquivo
                info = ydl.extract_info(entry_url, download=True)
                # caminho do arquivo baixado (preparado com o outtmpl)
                try:
                    downloaded_file = ydl.prepare_filename(info)
                except Exception:
                    # fallback simples
                    title = info.get('title') or f"video_{idx}"
                    ext = info.get('ext') or ('mp4' if fmt == 'mp4' else 'mp3')
                    downloaded_file = os.path.join(download_path, f"{title}.{ext}")
        except RuntimeError:
            messagebox.showinfo("Interrompido", "YouTube: Download interrompido pelo usuário.")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"YouTube: Erro ao baixar: {e}")
            return

        # se escolheu mp4 e pediu upscaling, roda o ffmpeg
        if fmt == "mp4" and res in scale_mapping:
            if utils.is_stop():
                messagebox.showinfo("Interrompido", "YouTube: Interrompido antes do upscaling.")
                return
            # montar nome de saída
            output_file = os.path.splitext(downloaded_file)[0] + "_upscaled.mp4"
            # chama o upscaling (que observa utils.is_stop())
            success, result = upscale_video_with_progress(downloaded_file, scale_mapping[res], output_file, up_prog_bar, up_prog_label)
            if not success:
                # Se foi cancelado pelo usuário, mostra e encerra
                if result and "Interrompido" in str(result):
                    messagebox.showinfo("Interrompido", "YouTube: Upscaling interrompido pelo usuário.")
                    return
                else:
                    messagebox.showerror("Erro", f"Upscaling falhou: {result}")
                    # não abortamos o loop inteiro — você pode decidir diferente
                    # continue para o próximo item da playlist
    # fim loop entries

    messagebox.showinfo("Concluído", "YouTube: Download(s) concluído(s)!")

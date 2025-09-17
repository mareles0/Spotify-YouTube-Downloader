# gui/main_window.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

from core.spotify import spotify_download_playlist, spotify_download_single
from core.youtube import download_youtube_video
import core.utils as utils


class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎧 Downloader Multi-Modal")
        self.root.geometry("980x700")

        self.default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        header = ctk.CTkLabel(root, text="🎵 Spotify & 🎬 YouTube Downloader",
                              font=("Segoe UI", 22, "bold"))
        header.pack(pady=12)

        self.tabview = ctk.CTkTabview(root, width=940, height=520)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)

        self.spotify_tab = self.tabview.add("Spotify")
        self.youtube_tab = self.tabview.add("YouTube")

        self.create_spotify_ui(self.spotify_tab)
        self.create_youtube_ui(self.youtube_tab)

    # ---------------- Spotify ----------------
    def create_spotify_ui(self, frame):
        self.spotify_url = ctk.CTkEntry(frame, placeholder_text="URL do Spotify (playlist ou track)")
        self.spotify_url.pack(pady=8, fill="x", padx=20)

        dir_frame = ctk.CTkFrame(frame)
        dir_frame.pack(fill="x", padx=20, pady=6)
        self.spotify_dir = ctk.CTkEntry(dir_frame, placeholder_text=self.default_download_dir)
        self.spotify_dir.pack(side="left", fill="x", expand=True, padx=(6, 6), pady=6)
        browse_btn = ctk.CTkButton(dir_frame, text="📁 Procurar", width=120, command=self.browse_spotify_dir)
        browse_btn.pack(side="left", padx=(6, 6), pady=6)

        actions = ctk.CTkFrame(frame)
        actions.pack(pady=6)
        ctk.CTkButton(actions, text="▶️ Iniciar", fg_color="green", command=self.start_spotify).grid(row=0, column=0, padx=6)
        ctk.CTkButton(actions, text="⏹️ Parar", fg_color="red", command=utils.set_stop).grid(row=0, column=1, padx=6)

        self.spotify_progress = ctk.CTkProgressBar(frame)
        self.spotify_progress.pack(fill="x", padx=20, pady=(12, 4))
        self.spotify_progress.set(0)

        self.spotify_label = ctk.CTkLabel(frame, text="Pronto")
        self.spotify_label.pack(pady=(2, 10))

    def browse_spotify_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.spotify_dir.delete(0, "end")
            self.spotify_dir.insert(0, path)

    def start_spotify(self):
        utils.reset_stop()
        url = self.spotify_url.get().strip()
        download_path = self.spotify_dir.get().strip() or self.default_download_dir
        os.makedirs(download_path, exist_ok=True)

        if not url:
            messagebox.showwarning("Aviso", "Insira uma URL válida do Spotify.")
            return

        def run():
            if "playlist" in url:
                spotify_download_playlist(url, download_path, self.spotify_progress, self.spotify_label)
            elif "track" in url:
                spotify_download_single(url, download_path, self.spotify_progress, self.spotify_label)
            else:
                messagebox.showwarning("Aviso", "Insira uma URL válida do Spotify.")

        threading.Thread(target=run, daemon=True).start()

    # ---------------- YouTube ----------------
    def create_youtube_ui(self, frame):
        self.youtube_url = ctk.CTkEntry(frame, placeholder_text="URL do YouTube (vídeo ou playlist)")
        self.youtube_url.pack(pady=8, fill="x", padx=20)

        dir_frame = ctk.CTkFrame(frame)
        dir_frame.pack(fill="x", padx=20, pady=6)
        self.youtube_dir = ctk.CTkEntry(dir_frame, placeholder_text=self.default_download_dir)
        self.youtube_dir.pack(side="left", fill="x", expand=True, padx=(6, 6), pady=6)
        browse_btn = ctk.CTkButton(dir_frame, text="📁 Procurar", width=120, command=self.browse_youtube_dir)
        browse_btn.pack(side="left", padx=(6, 6), pady=6)

        opt_frame = ctk.CTkFrame(frame)
        opt_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(opt_frame, text="Formato:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.youtube_format = ctk.CTkComboBox(opt_frame, values=["mp3", "mp4"])
        self.youtube_format.set("mp4")
        self.youtube_format.grid(row=0, column=1, padx=6, pady=6)
        ctk.CTkLabel(opt_frame, text="Resolução:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.youtube_res = ctk.CTkComboBox(opt_frame, values=["240p", "360p", "480p", "720p", "720p 60fps",
                                                              "1080p", "1080p 60fps", "4K", "4K 60fps"])
        self.youtube_res.set("720p")
        self.youtube_res.grid(row=0, column=3, padx=6, pady=6)

        actions = ctk.CTkFrame(frame)
        actions.pack(pady=6)
        ctk.CTkButton(actions, text="▶️ Iniciar", fg_color="green", command=self.start_youtube).grid(row=0, column=0, padx=6)
        ctk.CTkButton(actions, text="⏹️ Parar", fg_color="red", command=utils.set_stop).grid(row=0, column=1, padx=6)

        self.youtube_progress = ctk.CTkProgressBar(frame)
        self.youtube_progress.pack(fill="x", padx=20, pady=(12, 4))
        self.youtube_progress.set(0)
        self.youtube_label = ctk.CTkLabel(frame, text="Pronto")
        self.youtube_label.pack(pady=(2, 6))

        self.upscale_progress = ctk.CTkProgressBar(frame)
        self.upscale_progress.pack(fill="x", padx=20, pady=(6, 4))
        self.upscale_progress.set(0)
        self.upscale_label = ctk.CTkLabel(frame, text="Upscaling: aguardando")
        self.upscale_label.pack(pady=(2, 10))

    def browse_youtube_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.youtube_dir.delete(0, "end")
            self.youtube_dir.insert(0, path)

    def start_youtube(self):
        utils.reset_stop()
        url = self.youtube_url.get().strip()
        download_path = self.youtube_dir.get().strip() or self.default_download_dir
        fmt = self.youtube_format.get()
        res = self.youtube_res.get()
        os.makedirs(download_path, exist_ok=True)

        if not url:
            messagebox.showwarning("Aviso", "Insira uma URL válida do YouTube.")
            return

        def run():
            download_youtube_video(
                url, download_path, fmt, res,
                self.youtube_progress, self.youtube_label,
                self.upscale_progress, self.upscale_label
            )

        threading.Thread(target=run, daemon=True).start()

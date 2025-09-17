# core/ffmpeg_utils.py
import subprocess
import sys
import os
import core.utils as utils


def get_ffmpeg_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "ffmpeg.exe")
    return "ffmpeg"


def get_ffprobe_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "ffprobe.exe")
    return "ffprobe"


def get_video_duration(input_file):
    try:
        result = subprocess.run(
            [get_ffprobe_path(), "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", input_file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True
        )
        return float(result.stdout.strip())
    except Exception:
        return None


def upscale_video_with_progress(input_file, scale_filter, output_file, prog_bar=None, prog_label=None):
    """
    Executa ffmpeg com -progress=pipe:1 e atualiza prog_bar/prog_label.
    Observa utils.is_stop() e encerra o processo se o usuário pedir parada.
    """
    total_duration = get_video_duration(input_file)
    if total_duration is None:
        if prog_label:
            try:
                prog_label.configure(text="Upscaling: Erro ao obter duração")
            except Exception:
                pass
        return False, "Erro ao obter duração"

    cmd = [
        get_ffmpeg_path(), "-y", "-i", input_file,
        "-vf", scale_filter,
        "-progress", "pipe:1",
        "-nostats",
        output_file
    ]

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding="utf-8"
        )
    except Exception as e:
        return False, f"Erro ao iniciar ffmpeg: {e}"

    try:
        while True:
            if utils.is_stop():
                try:
                    process.terminate()
                except Exception:
                    pass
                return False, "Interrompido pelo usuário"

            line = process.stdout.readline()
            if not line:
                break
            line = line.strip()
            if line.startswith("out_time_ms="):
                try:
                    out_time_ms = int(line.split("=")[1])
                    current_time = out_time_ms / 1_000_000.0
                    percent = (current_time / total_duration) * 100
                    if percent > 100:
                        percent = 100
                    if prog_bar is not None:
                        try:
                            prog_bar.set(percent / 100)
                        except Exception:
                            pass
                    if prog_label is not None:
                        try:
                            prog_label.configure(text=f"Upscaling: {percent:.2f}%")
                        except Exception:
                            pass
                except Exception:
                    pass
            elif line.startswith("progress=") and line.split("=")[1] == "end":
                try:
                    if prog_bar is not None:
                        prog_bar.set(1)
                    if prog_label is not None:
                        prog_label.configure(text="Upscaling: concluído")
                except Exception:
                    pass
                break
    finally:
        process.wait()

    if process.returncode == 0:
        return True, output_file
    else:
        return False, f"Erro no upscaling (ffmpeg retornou {process.returncode})"

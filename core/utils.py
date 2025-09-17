import sys

stop_download = False


def set_stop():
    global stop_download
    stop_download = True


def reset_stop():
    global stop_download
    stop_download = False


def is_stop():
    return stop_download


def yt_progress_hook(progress, prog_bar=None, prog_label=None, prefix=""):
    """
    Hook genérico para yt_dlp. Se o interruptor de parada for acionado,
    lança RuntimeError para encerrar o download.
    Atualiza barra (prog_bar) com valor de 0..1 e label com porcentagem.
    """
    if is_stop():
        # sinaliza na label e aborta
        if prog_label:
            try:
                prog_label.configure(text=f"{prefix}: Cancelado")
            except Exception:
                pass
        raise RuntimeError("Cancelado pelo usuário")

    status = progress.get("status")
    if status == "downloading":
        downloaded = progress.get("downloaded_bytes", 0)
        total = progress.get("total_bytes") or progress.get("total_bytes_estimate") or 1
        percent = (downloaded / total) * 100
        try:
            if prog_bar is not None:
                prog_bar.set(percent / 100)
            if prog_label is not None:
                prog_label.configure(text=f"{prefix}: {percent:.2f}%")
        except Exception:
            pass
    elif status == "finished":
        try:
            if prog_bar is not None:
                prog_bar.set(1)
            if prog_label is not None:
                prog_label.configure(text=f"{prefix}: 100% concluído")
        except Exception:
            pass


class TextRedirector:
    """
    Mantido caso queira reativar logs na UI. Não é usado na versão atual.
    """
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
        self._orig = sys.stdout if tag == "stdout" else sys.stderr

    def write(self, message):
        try:
            self.widget.insert("end", message)
            self.widget.see("end")
        except Exception:
            pass
        try:
            self._orig.write(message)
        except Exception:
            pass

    def flush(self):
        try:
            self._orig.flush()
        except Exception:
            pass

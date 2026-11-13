"""Shared render helpers for the bcc_test4 module explainer videos.

Dark 1920x1080 @30 fps, silent H.264. Frames drawn with matplotlib (Agg) and
piped as raw RGBA into ffmpeg. All plotted numbers come from the caller,
which takes them from the real module run (see each render_*.py).
"""
import os, subprocess, sys, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

W, H, FPS = 1920, 1080, 30
BG = "#0b0d13"; PANEL = "#121622"; GRID = "#2a3142"
FG = "#e8ebf2"; DIM = "#8b94a8"; CYAN = "#4fd1ff"; ORANGE = "#ffb347"
RED = "#ff5c6c"; GREEN = "#6ee7a0"; VIOLET = "#b39dff"; YELLOW = "#ffe066"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "text.color": FG, "axes.labelcolor": FG,
    "xtick.color": DIM, "ytick.color": DIM, "axes.edgecolor": GRID,
    "axes.facecolor": PANEL, "figure.facecolor": BG, "savefig.facecolor": BG,
    "font.size": 16,
})

SRC_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../bcc_test4"))  # path edit: was /workspace/bcc_test4_videos/src/bcc_test4


def import_src():
    if SRC_ROOT not in sys.path:
        sys.path.insert(0, SRC_ROOT)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ramp(t, t0, dur=0.5):
    return ease((t - t0) / dur) if dur > 0 else float(t >= t0)


class Video:
    def __init__(self, out_dir, name, title, footer):
        self.out_dir = out_dir; self.name = name
        self.title = title; self.footer = footer
        self.scenes = []  # (duration, draw_fn, captions[(t, text)], heading)
        os.makedirs(out_dir, exist_ok=True)
        self.mp4 = os.path.join(out_dir, f"{name}.mp4")

    def add(self, dur, fn, captions=(), heading=""):
        self.scenes.append((dur, fn, list(captions), heading))

    @property
    def duration(self):
        return sum(s[0] for s in self.scenes)

    def chrome(self, fig, t, T, captions, heading):
        fig.text(0.03, 0.955, self.title, fontsize=20, color=DIM, weight="bold", va="center")
        if heading:
            fig.text(0.97, 0.955, heading, fontsize=20, color=FG, ha="right", va="center")
        cap = None; cap_t = 0
        for ct, text in captions:
            if t >= ct:
                cap, cap_t = text, ct
        if cap:
            a = min(ramp(t, cap_t, 0.35), 1 - ramp(t, T - 0.3, 0.3))
            fig.text(0.5, 0.075, cap, fontsize=30, color=FG, ha="center", va="center",
                     alpha=a, bbox=dict(boxstyle="round,pad=0.45", fc="#000000", ec="none", alpha=0.55 * a))
        fig.text(0.5, 0.018, self.footer, fontsize=13, color=DIM, ha="center", va="center")

    def render(self):
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
               "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", self.mp4]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        n = 0
        for dur, fn, caps, heading in self.scenes:
            nf = int(round(dur * FPS))
            for i in range(nf):
                t = i / FPS
                fig.clear()
                fn(fig, t, dur)
                self.chrome(fig, t, dur, caps, heading)
                fig.canvas.draw()
                p.stdin.write(fig.canvas.buffer_rgba().tobytes())
                n += 1
        p.stdin.close(); p.wait()
        plt.close(fig)
        print(f"{self.mp4}: {n} frames, {n / FPS:.2f}s")
        return self.mp4

    def extras(self, thumb_t):
        """Contact sheet (8 frames) and thumbnail PNG from the finished MP4."""
        d = self.duration
        sheet = os.path.join(self.out_dir, "contact_sheet.jpg")
        frames = []
        for k in range(8):
            ts = d * (k + 0.5) / 8
            f = os.path.join(self.out_dir, f"_cs{k}.png")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ts:.2f}", "-i", self.mp4,
                            "-frames:v", "1", "-vf", "scale=640:360", f], check=True)
            frames.append(f)
        inputs = sum([["-i", f] for f in frames], [])
        subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
                        "".join(f"[{i}:v]" for i in range(8)) + "concat=n=8:v=1:a=0,tile=4x2:padding=6:color=0x0b0d13",
                        "-frames:v", "1", "-q:v", "3", sheet], check=True)
        for f in frames:
            os.remove(f)
        thumb = os.path.join(self.out_dir, "thumbnail.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{thumb_t:.2f}", "-i", self.mp4,
                        "-frames:v", "1", "-vf", "scale=1280:720", thumb], check=True)
        return sheet, thumb


def title_card(title, subtitle, tag="TOY MODEL"):
    def fn(fig, t, T):
        a = ramp(t, 0.1, 0.6)
        fig.text(0.5, 0.58, title, fontsize=58, weight="bold", ha="center", va="center", alpha=a)
        fig.text(0.5, 0.47, subtitle, fontsize=28, color=DIM, ha="center", va="center", alpha=ramp(t, 0.5, 0.6))
        if tag:
            fig.text(0.5, 0.36, tag, fontsize=22, color=ORANGE, ha="center", va="center", weight="bold",
                     alpha=ramp(t, 0.9, 0.5),
                     bbox=dict(boxstyle="round,pad=0.5", fc="none", ec=ORANGE, alpha=ramp(t, 0.9, 0.5)))
    return fn


def end_card(lines, head="What this run shows"):
    def fn(fig, t, T):
        fig.text(0.5, 0.80, head, fontsize=40, weight="bold", ha="center", alpha=ramp(t, 0, 0.5))
        y = 0.66
        for i, (txt, col) in enumerate(lines):
            fig.text(0.5, y, txt, fontsize=27, color=col, ha="center", va="center", alpha=ramp(t, 0.4 + 0.5 * i, 0.5))
            y -= 0.095
    return fn


def style_ax(ax, grid=True):
    ax.set_facecolor(PANEL)
    for s in ax.spines.values():
        s.set_color(GRID)
    if grid:
        ax.grid(color=GRID, lw=0.8, alpha=0.6)
    ax.set_axisbelow(True)
    return ax

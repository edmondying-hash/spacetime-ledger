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

SRC_ROOT = "/workspace/bcc_test4_videos/v4/bcc_test4"


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


# ---------------- v2_sound additions: timeline export + audio mux ----------------
import json, hashlib


def scene_starts(video):
    out, t = [], 0.0
    for dur, fn, caps, heading in video.scenes:
        out.append({"start": t, "dur": dur, "heading": heading}); t += dur
    return out


def _measure_wav(wav, af=None):
    import re
    chain = (af + "," if af else "") + "ebur128=peak=true"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af", chain, "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])


def loudnorm_mux(silent_mp4, wav, final_mp4, I=-16.0, TP=-2.0):
    """Gain to I LUFS, then a 4x-oversampled look-ahead limiter at TP-1.0 dB (true-peak safe),
    re-measured and re-gained (3 iterations) so limiting does not pull loudness off target; AAC 192k."""
    lim = 10 ** ((TP - 1.0) / 20)
    gain = I - _measure_wav(wav)[0]
    for _ in range(3):
        af = (f"volume={gain:.3f}dB,aresample=192000,alimiter=limit={lim:.4f}:level=false:attack=2:release=60:asc=1,"
              f"aresample=48000")
        got, _tp = _measure_wav(wav, af)
        if abs(got - I) < 0.1: break
        gain += I - got
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent_mp4, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", final_mp4], check=True)


def audio_report(mp4):
    """Integrated LUFS / true peak (ebur128) and sample peak (astats) of the muxed AAC track."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-map", "0:a",
                        "-af", "ebur128=peak=true,astats=measure_overall=Peak_level", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    import re
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
    sp = max(float(x) for x in re.findall(r"Peak level dB: (-?[\d.]+)", r))
    return {"integrated_lufs": I, "true_peak_dbtp": tp, "sample_peak_dbfs": sp, "clipping": sp >= 0.0}


def finish(video, final_name, timeline, sfx_script, thumb_t, audio_only=False):
    """render silent -> timeline.json -> sfx wav -> loudnorm mux -> extras -> sha256 -> audio report."""
    out = video.out_dir
    json.dump(timeline, open(os.path.join(out, "timeline.json"), "w"), indent=1)
    final = os.path.join(out, final_name + ".mp4"); wav = os.path.join(out, final_name + "_sfx.wav")
    if audio_only and os.path.exists(final):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", final, "-map", "0:v", "-c", "copy", video.mp4], check=True)
    else:
        video.render()
    subprocess.run([sys.executable, sfx_script], check=True)
    loudnorm_mux(video.mp4, wav, final)
    os.remove(video.mp4); video.mp4 = final
    video.extras(thumb_t)
    h = hashlib.sha256(open(final, "rb").read()).hexdigest()
    open(final + ".sha256", "w").write(f"{h}  {final_name}.mp4\n")
    rep = audio_report(final); rep["duration_s"] = video.duration
    json.dump(rep, open(os.path.join(out, "audio_levels.json"), "w"), indent=1)
    print(final, rep)
    return rep

"""SONORA — a customizable floating lyrics desktop companion.
Python 3.10+, standard library only (Tkinter).
"""
from __future__ import annotations

import re
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk
from pathlib import Path

APP_NAME = "SONORA"
BG = "#0c1018"
PANEL = "#151b27"
PANEL_2 = "#20293a"
TEXT = "#f4f5fb"
MUTED = "#9aa4b8"
ACCENT = "#9b8cff"
ACCENT_2 = "#76e4d2"

DEMO_LYRICS = [
    (0.0, "A little light in the midnight"),
    (4.0, "A quiet pulse beneath the city"),
    (8.0, "We let the whole world fade away"),
    (12.0, "And keep the moment where it is"),
    (16.0, "\u266a  Breathe in, breathe out  \u266a"),
    (20.0, "We're only echoes in the blue"),
    (24.0, "But every echo leads to you"),
    (28.0, "Stay a little longer tonight"),
    (33.0, "Let the silence sing") ,
]


def parse_lrc(content: str) -> list[tuple[float, str]]:
    """Parse standard [mm:ss.xx] LRC timestamps, including multiple stamps per line."""
    rows: list[tuple[float, str]] = []
    stamp = re.compile(r"\[(\d{1,2}):(\d{2})(?:[.:](\d{1,3}))?\]")
    for raw in content.splitlines():
        matches = list(stamp.finditer(raw))
        if not matches:
            continue
        lyric = stamp.sub("", raw).strip()
        if not lyric:
            continue
        for match in matches:
            fraction = match.group(3) or "0"
            # LRC commonly uses hundredths, but tolerate milliseconds too.
            frac = int(fraction) / (1000 if len(fraction) == 3 else 100)
            rows.append((int(match.group(1)) * 60 + int(match.group(2)) + frac, lyric))
    return sorted(rows, key=lambda item: item[0])


def parse_srt(content: str) -> list[tuple[float, str]]:
    """Parse SubRip (.srt) captions into start-time/lyric rows."""
    rows: list[tuple[float, str]] = []
    timestamp = re.compile(
        r"(?P<start>\d{1,2}:\d{2}:\d{2}[,.]\d{1,3})"
        r"\s*-->\s*"
        r"(?P<end>\d{1,2}:\d{2}:\d{2}[,.]\d{1,3})"
    )

    def to_seconds(value: str) -> float:
        hours, minutes, remainder = value.replace(",", ".").split(":")
        seconds, fraction = remainder.split(".")
        return (
            int(hours) * 3600
            + int(minutes) * 60
            + int(seconds)
            + int(fraction.ljust(3, "0")[:3]) / 1000
        )

    for block in re.split(r"\r?\n\s*\r?\n", content.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next(
            (i for i, line in enumerate(lines) if timestamp.search(line)), None
        )
        if timing_index is None:
            continue
        match = timestamp.search(lines[timing_index])
        if not match:
            continue
        lyric_lines = lines[timing_index + 1:]
        if not lyric_lines:
            continue
        # Remove common SubRip/HTML formatting tags while preserving lyric text.
        lyric = re.sub(r"<[^>]+>", "", " ".join(lyric_lines)).strip()
        if lyric:
            rows.append((to_seconds(match.group("start")), lyric))

    return sorted(rows, key=lambda item: item[0])


def animation_profile(speed: float, transition: str) -> tuple[float, float, float, float]:
    """Return fade-in, hold, fade-out seconds and travel distance for a preset."""
    speed = max(0.35, min(2.5, float(speed)))
    travel = {
        "Smooth Rise": 104.0,
        "Gentle Glide": 125.0,
        "Soft Drift": 72.0,
        "Fade Only": 0.0,
    }.get(transition, 104.0)
    return 0.85 / speed, 1.45, 2.50 / speed, travel


def transition_ease(value: float, transition: str) -> float:
    """Clamp and ease a 0..1 animation fraction for the selected preset."""
    import math
    value = max(0.0, min(1.0, float(value)))
    if transition == "Gentle Glide":
        return 1.0 - (1.0 - value) ** 3
    if transition == "Soft Drift":
        return (1.0 - math.cos(value * math.pi)) / 2.0
    if transition == "Fade Only":
        return value
    return value * value * (3.0 - 2.0 * value)


class SonoraApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SONORA v6 · Floating Lyrics")
        self.root.geometry("980x680")
        self.root.minsize(860, 620)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.lyrics = DEMO_LYRICS.copy()
        self.track_title = "Midnight in Bloom"
        self.artist = "SONORA DEMO SESSION"
        self.current_time = 0.0
        self.duration = 38.0
        self.playing = False
        self.last_tick = None
        self.active_index = -1
        self.overlay = None
        self.overlay_label = None
        self.overlay_kicker = None
        self.lyric_canvas = None
        self.lyric_text_id = None
        self.overlay_animation_job = None
        self.overlay_animation_started = 0.0
        self.overlay_rest_x = 0
        self.overlay_rest_y = 0
        self._closing = False
        self.overlay_dismissed_by_animation = False
        self.last_animated_index = -2
        self.overlay_visible = tk.BooleanVar(value=True)
        self.always_on_top = tk.BooleanVar(value=True)
        self.glass_mode = tk.BooleanVar(value=True)
        self.show_next = tk.BooleanVar(value=True)
        self.theme = tk.StringVar(value="Aurora")
        self.font_size = tk.IntVar(value=25)
        self.opacity = tk.DoubleVar(value=0.94)
        # Advanced Overlay Studio preferences.
        self.font_family = tk.StringVar(value="Segoe UI")
        self.font_weight = tk.StringVar(value="Bold")
        self.background_style = tk.StringVar(value="Theme")
        self.custom_background = "#151d2c"
        self.fade_speed = tk.DoubleVar(value=1.0)
        self.transition = tk.StringVar(value="Smooth Rise")
        self.position = tk.StringVar(value="Bottom center")
        self.accent = ACCENT
        self._build_style()
        self._build_ui()
        self._build_overlay()
        self._refresh_lyrics()
        self._tick()

    def _build_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Horizontal.TScale", background=PANEL, troughcolor=PANEL_2)
        style.configure("TCombobox", fieldbackground=PANEL_2, background=PANEL_2, foreground=TEXT)

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=28, pady=(22, 15))
        brand = tk.Frame(header, bg=BG)
        brand.pack(side="left")
        tk.Label(brand, text="✳", fg=ACCENT_2, bg=BG, font=("Segoe UI Symbol", 22)).pack(side="left", padx=(0, 10))
        tk.Label(brand, text="SONORA v6", fg=TEXT, bg=BG, font=("Segoe UI", 17, "bold")).pack(side="left")
        tk.Label(brand, text="  ·  YOUR LYRICS, IN MOTION", fg=MUTED, bg=BG, font=("Segoe UI", 8, "bold")).pack(side="left", pady=(5, 0))
        tk.Button(header, text="＋  Import Lyrics", command=self.import_lyrics, bg=PANEL_2, fg=TEXT, activebackground="#303950", activeforeground=TEXT, relief="flat", bd=0, padx=15, pady=9, cursor="hand2", font=("Segoe UI", 9, "bold")).pack(side="right")

        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=28, pady=(0, 20))
        left = tk.Frame(content, bg=PANEL, highlightthickness=1, highlightbackground="#242d40")
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))
        right = tk.Frame(content, bg=PANEL, width=270, highlightthickness=1, highlightbackground="#242d40")
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        # Player / visualizer panel
        tk.Label(left, text="NOW PLAYING", fg=ACCENT_2, bg=PANEL, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22, pady=(20, 5))
        self.title_label = tk.Label(left, text=self.track_title, fg=TEXT, bg=PANEL, font=("Segoe UI", 22, "bold"))
        self.title_label.pack(anchor="w", padx=22)
        self.artist_label = tk.Label(left, text=self.artist, fg=MUTED, bg=PANEL, font=("Segoe UI", 9, "bold"))
        self.artist_label.pack(anchor="w", padx=23, pady=(2, 18))

        visual = tk.Frame(left, bg="#121724", height=125)
        visual.pack(fill="x", padx=22)
        visual.pack_propagate(False)
        self.wave_canvas = tk.Canvas(visual, bg="#121724", height=125, highlightthickness=0)
        self.wave_canvas.pack(fill="both", expand=True)
        self.wave_canvas.bind("<Configure>", lambda _e: self._draw_wave())
        self.wave_canvas.bind("<Button-1>", self._wave_seek)

        self.current_label = tk.Label(left, text="00:00", fg=MUTED, bg=PANEL, font=("Consolas", 9))
        self.current_label.pack(anchor="w", padx=23, pady=(14, 0))
        self.seek = ttk.Scale(left, from_=0, to=self.duration, command=self._seek_changed)
        self.seek.pack(fill="x", padx=22, pady=(0, 2))
        self.seek.bind("<ButtonRelease-1>", self._seek_release)
        self.duration_label = tk.Label(left, text="00:38", fg=MUTED, bg=PANEL, font=("Consolas", 9))
        self.duration_label.pack(anchor="e", padx=23)

        controls = tk.Frame(left, bg=PANEL)
        controls.pack(fill="x", padx=22, pady=(13, 18))
        self.play_btn = tk.Button(controls, text="▶  PLAY", command=self.toggle_play, bg=ACCENT, fg="#171326", activebackground="#b9a6ff", relief="flat", bd=0, padx=20, pady=11, cursor="hand2", font=("Segoe UI", 9, "bold"))
        self.play_btn.pack(side="left")
        tk.Button(controls, text="↺  RESTART", command=self.restart, bg=PANEL_2, fg=TEXT, activebackground="#303950", relief="flat", bd=0, padx=14, pady=11, cursor="hand2", font=("Segoe UI", 9, "bold")).pack(side="left", padx=8)
        tk.Button(controls, text="◉  PREVIEW OVERLAY", command=self.toggle_overlay, bg=PANEL_2, fg=TEXT, activebackground="#303950", relief="flat", bd=0, padx=14, pady=11, cursor="hand2", font=("Segoe UI", 9, "bold")).pack(side="right")

        tk.Label(left, text="LYRIC TIMELINE", fg=MUTED, bg=PANEL, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22, pady=(0, 8))
        list_wrap = tk.Frame(left, bg=PANEL)
        list_wrap.pack(fill="both", expand=True, padx=22, pady=(0, 18))
        self.lyric_list = tk.Listbox(list_wrap, bg="#141a27", fg="#c7cede", selectbackground="#3b315f", selectforeground="white", activestyle="none", relief="flat", bd=0, font=("Segoe UI", 10), highlightthickness=0)
        self.lyric_list.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(list_wrap, orient="vertical", command=self.lyric_list.yview)
        scroll.pack(side="right", fill="y")
        self.lyric_list.configure(yscrollcommand=scroll.set)
        self.lyric_list.bind("<Double-Button-1>", self._jump_to_selected)

        # Settings panel
        tk.Label(right, text="OVERLAY STUDIO", fg=TEXT, bg=PANEL, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=18, pady=(20, 3))
        tk.Label(right, text="Tune the look and motion.", fg=MUTED, bg=PANEL, font=("Segoe UI", 8)).pack(anchor="w", padx=18, pady=(0, 18))
        self._section(right, "APPEARANCE")
        self._setting_label(right, "Visual style")
        theme_menu = ttk.Combobox(right, textvariable=self.theme, values=["Aurora", "Midnight", "Paper", "Neon"], state="readonly")
        theme_menu.pack(fill="x", padx=18, pady=(0, 12))
        theme_menu.bind("<<ComboboxSelected>>", lambda _e: self._apply_overlay_style())
        self._setting_label(right, "Text size")
        tk.Scale(right, from_=17, to=38, orient="horizontal", variable=self.font_size, command=lambda _v: self._update_overlay_text(), bg=PANEL, fg=TEXT, troughcolor=PANEL_2, highlightthickness=0, bd=0, activebackground=ACCENT, showvalue=True).pack(fill="x", padx=14, pady=(0, 10))
        self._setting_label(right, "Overlay opacity")
        tk.Scale(right, from_=0.55, to=1.0, resolution=0.01, orient="horizontal", variable=self.opacity, command=lambda _v: self._set_opacity(), bg=PANEL, fg=TEXT, troughcolor=PANEL_2, highlightthickness=0, bd=0, activebackground=ACCENT, showvalue=True).pack(fill="x", padx=14, pady=(0, 10))
        self._section(right, "BEHAVIOR")
        self._toggle(right, "Always on top", self.always_on_top, self._set_topmost)
        self._toggle(right, "Show next line", self.show_next, self._update_overlay_text)
        self._toggle(right, "Soft glass background", self.glass_mode, self._apply_overlay_style)
        self._setting_label(right, "Screen position")
        pos = ttk.Combobox(right, textvariable=self.position, values=["Bottom center", "Top center", "Center", "Bottom left", "Bottom right"], state="readonly")
        pos.pack(fill="x", padx=18, pady=(0, 13))
        pos.bind("<<ComboboxSelected>>", lambda _e: self._place_overlay())
        tk.Button(right, text="✦  Advanced Overlay Studio", command=self.open_overlay_studio, bg="#30304a", fg=TEXT, activebackground="#41415f", relief="flat", bd=0, padx=10, pady=9, cursor="hand2", font=("Segoe UI", 9, "bold")).pack(fill="x", padx=18, pady=(2, 6))
        tk.Button(right, text="Hide overlay", command=self.hide_overlay, bg="#2a3040", fg=TEXT, activebackground="#3b455b", relief="flat", bd=0, padx=10, pady=9, cursor="hand2", font=("Segoe UI", 9, "bold")).pack(fill="x", padx=18, pady=(10, 6))
        tk.Label(right, text="TIP  ·  Drag to move  /  Double-click to play", fg="#77839b", bg=PANEL, font=("Segoe UI", 8)).pack(anchor="w", padx=18, pady=(9, 0))

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=28, pady=(0, 13))
        tk.Label(footer, text="SONORA  •  A LITTLE SPACE FOR THE WORDS THAT MATTER", fg="#68748b", bg=BG, font=("Segoe UI", 8, "bold")).pack(side="left")
        tk.Label(footer, text="SPACE  PLAY / PAUSE     ·     ESC  HIDE OVERLAY", fg="#68748b", bg=BG, font=("Segoe UI", 8)).pack(side="right")
        self.root.bind("<space>", lambda _e: self.toggle_play())
        self.root.bind("<Escape>", lambda _e: self.hide_overlay())

    def _section(self, parent, title):
        tk.Label(parent, text=title, fg=ACCENT_2, bg=PANEL, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=18, pady=(8, 8))

    def _setting_label(self, parent, text):
        tk.Label(parent, text=text, fg="#c2cada", bg=PANEL, font=("Segoe UI", 9)).pack(anchor="w", padx=18, pady=(0, 4))

    def _toggle(self, parent, text, variable, callback):
        tk.Checkbutton(parent, text=text, variable=variable, command=callback, bg=PANEL, fg="#c2cada", activebackground=PANEL, activeforeground=TEXT, selectcolor=PANEL_2, font=("Segoe UI", 9), relief="flat", highlightthickness=0).pack(anchor="w", padx=15, pady=3)

    def _build_overlay(self):
        self.overlay = tk.Toplevel(self.root)
        self.overlay.withdraw()
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        self.overlay.configure(bg="#111827")
        self.overlay_frame = tk.Frame(
            self.overlay, bg="#151d2c", padx=26, pady=18,
            highlightthickness=1, highlightbackground="#344158"
        )
        self.overlay_frame.pack(fill="both", expand=True)
        self.overlay_kicker = tk.Label(
            self.overlay_frame, text="SONORA  /  NOW PLAYING",
            bg="#151d2c", fg=ACCENT_2, font=("Segoe UI", 8, "bold")
        )
        self.overlay_kicker.pack(anchor="w")
        self.lyric_canvas = tk.Canvas(
            self.overlay_frame, width=720, height=112, bg="#151d2c",
            highlightthickness=0, bd=0
        )
        self.lyric_canvas.pack(fill="x", pady=(5, 0))
        self.lyric_text_id = self.lyric_canvas.create_text(
            2, 100, text="Let the words find you.", anchor="sw", width=710,
            fill=TEXT, font=self._overlay_font()
        )
        self.next_label = tk.Label(
            self.overlay_frame, text="", bg="#151d2c", fg="#9daac0",
            font=("Segoe UI", 10)
        )
        self.next_label.pack(anchor="w", pady=(0, 1))
        for widget in (self.overlay, self.overlay_frame, self.overlay_kicker,
                       self.lyric_canvas, self.next_label):
            widget.bind("<ButtonPress-1>", self._drag_start)
            widget.bind("<B1-Motion>", self._drag_move)
            widget.bind("<Double-Button-1>", lambda _e: self.toggle_play())
        self._apply_overlay_style()
        self._place_overlay()
        self.overlay.deiconify()

    def _hex_blend(self, start, end, amount):
        start, end = start.lstrip("#"), end.lstrip("#")
        a = tuple(int(start[i:i+2], 16) for i in (0, 2, 4))
        b = tuple(int(end[i:i+2], 16) for i in (0, 2, 4))
        rgb = [round(x + (y-x)*amount) for x, y in zip(a, b)]
        return "#" + "".join(f"{v:02x}" for v in rgb)

    def _lyric_colors(self):
        palette = {
            "Aurora": ("#f4f6ff", "#151d2c"),
            "Midnight": ("#f0f2ff", "#080b12"),
            "Paper": ("#252331", "#f2eee6"),
            "Neon": ("#d8fff6", "#101b20"),
        }
        return palette.get(self.theme.get(), palette["Aurora"])

    def _cancel_overlay_animation(self):
        """Cancel the sole whole-window animation callback, if one is pending."""
        job = self.overlay_animation_job
        self.overlay_animation_job = None
        if job and not self._closing:
            try:
                self.root.after_cancel(job)
            except tk.TclError:
                pass

    def _animate_overlay_card(self):
        """Animate the complete Toplevel surface using the window alpha channel."""
        self.overlay_animation_job = None
        if self._closing or not self.overlay or not self.overlay.winfo_exists():
            return

        now = self.root.tk.call("clock", "milliseconds")
        elapsed = max(0.0, (now - self.overlay_animation_started) / 1000.0)

        # User-adjustable fade speed; 1.0x retains the cinematic default.
        transition = self.transition.get()
        fade_in, hold, fade_out, travel = animation_profile(
            self.fade_speed.get(), transition
        )
        total = fade_in + hold + fade_out
        ease = lambda value: transition_ease(value, transition)

        if elapsed < fade_in:
            opacity_factor = ease(elapsed / fade_in)
        elif elapsed < fade_in + hold:
            opacity_factor = 1.0
        else:
            opacity_factor = 1.0 - ease(
                (elapsed - fade_in - hold) / fade_out
            )

        # Drift begins gently during the hold and completes with the dissolve.
        travel_progress = ease(min(1.0, elapsed / total))
        y = self.overlay_rest_y - travel * travel_progress
        self.overlay.geometry(f"+{self.overlay_rest_x}+{round(y)}")

        alpha = max(0.0, min(1.0, self.opacity.get() * opacity_factor))
        try:
            # Tk maps -alpha to the native top-level window opacity on Windows.
            self.overlay.attributes("-alpha", alpha)
        except tk.TclError:
            # Do not leave a ghost window if the platform cannot apply alpha.
            if elapsed >= total:
                self.overlay.withdraw()
            else:
                self.overlay_animation_job = self.root.after(
                    24, self._animate_overlay_card
                )
            return

        if elapsed < total:
            self.overlay_animation_job = self.root.after(
                16, self._animate_overlay_card
            )
        else:
            # Explicitly set exact zero before restoring the stable anchor.
            try:
                self.overlay.attributes("-alpha", 0.0)
            except tk.TclError:
                pass
            self.overlay.geometry(
                f"+{self.overlay_rest_x}+{self.overlay_rest_y}"
            )
            self.overlay_dismissed_by_animation = True

    def _animate_lyric(self, index):
        if (self._closing or not self.lyric_canvas
                or index < 0 or index >= len(self.lyrics)):
            return

        self._cancel_overlay_animation()
        self.overlay_dismissed_by_animation = False
        self.last_animated_index = index
        self.overlay.update_idletasks()

        # Keep the selected/dragged resting point as the immutable animation anchor.
        if not self.overlay_rest_x and not self.overlay_rest_y:
            self.overlay_rest_x = self.overlay.winfo_x()
            self.overlay_rest_y = self.overlay.winfo_y()

        self.overlay.geometry(
            f"+{self.overlay_rest_x}+{self.overlay_rest_y}"
        )
        self.lyric_canvas.coords(self.lyric_text_id, 2, 100)
        self.lyric_canvas.itemconfigure(
            self.lyric_text_id,
            text=self.lyrics[index][1],
            font=self._overlay_font(),
            fill=self._lyric_colors()[0],
        )
        try:
            self.overlay.attributes("-alpha", 0.0)
            self.overlay.deiconify()
            self.overlay.lift()
        except tk.TclError:
            pass

        self.overlay_animation_started = self.root.tk.call(
            "clock", "milliseconds"
        )
        self.overlay_animation_job = self.root.after(
            16, self._animate_overlay_card
        )

    def _drag_start(self, event):
        self._drag_x, self._drag_y = event.x_root - self.overlay.winfo_x(), event.y_root - self.overlay.winfo_y()

    def _drag_move(self, event):
        x, y = event.x_root - self._drag_x, event.y_root - self._drag_y
        self.overlay_rest_x, self.overlay_rest_y = x, y
        self.overlay.geometry(f"+{x}+{y}")

    def _apply_overlay_style(self, *_):
        themes = {
            "Aurora": ("#1c2332", TEXT, ACCENT_2, "#a4aec1", "#414a60"),
            "Midnight": ("#080b12", "#f0f2ff", "#a78bfa", "#929bb0", "#34394b"),
            "Paper": ("#f2eee6", "#252331", "#7256bd", "#656171", "#d2cabb"),
            "Neon": ("#101b20", "#d8fff6", "#5fffe0", "#8bbeb5", "#28675d"),
        }
        bg, fg, kick, sub, border = themes.get(self.theme.get(), themes["Aurora"])
        style = self.background_style.get()
        if style == "Custom":
            bg = self.custom_background
        elif style == "Dark":
            bg, fg, sub = "#10131b", "#f4f5fb", "#b9c3d5"
            border = "#30394d"
        elif style == "Light":
            bg, fg, sub = "#f3f0e9", "#252331", "#656171"
            border = "#d2cabb"
        elif style == "Minimal":
            border = bg
        elif style == "Custom":
            rgb = tuple(int(self.custom_background[i:i+2], 16) for i in (1, 3, 5))
            brightness = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
            fg, sub = (("#252331", "#656171") if brightness > 150
                       else ("#f4f5fb", "#b9c3d5"))
        if not self.glass_mode.get() and style == "Theme":
            bg = "#080b12" if self.theme.get() != "Paper" else "#f2eee6"
        self.overlay.configure(bg=bg)
        self.overlay_frame.configure(bg=bg, highlightbackground=border)
        self.overlay_kicker.configure(bg=bg, fg=kick)
        self.lyric_canvas.configure(bg=bg)
        self.lyric_canvas.itemconfigure(
            self.lyric_text_id, fill=fg,
            font=self._overlay_font()
        )
        self.next_label.configure(bg=bg, fg=sub)
        self._update_overlay_text()

    def _overlay_font(self):
        weight = "bold" if self.font_weight.get() == "Bold" else "normal"
        return (self.font_family.get(), self.font_size.get(), weight)

    def open_overlay_studio(self):
        """Open the advanced appearance and motion controls."""
        if getattr(self, "studio_window", None) is not None:
            try:
                if self.studio_window.winfo_exists():
                    self.studio_window.deiconify()
                    self.studio_window.lift()
                    return
            except tk.TclError:
                pass
        win = tk.Toplevel(self.root)
        self.studio_window = win
        win.title("SONORA · Advanced Overlay Studio")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.transient(self.root)
        body = tk.Frame(win, bg=PANEL, padx=22, pady=18)
        body.pack(fill="both", expand=True, padx=12, pady=12)
        tk.Label(body, text="OVERLAY APPEARANCE", bg=PANEL, fg=ACCENT_2,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 8))

        def label(text):
            tk.Label(body, text=text, bg=PANEL, fg="#c2cada",
                     font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 3))

        label("Background style")
        bg_menu = ttk.Combobox(body, textvariable=self.background_style,
                               values=["Theme", "Dark", "Light", "Minimal", "Custom"],
                               state="readonly", width=31)
        bg_menu.pack(fill="x")
        bg_menu.bind("<<ComboboxSelected>>", lambda _e: self._apply_overlay_style())
        tk.Button(body, text="Choose custom background color…",
                  command=self._choose_overlay_background, bg=PANEL_2, fg=TEXT,
                  activebackground="#303950", relief="flat", bd=0, pady=7).pack(fill="x", pady=(7, 2))

        label("Font family")
        fonts = ["Segoe UI", "Arial", "Calibri", "Cambria", "Georgia",
                 "Trebuchet MS", "Verdana", "Tahoma", "Consolas", "Courier New"]
        font_menu = ttk.Combobox(body, textvariable=self.font_family,
                                 values=fonts, state="readonly", width=31)
        font_menu.pack(fill="x")
        font_menu.bind("<<ComboboxSelected>>", lambda _e: self._apply_overlay_style())

        label("Font weight")
        weight_menu = ttk.Combobox(body, textvariable=self.font_weight,
                                   values=["Regular", "Bold"], state="readonly", width=31)
        weight_menu.pack(fill="x")
        weight_menu.bind("<<ComboboxSelected>>", lambda _e: self._apply_overlay_style())

        label("Fade speed  ·  0.5× slower to 2× faster")
        tk.Scale(body, from_=0.5, to=2.0, resolution=0.05, orient="horizontal",
                 variable=self.fade_speed, bg=PANEL, fg=TEXT, troughcolor=PANEL_2,
                 highlightthickness=0, bd=0, activebackground=ACCENT,
                 command=lambda _v: None).pack(fill="x")
        label("Animation transition")
        transition_menu = ttk.Combobox(
            body, textvariable=self.transition,
            values=["Smooth Rise", "Gentle Glide", "Soft Drift", "Fade Only"],
            state="readonly", width=31)
        transition_menu.pack(fill="x")
        tk.Button(body, text="▶  Preview animation", command=self._preview_overlay_animation,
                  bg=PANEL_2, fg=TEXT, activebackground="#303950", relief="flat",
                  bd=0, pady=8).pack(fill="x", pady=(12, 2))
        tk.Label(body, text="Appearance changes apply immediately. Motion settings\nare used for the next lyric or animation preview.",
                 bg=PANEL, fg=MUTED, justify="left", font=("Segoe UI", 8)).pack(anchor="w", pady=(13, 8))
        tk.Button(body, text="Done", command=win.destroy, bg=ACCENT, fg="#171326",
                  activebackground="#b9a6ff", relief="flat", bd=0, padx=18,
                  pady=8, font=("Segoe UI", 9, "bold")).pack(anchor="e")
        win.update_idletasks()
        win.geometry(f"{win.winfo_reqwidth()}x{win.winfo_reqheight()}")

    def _preview_overlay_animation(self):
        """Replay the current lyric animation, or the first sample line."""
        if self.lyrics:
            self._animate_lyric(self.active_index if self.active_index >= 0 else 0)

    def _choose_overlay_background(self):
        chosen = colorchooser.askcolor(color=self.custom_background,
                                       title="Choose overlay background",
                                       parent=getattr(self, "studio_window", self.root))
        if chosen and chosen[1]:
            self.custom_background = chosen[1]
            self.background_style.set("Custom")
            self._apply_overlay_style()

    def _set_opacity(self, *_):
        if self.overlay_animation_job:
            return
        try:
            self.overlay.attributes(
                "-alpha", 0.0 if self.overlay_dismissed_by_animation
                else self.opacity.get()
            )
        except tk.TclError:
            pass

    def _set_topmost(self):
        self.overlay.attributes("-topmost", self.always_on_top.get())

    def _place_overlay(self):
        self.root.update_idletasks()
        self.overlay.update_idletasks()
        w, h = max(420, self.overlay.winfo_reqwidth()), self.overlay.winfo_reqheight()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        positions = {
            "Bottom center": ((sw-w)//2, sh-h-95),
            "Top center": ((sw-w)//2, 65),
            "Center": ((sw-w)//2, (sh-h)//2),
            "Bottom left": (35, sh-h-95),
            "Bottom right": (sw-w-35, sh-h-95),
        }
        x, y = positions.get(self.position.get(), positions["Bottom center"])
        self.overlay_rest_x, self.overlay_rest_y = x, y
        self.overlay.geometry(f"{w}x{h}+{x}+{y}")
        self._set_opacity()

    def _update_overlay_text(self):
        if not self.overlay or not self.overlay.winfo_exists():
            return
        idx = self.active_index
        if idx < 0 and self.lyrics:
            line, next_line = "Ready when you are.", self.lyrics[0][1]
        elif 0 <= idx < len(self.lyrics):
            line = self.lyrics[idx][1]
            next_line = self.lyrics[idx+1][1] if idx+1 < len(self.lyrics) else ""
        else:
            line, next_line = "The session has ended.", ""

        self.overlay_kicker.configure(text=f"SONORA  /  {self.track_title.upper()}")
        self.next_label.configure(
            text=("NEXT  ·  " + next_line) if self.show_next.get() and next_line else ""
        )
        if idx >= 0 and idx != self.last_animated_index:
            self._animate_lyric(idx)
        elif idx == self.last_animated_index and self.lyric_canvas:
            self.lyric_canvas.itemconfigure(
                self.lyric_text_id, font=self._overlay_font()
            )
        elif idx < 0 and self.last_animated_index != -1:
            self.last_animated_index = -1
            self.lyric_canvas.coords(self.lyric_text_id, 2, 82)
            self.lyric_canvas.itemconfigure(
                self.lyric_text_id, text=line, fill=self._lyric_colors()[0],
                font=self._overlay_font()
            )
        self.overlay.update_idletasks()
        self._place_overlay_if_needed()

    def _place_overlay_if_needed(self):
        if self.overlay_animation_job:
            return
        if self.position.get() != "Custom":
            # Keep selected anchor while allowing the window height to adapt.
            self._place_overlay()

    def _refresh_lyrics(self):
        self.lyric_list.delete(0, tk.END)
        for seconds, line in self.lyrics:
            m, s = int(seconds // 60), int(seconds % 60)
            self.lyric_list.insert(tk.END, f"{m:02d}:{s:02d}   {line}")
        self.duration = max(10.0, self.lyrics[-1][0] + 5 if self.lyrics else 30.0)
        self.seek.configure(to=self.duration)
        self.duration_label.configure(text=self._fmt(self.duration))
        self._draw_wave()
        self._update_overlay_text()

    @staticmethod
    def _fmt(seconds):
        return f"{int(seconds)//60:02d}:{int(seconds)%60:02d}"

    def _draw_wave(self):
        if not hasattr(self, "wave_canvas"):
            return
        c = self.wave_canvas
        c.delete("all")
        w, h = max(1, c.winfo_width()), max(1, c.winfo_height())
        # A calm, deterministic waveform so it looks consistent between sessions.
        heights = [12, 20, 32, 17, 42, 25, 52, 31, 18, 38, 57, 26, 44, 19, 34, 49, 24, 15, 40, 28, 54, 21, 36, 17, 46, 27, 14, 34, 50, 23, 39, 18, 29, 45, 16, 33, 52, 25, 40, 19, 31, 48, 22, 37]
        gap = 5
        barw = max(2, (w - 44) / len(heights) - gap)
        usable = w - 44
        progress_x = 22 + usable * (self.current_time / max(1, self.duration))
        for i, val in enumerate(heights):
            x = 22 + i * (usable / len(heights))
            color = ACCENT if x < progress_x else "#30394d"
            c.create_rectangle(x, (h-val)/2, x+barw, (h+val)/2, fill=color, outline="", width=0)
        c.create_line(progress_x, 15, progress_x, h-15, fill=ACCENT_2, width=2)

    def _wave_seek(self, event):
        ratio = min(1, max(0, (event.x - 22) / max(1, self.wave_canvas.winfo_width() - 44)))
        self.current_time = ratio * self.duration
        self._sync_active_line()
        self._draw_wave()
        self._update_overlay_text()

    def _seek_changed(self, value):
        self.current_label.configure(text=self._fmt(float(value)))

    def _seek_release(self, _event):
        self.current_time = float(self.seek.get())
        self._sync_active_line()
        self._draw_wave()
        self._update_overlay_text()

    def _sync_active_line(self):
        idx = -1
        for i, (stamp, _line) in enumerate(self.lyrics):
            if stamp <= self.current_time:
                idx = i
            else:
                break
        self.active_index = idx
        if idx >= 0:
            self.lyric_list.selection_clear(0, tk.END)
            self.lyric_list.selection_set(idx)
            self.lyric_list.see(idx)
        self._update_overlay_text()

    def _jump_to_selected(self, _event=None):
        selected = self.lyric_list.curselection()
        if selected:
            self.current_time = self.lyrics[selected[0]][0]
            self.seek.set(self.current_time)
            self._sync_active_line()
            self._draw_wave()

    def toggle_play(self):
        self.playing = not self.playing
        self.play_btn.configure(text="Ⅱ  PAUSE" if self.playing else "▶  PLAY")
        self.last_tick = None

    def restart(self):
        self.current_time = 0
        self.seek.set(0)
        self._sync_active_line()
        self._draw_wave()

    def toggle_overlay(self):
        if self.overlay.state() == "withdrawn":
            self.overlay.deiconify()
        self._cancel_overlay_animation()
        self.overlay_dismissed_by_animation = False
        try:
            self.overlay.attributes("-alpha", self.opacity.get())
        except tk.TclError:
            pass
        self.overlay.lift()
        self.overlay_visible.set(True)

    def hide_overlay(self):
        self._cancel_overlay_animation()
        try:
            self.overlay.attributes("-alpha", self.opacity.get())
        except tk.TclError:
            pass
        self.overlay.withdraw()
        self.overlay_visible.set(False)

    def import_lyrics(self):
        path = filedialog.askopenfilename(
            title="Import synchronized lyrics",
            filetypes=[
                ("Supported lyrics", "*.lrc *.srt"),
                ("SubRip subtitles", "*.srt"),
                ("LRC lyrics", "*.lrc"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        try:
            content = Path(path).read_text(encoding="utf-8-sig")
            extension = Path(path).suffix.lower()
            if extension == ".srt":
                parsed = parse_srt(content)
                format_name = "SRT"
                if not parsed:
                    raise ValueError(
                        "No valid SubRip timestamp blocks were found. "
                        "Expected timestamps like 00:00:12,500 --> 00:00:15,000."
                    )
            else:
                parsed = parse_lrc(content)
                format_name = "LRC"
                if not parsed:
                    raise ValueError("No [mm:ss.xx] timestamps were found in this file.")

            self.lyrics = parsed
            self.track_title = Path(path).stem.replace("_", " ").replace("-", " ").title()
            self.artist = f"IMPORTED {format_name} SESSION"
            self.title_label.configure(text=self.track_title)
            self.artist_label.configure(text=self.artist)
            self.current_time = 0
            self.seek.set(0)
            self.active_index = -1
            self.playing = False
            self.play_btn.configure(text="▶  PLAY")
            self._refresh_lyrics()
            self._sync_active_line()
        except Exception as exc:
            messagebox.showerror("Couldn't import lyrics", str(exc))

    def _tick(self):
        now = self.root.tk.call("clock", "milliseconds")
        if self.playing:
            if self.last_tick is not None:
                self.current_time += min(0.25, max(0, (now - self.last_tick) / 1000))
            if self.current_time >= self.duration:
                self.current_time = self.duration
                self.playing = False
                self.play_btn.configure(text="▶  PLAY")
            self.seek.set(self.current_time)
            self.current_label.configure(text=self._fmt(self.current_time))
            self._sync_active_line()
            self._draw_wave()
        self.last_tick = now
        self.root.after(100, self._tick)

    def close(self):
        self._closing = True
        if self.overlay_animation_job:
            try:
                self.root.after_cancel(self.overlay_animation_job)
            except tk.TclError:
                pass
            self.overlay_animation_job = None
        try:
            self.overlay.destroy()
        except tk.TclError:
            pass
        self.root.destroy()


def main():
    root = tk.Tk()
    SonoraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

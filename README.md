# 🎵 SONORA — Floating Lyrics Desktop Application

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-FFB000)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Project-In%20Development-orange)

**SONORA** is a lightweight, customizable floating lyrics desktop application designed to display synchronized lyrics through an elegant, animated overlay.

Built with Python and Tkinter, SONORA provides an organized lyrics interface, timestamp-based synchronization, support for LRC and SRT subtitle files, and an advanced Overlay Studio for customizing the appearance and animation of floating lyrics.

The application focuses on making lyrics more visually appealing through smooth transitions, customizable typography, background styles, and adjustable animation settings.

---

# 🖥️ Application Preview

<p align="center">
  <img src="image/SONORA%20UI.PNG" width="850" alt="SONORA Floating Lyrics Desktop Application Interface">
</p>

<p align="center">
  <b>SONORA — Advanced Overlay Studio and Floating Lyrics Interface</b>
</p>

---

# 📌 Overview

Lyrics are an important part of the music-listening experience. However, switching between music applications and lyric websites can interrupt the experience.

SONORA was developed to provide a dedicated floating lyrics interface that displays timestamped lyrics in an elegant and customizable desktop overlay.

The application supports importing both LRC and SRT files, allowing users to display synchronized lyrics and subtitle-style captions. It also provides playback controls, a lyric timeline, and customizable overlay positioning.

With the introduction of the **Advanced Overlay Studio**, users can personalize the appearance and behavior of their floating lyrics, including background styles, font families, font weights, fade speed, and animation transitions.

SONORA aims to provide a simple yet visually appealing desktop experience for users who enjoy following lyrics while working, studying, or using their computers.

---

# ✨ Features

## 🎼 Lyrics Management

- 🎵 **LRC Importing** — Import timestamped `.lrc` lyric files.
- 📝 **SRT Importing** — Import `.srt` subtitle files.
- 🔍 **Automatic Format Detection** — Automatically select the appropriate parser based on the imported file extension.
- 🔤 **Multiline SRT Captions** — Preserve multiple caption lines within a single subtitle entry.
- ⏱️ **Timestamp Synchronization** — Display lyrics according to their associated timestamps.
- 🔁 **Multiple LRC Timestamps** — Support multiple timestamps assigned to the same lyric line.
- 📋 **Lyric Timeline** — View imported lyrics in an organized timeline.
- ⏩ **Direct Timeline Seeking** — Double-click a lyric entry to jump to its timestamp.

## 🪟 Floating Lyrics Overlay

- **Always-on-Top Window** — Keep the floating lyrics visible above other application windows.
- **Draggable Overlay** — Move the floating lyrics window to a preferred screen position.
- **Custom Positioning** — Choose from available placement presets.
- **Animated Lyrics** — Display lyrics using smooth fade and movement transitions.
- **Whole-Window Transparency** — Fade the entire overlay, including its background and text.
- **Adjustable Overlay Opacity** — Customize the overlay's transparency.
- **Previous and Next Lyrics** — Optionally display upcoming lyric information.
- **Live Animation Preview** — Preview the selected overlay animation.

## 🎨 Advanced Overlay Studio

SONORA includes an Overlay Studio that provides additional customization options.

### Background Customization

- Theme-based background.
- Dark background.
- Light background.
- Minimal background.
- Custom background color.

### Typography Customization

Choose from the following font families:

- Segoe UI
- Arial
- Calibri
- Cambria
- Georgia
- Trebuchet MS
- Verdana
- Tahoma
- Consolas
- Courier New

Additional typography options:

- Regular font weight.
- Bold font weight.
- Adjustable lyric font size.

### Animation Customization

Choose from four animation transitions:

| Transition | Description |
|---|---|
| Smooth Rise | Smooth upward movement with fading. |
| Gentle Glide | A longer and more gradual upward transition. |
| Soft Drift | A subtle floating movement. |
| Fade Only | Fade in and out without upward movement. |

### Adjustable Fade Speed

Customize the animation speed:

- 0.5× — Slower fading.
- 1.0× — Default speed.
- 1.5× — Faster fading.
- 2.0× — Much faster fading.

The visible holding duration remains consistent while fade-in and fade-out durations are adjusted.

## 🎛️ Playback and Interface

- ▶️ Play and pause controls.
- ↺ Restart playback.
- ⏱️ Current playback time and duration.
- 📊 Waveform-style timeline visualization.
- 🖱️ Clickable seeking.
- 🎨 Multiple interface themes.
- ⌨️ Keyboard shortcuts.
- 🌙 Modern dark interface.

---

# 🛠️ Technologies Used

## Programming Language

- **Python 3.10+** — Main programming language used to develop SONORA.

## Desktop Interface

- **Tkinter** — Provides the desktop graphical user interface.
- **Tkinter ttk** — Provides themed interface components and controls.

## Core Functionality

- **Regular Expressions (re)** — Used for parsing LRC timestamps and SRT subtitle timing.
- **Pathlib** — Used for handling file paths.
- **Python Time and Standard Library Utilities** — Support playback timing and animation logic.

## Development Tools

- Visual Studio Code.
- Git.
- GitHub.
- Python.
- Windows Desktop Environment.

**Note:** SONORA is designed to use Python's standard library and does not require additional third-party Python packages for its current core functionality.

---

# 🚀 Installation and Setup

Follow these instructions to install and run SONORA locally.

## Prerequisites

Before installing the application, ensure that you have:

- [Python 3.10 or newer](https://www.python.org/downloads/)
- [Git](https://git-scm.com/) (optional, for cloning the repository)
- Visual Studio Code or another code editor (optional)

**Important:** Ensure that Python and Tkinter are available in your installation. On Windows, the standard Python installer generally includes Tkinter.

## 1. Clone the Repository

```bash
git clone https://github.com/rheillunio2-byte/Sonora.git
```

## 2. Navigate to the Project Folder

```bash
cd Sonora
```

## 3. Open the Project in Visual Studio Code

```bash
code .
```

Alternatively, open Visual Studio Code manually and select the SONORA project folder.

## 4. Run the Application

### Windows

Double-click:

```text
run.bat
```

Alternatively, execute:

```bash
py -3 main.py
```

If the Python launcher is unavailable, try:

```bash
python main.py
```

### Linux and macOS

If Tkinter is installed and supported by your Python environment:

```bash
python3 main.py
```

**Note:** SONORA is primarily designed and targeted for Windows desktop environments. Overlay transparency and window behavior may vary on other operating systems.

---

# 📖 How to Use SONORA

## 1. Launching the Application

1. Open the SONORA project folder.
2. Run `run.bat` on Windows.
3. Wait for the main application window to appear.
4. Explore the player interface and overlay settings.

## 2. Importing Lyrics

SONORA supports LRC and SRT files.

1. Click **Import Lyrics**.
2. Select an `.lrc` or `.srt` file from your computer.
3. SONORA automatically identifies the format based on the file extension.
4. The imported lyrics are displayed in the lyric timeline.
5. Use the playback controls to navigate through the lyrics.

### Supported LRC Format

Example:

```text
[00:05.00]First lyric line
[00:09.50]Second lyric line
[00:14.00]Third lyric line
[00:18.25]Fourth lyric line
```

SONORA also supports multiple timestamps on a single lyric line:

```text
[00:05.00][00:10.00]Repeated lyric line
```

### Supported SRT Format

Example:

```text
1
00:00:05,000 --> 00:00:08,000
First subtitle line

2
00:00:09,000 --> 00:00:12,000
Second subtitle line

3
00:00:13,000 --> 00:00:17,000
A multiline subtitle
with an additional caption line.
```

SONORA preserves multiline caption content within each subtitle entry.

## 3. Using Playback Controls

The main interface includes controls for navigating through the lyric timeline.

Available controls include:

- **Play** — Start lyric timeline playback.
- **Pause** — Pause the current timeline.
- **Restart** — Return to the beginning.
- **Timeline Seeking** — Navigate to a specific playback position.
- **Lyric Selection** — Double-click a lyric entry to jump to its timestamp.

**Playback note:** The current player controls drive SONORA's internal lyric timeline. They do not currently function as a system-wide music player or automatically retrieve playback information from Spotify, YouTube, or other music applications.

## 4. Opening the Floating Lyrics Overlay

1. Launch SONORA.
2. Use the overlay preview control.
3. Enable the floating lyrics window.
4. Move the overlay to your preferred screen position.
5. Start the lyric timeline to see the synchronized lyrics.

The overlay can remain on top of other application windows when Always on Top is enabled.

## 5. Customizing the Overlay

Open the **Overlay Studio** to access the available customization options.

### Background Style

Choose between:

- Theme
- Dark
- Light
- Minimal
- Custom

The Custom option allows you to select a preferred background color.

### Font Family and Weight

Choose a font that matches your preferred appearance.

You can also switch between Regular and Bold font weights.

### Animation Speed

Adjust the fade speed to make the overlay appear and disappear more slowly or quickly.

A lower speed value creates longer fade durations, while a higher value creates shorter fade durations.

### Animation Transition

Experiment with the available transitions:

- Smooth Rise.
- Gentle Glide.
- Soft Drift.
- Fade Only.

### Preview Your Settings

Use the animation preview to see how your selected settings affect the floating lyrics before using them during playback.

---

# ⚙️ Core Modules

SONORA is organized around several functional components.

- **Lyrics Import Module:** Handles LRC and SRT file selection and importing.
- **LRC Parser:** Extracts lyric text and timestamps from LRC files.
- **SRT Parser:** Processes subtitle timestamps and multiline caption content.
- **Synchronization Module:** Determines which lyric should be displayed according to the current timeline position.
- **Playback Controller:** Handles play, pause, restart, and seeking operations.
- **Floating Overlay Module:** Creates and manages the separate floating lyrics window.
- **Animation Module:** Controls fade-in, holding, fade-out, movement, and transition easing.
- **Overlay Studio Module:** Manages background, font, fade-speed, and transition customization.
- **Positioning Module:** Handles overlay placement, dragging, and stable positioning.
- **Interface Module:** Manages the main application window, controls, timeline, and visual themes.

---

# 📂 Project Structure

```text
Sonora/
│
├── image/
│   └── SONORA UI.PNG
│
├── tests/
│   └── test_parsers.py
│
├── main.py
├── run.bat
├── .gitignore
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

### File Descriptions

| File / Folder | Purpose |
|---|---|
| `image/` | Stores project screenshots and visual references. |
| `image/SONORA UI.PNG` | Screenshot of the SONORA application interface. |
| `tests/` | Contains automated regression tests. |
| `tests/test_parsers.py` | Tests LRC/SRT parsing and animation-related logic. |
| `main.py` | Main Python application, interface, lyric parsing, playback, overlay, and animation functionality. |
| `run.bat` | Windows launcher for SONORA. |
| `.gitignore` | Specifies files and folders excluded from Git tracking. |
| `README.md` | Project overview, features, installation instructions, and documentation. |
| `CONTRIBUTING.md` | Guidelines for contributing to SONORA. |
| `LICENSE` | Contains the project's license. |

---

# ⚠️ Limitations and Important Notes

SONORA is a desktop application focused on timestamp-based lyric display and floating overlay customization.

The following limitations should be considered:

- The current playback controller drives an internal lyric timeline rather than controlling external music applications.
- SONORA does not currently detect the active song or automatically retrieve playback positions from Spotify, YouTube, or other music services.
- Lyrics must be supplied through supported LRC or SRT files.
- Incorrect or missing timestamps may affect synchronization.
- SRT multiline captions are combined for display within a single subtitle entry.
- Available fonts depend on the fonts installed on the operating system.
- Whole-window transparency depends on operating system and window manager support.
- Native overlay transparency and visual smoothness should be verified on the target Windows environment.
- The application does not currently provide MP4 importing or video playback functionality.

SONORA is intended to remain focused on synchronized lyrics rather than becoming a general-purpose video player.

---

# 🔮 Future Improvements

Possible future enhancements for SONORA include:

- Improved lyric synchronization controls.
- More customizable animation easing.
- Additional background styles and visual effects.
- More typography and font customization options.
- Additional overlay positioning controls.
- Improved multiline caption presentation.
- Better handling of malformed LRC and SRT files.
- Additional keyboard shortcuts.
- More advanced overlay preview functionality.
- Improved Windows transparency compatibility.
- Optional external music-player synchronization.
- More extensive automated testing.

These are proposed enhancements and are not necessarily available in the current version.

---

# 🤝 Contributing

Contributions, suggestions, bug reports, documentation updates, and feature improvements are welcome.

If you would like to contribute to SONORA, please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on setting up the development environment, following coding standards, reporting bugs, and submitting pull requests.

---

# 📄 License

This project is distributed under the MIT License.

See the [LICENSE](https://github.com/rheillunio2-byte/Sonora?tab=MIT-1-ov-file) file for the applicable terms and conditions.

---

# 👨‍💻 Developer

**Rheil Evans T. Lunio**

GitHub: [https://github.com/rheillunio2-byte](https://github.com/rheillunio2-byte)

Repository: [https://github.com/rheillunio2-byte/Sonora](https://github.com/rheillunio2-byte/Sonora)

---

**SONORA — Your Lyrics, In Motion.**
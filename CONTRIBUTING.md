# 🤝 Contributing to SONORA

Thank you for your interest in contributing to **SONORA**!

Contributions are welcome, whether they involve fixing bugs, improving lyric synchronization, developing new overlay features, enhancing animations, improving the user interface, or updating documentation.

This guide explains how to contribute while keeping the project organized, consistent, and maintainable.

---

## 📌 Table of Contents

1. Getting Started
2. Development Requirements
3. Setting Up the Project
4. Types of Contributions
5. Contribution Guidelines
6. Coding Standards
7. Working with LRC and SRT Files
8. Working with the Floating Overlay
9. Working with Animations and Transparency
10. Reporting Bugs
11. Suggesting Features
12. Submitting Changes
13. Pull Request Guidelines
14. Code of Conduct

---

## 1. Getting Started

Before contributing, familiarize yourself with the project and its existing functionality.

SONORA is a Python-based desktop lyrics application developed using Tkinter.

Its main components include:

- LRC lyric importing.
- SRT subtitle importing.
- Automatic lyric format detection.
- Timestamp-based lyric synchronization.
- Multiline subtitle handling.
- Floating lyrics overlay.
- Overlay positioning and customization.
- Animation and transparency controls.
- Advanced Overlay Studio.
- Playback timeline and controls.

You can begin contributing by reviewing the existing source code, identifying potential improvements, or selecting an issue that you would like to address.

---

## 2. Development Requirements

Before starting development, ensure that you have the following tools installed:

- **Python 3.10+** – Main programming language.
- **Tkinter** – Desktop graphical user interface framework.
- **Git** – Version control system.
- **Code Editor** – Visual Studio Code or another preferred editor.
- **Windows Desktop Environment** – Recommended for testing native overlay behavior.

Basic familiarity with the following technologies is recommended:

- Python.
- Tkinter.
- Object-oriented programming.
- Regular expressions.
- Desktop application development.
- Git and GitHub.

Understanding Windows window transparency and Tkinter's window-management functionality is helpful when modifying the floating overlay.

**Note:** SONORA's current core implementation uses Python's standard library and does not require additional third-party Python packages.

---

## 3. Setting Up the Project

Follow these steps to prepare your local development environment.

### Step 1: Fork the Repository

Fork the SONORA repository to your own GitHub account.

Repository:

https://github.com/rheillunio2-byte/Sonora

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/Sonora.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 3: Enter the Project Directory

```bash
cd Sonora
```

### Step 4: Open the Project in Visual Studio Code

```bash
code .
```

Alternatively, open Visual Studio Code manually and select the SONORA project folder.

### Step 5: Run the Application

On Windows:

```bash
py -3 main.py
```

Alternatively, double-click:

```text
run.bat
```

### Step 6: Run the Tests

SONORA includes regression tests for lyric parsing and animation-related functionality.

Run the tests using:

```bash
py -3 -m unittest discover -s tests -v
```

### Step 7: Create a Branch

Create a separate branch for your contribution.

For new features:

```bash
git checkout -b feature/your-feature-name
```

For bug fixes:

```bash
git checkout -b fix/your-bug-name
```

Avoid making unrelated changes directly to the main branch.

---

## 4. Types of Contributions

### A. Bug Fixes

You can help improve SONORA by identifying and correcting problems such as:

- Incorrect LRC timestamp parsing.
- Incorrect SRT timestamp handling.
- Lyrics appearing at the wrong time.
- Multiline subtitle formatting problems.
- Overlay positioning issues.
- Cumulative animation movement.
- Incomplete transparency.
- Animation flickering.
- Incorrect fade timing.
- Overlay windows failing to close properly.
- Broken interface controls.
- Importing errors.

### B. Feature Improvements

Suggestions and implementations for new functionality are welcome, including:

- Additional LRC and SRT parsing capabilities.
- Improved lyric synchronization.
- More advanced overlay customization.
- Additional background styles.
- More font families and typography options.
- Additional animation transitions.
- Adjustable animation durations.
- Improved lyric preview functionality.
- More positioning presets.
- Better keyboard shortcuts.
- Improved accessibility.

### C. User Interface Improvements

Contributions to the design and usability of SONORA are also encouraged.

Examples include:

- More consistent spacing and typography.
- Improved settings organization.
- Smoother transitions and animations.
- Better overlay previews.
- Improved color combinations.
- More intuitive controls.
- Better screen positioning.
- Improved desktop scaling.

### D. Documentation Improvements

You may also contribute by:

- Correcting documentation errors.
- Improving installation instructions.
- Adding usage examples.
- Updating technical explanations.
- Improving the README.
- Clarifying known limitations.
- Documenting new overlay settings.

---

## 5. Contribution Guidelines

To maintain project quality, please follow these guidelines:

1. Keep contributions relevant to SONORA.
2. Avoid introducing unnecessary dependencies.
3. Preserve existing functionality unless a change is intentional.
4. Use clear and descriptive names for variables, functions, and classes.
5. Keep code organized and readable.
6. Test changes before submitting them.
7. Avoid committing generated files or unnecessary dependencies.
8. Update documentation when a contribution changes application behavior.
9. Explain significant changes clearly in your pull request.
10. Do not include private credentials, API keys, or sensitive information in commits.
11. Preserve compatibility with supported LRC and SRT formats.
12. Avoid introducing unrelated video playback functionality or MP4 support.

---

## 6. Coding Standards

Consistency helps make SONORA easier to maintain and improve.

### Python

- Follow standard Python naming conventions.
- Use descriptive variable and function names.
- Prefer reusable functions and methods.
- Keep classes focused on their intended responsibilities.
- Avoid unnecessary code duplication.
- Handle invalid inputs and exceptions appropriately.
- Remove unused imports and variables.
- Add comments when explaining non-obvious implementation details.
- Use type hints where appropriate.

### Tkinter and Interface Development

- Maintain consistent spacing and styling.
- Use appropriate Tkinter widgets.
- Avoid unnecessarily complicated widget hierarchies.
- Keep interface controls organized.
- Use callbacks appropriately.
- Prevent overlapping or unnecessary scheduled callbacks.
- Ensure windows close safely.
- Avoid blocking the interface during animations or playback updates.

### File Organization

Place code in the appropriate project files and directories.

Keep the main application organized and avoid introducing unnecessary source files or dependencies.

---

## 7. Working with LRC and SRT Files

Lyrics importing and timestamp accuracy are essential parts of SONORA.

Contributions to these components should preserve compatibility with supported file formats.

### LRC Format

SONORA supports standard timestamp-based LRC files.

Example:

```text
[00:05.00]First lyric line
[00:09.50]Second lyric line
[00:14.00]Third lyric line
```

Multiple timestamps on the same line are also supported.

```text
[00:05.00][00:10.00]Repeated lyric line
```

When modifying the LRC parser, ensure that:

- Timestamps are converted into seconds correctly.
- Multiple timestamps are handled.
- Lyric text is preserved.
- Entries are sorted by timestamp.
- Empty or invalid lines are handled safely.
- Existing supported timestamp precision remains compatible.

### SRT Format

SONORA supports SubRip subtitle files.

Example:

```text
1
00:00:05,000 --> 00:00:08,000
First subtitle line

2
00:00:09,000 --> 00:00:12,000
Second subtitle line
```

Multiline captions are also supported.

```text
3
00:00:13,000 --> 00:00:17,000
First caption line
Second caption line
```

When modifying the SRT parser, ensure that:

- Subtitle timestamps are interpreted correctly.
- Comma and decimal timestamp separators are supported.
- Multiple subtitle blocks are processed.
- Multiline captions remain together.
- Subtitle formatting tags are handled appropriately.
- Invalid blocks do not crash the application.
- Existing synchronization behavior is preserved.

### Testing Lyric Importing

Whenever possible, test:

- Standard LRC files.
- LRC files with multiple timestamps.
- LRC files with fractional timestamps.
- Standard SRT files.
- SRT files using comma milliseconds.
- SRT files using decimal milliseconds.
- Multiline SRT captions.
- Empty files.
- Invalid timestamps.
- Multiple lyric entries.
- Files with different line endings.

Do not assume that an imported file is valid simply because it opens successfully.

---

## 8. Working with the Floating Overlay

The floating lyrics overlay is one of SONORA's most important components.

Changes to this functionality should prioritize stability, positioning accuracy, readability, and transparency.

When modifying the overlay:

- Preserve the ability to move the floating window.
- Maintain the Always on Top functionality.
- Keep the overlay positioning consistent.
- Prevent cumulative movement after repeated animations.
- Ensure that new lyrics can appear correctly.
- Avoid unnecessary window recreation.
- Prevent overlapping animation callbacks.
- Handle window closing safely.
- Restore the correct overlay state when an animation finishes.

### Positioning Requirements

The overlay should maintain a stable original anchor position.

Animation movement should be calculated relative to that anchor instead of repeatedly modifying the current window position.

This helps prevent progressive upward drifting.

After the animation finishes, the overlay should return to its intended position.

---

## 9. Working with Animations and Transparency

Animation quality is a major part of SONORA's visual experience.

Contributions should prioritize smooth movement, consistent timing, and complete transparency.

### Complete Overlay Transparency

The entire floating overlay should fade together.

This includes:

- Main lyric text.
- Previous and next lyric text.
- Background card.
- Borders.
- Decorative elements.
- Other overlay components.

Avoid implementations that fade only the text while leaving the background visible.

The final opacity should explicitly reach:

```python
0.0
```

### Animation Performance

When modifying animation functionality:

- Use smooth easing where appropriate.
- Avoid sudden movement.
- Prevent overlapping callbacks.
- Cancel existing animations safely when necessary.
- Restore the correct opacity when a new lyric appears.
- Keep animation timing consistent.
- Avoid unnecessary interface updates.
- Ensure the overlay does not flicker.

### Animation Transitions

SONORA currently provides four transition styles:

- Smooth Rise.
- Gentle Glide.
- Soft Drift.
- Fade Only.

Additional transitions are welcome, provided they remain smooth and compatible with the existing overlay system.

### Windows Compatibility

Windows transparency behavior should be considered when modifying the overlay.

The application uses Tkinter's top-level window transparency functionality.

Test changes on an actual Windows desktop whenever possible, especially when modifying:

- Window opacity.
- Overlay positioning.
- Animation callbacks.
- Window visibility.
- Window closing behavior.

Do not assume that a transparency implementation works correctly simply because the Python code executes without errors.

---

## 10. Reporting Bugs

If you encounter a problem, please report it through the repository's GitHub Issues section.

A useful bug report should include:

**Title:** A short description of the problem.

**Description:** Explain what happened and what you expected to happen.

**Steps to Reproduce:** Provide the steps needed to reproduce the issue.

**Expected Behavior:** Describe the correct result or behavior.

**Actual Behavior:** Describe what happened instead.

**Environment:** Include relevant information such as:

- Operating system.
- Windows version.
- Python version.
- Application version or commit.
- Display scaling settings, when relevant.

**Screenshots or Recordings:** Include screenshots or screen recordings when they help demonstrate the problem.

For lyric synchronization bugs, include the relevant LRC or SRT sample when possible.

For animation bugs, explain which transition, background style, and fade speed were selected.

---

## 11. Suggesting Features

Feature suggestions are welcome.

Before submitting a new suggestion:

1. Check whether a similar feature request already exists.
2. Explain the problem the proposed feature addresses.
3. Describe how the feature should work.
4. Explain how it would improve SONORA.
5. Include screenshots, examples, or reference materials when useful.

Suggestions should be practical, relevant, and consistent with SONORA's purpose as a synchronized floating lyrics application.

---

## 12. Submitting Changes

After completing your changes, review and test them before committing.

### Step 1: Check Your Changes

```bash
git status
```

### Step 2: Stage the Relevant Files

```bash
git add .
```

Only stage files that belong to your contribution.

### Step 3: Commit Your Changes

Use a clear and descriptive commit message.

```bash
git commit -m "Improve floating overlay animation"
```

Other examples:

```bash
git commit -m "Fix LRC timestamp parsing"
git commit -m "Improve SRT multiline handling"
git commit -m "Add overlay background customization"
git commit -m "Enhance animation transitions"
git commit -m "Improve overlay positioning"
git commit -m "Update project documentation"
```

### Step 4: Push Your Branch

```bash
git push origin feature/your-feature-name
```

### Step 5: Open a Pull Request

Visit your fork on GitHub and create a pull request targeting the original repository's main branch.

---

## 13. Pull Request Guidelines

Before submitting a pull request, make sure that:

- [ ] Your changes address the intended issue or feature.
- [ ] Your code follows the project's coding standards.
- [ ] Existing functionality has not been unintentionally broken.
- [ ] LRC importing has been tested where applicable.
- [ ] SRT importing has been tested where applicable.
- [ ] Multiline subtitle handling remains functional.
- [ ] Animation behavior has been tested.
- [ ] Overlay positioning remains stable.
- [ ] Transparency behavior has been checked.
- [ ] Existing settings remain functional.
- [ ] No unnecessary files or dependencies were added.
- [ ] Documentation has been updated when necessary.
- [ ] Your commit messages are clear and descriptive.

### Pull Request Description

A good pull request should explain:

**Summary:** What did you change?

**Purpose:** Why was the change necessary?

**Implementation:** How did you implement it?

**Testing:** What did you test?

**Screenshots or Recordings:** Include before-and-after visuals for interface or animation changes when appropriate.

Keep pull requests focused. If you are proposing several unrelated changes, consider submitting separate pull requests.

---

## 14. Code of Conduct

All contributors are expected to maintain a respectful and collaborative environment.

Please:

- Be respectful when communicating with others.
- Provide constructive feedback.
- Respect different levels of experience.
- Avoid personal attacks or inappropriate language.
- Focus discussions on improving the project.
- Be open to suggestions and revisions.

Contributions should help make SONORA more reliable, accessible, customizable, and enjoyable to use.

---

## 📬 Thank You for Contributing!

Thank you for taking the time to contribute to SONORA.

Every improvement, whether a small bug fix, a synchronization enhancement, an animation refinement, a new customization option, or a documentation update, helps make the project better.

**Together, we can make SONORA a more elegant, reliable, and customizable floating lyrics application.**

---

*SONORA — Your Lyrics, In Motion.*
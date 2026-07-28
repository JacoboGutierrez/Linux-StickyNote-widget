# Virtual Sticky Notes for Linux — v1.4

A desktop application built with Python and PySide6 for creating persistent virtual sticky notes.

## What's new in version 1.4

- When the **CRS** or **Default** theme is selected from a note, all currently visible notes immediately switch to the selected theme.
- The theme change is saved for every visible note and restored in the next session.
- Hidden notes keep their existing theme and are not modified until they are visible during a new theme change.

## Features

- Create, edit, duplicate, and delete notes.
- Show or hide each note using the checkbox in the note list.
- Automatically save text, title, color, position, and size.
- Restore visible notes and their order when the next session starts.
- Reorder notes by dragging items in the manager panel.
- Includes eight pastel colors and a custom color picker.
- Includes the **Default** and **CRS** themes.
- Change the theme of all visible notes at the same time.
- Choose individually whether each note behaves as a normal window or stays above all other windows.
- Includes an **English / Español** language selector, with English as the default language and persistent language preferences.
- Note scrollbars are invisible, while scrolling remains available through the mouse wheel, keyboard, or touchpad.
- Vertical manager panel with a minimum size of **423 × 623 px**.
- Linux system tray integration.

## Updating an existing installation

Extract this version and run the installer again:

```bash
chmod +x install.sh
./install.sh
```

The installer replaces the application while preserving saved notes, positions, colors, themes, and individual always-on-top settings.

## Running without installation

```bash
chmod +x run.sh
./run.sh
```

On the first run, the script creates a virtual environment and installs PySide6.

## Installing in the application menu

```bash
chmod +x install.sh
./install.sh
```

Then search for **Virtual Sticky Notes** or **Notas Adhesivas** in your Linux application menu.

## Uninstalling

```bash
chmod +x uninstall.sh
./uninstall.sh
```

## Saved data

Notes continue using the same data location as previous versions, usually:

```text
~/.local/share/SantiApps/Notas Adhesivas/
```

The selected language is stored through the local Qt settings for `SantiApps/virtual-sticky-notes`.

## Wayland note

On some Wayland desktop environments, the compositor may limit the option to keep a window above all others. This behavior is usually more consistent on X11.

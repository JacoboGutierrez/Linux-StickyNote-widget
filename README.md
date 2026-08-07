<p align="center">
  <img
    src="https://github.com/JacoboGutierrez/JacoboGutierrez/blob/main/stickynote-01.png?raw=true"
    alt="Santiago Gutierrez profile banner"
  />
</p>

<p align="center">
  <img
    src="https://github.com/JacoboGutierrez/JacoboGutierrez/blob/main/stickynote-02.png?raw=true"
    alt="Santiago Gutierrez profile banner"
  />
</p>

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

<hr>

# Español: #

# Virtual Sticky Notes para Linux — v1.4

Aplicación de escritorio desarrollada con Python y PySide6 para crear notas adhesivas virtuales persistentes.

## Novedades de la versión 1.4

- Al seleccionar el tema **CRS** o **Por defecto** desde una nota, todas las notas visibles cambian inmediatamente al tema elegido.
- El cambio de tema se guarda en cada una de las notas visibles para restaurarlo en la próxima sesión.
- Las notas ocultas conservan el tema que tenían y no se modifican hasta que estén visibles durante un nuevo cambio de tema.

## Funciones

- Crea, edita, duplica y elimina notas.
- Muestra u oculta cada nota mediante la casilla de la lista.
- Guarda automáticamente el texto, título, color, posición y tamaño.
- Restaura las notas visibles y su orden al abrir la siguiente sesión.
- Permite reordenar las notas arrastrando los elementos dentro del administrador.
- Incluye ocho colores pastel y un selector de color personalizado.
- Incluye los temas **Por defecto** y **CRS**.
- Cambia simultáneamente el tema de todas las notas visibles.
- Permite elegir individualmente si cada nota se comporta como una ventana normal o permanece encima de las demás ventanas.
- Incluye un selector de idioma **English / Español**, con inglés como idioma predeterminado y guardado automático de la preferencia.
- Las barras de desplazamiento de las notas son invisibles, pero el desplazamiento continúa funcionando con la rueda del mouse, el teclado o el touchpad.
- Panel vertical con un tamaño mínimo de **423 × 623 px**.
- Integración con el área de notificación de Linux.

## Actualizar una instalación anterior

Descomprime esta versión y vuelve a ejecutar:

```bash
chmod +x install.sh
./install.sh
```

El instalador reemplaza el programa, pero conserva las notas guardadas, sus posiciones, colores, temas y configuraciones individuales de superposición.

## Ejecutar sin instalar

```bash
chmod +x run.sh
./run.sh
```

La primera ejecución crea un entorno virtual e instala PySide6.

## Instalar en el menú de aplicaciones

```bash
chmod +x install.sh
./install.sh
```

Después busca **Virtual Sticky Notes** o **Notas Adhesivas** en el menú de aplicaciones de Linux.

## Desinstalar

```bash
chmod +x uninstall.sh
./uninstall.sh
```

## Datos guardados

Las notas continúan utilizando la misma ubicación de datos de las versiones anteriores, normalmente:

```text
~/.local/share/SantiApps/Notas Adhesivas/
```

El idioma se guarda mediante la configuración local de Qt para `SantiApps/virtual-sticky-notes`.

## Nota sobre Wayland

En algunos escritorios que utilizan Wayland, el compositor puede limitar la opción de mantener una ventana siempre encima. En X11, este comportamiento suele ser más consistente.

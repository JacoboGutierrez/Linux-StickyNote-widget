#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$HOME/.local/share/virtual-sticky-notes"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/virtual-sticky-notes.desktop"

command -v python3 >/dev/null 2>&1 || {
  echo "Error: python3 no está instalado." >&2
  exit 1
}

if ! python3 -m venv --help >/dev/null 2>&1; then
  echo "Error: falta el módulo venv de Python. En Debian/Ubuntu instala python3-venv." >&2
  exit 1
fi

mkdir -p "$APP_DIR" "$DESKTOP_DIR"
cp "$SOURCE_DIR/main.py" "$SOURCE_DIR/requirements.txt" "$SOURCE_DIR/run.sh" "$APP_DIR/"
cp -r "$SOURCE_DIR/assets" "$APP_DIR/"
chmod +x "$APP_DIR/run.sh"

if [[ ! -d "$APP_DIR/.venv" ]]; then
  python3 -m venv "$APP_DIR/.venv"
fi
"$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Virtual Sticky Notes
Name[es]=Notas Adhesivas
Comment=Persistent virtual sticky notes
Comment[es]=Notas adhesivas virtuales persistentes
Exec=$APP_DIR/.venv/bin/python $APP_DIR/main.py
Icon=$APP_DIR/assets/virtual-sticky-notes.svg
Terminal=false
Categories=Utility;Office;
StartupNotify=true
EOF
chmod +x "$DESKTOP_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi

echo "Instalación completada. Busca 'Virtual Sticky Notes' o 'Notas Adhesivas' en el menú de aplicaciones."

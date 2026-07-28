#!/usr/bin/env bash
set -euo pipefail
rm -rf "$HOME/.local/share/virtual-sticky-notes"
rm -f "$HOME/.local/share/applications/virtual-sticky-notes.desktop"
echo "Aplicación desinstalada. Tus notas guardadas permanecen en la carpeta de datos de Qt/SantiApps."

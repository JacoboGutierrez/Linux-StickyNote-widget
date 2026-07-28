# Virtual Sticky Notes para Linux — v1.4

Aplicación de escritorio hecha con Python y PySide6 para crear notas adhesivas virtuales persistentes.

## Novedades de la versión 1.4

- Al seleccionar el tema **CRS** o **Default / Por defecto** desde una nota, todas las notas visibles cambian inmediatamente al tema elegido.
- El cambio de tema se guarda en cada una de las notas visibles para restaurarlo en la próxima sesión.
- Las notas ocultas conservan el tema que tenían; no se modifican hasta que estén visibles durante un nuevo cambio de tema.

## Funciones

- Crea, edita, duplica y elimina notas.
- Muestra u oculta cada nota mediante la casilla de la lista.
- Guarda automáticamente texto, título, color, posición y tamaño.
- Restaura las notas visibles y su orden al abrir la siguiente sesión.
- Permite reordenarlas arrastrando elementos en el administrador.
- Incluye ocho colores pastel y selector de color personalizado.
- Incluye los temas **Default / Por defecto** y **CRS**.
- Cambia simultáneamente el tema de todas las notas que estén visibles.
- Permite elegir individualmente si cada nota queda como ventana normal o permanece encima de las demás.
- Incluye selector de idioma **English / Español**, con inglés por defecto y preferencia persistente.
- Las barras de desplazamiento de las notas son invisibles, manteniendo el desplazamiento con rueda, teclado o touchpad.
- Panel vertical con tamaño mínimo de **423 × 623 px**.
- Se integra al área de notificación.

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

Las notas siguen utilizando la misma ubicación de datos de las versiones anteriores, normalmente:

```text
~/.local/share/SantiApps/Notas Adhesivas/
```

El idioma se guarda mediante la configuración local de Qt para `SantiApps/virtual-sticky-notes`.

## Nota sobre Wayland

En algunos escritorios con Wayland, el compositor puede limitar la opción de mantener una ventana siempre encima. En X11 el comportamiento suele ser más consistente.

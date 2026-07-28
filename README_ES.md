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

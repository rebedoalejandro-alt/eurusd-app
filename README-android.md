# APK: Conversor EUR → USD (Kivy)

Este proyecto incluye una app muy simple hecha con Kivy (`main.py`) que:
- Toma un monto en euros
- Convierte a dólares con tasa en vivo desde internet
- Tiene un botón "Convertir" y un botón "Limpiar"

A continuación, pasos para probar en el PC y luego generar la APK en Windows usando WSL + Buildozer.

## 1) Probar en el PC (opcional)
En tu máquina (Windows), crea y activa un virtualenv, instala Kivy y ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install kivy
python main.py
```

Deberías ver la ventana con el campo de euros, y los botones Convertir/Limpiar.

## 2) Generar APK en Windows con WSL + Buildozer
La forma más estable de compilar APK con Kivy en Windows es usando WSL (Ubuntu) y Buildozer.

1. Instala WSL (si no lo tienes) y Ubuntu desde Microsoft Store.
2. Abre Ubuntu (WSL) y ve a tu carpeta del proyecto (montada en `/mnt/c/...`). Ejemplo:
   ```bash
   cd "/mnt/c/Users/<TU_USUARIO>/Downloads/testing"
   ```
3. Instala dependencias del sistema y Buildozer:
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-setuptools python3-venv git zip unzip openjdk-17-jdk
   pip3 install --upgrade pip
   pip3 install buildozer cython
   ```
4. Crea y activa un virtualenv en WSL (recomendado):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   ```
5. Instala requisitos de Python:
   ```bash
   pip install kivy requests
   ```
6. Compila APK (la primera vez tardará bastante):
   ```bash
   buildozer android debug
   ```
   - Buildozer descargará el SDK/NDK de Android y generará `bin/*.apk`.

7. Copia el APK a tu móvil e instálalo (activa orígenes desconocidos en Android si es necesario).

Notas:
- Si usas WSL2, asegúrate de tener suficiente espacio en disco y una conexión estable.
- Si Buildozer pide aceptar licencias del SDK, sigue las instrucciones en pantalla.
- La app requiere conexión a internet para obtener la tasa (permiso incluido en `buildozer.spec`). Si no hay conexión, mostrará "Error de conexión".

## 3) Personalización rápida
- Nombre de la app: cambia `title` en `buildozer.spec`.
- Ícono: define `icon.filename` en `buildozer.spec` y añade la imagen.
- Permisos: esta app no necesita permisos; si en el futuro necesitas internet, añade `android.permissions = INTERNET`.

## 4) Problemas comunes
- Error de Java/SDK: asegúrate de tener `openjdk-17-jdk` y deja que Buildozer instale el SDK/NDK.
- Rutas con espacio: procura usar rutas sin espacios o comillas.
- Tiempo de compilación: la primera compilación puede tardar 10–30 minutos.

¡Listo! Con esto deberías poder generar tu APK de conversión EUR → USD.

## (Alternativa) Generar APK automáticamente con GitHub Actions
Si no quieres instalar nada localmente, puedes usar la acción incluida para construir en la nube:

1. Crea un repositorio en GitHub y sube este proyecto (incluye todos los archivos).
2. En GitHub, ve a la pestaña "Actions" y ejecuta el workflow "Build Android APK" (o haz un push a `main`).
3. Espera a que termine (puede tardar 10–30 minutos en la primera vez).
4. Descarga el artefacto `eurusd-apk` que contendrá `bin/*.apk` (APK de debug listo para instalar).

Notas:
- El workflow usa la imagen Docker `kivy/buildozer` para compilar y adjunta el APK como artefacto.
- Es un APK de debug (firma de depuración). Para publicar en Play Store se requiere firma de release.

# Buildozer specification file

[app]
title = EUR a USD
package.name = eurusd
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1.0

requirements = python3,kivy,requests,certifi
orientation = portrait
fullscreen = 0
log_level = 2

# Icon/splash (opcionales)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

# Permisos
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 0

[app@android]
# Ajustes específicos de Android
android.archs = armeabi-v7a, arm64-v8a

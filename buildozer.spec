[app]

title = NovaRockTierList
package.name = bandtierlist
package.domain = com.ramslayer

source.dir = .
source.include_exts = py
source.exclude_dirs = .git,venv,logs,cache

version = 0.1

requirements = python3==3.10.13,hostpython3==3.10.13,setuptools,cython==0.29.33,kivy==2.3.0,Pillow,colorlog

orientation = portrait
fullscreen = 0

android.api = 34
android.minapi = 24

android.ndk = 25b
android.ndk_api = 24

android.archs = arm64-v8a

android.copy_libs = 1
android.allow_backup = True

android.enable_androidx = True

android.release_artifact = apk

p4a.branch = master

# Optional, added to automate building
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
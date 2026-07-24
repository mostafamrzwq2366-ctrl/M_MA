[app]

# (str) Title of your application
title = My Application

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Requirements
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (list) Supported architectures
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

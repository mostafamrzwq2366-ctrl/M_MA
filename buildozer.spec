[app]

# (str) Title of your application
title = TwistMena

# (str) Package name
package.name = M_MA

# (str) Package domain (needed for android packaging)
package.domain = org.twistmena

# (list) Source files to include (let it find python files automatically)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# حط هنا المتطلبات بتاعتك زي kivy و requests
requirements = python3,kivy,requests

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1

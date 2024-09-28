[app]
# (str) Title of your application
title = Capital Connect

# (str) Package name
package.name = bulkmessage

# (str) Package domain (unique identifier)
package.domain = com.mycapital.capitalconnect

# (str) The directory where the source files are located
source.dir = .  # Set to current directory where your main .py file is located

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Main script of your application
source.main = main.py  # Specify your main Python file here

# (list) Application requirements
requirements = python3, kivy, android, pyjnius, plyer

# (str) Android version requirements
android.api = 31  # Target API level
android.minapi = 21  # Minimum API level

# (list) Permissions required by the app
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_SMS, RECEIVE_BOOT_COMPLETED

# (str) Application version
version = 0.1

# (str) Presplash of the app
presplash.filename = %(source.dir)s/data/presplash.png  # Presplash image

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Orientation support for the app (only vertical supported for SMS apps)
orientation = portrait

# (str) Application icon (add if you have a custom one)
# icon.filename = %(source.dir)s/data/icon.png  # Uncomment and set your icon path

# (str) Screenshots (one for each file)
# android.screenshots = 1  # Uncomment to add screenshots

# (str) Add additional source files required for compilation
# android.add_src = src/main/java  # Uncomment if you have Java source files

# (str) Add additional jar libraries to compile into the app
# android.add_jars = libs/android-support-v4.jar  # Uncomment if you have jar files

# (list) Screens to support (phone or tablet)
# screens = small, normal, large, xlarge  # Uncomment to specify screen support

# (str) Any additional arguments for the build process
# build_args = --sdk_root=<path_to_android_sdk> --ndk_root=<path_to_android_ndk>  # Uncomment to specify SDK/NDK paths

# (list) Features your app depends on
# android.features = android.hardware.camera, android.hardware.telephony  # Uncomment to specify hardware features

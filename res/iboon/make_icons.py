"""
Disabled. The icons are the approved TeamViewer by iBoon artwork (2026-11-24),
committed as files; this script used to draw the old placeholder mark (a
monitor with an arrow) and would overwrite them. It only says so now.

The artwork comes as a full set laid out like this repository: the
teamviewer-by-iboon logo's `platform/remote-by-iboon` folder. To change the
logo, copy the new set over the repository root, so these stay one drawing:

    res/{icon,mac-icon,32x32,64x64,128x128,128x128@2x}.png, res/icon.ico,
    res/tray-icon.ico, res/mac-tray-{dark,light}-x2.png,
    res/{logo,logo-header,scalable}.svg, flutter/assets/icon.svg,
    flutter/windows/runner/resources/app_icon.ico,
    flutter/macos/Runner/AppIcon.icns, the iOS AppIcon set, the Android
    mipmaps and ic_launcher_background.xml, and fastlane's icon.png.
"""

import sys

if __name__ == "__main__":
    sys.exit("make_icons.py is disabled: the icons are the approved artwork, copied in as files (see the top of this script).")

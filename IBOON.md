# TeamViewer by iBoon: the client (remote-by-iboon)

This repository is iBoon Technologies' build of [RustDesk](https://github.com/rustdesk/rustdesk)
(AGPL-3.0), used inside iBoon for remote support. It is the client that
TeamViewer by iBoon installs: the TeamViewer by iBoon service
(the teamviewer-by-iboon repository) decides who may see whose screen,
iBoon Agent installs this client on employee computers and drives it, and
this client moves the pixels.

The two stay separate repositories, but on an employee's computer this client
is called **TeamViewer by iBoon** wherever people read its name. (Builds up to
iboon-1.4.9-1 called it "Remote by iBoon".)

It is RustDesk with a small set of changes, all on the `iboon` branch on top
of the upstream release tag they are based on. The source of every build we
distribute is the tag it was built from (`iboon-<rustdesk version>-<n>`), and
the build itself is attached to that tag's GitHub release.

## What differs from upstream

| Change | Where |
| --- | --- |
| Name: `RemoteByiBoon` internally on Windows (exe, service, install folder, IPC), `rustdesk` on Linux; "TeamViewer by iBoon" wherever people read it (see the table below) | `src/common.rs` (`IBOON_DISPLAY_NAME`, `get_display_app_name`, `apply_iboon_branding`), `src/lang.rs`, `flutter/lib/consts.dart` and its three uses, `flutter/windows/runner/Runner.rc`, `Cargo.toml` |
| iBoon's own RustDesk server and key built in | `src/common.rs` (`IBOON_*`, overridable at build time with the env vars of the same names) |
| No settings page, address book or RustDesk account; RustDesk's own update check off; only a one-time password gets in; command-line settings still allowed (iBoon Agent configures each session with them) | `src/common.rs` |
| Icons | `res/iboon/make_icons.py` renders all of them |
| Installed-apps name, installer title, shortcuts, service display name | `res/msi/preprocess.py` (`--display-name`, `DisplayProduct`), `res/msi/Package/Package.wxs`, `res/msi/Package/Components/Folders.wxs` |
| CI: Windows x64 MSI and Linux x86_64 .deb only | `res/iboon/make_workflow.py` generates `.github/workflows/iboon-build.yml` from upstream's `flutter-build.yml`; `iboon-release.yml` runs it on `iboon-*` tags |

### Where people read "TeamViewer by iBoon"

| What people see | Where it comes from |
| --- | --- |
| Main, remote, file-transfer and connection-manager window titles, the title bar text | `kIboonDisplayName` (`flutter/lib/consts.dart`): `getWindowName` in `common.dart`, `main.dart`, `tabbar_widget.dart`; the Windows runner's first title via `get_iboon_display_name` (`src/flutter.rs`, `flutter/windows/runner/main.cpp`); the Linux runner's first title (`flutter/linux/my_application.cc`) |
| Every translated string that says "RustDesk" (dialogs, connection messages, About), on Windows and Linux | `src/lang.rs` (always the display name, also on Linux where `is_rustdesk()` is true) |
| Tray tooltip | `src/tray.rs` |
| Windows notifications (install / update toasts) | `src/core_main.rs` |
| Linux administrator-password dialog title | `src/platform/gtk_sudo.rs` |
| File description and product name (file Properties, UAC prompt, Task Manager, Startup apps) | `flutter/windows/runner/Runner.rc`, `Cargo.toml` (`[package.metadata.winres]`) |
| Settings > Apps / Add or Remove Programs | `res/msi/preprocess.py` (`DisplayName` from `--display-name`); `src/platform/windows.rs` for a self-install |
| MSI product name and installer dialogs | `DisplayProduct` in `res/msi/preprocess.py`, used by `Package.wxs` |
| Start menu folder, Start menu and desktop shortcuts, "Uninstall TeamViewer by iBoon" | `Folders.wxs` (`DisplayProduct`) and the MSI language strings, rewritten by `preprocess.py` |
| Windows service display name ("TeamViewer by iBoon Service") | `preprocess.py` rewrites the MSI custom action's display name; `src/platform/windows.rs` for `sc create` |
| Linux menu entry | `res/rustdesk.desktop`, `res/rustdesk-link.desktop` (`Name=`); the .deb description in `build.py` |

What stays internal, on purpose: the Windows exe, service name, install folder
(`C:\Program Files\RemoteByiBoon`), config folder, IPC pipes, registry keys
and firewall rule (`RemoteByiBoon`); the startup tray shortcut and printer names
(`RemoteByiBoon Tray`, `RemoteByiBoon Printer`, which code finds by those
names); the Linux package, binary, service and .desktop file names
(`rustdesk`); and the MSI UpgradeCode, which `preprocess.py` derives from
`RemoteByiBoon.exe`, so every new MSI upgrades the installed one in place.
iBoon Agent finds the client, its service and its processes by these names.
The release file names (`remote-by-iboon-<version>-x86_64.msi`,
`rustdesk-<version>-x86_64.deb`) also stay, since nobody installs them by hand.

These reuse upstream's own "custom client" code path (`apply_custom_client_data`,
split out of `read_custom_client`), so everything upstream already does for a
branded client applies here too.

On Linux the internal name stays `rustdesk`: its packaging, systemd unit and
process detection are written for that binary name. Everything else above
applies.

## Moving to a new RustDesk release

```sh
git fetch upstream --tags
git rebase <new upstream tag>          # onto the iboon branch
python res/iboon/make_workflow.py      # re-derive the CI from upstream's
python res/iboon/make_icons.py
git tag iboon-<version>-1 && git push origin iboon --tags
```

Then pin the new MSI/.deb hashes in iboon-agent (`src-tauri/rustdesk-pins.json`)
and upload them with its `scripts/upload-rustdesk.mjs`. A rebuild of the same
RustDesk version is tagged `iboon-<version>-<n+1>`; the Agent reinstalls when
its pinned release differs from the one it last installed.

## Licence

RustDesk is Copyright © Purslane Tech Pte. Ltd. and contributors, licensed
under the GNU Affero General Public License v3.0 (see `LICENCE`). Our changes
are released under the same licence.

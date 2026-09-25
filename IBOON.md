# Remote by iBoon

This repository is iBoon Technologies' build of [RustDesk](https://github.com/rustdesk/rustdesk)
(AGPL-3.0), used inside iBoon for remote support: TeamViewer by iBoon decides
who may see whose screen, iBoon Agent installs this client on employee
computers and drives it, and this client moves the pixels.

It is RustDesk with a small set of changes, all on the `iboon` branch on top
of the upstream release tag they are based on. The source of every build we
distribute is the tag it was built from (`iboon-<rustdesk version>-<n>`), and
the build itself is attached to that tag's GitHub release.

## What differs from upstream

| Change | Where |
| --- | --- |
| Name: `RemoteByiBoon` internally on Windows (exe, service, install folder, IPC), "Remote by iBoon" wherever people read it | `src/common.rs` (`apply_iboon_branding`), `src/lang.rs`, `flutter/lib/consts.dart` and its three uses, `flutter/windows/runner/Runner.rc`, `Cargo.toml` |
| iBoon's own RustDesk server and key built in | `src/common.rs` (`IBOON_*`, overridable at build time with the env vars of the same names) |
| No settings page, address book or RustDesk account; RustDesk's own update check off; only a one-time password gets in; command-line settings still allowed (iBoon Agent configures each session with them) | `src/common.rs` |
| Icons | `res/iboon/make_icons.py` renders all of them |
| Installed-apps name | `res/msi/preprocess.py` (`--display-name`) |
| CI: Windows x64 MSI and Linux x86_64 .deb only | `res/iboon/make_workflow.py` generates `.github/workflows/iboon-build.yml` from upstream's `flutter-build.yml`; `iboon-release.yml` runs it on `iboon-*` tags |

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
and upload them with its `scripts/upload-rustdesk.mjs`.

## Licence

RustDesk is Copyright © Purslane Tech Pte. Ltd. and contributors, licensed
under the GNU Affero General Public License v3.0 (see `LICENCE`). Our changes
are released under the same licence.

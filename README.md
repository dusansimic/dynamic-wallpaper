<img align="left" style="vertical-align: middle" width="120" height="120" src="data/icons/hicolor/scalable/apps/me.dusansimic.DynamicWallpaper.svg">

# Dynamic Wallpaper

Dynamic wallpaper creator for GNOME 42 and beyond

🎨 Icon designed by [Rokwallaby](https://github.com/Rokwallaby).

![Light screenshot](data/screenshots/main.png#gh-light-mode-only)
![Dark screenshot](data/screenshots/main-dark.png#gh-dark-mode-only)

## 💻 Installation

Dynamic Wallpaper is [available on Flathub](https://flathub.org/apps/details/me.dusansimic.DynamicWallpaper).

<a href='https://flathub.org/apps/details/me.dusansimic.DynamicWallpaper'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a>

To download development snapshots, you can use the artifacts from
[CI](https://github.com/dusansimic/dynamic-wallpaper/actions) builds. Download
the latest artifact and install the flatpak file from the
archive (`flatpak install dynamic-wallpaper.flatpak`).

## 🛠️ Dependencies

Please make sure you have these dependencies first before building.

```
gtk4
libadwaita-1
meson
python3
```

## 🏗️ Building

Clone the repo and run:

```bash
meson _build --prefix=/usr && cd _build
sudo ninja install
```

## 📜 License

This app is licensed under the GPL2 license.


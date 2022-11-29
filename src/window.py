# window.py
#
# Copyright 2022 Dušan Simić
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from gi.repository import Gtk, Adw, Gio
from .gdwFileRow import FileRow
import os
import shutil
import xml.etree.cElementTree as ET


@Gtk.Template(resource_path='/me/dusansimic/DynamicWallpaper/window.ui')
class DynamicWallpaperWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DynamicWallpaperWindow'

    toast_overlay = Gtk.Template.Child()
    input_rows = Gtk.Template.Child()
    entry_name = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._setup_actions()
        self.entry_name.grab_focus()

        self.file_light = FileRow(self, _('_Light wallpaper'))
        self.file_light.set_use_underline(True)
        self.file_dark = FileRow(self, _('_Dark wallpaper'))
        self.file_dark.set_use_underline(True)

        self.input_rows.add(self.file_light)
        self.input_rows.add(self.file_dark)

    def _setup_actions(self):
        _create_action = Gio.SimpleAction.new('create', None)
        _create_action.connect('activate', self._on_create_action)
        self.add_action(_create_action)

    def _on_create_action(self, _action, _param):
        wp_name = self.entry_name.get_text().strip()

        if wp_name == "":
            self.toast_overlay.add_toast(Adw.Toast.new(_('Wallpaper name not set')))
            return
        elif not self._filename_valid(wp_name):
            self.toast_overlay.add_toast(Adw.Toast.new(_('Wallpaper name cannot contain null or /')))
            return

        data_dir = os.path.join(os.environ.get('HOME'), '.local', 'share')
        wall_dir = os.path.join(data_dir, 'backgrounds', wp_name)
        xml_path = os.path.join(data_dir, 'gnome-background-properties', '{}.xml'.format(wp_name))
        if any(map(os.path.exists, [wall_dir, xml_path])):
            self.toast_overlay.add_toast(Adw.Toast.new(_('Wallpaper with the same name already exists')))
            return

        try:
            light_path = self.file_light.wp_file.path
            dark_path = self.file_dark.wp_file.path
        except AttributeError:
            self.toast_overlay.add_toast(Adw.Toast.new(_('No wallpapers selected')))

        if (light_path == "" or not os.path.exists(light_path)):
            self.toast_overlay.add_toast(Adw.Toast.new(_('Light mode wallpaper not selected')))
            return
        if (dark_path == "" or not os.path.exists(dark_path)):
            self.toast_overlay.add_toast(Adw.Toast.new(_('Dark mode wallpaper not selected')))
            return

        data_dir = os.path.join(os.environ.get('HOME'), '.local', 'share')
        props_dir = os.path.join(data_dir, 'gnome-background-properties')
        bgs_dir = os.path.join(data_dir, 'backgrounds', wp_name)

        l_wall_path = os.path.join(bgs_dir, "{}-l{}".format(wp_name, self.file_light.wp_file.ext))
        d_wall_path = os.path.join(bgs_dir, "{}-d{}".format(wp_name, self.file_dark.wp_file.ext))
        xml_path = os.path.join(props_dir, "{}.xml".format(wp_name))

        self._make_dirs(props_dir, bgs_dir)
        self._copy_wallpapers(l_wall_path, d_wall_path)
        self._write_xml(wp_name, l_wall_path, d_wall_path, xml_path)

        self.toast_overlay.add_toast(Adw.Toast.new(_('New dynamic wallpaper created')))

    def _make_dirs(self, props_dir, bgs_dir):
        os.makedirs(props_dir, exist_ok=True)
        os.makedirs(bgs_dir, exist_ok=True)

    def _copy_wallpapers(self, l_wall_path, d_wall_path):
        shutil.copyfile(self.file_light.wp_file.path, l_wall_path)
        shutil.copyfile(self.file_dark.wp_file.path, d_wall_path)

    def _write_xml(self, wp_name, l_wall_path, d_wall_path, xml_path):
        tree = ET.Element('wallpapers')
        wallpaper = ET.SubElement(tree, 'wallpaper', {'deleted': 'false'})
        ET.SubElement(wallpaper, 'name').text = wp_name
        ET.SubElement(wallpaper, 'filename').text = l_wall_path
        ET.SubElement(wallpaper, 'filename-dark').text = d_wall_path
        ET.SubElement(wallpaper, 'options').text = 'zoom'
        ET.SubElement(wallpaper, 'shade_type').text = 'solid'
        ET.SubElement(wallpaper, 'pcolor').text = '#3465a4'
        ET.SubElement(wallpaper, 'scolor').text = '#000000'
        with open(os.path.join(xml_path), 'wb') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">'.encode('UTF-8'))
            ET.ElementTree(tree).write(f, 'utf-8')

    def _filename_valid(self, filename) -> bool:
        invalid_chars = ['\0', '/']
        return not any([c in invalid_chars for c in filename])


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
from .wallpaper_picker import WallpaperPicker
import os
import shutil
import xml.etree.cElementTree as ET


@Gtk.Template(resource_path='/me/dusansimic/DynamicWallpaper/window.ui')
class DynamicWallpaperWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'DynamicWallpaperWindow'

    wallpaper_name = None
    images = {
        'light': None,
        'dark': None,
    }
    open_chooser = None

    toast_overlay = Gtk.Template.Child()
    name_entry = Gtk.Template.Child()
    picker_buttons = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._setup_actions()

        self.name_entry.grab_focus()

        self.light_picker = WallpaperPicker(self, 'Select light wallpaper')
        self.dark_picker = WallpaperPicker(self, 'Select dark wallpaper')

        self.picker_buttons.append(self.light_picker)
        self.picker_buttons.append(self.dark_picker)

        images_filter = Gtk.FileFilter()
        images_filter.set_name(_('PNG & JPEG'))
        images_filter.add_mime_type('image/png')
        images_filter.add_mime_type('image/jpeg')

        self.wallpaper_chooser = Gtk.FileChooserNative.new(
            _('Select wallpaper'),
            self,
            Gtk.FileChooserAction.OPEN,
            None,
            None,
        )
        self.wallpaper_chooser.set_filter(images_filter)
        self.wallpaper_chooser.set_select_multiple(False)
        self.wallpaper_chooser.connect('response', self._on_wallpaper_chooser_response)

    def _setup_actions(self):
        _light_open_action = Gio.SimpleAction.new('light_open', None)
        _light_open_action.connect('activate', self._on_light_open_action)
        self.add_action(_light_open_action)

        _dark_open_action = Gio.SimpleAction.new('dark_open', None)
        _dark_open_action.connect('activate', self._on_dark_open_action)
        self.add_action(_dark_open_action)

        _create_action = Gio.SimpleAction.new('create', None)
        _create_action.connect('activate', self._on_create_action)
        self.add_action(_create_action)

    def _on_wallpaper_chooser_response(self, dialog, response):
        dialog.hide()
        if response == Gtk.ResponseType.ACCEPT:
            files = dialog.get_files()
            if files:
                f = files[0]
                path = f.get_path()
                _, extension = os.path.splitext(path)
                self.images[self.open_chooser] = {
                    'path': path,
                    'extension': extension,
                }
        self.open_chooser = None

    def _on_light_open_action(self, _action, _param):
        self.open_chooser = 'light'
        self.wallpaper_chooser.show()

    def _on_dark_open_action(self, _action, _param):
        self.open_chooser = 'dark'
        self.wallpaper_chooser.show()

    def _on_create_action(self, _action, _param):
        self.wallpaper_name = self.name_entry.get_text().strip()

        if (self.wallpaper_name == ""):
            self.toast_overlay.add_toast(Adw.Toast.new('Wallpaper name not set'))
            return
        if (self.images['light'] == None):
            self.toast_overlay.add_toast(Adw.Toast.new('Light mode wallpaper not selected'))
            return
        if (self.images['dark'] == None):
            self.toast_overlay.add_toast(Adw.Toast.new('Dark mode wallpaper not selected'))
            return

        data_dir = os.path.join(os.environ.get('HOME'), '.local', 'share')
        props_dir = os.path.join(data_dir, 'gnome-background-properties')
        bgs_dir = os.path.join(data_dir, 'backgrounds', self.wallpaper_name)

        l_wall_path = os.path.join(bgs_dir, "{}-l{}".format(self.wallpaper_name, self.images['light']['extension']))
        d_wall_path = os.path.join(bgs_dir, "{}-d{}".format(self.wallpaper_name, self.images['dark']['extension']))
        xml_path = os.path.join(props_dir, "{}.xml".format(self.wallpaper_name))

        self._make_dirs(props_dir, bgs_dir)
        self._copy_wallpapers(l_wall_path, d_wall_path)
        self._write_xml(l_wall_path, d_wall_path, xml_path)

        self.toast_overlay.add_toast(Adw.Toast.new('New dynamic wallpaper created'))

    def _make_dirs(self, props_dir, bgs_dir):
        os.makedirs(props_dir, exist_ok=True)
        os.makedirs(bgs_dir, exist_ok=True)

    def _copy_wallpapers(self, l_wall_path, d_wall_path):
        shutil.copyfile(self.images['light']['path'], l_wall_path)
        shutil.copyfile(self.images['dark']['path'], d_wall_path)

    def _write_xml(self, l_wall_path, d_wall_path, xml_path):
        tree = ET.Element('wallpapers')
        wallpaper = ET.SubElement(tree, 'wallpaper', {'deleted': 'false'})
        ET.SubElement(wallpaper, 'name').text = self.wallpaper_name
        ET.SubElement(wallpaper, 'filename').text = l_wall_path
        ET.SubElement(wallpaper, 'filename-dark').text = d_wall_path
        ET.SubElement(wallpaper, 'options').text = 'zoom'
        ET.SubElement(wallpaper, 'shade_type').text = 'solid'
        ET.SubElement(wallpaper, 'pcolor').text = '#3465a4'
        ET.SubElement(wallpaper, 'scolor').text = '#000000'
        with open(os.path.join(xml_path), 'wb') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">'.encode('UTF-8'))
            ET.ElementTree(tree).write(f, 'utf-8')

class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Dynamic Wallpaper'
        self.props.version = "0.0.1"
        self.props.authors = ['Dušan Simić']
        self.props.copyright = '2022 Dušan Simić'
        self.props.logo_icon_name = 'me.dusansimic.DynamicWallpaper'
        self.props.modal = True
        self.set_transient_for(parent)


# main.py
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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import DynamicWallpaperWindow

class DynamicWallpaperApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, app_id, version):
        super().__init__(application_id=app_id,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.on_quit_action, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self._app_id = app_id
        self._version = version

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = DynamicWallpaperWindow(application=self)
        win.present()

    def on_quit_action(self, widget, _):
        """Callback for the app.quit acgtion."""
        self.quit()

    # I'm not sure what's passed here as an argument
    def on_about_action(self, _action, _none):
        """Callback for the app.about action."""
        artists = [
          'Rokwallaby',
          'David Lapshin <ddaudix@gmail.com>'
        ]

        developers = [
          'Dušan Simić <dusan.simic1810@gmail.com>',
          'Mattia B'
        ]

        about = Adw.AboutWindow(
          application_name = _('Dynamic Wallpaper'),
          application_icon = self._app_id,
          version = self._version,
          copyright = '© 2022 Dušan Simić',
          website = 'https://github.com/dusansimic/dynamic-wallpaper',
          license_type = Gtk.License(Gtk.License.GPL_2_0),
          issue_url = 'https://github.com/dusansimic/dynamic-wallpaper/issues/new/choose',
          developer_name = 'Dušan Simić',
          developers = developers,
          artists = artists,
          translator_credits = _('translator-credits'),
          transient_for = self.props.active_window,
        )
        about.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(app_id, version):
    """The application's entry point."""
    app = DynamicWallpaperApplication(app_id, version)
    return app.run(sys.argv)

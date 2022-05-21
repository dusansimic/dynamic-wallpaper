from gi.repository import Gtk, Adw, Gio
from enum import Enum
import os
import uuid

class WallpaperType(Enum):
    LIGHT = 1
    DARK = 2

    def label(self):
        return {
            'LIGHT': _('Light'),
            'DARK': _('Dark'),
        }[self.name]

    def icon(self):
        return {
            'LIGHT': 'weather-clear',
            'DARK': 'weather-clear-night',
        }[self.name]

@Gtk.Template(resource_path='/me/dusansimic/DynamicWallpaper/wallpaper_picker.ui')
class WallpaperPicker(Adw.Bin):
  __gtype_name__ = 'WallpaperPicker'

  wallpaper = None

  picker_button = Gtk.Template.Child()
  label = Gtk.Template.Child()
  icon = Gtk.Template.Child()
  picture_overlay = Gtk.Template.Child()
  wallpaper_picture = Gtk.Template.Child()
  #delete_button = Gtk.Template.Child()

  def __init__(self, parent, type, uid = None):
    Adw.Bin.__init__(self)

    self._uid = uuid.uuid4() if uid == None else uid

    self.picker_button.set_action_name('win.{}_open'.format(self._uid))
    #self.delete_button.set_action_name('win.{}_delete'.format(self._uid))
    self.label.set_label(type.label())
    self.icon.set_from_icon_name(type.icon())

    self._update_state()
    self._setup_actions(parent)

    images_filter = Gtk.FileFilter()
    images_filter.set_name(_('PNG & JPEG'))
    images_filter.add_mime_type('image/png')
    images_filter.add_mime_type('image/jpeg')

    self.wallpaper_chooser = Gtk.FileChooserNative.new(
      _('Select wallpaper'),
      parent,
      Gtk.FileChooserAction.OPEN,
      None,
      None,
    )
    self.wallpaper_chooser.set_filter(images_filter)
    self.wallpaper_chooser.set_select_multiple(False)
    self.wallpaper_chooser.connect('response', self._on_wallpaper_chooser_response)

  def _setup_actions(self, parent):
    open_action = Gio.SimpleAction.new('{}_open'.format(self._uid), None)
    open_action.connect('activate', self._on_open_action)
    parent.add_action(open_action)

    delete_action = Gio.SimpleAction.new('{}_delete'.format(self._uid), None)
    delete_action.connect('activate', self._on_delete_action)
    parent.add_action(delete_action)

  def _update_state(self):
    self.picker_button.set_visible(bool(not self.wallpaper))
    self.picture_overlay.set_visible(bool(self.wallpaper))

  def _update_image(self):
    self.picture_overlay.set_from_file(self.wallpaper.path)

  def _on_open_action(self, _action, _param):
    self.wallpaper_chooser.show()

  def _on_wallpaper_chooser_response(self, dialog, response):
    dialog.hide()
    if response == Gtk.ResponseType.ACCEPT:
      files = dialog.get_files()
      if files:
        f = files[0]
        path = f.get_path()
        filename = os.path.basename(path)
        _, extension = os.path.splitext(path)
        self.wallpaper = Wallpaper(path, filename, extension)
        self.wallpaper_picture.set_filename(path)
        self._update_state()
        self._update_image()

  def _on_delete_action(self, _action, _param):
    self.wallpaper = None
    self._update_state()

  def _humanize(self, num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"

class Wallpaper:
  def __init__(self, path, filename, extension):
    self.path = path
    self.filename = filename
    self.extension = extension


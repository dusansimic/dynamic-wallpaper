from gi.repository import Gtk, Adw, Gio
import os
import uuid

@Gtk.Template(resource_path='/me/dusansimic/DynamicWallpaper/gdw-file-row.ui')
class FileRow(Adw.ActionRow):
    __gtype_name__ = 'GdwFileRow'

    wp_file = None

    button_open = Gtk.Template.Child()
    button_delete = Gtk.Template.Child()

    def __init__(self, parent, label, uid = None):
        Adw.ActionRow.__init__(self)

        self._uid = uuid.uuid4() if uid == None else uid

        self.set_title(label)
        self.button_open.set_action_name('win.{}_open'.format(self._uid))
        self.button_delete.set_action_name('win.{}_delete'.format(self._uid))

        self._setup_actions(parent)

        imgs_filter = Gtk.FileFilter()
        imgs_filter.set_name(_('PNG & JPEG'))
        imgs_filter.add_mime_type('image/png')
        imgs_filter.add_mime_type('image/jpeg')

        self._chooser = Gtk.FileChooserNative.new(
            _('Select wallpaper'),
            parent,
            Gtk.FileChooserAction.OPEN,
            None,
            None
        )
        self._chooser.set_filter(imgs_filter)
        self._chooser.set_select_multiple(False)
        self._chooser.connect('response', self._on_chooser_response)

    def _setup_actions(self, parent):
        open_action = Gio.SimpleAction.new('{}_open'.format(self._uid), None)
        open_action.connect('activate', self._on_open_action)
        parent.add_action(open_action)

        delete_action = Gio.SimpleAction.new('{}_delete'.format(self._uid), None)
        delete_action.connect('activate', self._on_delete_action)
        parent.add_action(delete_action)

    def _update_state(self):
        self.button_open.set_visible(bool(not self.wp_file))
        self.button_delete.set_visible(bool(self.wp_file))
        self.set_subtitle(self.wp_file.fname if self.wp_file else '')

    def _on_open_action(self, _action, _param):
        self._chooser.show()

    def _on_chooser_response(self, dialog, response):
        dialog.hide()
        if response == Gtk.ResponseType.ACCEPT:
            files = dialog.get_files()
            if files:
                f = files[0]
                path = f.get_path()
                fname = os.path.basename(path)
                _, ext = os.path.splitext(path)
                self.wp_file = Wallpaper(path, fname, ext)
                self._update_state()

    def _on_delete_action(self, _action, _param):
        self.wp_file = None
        self._update_state()

class Wallpaper:
    def __init__(self, path, fname, ext):
        self.path = path
        self.fname = fname
        self.ext = ext


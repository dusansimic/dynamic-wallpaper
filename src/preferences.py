from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/me/dusansimic/DynamicWallpaper/preferences.ui')
class PreferencesDialog(Adw.PreferencesWindow):
    __gtype_name__ = 'DynamicWallpaperPreferencesWindow'

    def __init__(self, parent):
        Adw.PreferencesWindow.__init__(self)
        self.set_transient_for(parent)

from gi.repository import Gtk

@Gtk.Template(resource_path='/me/dusansimic/DynamicWallpaper/wallpaper_picker.ui')
class WallpaperPicker(Gtk.Box):
    __gtype_name__ = 'WallpaperPicker'

    image = None

    def __init__(self):
        Gtk.Box.__init__(self)
        #select_button = Gtk.Template.Child()
        #action_row = Gtk.Template.Child()
        #print(select_button)
        #select_button.set_visible(True)
        #action_row.set_visible(False)

    def _remove_image(self):
        print('removing image')

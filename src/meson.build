pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'me.dusansimic.DynamicWallpaper')
gnome = import('gnome')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('app_id', app_id)

configure_file(
  input: '@0@.in'.format(app_id),
  output: '@0@'.format(app_id),
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

dynamic_wallpaper_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'gdwFileRow.py',
]

dependencies = [
	dependency('gtk4'),
	dependency('libadwaita-1', version: '>= 1.2.alpha'),
]

install_data(dynamic_wallpaper_sources, install_dir: moduledir)

config = configuration_data()
config.set('app_id', app_id)

subdir('ui')

gnome.compile_resources(app_id,
  'dynamic_wallpaper.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: join_paths(get_option('prefix'), get_option('datadir'), meson.project_name()),
  dependencies: blueprints
)

desktop_conf = configure_file(
  input: '@0@.desktop.in'.format(meson.project_name()),
  output: '@0@.desktop.in'.format(app_id),
  configuration: config,
)

desktop_file = i18n.merge_file(
  input: desktop_conf,
  output: '@0@.desktop'.format(app_id),
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_conf = configure_file(
	input: '@0@.appdata.xml.in'.format(meson.project_name()),
	output: '@0@.appdata.xml.in'.format(app_id),
	configuration: config,
)

appstream_file = i18n.merge_file(
  input: appstream_conf,
  output: '@0@.appdata.xml'.format(app_id),
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate-relax', appstream_file]
  )
endif

install_data('@0@.gschema.xml'.format(meson.project_name()),
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

subdir('icons')

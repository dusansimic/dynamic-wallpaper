blueprints = custom_target('blueprints',
  input: files(
    'window.blp',
    'gdw-file-row.blp',
    'help-overlay.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@']
)

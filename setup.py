import cx_Freeze  # pip install cx_freeze

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable("main.py", base="Win32GUI")]
excludes = []

cx_Freeze.setup(
    name="shreck game",
    options={"build_exe":
                 {'include_msvcr': True,
                  "packages": ["pygame", "pygame_gui", "pytmx"], # прописываем все зависимости проекта
                  "zip_include_packages": ["pygame/", "SQLAlchemy", 'pygame_gui', 'pygame-ce', 'sqlite3',
                                            'pygame_gui/', 'pygame_gui.data',
                                           'pygame_gui.data/', 'pygame_gui.core.ui_font_dictionary', 'pygame_gui.data/FiraCode-Regular.ttf'],
                  "include_files": ['data/', 'map/', 'stat.txt', 'themes.json', 'scripts.py', 'entities.py',
                                    'levels.py', 'map.py', 'sound_effects_settings.py', 'sprite_tools.py', 'particles.py'], # прописываем все свои папочи и важные документы
                  "excludes": excludes}},
    executables=executables
)
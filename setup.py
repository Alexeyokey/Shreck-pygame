import cx_Freeze  # pip install cx_freeze
import sys
base = "Win32GUI" if sys.platform == "win32" else None
executables = [cx_Freeze.Executable("main.py", base=base)]
excludes = []

cx_Freeze.setup(
    name="shreck game",
    options={"build_exe":
                 {'include_msvcr': True,
                  "packages": ["pygame", "pygame_gui", "pytmx"], # прописываем все зависимости проекта
                  "zip_include_packages": ["pygame/", 'pygame_gui/', 'pygame-ce'],
                  "include_files": ['data', 'map', 'stat.txt', 'themes.json', 'scripts.py', 'entities.py', "shrek_09. Smash Mouth - All Star.mp3",
                                    'levels.py', 'map.py', 'sound_effects_settings.py', 'sprite_tools.py', 'particles.py'], # прописываем все свои папочи и важные документы
                  "excludes": excludes}},
    executables=executables
)
from cx_Freeze import Executable, setup

# Список всех файлов и папок вашего проекта, за исключением исполняемого,
# находящихся в корневой папке
# include_files = ['game', 'test']  # file or directory
include_files = ['chromedriver.exe']  # file or directory

options = {
'build_exe': {
    'include_msvcr': True,
    'build_exe': 'Kaban Parse',
    'include_files': include_files,
    }
}

# Задаем исполняемый файл и свою иконку.
executables = [
    Executable("kaban_parse.py", icon='favicon.ico'),
]

setup(
    name="Kaban Parsing",
    version="0.1",
    description="Game",
    executables=executables,
    options=options,
)
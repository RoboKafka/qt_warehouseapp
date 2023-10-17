from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
build_options = {
    'packages': ['PySide6'],
    'excludes': [],
    'includes': ['dataframe_palletfind', 'log', 'tabview']
}

base = None

executables = [
    Executable('widget.py', base=base)  # Assuming your main script is named 'main.py'
]

setup(
    name='Warehouse_loc',
    version='0.1',
    description='Description of your app',
    options={'build_exe': build_options},
    executables=executables
)

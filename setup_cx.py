from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "tkinter",
        "openpyxl",
        "csv",
    ],
    "excludes": [
        "unittest",
        "email",
        "http",
        "html",
        "xml",
        "sqlite3",
        "logging",
        "distutils",
        "setuptools",
        "numpy",
        "pandas",
    ],
    "optimize": 2,
    "include_msvcr": False,
}

# --------------- MSI CUSTOM SHORTCUTS ----------------

# (Shortcut | Directory | Name | Component | Target | Args | Description | Hotkey | Icon | IconIndex | ShowCmd | WkDir)
shortcut_table = [
    (
        "DesktopShortcut",         # ID
        "DesktopFolder",           # where: Desktop
        "Porovnávač sloupců",      # shortcut name
        "MAINEXEC",                # component
        "[TARGETDIR]PorovnavacSloupcu.exe",  # target EXE
        None,
        "Porovnávač sloupců – ultra lite",   # description
        None,
        None,
        None,
        None,
        None,
    ),
    (
        "StartMenuShortcut",
        "StartMenuFolder",
        "Porovnávač sloupců",
        "MAINEXEC",
        "[TARGETDIR]PorovnavacSloupcu.exe",
        None,
        "Porovnávač sloupců – ultra lite",
        None,
        None,
        None,
        None,
        None,
    )
]

msi_data = {
    "Shortcut": shortcut_table
}

# ---------------------------------------------------------

executables = [
    Executable(
        script="column_comparer.py",
        base="gui",
        target_name="PorovnavacSloupcu.exe",
        # icon="app.ico",
    )
]

setup(
    name="PorovnavacSloupcu",
    version="1.0",
    description="Ultra-lehký porovnávač sloupců",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": {
            "data": msi_data,
            "upgrade_code": "{12345678-ABCD-4321-ABCD-1234567890FF}",
            "initial_target_dir": r"[ProgramFilesFolder]\PorovnavacSloupcu"
        },
    },
    executables=executables
)

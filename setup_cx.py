from cx_Freeze import setup, Executable

# ---------------------- build_exe options ----------------------
build_exe_options = {
    "packages": [
        "tkinter",
        "openpyxl",
        "xml",   # kvůli openpyxl → xml.etree.ElementTree
        "csv",
    ],
    "includes": [
        "xml.etree.ElementTree",  # explicitně přibalit
    ],
    "excludes": [
        "numpy",
        "pandas",
        "unittest",
        "distutils",
        "setuptools",
    ],
    "optimize": 1,
    "include_msvcr": False,
}

# ---------------------- zástupci pro MSI -----------------------
# (Shortcut | Directory | Name | Component_ | Target | Args | Description | Hotkey | Icon | IconIndex | ShowCmd | WkDir)
shortcut_table = [
    (
        "DesktopShortcut",
        "DesktopFolder",
        "Porovnávač sloupců",
        "TARGETDIR",  # bezpečný Component_ → existuje vždy
        "[TARGETDIR]PorovnavacSloupcu.exe",
        None,
        "Porovnávač sloupců – ultra lite",
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
        "TARGETDIR",
        "[TARGETDIR]PorovnavacSloupcu.exe",
        None,
        "Porovnávač sloupců – ultra lite",
        None,
        None,
        None,
        None,
        None,
    ),
]

msi_data = {
    "Shortcut": shortcut_table
}

# ------------------------- Executable --------------------------
executables = [
    Executable(
        "column_comparer.py",
        base="gui",
        target_name="PorovnavacSloupcu.exe",
        # pokud máš ikonu, přidej soubor .ico a odkomentuj:
        # icon="porovnavac.ico",
    )
]

# --------------------------- setup -----------------------------
setup(
    name="PorovnavacSloupcu",
    version="1.0",
    description="Ultra-lehký porovnávač sloupců (openpyxl + csv, bez pandas)",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": {
            "data": msi_data,
            "upgrade_code": "{12345678-ABCD-4321-ABCD-1234567890FF}",
            "initial_target_dir": r"[ProgramFilesFolder]\PorovnavacSloupcu",
        },
    },
    executables=executables,
)

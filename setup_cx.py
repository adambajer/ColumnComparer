from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "tkinter",
        "openpyxl",
        "xml",     # ← DŮLEŽITÉ: přibalis xml
        "csv",
    ],
    "includes": [
        "xml.etree.ElementTree",   # ← explicitně kvůli openpyxl
    ],
    "excludes": [
        "numpy",
        "pandas",
        "unittest",
        "distutils",
        "setuptools",
        # nic víc teď neřežeme, ať je to stabilní
    ],
    "optimize": 1,
    "include_msvcr": False,
}

# zkratka: už nebudu řešit shortcuts, ať teď hlavně běží appka
executables = [
    Executable(
        "column_comparer.py",
        base="gui",
        target_name="PorovnavacSloupcu.exe",
    )
]

setup(
    name="PorovnavacSloupcu",
    version="1.0",
    description="Ultra-lehký porovnávač sloupců (openpyxl + csv, bez pandas)",
    options={
        "build_exe": build_exe_options,
    },
    executables=executables
)

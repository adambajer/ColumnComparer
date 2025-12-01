from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "tkinter",
        "openpyxl",
        "csv"
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
        "numpy",        # jistota
        "pandas",
    ],
    "optimize": 2,
    "include_msvcr": False,   # zmenší installer
}

executables = [
    Executable(
        "column_comparer.py",
        base="gui",
        target_name="PorovnavacSloupcu.exe"
    )
]

setup(
    name="PorovnavacSloupcu",
    version="1.0",
    description="Ultra-lehký porovnávač sloupců",
    options={"build_exe": build_exe_options},
    executables=executables
)

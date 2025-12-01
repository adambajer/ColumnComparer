from cx_Freeze import setup, Executable

build_options = {
    "packages": []
}

setup(
    name="ColumnComparer",
    version="1.0",
    description="Porovnání CSV sloupců",
    options={"build_exe": build_options},
    executables=[
        Executable(
            script="column_comparer.py",
            base="gui",               # ⬅️ SEM
        )
    ]
)

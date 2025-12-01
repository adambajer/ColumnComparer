Univerzální porovnávač sloupců (Excel / CSV)
===========================================

Struktura projektu
------------------
- column_comparer.py  ... hlavní GUI aplikace (Tkinter)
- setup_cx.py         ... build skript pro cx_Freeze (EXE + MSI)

Doporučená verze Pythonu: 3.10 nebo 3.11 z python.org
Nedoporučuji MS Store variantu.

Instalace závislostí a build (ve Windows)
-----------------------------------------

1) Vytvoř virtuální prostředí:

    py -3.11 -m venv .venv
    .\.venv\Scripts\activate

2) Nainstaluj balíčky:

    pip install cx-Freeze pandas openpyxl

3) Build standalone EXE:

    python setup_cx.py build

   Výsledek:
     build\exe.win-amd64-3.11\PorovnavacSloupcu.exe

4) Build MSI instalátoru:

    python setup_cx.py bdist_msi

   Výsledek:
     dist\PorovnavacSloupcu-1.0-amd64.msi

Aplikace pak běží jako normální Windows program a uživatel nepotřebuje
instalovaný Python ani knihovny.

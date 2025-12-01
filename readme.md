# ColumnComparer – README

Univerzální porovnávač sloupců (Excel / CSV)
===========================================

Tento projekt obsahuje GUI aplikaci pro Windows napsanou v Pythonu (Tkinter), která umožňuje:

- načíst dvě tabulky (Excel / CSV / TXT),
- vybrat sloupce kliknutím na hlavičku,
- porovnat hodnoty mezi sloupci,
- zobrazit odpovídající řádky,
- exportovat výsledek do CSV nebo Excelu,
- vytvořit instalátor pomocí **cx_Freeze** (EXE + MSI).

---

## 🗂 Struktura projektu

```
ColumnComparer/
│
├── column_comparer.py   # hlavní aplikace (Tkinter GUI)
├── setup_cx.py          # cx_Freeze build skript
└── README.md            # tento dokument
```

---

## 🐍 Doporučený Python

Používej **Python 3.10 nebo 3.11** z python.org  
(ne MS Store verzi → má problémy s cx_Freeze a base EXE).

---

## 📦 Instalace závislostí + build (Windows)

### 1) Vytvoř virtuální prostředí

```bat
py -3.11 -m venv .venv
.\.venv\Scriptsctivate
```

### 2) Nainstaluj balíčky

```bat
pip install cx-Freeze pandas openpyxl
```

### 3) Build samostatného EXE

```bat
python setup_cx.py build
```

Výsledek najdeš zde:

```
build\exe.win-amd64-3.11\PorovnavacSloupcu.exe
```

Tento EXE **obsahuje Python i všechny knihovny**.

---

## 📦 Build instalátoru (MSI)

cx_Freeze umí vytvořit MSI balíček:

```bat
python setup_cx.py bdist_msi
```

Výsledek:

```
dist\PorovnavacSloupcu-1.0-amd64.msi
```

---

## ⚙ Použití aplikace

1. Spusť `PorovnavacSloupcu.exe` nebo nainstalovanou aplikaci.
2. Načti tabulku 1 a 2 (Excel/CSV).
3. Klikni na hlavičku sloupce v každé tabulce → sloupec se vybere.
4. Klikni na **Porovnat vybrané sloupce**.
5. Výsledek se zobrazí dole.
6. Můžeš ho **exportovat** jako `.xlsx` nebo `.csv`.

---

## 📝 Poznámky

- Aplikace načítá všechny hodnoty jako text (`dtype=str`) → spolehlivější porovnávání.
- Podporuje autodetekci oddělovače u CSV/TXT (`sep=None`).
- Pokud Excel obsahuje „0 worksheets“, zobrazí jasnou chybu.

---

## 📄 Licence

Volně použitelné, upravitelné a distribuovatelné.


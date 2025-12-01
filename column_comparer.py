import os
import warnings

# umlčení otravného UserWarning z openpyxl
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="openpyxl"
)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from openpyxl import load_workbook


def read_table(filepath: str) -> pd.DataFrame:
    """
    Načte tabulku z Excelu nebo CSV/TXT do pandas DataFrame.
    - Excel: vezmeme první list, předtím ověříme, že nějaké listy existují.
    - CSV/TXT: automatická detekce oddělovače.
    Vše se načítá jako string (dtype=str), aby šlo dobře porovnávat.
    """
    ext = os.path.splitext(filepath)[1].lower()

    # Excel soubory
    if ext in (".xlsx", ".xlsm", ".xltx", ".xltm", ".xls"):
        try:
            wb = load_workbook(filepath, read_only=True, data_only=True)
        except Exception as e:
            raise RuntimeError(f"Soubor nevypadá jako platný Excel: {e}")

        if not wb.sheetnames:
            wb.close()
            raise RuntimeError("Soubor neobsahuje žádné listy (0 worksheets found).")

        first_sheet = wb.sheetnames[0]
        wb.close()

        try:
            df = pd.read_excel(
                filepath,
                sheet_name=first_sheet,
                dtype=str,
                engine="openpyxl"
            )
        except Exception as e:
            raise RuntimeError(f"Chyba při čtení listu '{first_sheet}': {e}")

        return df

    # CSV / TXT
    if ext in (".csv", ".txt"):
        try:
            df = pd.read_csv(
                filepath,
                sep=None,
                engine="python",
                dtype=str
            )
        except Exception as e:
            raise RuntimeError(f"Chyba při čtení CSV/TXT souboru: {e}")

        return df

    raise RuntimeError(f"Nepodporovaný typ souboru: {ext}")


class ColumnComparerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Univerzální porovnávač sloupců (Excel / CSV)")
        self.geometry("1400x800")

        self.df1 = None
        self.df2 = None

        self.selected_col1_name = None
        self.selected_col2_name = None

        self.last_result_df = None

        self.tree1 = None
        self.tree2 = None
        self.tree_result = None

        self.lbl_file1 = None
        self.lbl_file2 = None
        self.lbl_sel1 = None
        self.lbl_sel2 = None

        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 5))

        # Tabulka 1
        frame_left = ttk.Labelframe(paned, text="Tabulka 1")
        paned.add(frame_left, weight=1)

        left_top = ttk.Frame(frame_left)
        left_top.pack(side=tk.TOP, fill=tk.X, pady=(2, 2))

        btn1 = ttk.Button(
            left_top,
            text="Načíst tabulku 1 (Excel/CSV)",
            command=self.load_table1
        )
        btn1.pack(side=tk.LEFT, padx=5)

        self.lbl_file1 = ttk.Label(left_top, text="(není načteno)")
        self.lbl_file1.pack(side=tk.LEFT, padx=5)

        self.tree1 = self._create_table_widget(
            frame_left,
            on_header_click=self._on_tree1_header_click
        )

        # Tabulka 2
        frame_right = ttk.Labelframe(paned, text="Tabulka 2")
        paned.add(frame_right, weight=1)

        right_top = ttk.Frame(frame_right)
        right_top.pack(side=tk.TOP, fill=tk.X, pady=(2, 2))

        btn2 = ttk.Button(
            right_top,
            text="Načíst tabulku 2 (Excel/CSV)",
            command=self.load_table2
        )
        btn2.pack(side=tk.LEFT, padx=5)

        self.lbl_file2 = ttk.Label(right_top, text="(není načteno)")
        self.lbl_file2.pack(side=tk.LEFT, padx=5)

        self.tree2 = self._create_table_widget(
            frame_right,
            on_header_click=self._on_tree2_header_click
        )

        # Spodní panel
        bottom_controls = ttk.Frame(self, padding=5)
        bottom_controls.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(bottom_controls, text="Vybraný sloupec – Tabulka 1:").pack(
            side=tk.LEFT, padx=(0, 5)
        )
        self.lbl_sel1 = ttk.Label(bottom_controls, text="(nevybrán)")
        self.lbl_sel1.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(bottom_controls, text="Vybraný sloupec – Tabulka 2:").pack(
            side=tk.LEFT, padx=(0, 5)
        )
        self.lbl_sel2 = ttk.Label(bottom_controls, text="(nevybrán)")
        self.lbl_sel2.pack(side=tk.LEFT, padx=(0, 15))

        btn_compare = ttk.Button(
            bottom_controls,
            text="Porovnat vybrané sloupce",
            command=self.compare_columns
        )
        btn_compare.pack(side=tk.LEFT, padx=10)

        btn_export = ttk.Button(
            bottom_controls,
            text="Exportovat výsledek…",
            command=self.export_results
        )
        btn_export.pack(side=tk.LEFT, padx=5)

        # Výsledky
        result_frame = ttk.Labelframe(
            self, text="Výsledné řádky (z tabulky 1)", padding=5
        )
        result_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 5))

        self.tree_result = self._create_table_widget(result_frame, on_header_click=None)

    def _create_table_widget(self, parent, on_header_click=None):
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(container, show="headings")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        if on_header_click is not None:
            def header_handler(event, tv=tree, cb=on_header_click):
                region = tv.identify_region(event.x, event.y)
                if region == "heading":
                    col_id = tv.identify_column(event.x)  # "#1", "#2", ...
                    try:
                        idx = int(col_id.replace("#", "")) - 1
                    except ValueError:
                        return
                    cols = list(tv["columns"])
                    if 0 <= idx < len(cols):
                        cb(tv, idx, cols[idx])
            tree.bind("<Button-1>", header_handler, add="+")

        return tree

    def load_table1(self):
        filepath = filedialog.askopenfilename(
            title="Vyber soubor (tabulka 1)",
            filetypes=[
                ("Tabulky", "*.xlsx *.xlsm *.xltx *.xltm *.xls *.csv *.txt"),
                ("Všechny soubory", "*.*"),
            ],
        )
        if not filepath:
            return

        try:
            self.df1 = read_table(filepath)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst tabulku 1:\\n{e}")
            return

        self.lbl_file1.config(text=os.path.basename(filepath))
        self._fill_tree(self.tree1, self.df1)

        self.selected_col1_name = None
        self.lbl_sel1.config(text="(nevybrán)")
        self._clear_header_selection(self.tree1)

    def load_table2(self):
        filepath = filedialog.askopenfilename(
            title="Vyber soubor (tabulka 2)",
            filetypes=[
                ("Tabulky", "*.xlsx *.xlsm *.xltx *.xltm *.xls *.csv *.txt"),
                ("Všechny soubory", "*.*"),
            ],
        )
        if not filepath:
            return

        try:
            self.df2 = read_table(filepath)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst tabulku 2:\\n{e}")
            return

        self.lbl_file2.config(text=os.path.basename(filepath))
        self._fill_tree(self.tree2, self.df2)

        self.selected_col2_name = None
        self.lbl_sel2.config(text="(nevybrán)")
        self._clear_header_selection(self.tree2)

    def _fill_tree(self, tree, df: pd.DataFrame):
        tree.delete(*tree.get_children())

        cols = list(df.columns)
        tree["columns"] = cols

        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, stretch=True)

        for _, row in df.iterrows():
            values = [str(row[c]) if pd.notna(row[c]) else "" for c in cols]
            tree.insert("", tk.END, values=values)

    def _clear_header_selection(self, tree):
        cols = list(tree["columns"])
        for c in cols:
            tree.heading(c, text=c)

    def _update_header_selection(self, tree, selected_name: str):
        cols = list(tree["columns"])
        for c in cols:
            label = f"[{c}]" if c == selected_name else c
            tree.heading(c, text=label)

    def _on_tree1_header_click(self, tree, idx, col_name):
        if not col_name:
            return
        self.selected_col1_name = col_name
        self.lbl_sel1.config(text=self.selected_col1_name)
        self._update_header_selection(tree, self.selected_col1_name)

    def _on_tree2_header_click(self, tree, idx, col_name):
        if not col_name:
            return
        self.selected_col2_name = col_name
        self.lbl_sel2.config(text=self.selected_col2_name)
        self._update_header_selection(tree, self.selected_col2_name)

    def compare_columns(self):
        if self.df1 is None or self.df2 is None:
            messagebox.showwarning("Pozor", "Nejdřív načti obě tabulky.")
            return

        if not self.selected_col1_name or not self.selected_col2_name:
            messagebox.showwarning(
                "Pozor",
                "Vyber sloupec v Tabulce 1 a Tabulce 2 kliknutím na jejich hlavičky."
            )
            return

        col1 = self.selected_col1_name
        col2 = self.selected_col2_name

        if col1 not in self.df1.columns:
            messagebox.showerror("Chyba", f"Sloupec '{col1}' není v tabulce 1.")
            return
        if col2 not in self.df2.columns:
            messagebox.showerror("Chyba", f"Sloupec '{col2}' není v tabulce 2.")
            return

        values2 = set(self.df2[col2].dropna().astype(str))

        mask = self.df1[col1].astype(str).isin(values2)
        result_df = self.df1[mask].copy()

        self.last_result_df = result_df

        if result_df.empty:
            messagebox.showinfo(
                "Výsledek",
                "Nebyly nalezeny žádné shodné hodnoty ve vybraných sloupcích."
            )
        else:
            messagebox.showinfo(
                "Výsledek",
                f"Nalezeno {len(result_df)} řádků v tabulce 1, které mají hodnotu "
                f"ze sloupce '{col2}' tabulky 2."
            )

        self._fill_tree(self.tree_result, result_df)

    def export_results(self):
        if self.last_result_df is None or self.last_result_df.empty:
            messagebox.showwarning(
                "Nic k exportu",
                "Nejdřív proveď porovnání, aby vznikly nějaké výsledky."
            )
            return

        filepath = filedialog.asksaveasfilename(
            title="Uložit výsledky",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel sešit", "*.xlsx"),
                ("CSV soubor", "*.csv"),
                ("Všechny soubory", "*.*"),
            ],
        )
        if not filepath:
            return

        ext = os.path.splitext(filepath)[1].lower()
        try:
            if ext == ".csv":
                self.last_result_df.to_csv(
                    filepath, index=False, encoding="utf-8-sig"
                )
            else:
                self.last_result_df.to_excel(
                    filepath, index=False, engine="openpyxl"
                )
            messagebox.showinfo("Export hotov", f"Výsledky byly uloženy do:\\n{filepath}")
        except Exception as e:
            messagebox.showerror("Chyba při exportu", f"{e}")


if __name__ == "__main__":
    app = ColumnComparerApp()
    app.mainloop()

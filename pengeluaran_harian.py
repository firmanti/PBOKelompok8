import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

class DailyExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catatan Pengeluaran Harian")
        self.root.geometry("900x600")
        self.root.configure(bg="#1a237e")

        # Judul Aplikasi
        title_label = tk.Label(
            self.root,
            text="Catatan Pengeluaran Harian",
            font=("Georgia", 24, "bold"),
            fg="#ffc107",
            bg="#1a237e",
        )
        title_label.pack(pady=10)

        # Frame Utamaw
        main_frame = tk.Frame(self.root, bg="#1a237e")
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Frame Input
        input_frame = tk.LabelFrame(main_frame, text="Input Pengeluaran", bg="#3949ab", fg="white", font=("Arial", 12, "bold"))
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.name_entry = self.create_entry(input_frame, "Nama Pengeluaran:", 0)
        self.category_combobox = self.create_combobox(input_frame, "Kategori:", 1)
        self.amount_entry = self.create_entry(input_frame, "Jumlah (Rp):", 2)
        self.date_entry = self.create_entry(input_frame, "Tanggal (YYYY-MM-DD):", 3, datetime.now().strftime("%Y-%m-%d"))
        self.note_entry = self.create_entry(input_frame, "Keterangan:", 4)

        add_button = tk.Button(
            input_frame, text="Tambah", font=("Arial", 12, "bold"), bg="#4caf50", fg="white",
            command=self.add_expense
        )
        add_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

        # Frame Tabel
        table_frame = tk.LabelFrame(main_frame, text="Data Pengeluaran", bg="#3949ab", fg="white", font=("Arial", 12, "bold"))
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.expense_table = self.create_table(table_frame)

        # Total Pengeluaran
        self.total_label = tk.Label(
            main_frame,
            text="Total Pengeluaran: Rp 0",
            font=("Georgia", 14, "bold"),
            fg="#ff5722",
            bg="#1a237e",
        )
        self.total_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Frame Tombol
        button_frame = tk.Frame(main_frame, bg="#1a237e")
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.create_action_buttons(button_frame)

        # Memberikan weight untuk tata letak grid
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)

        # Contoh pengeluaran awal
        self.expenses = [
            {"name": "Makan Siang", "category": "Makanan", "amount": 50000, "date": "2024-11-28", "note": "Di restoran"},
            {"name": "Transportasi Pulang", "category": "Transportasi", "amount": 20000, "date": "2024-11-28", "note": "Ojek online"},
            {"name": "Nonton Film", "category": "Hiburan", "amount": 75000, "date": "2024-11-27", "note": "Bioskop"},
            {"name": "Beli Buku", "category": "Lainnya", "amount": 120000, "date": "2024-11-26", "note": "Di toko buku"},
            {"name": "Makan Malam", "category": "Makanan", "amount": 80000, "date": "2024-11-25", "note": "Restoran cepat saji"},
            {"name": "Parkir Motor", "category": "Transportasi", "amount": 15000, "date": "2024-11-25", "note": "Di pusat perbelanjaan"},
            {"name": "Pajak Motor", "category": "Lainnya", "amount": 300000, "date": "2024-11-24", "note": "Pembayaran tahunan"},
        ]

        self.update_table()

    def create_entry(self, parent, label_text, row, default_value=""):
        tk.Label(parent, text=label_text, font=("Arial", 12), bg="#3949ab", fg="white").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(parent, font=("Arial", 12), width=25)
        entry.grid(row=row, column=1, padx=10, pady=5)
        entry.insert(0, default_value)
        return entry

    def create_combobox(self, parent, label_text, row):
        tk.Label(parent, text=label_text, font=("Arial", 12), bg="#3949ab", fg="white").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        combobox = ttk.Combobox(
            parent,
            values=["Makanan", "Transportasi", "Hiburan", "Lainnya"],
            font=("Arial", 12),
            state="readonly",
        )
        combobox.grid(row=row, column=1, padx=10, pady=5)
        combobox.set("Pilih Kategori")
        return combobox

    def create_table(self, parent):
        treeview = ttk.Treeview(
            parent,
            columns=("Nama", "Kategori", "Jumlah", "Tanggal", "Keterangan"),
            show="headings",
            height=12,
        )
        treeview.heading("Nama", text="Nama Pengeluaran")
        treeview.heading("Kategori", text="Kategori")
        treeview.heading("Jumlah", text="Jumlah (Rp)")
        treeview.heading("Tanggal", text="Tanggal")
        treeview.heading("Keterangan", text="Keterangan")
        treeview.column("Nama", width=150)
        treeview.column("Kategori", width=100)
        treeview.column("Jumlah", width=100)
        treeview.column("Tanggal", width=100)
        treeview.column("Keterangan", width=150)
        treeview.pack(fill="both", expand=True, padx=10, pady=10)
        return treeview

    def create_action_buttons(self, parent):
        tk.Button(parent, text="Filter", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=self.filter_data).pack(side="left", padx=10, pady=5)
        tk.Button(parent, text="Hapus", font=("Arial", 12, "bold"), bg="#e53935", fg="white", command=self.delete_expense).pack(side="left", padx=10, pady=5)
        tk.Button(parent, text="Hapus Semua", font=("Arial", 12, "bold"), bg="#d32f2f", fg="white", command=self.clear_all_data).pack(side="left", padx=10, pady=5)
        tk.Button(parent, text="Simpan", font=("Arial", 12, "bold"), bg="#1976d2", fg="white", command=self.save_expenses).pack(side="left", padx=10, pady=5)
        tk.Button(parent, text="Grafik", font=("Arial", 12, "bold"), bg="#ff8f00", fg="white", command=self.show_graph).pack(side="left", padx=10, pady=5)

    def add_expense(self):
        name = self.name_entry.get()
        category = self.category_combobox.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        note = self.note_entry.get()

        if not name or category == "Pilih Kategori" or not amount or not date:
            messagebox.showerror("Error", "Semua kolom wajib diisi!")
            return

        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Tanggal harus dalam format YYYY-MM-DD!")
            return

        self.expenses.append({"name": name, "category": category, "amount": amount, "date": date, "note": note})
        self.update_table()
        self.clear_entries()

    def update_table(self):
        for row in self.expense_table.get_children():
            self.expense_table.delete(row)

        for expense in self.expenses:
            self.expense_table.insert(
                "", "end",
                values=(
                    expense["name"],
                    expense["category"],
                    f"Rp {expense['amount']:,}",
                    expense["date"],
                    expense["note"],
                ),
            )

        total = sum(expense["amount"] for expense in self.expenses)
        self.total_label.config(text=f"Total Pengeluaran: Rp {total:,}")
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.category_combobox.set("Pilih Kategori")
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)

    def delete_expense(self):
        selected_item = self.expense_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih data yang ingin dihapus!")
            return

        for item in selected_item:
            values = self.expense_table.item(item, "values")
            self.expenses = [expense for expense in self.expenses if not (
                expense["name"] == values[0] and
                expense["category"] == values[1] and
                expense["amount"] == int(values[2]) and
                expense["date"] == values[3] and
                expense["note"] == values[4]
            )]
            self.expense_table.delete(item)

        self.update_table()

    def clear_all_data(self):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua data?"):
            self.expenses.clear()
            self.update_table()

    def save_expenses(self):
        file_name = askstring("Simpan Data", "Masukkan nama file (tanpa ekstensi):")
        if not file_name:
            return

        file_name += ".csv"
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Nama Pengeluaran", "Kategori", "Jumlah (Rp)", "Tanggal", "Keterangan"])
            for expense in self.expenses:
                writer.writerow([expense["name"], expense["category"], expense["amount"], expense["date"], expense["note"]])

        messagebox.showinfo("Berhasil", f"Data berhasil disimpan ke {file_name}!")

    def show_graph(self):
        if not self.expenses:
            messagebox.showerror("Error", "Tidak ada data untuk ditampilkan dalam grafik!")
            return

        df = pd.DataFrame(self.expenses)
        summary = df.groupby("category")["amount"].sum()

        # Diagram Batang
        plt.figure(figsize=(10, 6))
        summary.plot(kind="bar", color=["#4caf50", "#2196f3", "#ff5722", "#ff9800"])
        plt.title("Pengeluaran Berdasarkan Kategori")
        plt.xlabel("Kategori")
        plt.ylabel("Total Pengeluaran (Rp)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Diagram Lingkaran
        plt.figure(figsize=(8, 8))
        summary.plot(kind="pie", autopct='%1.1f%%', colors=["#4caf50", "#2196f3", "#ff5722", "#ff9800"])
        plt.title("Proporsi Pengeluaran Berdasarkan Kategori")
        plt.ylabel("")
        plt.tight_layout()

        plt.show()


    def filter_data(self):
        category = askstring("Filter Data", "Masukkan kategori yang ingin difilter:")
        if not category:
            return

        filtered_expenses = [expense for expense in self.expenses if expense["category"].lower() == category.lower()]
        if not filtered_expenses:
            messagebox.showinfo("Hasil Filter", f"Tidak ada data dengan kategori '{category}'.")
            return

        total = sum(expense["amount"] for expense in filtered_expenses)
        messagebox.showinfo("Hasil Filter", f"Total Pengeluaran untuk kategori '{category}': Rp {total:,}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DailyExpenseApp(root)
    root.mainloop()

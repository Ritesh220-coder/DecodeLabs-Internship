import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report


class DashboardAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Classification Dashboard")
        self.root.geometry("1180x720")
        self.root.configure(bg="#0b1020")

        self.df = None
        self.target_var = tk.StringVar()
        self.file_var = tk.StringVar(value="No file loaded")
        self.shape_var = tk.StringVar(value="Rows: 0 | Columns: 0")
        self.acc_var = tk.StringVar(value="Accuracy: --")
        self.status_var = tk.StringVar(value="Status: Waiting for dataset")

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground="#e5e7eb",
            background="#e5e7eb",
            foreground="#111827",
            padding=8
        )

    def build_ui(self):
        header = tk.Frame(self.root, bg="#111827", height=80)
        header.pack(fill="x")

        tk.Label(
            header,
            text="AI Classification Dashboard",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#111827"
        ).pack(side="left", padx=24, pady=18)

        tk.Label(
            header,
            text="Project 2 - Data Classification Using AI",
            font=("Segoe UI", 11),
            fg="#cbd5e1",
            bg="#111827"
        ).pack(side="left", pady=26)

        main = tk.Frame(self.root, bg="#0b1020")
        main.pack(fill="both", expand=True, padx=18, pady=18)

        left = tk.Frame(main, bg="#172033", width=290)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)

        right = tk.Frame(main, bg="#0b1020")
        right.pack(side="right", fill="both", expand=True)

        tk.Label(
            left,
            text="Control Panel",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#172033"
        ).pack(anchor="w", padx=18, pady=(20, 12))

        self.make_button(left, "Load CSV", self.load_csv, "#2563eb")
        self.make_button(left, "Show Data Info", self.show_info, "#7c3aed")
        self.make_button(left, "Train Model", self.train_model, "#16a34a")

        tk.Label(
            left,
            text="Select Target Column",
            font=("Segoe UI", 11, "bold"),
            fg="#dbeafe",
            bg="#172033"
        ).pack(anchor="w", padx=18, pady=(22, 8))

        self.target_combo = ttk.Combobox(
            left,
            textvariable=self.target_var,
            state="readonly",
            width=24
        )
        self.target_combo.pack(padx=18, pady=(0, 14))

        info_card = tk.Frame(left, bg="#1e293b", bd=0)
        info_card.pack(fill="x", padx=18, pady=8)

        tk.Label(info_card, text="Current File", font=("Segoe UI", 10, "bold"), fg="#93c5fd", bg="#1e293b").pack(anchor="w", padx=12, pady=(12, 4))
        tk.Label(info_card, textvariable=self.file_var, font=("Segoe UI", 10), fg="white", bg="#1e293b", wraplength=230, justify="left").pack(anchor="w", padx=12)

        tk.Label(info_card, textvariable=self.shape_var, font=("Segoe UI", 10), fg="#cbd5e1", bg="#1e293b").pack(anchor="w", padx=12, pady=(8, 12))

        cards = tk.Frame(right, bg="#0b1020")
        cards.pack(fill="x", pady=(0, 16))

        self.metric_card(cards, "Model Accuracy", self.acc_var, "#0f766e").pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.metric_card(cards, "App Status", self.status_var, "#7c2d12").pack(side="left", fill="x", expand=True, padx=(8, 0))

        output_card = tk.Frame(right, bg="#111827")
        output_card.pack(fill="both", expand=True)

        tk.Label(
            output_card,
            text="Analysis Output",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#111827"
        ).pack(anchor="w", padx=20, pady=(18, 10))

        self.text = tk.Text(
            output_card,
            wrap="word",
            font=("Consolas", 11),
            bg="#f8fafc",
            fg="#0f172a",
            insertbackground="#0f172a",
            relief="flat",
            padx=16,
            pady=16
        )
        self.text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def metric_card(self, parent, title, variable, color):
        frame = tk.Frame(parent, bg=color, height=90)
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg=color
        ).pack(anchor="w", padx=16, pady=(14, 6))

        tk.Label(
            frame,
            textvariable=variable,
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=color
        ).pack(anchor="w", padx=16)

        return frame

    def make_button(self, parent, text, command, color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            bd=0,
            width=24,
            pady=10,
            cursor="hand2"
        )
        btn.pack(padx=18, pady=8)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return

        try:
            self.df = pd.read_csv(path)
            self.target_combo["values"] = list(self.df.columns)

            if "OrderStatus" in self.df.columns:
                self.target_var.set("OrderStatus")
            else:
                self.target_var.set(self.df.columns[-1])

            self.file_var.set(path.split("/")[-1] if "/" in path else path.split("\\")[-1])
            self.shape_var.set(f"Rows: {self.df.shape[0]} | Columns: {self.df.shape[1]}")
            self.status_var.set("Status: Dataset loaded successfully")

            self.text.delete("1.0", tk.END)
            self.text.insert(
                tk.END,
                "Dataset loaded successfully.\n\n"
                f"File: {self.file_var.get()}\n"
                f"Rows: {self.df.shape[0]}\n"
                f"Columns: {self.df.shape[1]}\n"
                f"Default target column: {self.target_var.get()}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_info(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a dataset first")
            return

        info = ""
        info += "DATASET OVERVIEW\n"
        info += "=" * 70 + "\n\n"
        info += f"Shape: {self.df.shape}\n\n"
        info += f"Columns:\n{list(self.df.columns)}\n\n"
        info += f"First 5 Rows:\n{self.df.head()}\n\n"
        info += f"Missing Values:\n{self.df.isna().sum()}\n"

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, info)
        self.status_var.set("Status: Showing dataset information")

    def train_model(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a dataset first")
            return

        target = self.target_var.get()
        if not target:
            messagebox.showwarning("Warning", "Select a target column")
            return

        try:
            data = self.df.copy()
            data = data.fillna("Missing")

            X = data.drop(columns=[target])
            y = data[target]

            for col in X.columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))

            y_encoder = LabelEncoder()
            y = y_encoder.fit_transform(y.astype(str))

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            model = DecisionTreeClassifier()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)

            self.acc_var.set(f"Accuracy: {acc:.4f}")
            self.status_var.set("Status: Model trained successfully")

            result = ""
            result += "MODEL TRAINING RESULTS\n"
            result += "=" * 70 + "\n\n"
            result += f"Target Column: {target}\n"
            result += f"Accuracy Score: {acc:.4f}\n\n"
            result += "Classification Report:\n"
            result += report

            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardAIApp(root)
    root.mainloop()
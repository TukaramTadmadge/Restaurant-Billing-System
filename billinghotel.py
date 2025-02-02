from tkinter import *
import random
from tkinter import messagebox

class BillApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Restaurant Billing System")

        # Colors and data
        self.colors = {"title": "red", "frame_bg": "lightblue", "bill_bg": "lightyellow", "summary_bg": "lightpink"}
        self.items = {
            "Snacks": [("Samosa", 15), ("Paneer Tikka", 120), ("Chicken Tikka", 150), ("Spring Roll", 100), ("French Fries", 80)],
            "Main Course": [("Butter Chicken", 200), ("Pasta", 150), ("Rice", 100), ("Naan", 20), ("Paneer Butter Masala", 180)],
            "Drinks": [("Coke", 50), ("Pepsi", 50), ("Lassi", 60), ("Juice", 70), ("Water", 20)],
        }
        self.customer = {k: StringVar() for k in ["Name", "Phone"]}
        self.customer["Bill No"] = StringVar(value=str(random.randint(1000, 9999)))
        self.item_vars = {cat: [IntVar() for _ in items] for cat, items in self.items.items()}
        self.total_vars, self.tax_vars, self.grand_total = {cat: StringVar() for cat in self.items}, {cat: StringVar() for cat in self.items}, StringVar()

        self.create_title()
        self.create_frame("Customer Details", self.customer_frame, 0, 80, 1)
        self.create_product_frames()
        self.create_bill_area()
        self.create_frame("Summary", self.summary_buttons, 0, 560, 1)

    def create_title(self):
        Label(self.root, text="Restaurant Billing System", font=("Arial Black", 20), bg=self.colors["title"], fg="white").pack(fill=X)

    def create_frame(self, title, content_fn, x, y, relwidth=0, width=325, height=380):
        frame = LabelFrame(self.root, text=title, font=("Arial Black", 12), bg=self.colors["frame_bg"], relief=GROOVE, bd=10)
        frame.place(x=x, y=y, relwidth=relwidth, width=width, height=height)
        content_fn(frame)

    def customer_frame(self, frame):
        for i, (label, var) in enumerate(self.customer.items()):
            Label(frame, text=label, font=("Arial Black", 14), bg=self.colors["frame_bg"]).grid(row=0, column=2 * i, padx=15)
            entry = Entry(frame, textvariable=var, width=20)
            entry.grid(row=0, column=2 * i + 1)
            if label == "Phone":
                entry.bind("<FocusOut>", self.validate_phone)

    def validate_phone(self, event):
        phone = self.customer["Phone"].get()
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Error", "Phone number must be a 10-digit number!")
            self.customer["Phone"].set("")

    def create_product_frames(self):
        x = 5
        for category, items in self.items.items():
            self.create_frame(category, lambda f: self.product_frame(f, category, items), x, 180)
            x += 335

    def product_frame(self, frame, category, items):
        for i, (item, price) in enumerate(items):
            Label(frame, text=f"{item} ({price} Rs)", font=("Arial Black", 10), bg=self.colors["frame_bg"]).grid(row=i, column=0, pady=5, sticky="w")
            Entry(frame, textvariable=self.item_vars[category][i], width=10).grid(row=i, column=1, padx=10)

    def create_bill_area(self):
        frame = Frame(self.root, bd=10, relief=GROOVE, bg=self.colors["bill_bg"])
        frame.place(x=1010, y=180, width=330, height=380)
        Label(frame, text="Bill Area", font=("Arial Black", 16), bg=self.colors["bill_bg"]).pack(fill=X)
        scrol_y = Scrollbar(frame, orient=VERTICAL)
        self.txtarea = Text(frame, yscrollcommand=scrol_y.set)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)

    def summary_buttons(self, frame):
        for i, category in enumerate(self.items):
            Label(frame, text=f"Total {category} Price", font=("Arial Black", 10), bg=self.colors["summary_bg"]).grid(row=i, column=0, pady=5)
            Entry(frame, textvariable=self.total_vars[category], width=20).grid(row=i, column=1)
            Label(frame, text=f"{category} Tax", font=("Arial Black", 10), bg=self.colors["summary_bg"]).grid(row=i, column=2)
            Entry(frame, textvariable=self.tax_vars[category], width=20).grid(row=i, column=3)

        Label(frame, text="Grand Total", font=("Arial Black", 10), bg=self.colors["summary_bg"]).grid(row=len(self.items), column=0)
        Entry(frame, textvariable=self.grand_total, width=20).grid(row=len(self.items), column=1)

        btn_frame = Frame(self.root, bd=7, bg="orange")
        btn_frame.place(x=830, y=560, width=500, height=140)
        Button(btn_frame, text="Total", font=("Arial Black", 12), bg="orange", command=self.calculate_total).grid(row=0, column=0, padx=20)
        Button(btn_frame, text="Clear", font=("Arial Black", 12), bg="orange", command=self.clear).grid(row=0, column=1, padx=20)
        Button(btn_frame, text="Exit", font=("Arial Black", 12), bg="orange", command=self.root.quit).grid(row=0, column=2, padx=20)

    def calculate_total(self):
        if all(var.get() == 0 for vars in self.item_vars.values() for var in vars):
            messagebox.showerror("Error", "No items added!")
            return

        grand_total = 0
        self.txtarea.delete(1.0, END)
        self.txtarea.insert(END, f"{'Restaurant Billing System':^40}\n")
        self.txtarea.insert(END, f"Customer Name: {self.customer['Name'].get()}\nPhone: {self.customer['Phone'].get()}\n")
        self.txtarea.insert(END, "-" * 40 + "\nItem\tQty\tPrice\n" + "-" * 40 + "\n")

        for category, vars in self.item_vars.items():
            total = sum(var.get() * price for var, (_, price) in zip(vars, self.items[category]))
            tax = round(total * 0.05, 2)
            self.total_vars[category].set(f"{total} Rs")
            self.tax_vars[category].set(f"{tax} Rs")
            grand_total += total + tax

            for var, (item, price) in zip(vars, self.items[category]):
                if var.get() > 0:
                    self.txtarea.insert(END, f"{item}\t{var.get()}\t{var.get() * price}\n")

        self.grand_total.set(f"{grand_total} Rs")
        self.txtarea.insert(END, "-" * 40 + f"\nGrand Total: {self.grand_total.get()}\n")

    def clear(self):
        for var in {**self.customer, **self.total_vars, **self.tax_vars}.values():
            var.set("")
        for vars in self.item_vars.values():
            for var in vars:
                var.set(0)
        self.grand_total.set("")
        self.txtarea.delete(1.0, END)

# Run the application
root = Tk()
app = BillApp(root)
root.mainloop()

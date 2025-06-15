import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from translations import tr, set_language_global
from intersection import check_intersection
from convex_hull import compute_convex_hull
from datetime import datetime
import csv
import os

class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(tr("title"))
        self.theme_mode = "dark"
        ttk.Style().theme_use("clam")
        self.center_window(1200, 800)
        self.content_frame = ttk.Frame(self.root, padding=20)
        self.content_frame.pack(fill="both", expand=True)
        self.apply_theme()
        self.render_main_menu()

    def center_window(self, width, height):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def apply_theme(self):
        style = ttk.Style()
        if self.theme_mode == "dark":
            self.bg_color = "#2e2e2e"
            fg = "#ffffff"
            btn_bg = "#444444"
            btn_fg = fg
            btn_active = "#3c3c3c"
        else:
            self.bg_color = "#f0f0f0"
            fg = "#000000"
            btn_bg = "#cccccc"
            btn_fg = fg
            btn_active = "#bbbbbb"

        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=fg)
        style.configure("TButton", background=btn_bg, foreground=btn_fg, font=("Segoe UI", 11, "bold"))
        style.map("TButton",
                  background=[("active", btn_active)],
                  relief=[("pressed", "sunken")])
        self.root.configure(bg=self.bg_color)
        style.configure("TRadiobutton",
            background=self.bg_color,
            foreground=fg,
            font=("Segoe UI", 10, "bold")
        )

        style.map("TRadiobutton",
            background=[
                ("active", "#3a3a3a") if self.theme_mode == "dark" else ("active", "#e0e0e0")
            ],
            foreground=[
                ("active", "#ffffff") if self.theme_mode == "dark" else ("active", "#000000")
            ]
        )

    def render_main_menu(self):
        self.clear_frame()
        wrapper = ttk.Frame(self.content_frame)
        wrapper.pack(fill="both", expand=False, anchor="n", pady=70)
        ttk.Label(wrapper, text=tr("main_title"), font=("Segoe UI", 28, "bold")).pack(pady=(20, 30))

        for text, cmd in [
            (tr("new"), lambda: self.render_project_menu("new")),
            (tr("load"), lambda: self.render_project_menu("load")),
            (tr("options"), self.render_options_menu),
            (tr("info"), self.show_info),
            (tr("exit"), self.root.destroy)
        ]: ttk.Button(wrapper, text=text, command=cmd, width=30).pack(pady=8, ipady=6)

    def render_project_menu(self, mode=0):
        self.clear_frame()
        wrapper = ttk.Frame(self.content_frame)
        wrapper.pack(fill="both", expand=False, anchor="n", pady=70)

        if mode == "new":
            ttk.Label(wrapper, text=tr("new"), font=("Segoe UI", 22, "bold")).pack(pady=(30, 30))
            ttk.Button(wrapper, text=tr("intersection"), command=self.open_intersection_window, width=30).pack(pady=8, ipady=6)
            ttk.Button(wrapper, text=tr("convex"), command=self.open_convex_hull_window, width=30).pack(pady=8, ipady=6)
        else:
            ttk.Label(wrapper, text=tr("load"), font=("Segoe UI", 22, "bold")).pack(pady=(30, 30))
            ttk.Button(wrapper, text=tr("intersection"), command=lambda: self.load_data("intersection"), width=30).pack(pady=8, ipady=6)
            ttk.Button(wrapper, text=tr("convex"), command=lambda: self.load_data("convex_hull"), width=30).pack(pady=8, ipady=6)
        ttk.Button(wrapper, text=tr("back"), command=self.render_main_menu, width=30).pack(pady=30)

    def render_options_menu(self):
        self.clear_frame()
        wrapper = ttk.Frame(self.content_frame)
        wrapper.pack(fill="both", expand=False, anchor="n", pady=30)
        ttk.Label(wrapper, text=tr("options"), font=("Segoe UI", 22, "bold")).pack(pady=(30, 10))

        def section(title, options):
            frame = tk.LabelFrame(
                wrapper,
                text=title,
                font=("Segoe UI", 12, "bold"),
                labelanchor="n",
                padx=15,
                pady=15,
                bd=2,
                relief="groove",
                width=600,
                bg=self.bg_color
            )
            frame.pack(pady=15, anchor="center")
            btn_row = ttk.Frame(frame)
            btn_row.pack(anchor="center")

            for label, func in options:
                ttk.Button(btn_row, text=label, command=func, width=15).pack(side="left", padx=8, pady=4)

        section(tr("language"), [
            ("Polski", lambda: self.set_language("PL")),
            ("English", lambda: self.set_language("EN"))
        ])
        section(tr("theme"), [
            ("Dark", lambda: self.set_theme("dark")),
            ("Light", lambda: self.set_theme("light"))
        ])
        section(tr("size"), [
            ("1200x900", lambda: self.center_window(1200, 800)),
            ("1400x1000", lambda: self.center_window(1400, 900))
        ])

        ttk.Button(wrapper, text=tr("back"), command=self.render_main_menu, width=30).pack(pady=30)

    def set_language(self, lang):
        set_language_global(lang)
        self.render_options_menu()

    def set_theme(self, mode):
        self.theme_mode = mode
        self.apply_theme()
        self.render_options_menu()

    def show_info(self):
        self.clear_frame()
        wrapper = ttk.Frame(self.content_frame)
        wrapper.pack(fill="both", expand=False, anchor="n", pady=60)
        ttk.Label(wrapper, text=tr("info_title"), font=("Segoe UI", 22, "bold")).pack(pady=(30, 10), anchor="n")

        box_container = tk.Frame(
            wrapper,
            bd=1,
            relief="solid",
            bg=self.bg_color
        )
        box_container.pack(pady=10, ipadx=20, ipady=20, anchor="center")

        text_label = ttk.Label(
            box_container,
            text=tr("info_text"),
            wraplength=600,
            justify="left",
            font=("Segoe UI", 12)
        )
        text_label.pack(padx=10, pady=(50, 0))
        ttk.Button(wrapper, text=tr("back"), command=self.render_main_menu, width=30).pack(pady=20)

    def load_data(self, mode):
        self.clear_frame()
        wrapper = ttk.Frame(self.content_frame)
        wrapper.pack(expand=True, anchor="center", padx=20, pady=20)
        ttk.Label(wrapper, text=tr("prompt"), font=("Segoe UI", 22, "bold")).pack(pady=(0, 10))

        list_frame = ttk.Frame(wrapper)
        list_frame.pack(anchor="center", pady=20)
        canvas_container = tk.Frame(list_frame, background=self.bg_color, borderwidth=2, relief="groove")
        canvas_container.pack(pady=10, padx=10)

        canvas = tk.Canvas(
            canvas_container,
            width=450,
            height=500,
            background=self.bg_color,
            highlightthickness=0,
            borderwidth=0
        )
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=(10, 0, 0, 0))

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        folder = f"saves/{mode}"
        os.makedirs(folder, exist_ok=True)
        files = sorted(os.listdir(folder), reverse=True)
        files = [f for f in files if f.endswith(".csv")]

        if not files:
            ttk.Label(scrollable_frame, text=tr("no_data_saved"), font=("Segoe UI", 12)).pack(pady=20)
        else:
            for fname in files:
                full_path = os.path.join(folder, fname)

                card = ttk.Frame(scrollable_frame, width=660, padding=12, relief="ridge", borderwidth=2)
                card.pack(pady=8, anchor="center")

                content = ttk.Frame(card)
                content.pack(fill="x")

                ttk.Label(content, text=fname, font=("Segoe UI", 11, "bold")).pack(side="left", padx=10)

                btn_frame = ttk.Frame(content)
                btn_frame.pack(side="right")

                load_btn = ttk.Button(btn_frame, text=tr("load"), width=7,
                    command=lambda path=full_path, m=mode: self.load_points_from_file(path, m))
                load_btn.pack(side="left", padx=(0, 6))

                delete_btn = ttk.Button(btn_frame, text=tr("delete"), width=7,
                    command=lambda path=full_path, row=card: self.delete_saved_file(path, row))
                delete_btn.pack(side="left")

        ttk.Button(wrapper, text=tr("back"), command=self.render_main_menu, width=30).pack(pady=10)

    def load_points_from_file(self, path, mode):
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                points = [(float(row["X"]), float(row["Y"])) for row in reader]

            if len(points) != 4:
                messagebox.showerror(tr("error"), tr("error_info"))
                return

            self.clear_frame()
            wrapper = ttk.Frame(self.content_frame)
            wrapper.pack(fill="both", expand=True, anchor="n")

            label_key = "coords_prompt_2" if mode == "intersection" else "coords_prompt_4"
            ttk.Label(wrapper, text=tr(label_key), font=("Segoe UI", 16)).pack(pady=10)

            flat_coords = [coord for pt in points for coord in pt]

            if mode == "intersection":
                callback = lambda _: check_intersection(*flat_coords)
            else:
                callback = lambda _: compute_convex_hull(flat_coords)

            self.render_coord_input(wrapper, callback)
            self.root.after(100, lambda: self.fill_loaded_points(points))
            self.root.after(150, self.redraw_all_points)

        except Exception as e:
            messagebox.showerror(tr("error"), f"{tr('save_error')}\n{str(e)}")

    def fill_loaded_points(self, points):
        try:
            for i, (x, y) in enumerate(points):
                self.entries[i * 2].delete(0, tk.END)
                self.entries[i * 2].insert(0, str(x))
                self.entries[i * 2 + 1].delete(0, tk.END)
                self.entries[i * 2 + 1].insert(0, str(y))
        except Exception as e:
            print(tr("error"), e)

    def delete_saved_file(self, path, row):
        confirm = messagebox.askyesno(tr("delete"), tr("delete_confirm").format(filename=os.path.basename(path)))
        if confirm:
            try:
                os.remove(path)
                row.destroy()
            except Exception as e:
                messagebox.showerror(tr("error"), str(e))

    def open_intersection_window(self):
        self.clear_frame()
        wrapper = ttk.Frame(self.content_frame)
        wrapper.pack(fill="both", expand=True, anchor="n")
        ttk.Label(wrapper, text=tr("coords_prompt_2"), font=("Segoe UI", 16)).pack(pady=10)

        self.render_coord_input(wrapper, self.compute_intersection)

    def open_convex_hull_window(self):
        self.clear_frame()
        wrapper = ttk.Frame(self.content_frame)
        wrapper.pack(fill="both", expand=False, anchor="n", pady=70)

        ttk.Label(wrapper, text=tr("coords_prompt_4"), font=("Segoe UI", 16)).pack(pady=10)
        self.render_coord_input(wrapper, self.compute_convex_hull)

    def render_coord_input(self, parent, callback):
        self.entries = []
        selected_point_index = tk.IntVar(value=0)
        input_frame = ttk.Frame(parent)
        input_frame.pack(pady=10)

        for i in range(8):
            input_frame.columnconfigure(i, minsize=45)

        for i in range(4):
            rb = ttk.Radiobutton(
                input_frame,
                text=f"P{i+1}",
                variable=selected_point_index,
                value=i
            )
            rb.grid(row=0, column=i * 2, columnspan=2, pady=(0, 4))

        ttk.Label(input_frame, text="────────").grid(row=1, column=1, columnspan=2)
        ttk.Label(input_frame, text="────────").grid(row=1, column=5, columnspan=2)

        for i in range(4):
            ttk.Label(input_frame, text="x").grid(row=2, column=i * 2, padx=(0, 0))
            ttk.Label(input_frame, text="y").grid(row=2, column=i * 2 + 1, padx=(0, 0))

        point_dots = [None] * 4
        point_labels = [None] * 4
        colors = ['red', 'blue', 'green', 'orange']
        segment_lines = [None, None]

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.grid(True)
        ax.set_title(tr("plot_title"))

        if self.theme_mode == "dark":
            fig.patch.set_facecolor('#2e2e2e')
            ax.set_facecolor('#1e1e1e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=(10, 0))

        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(pady=0)

        class CustomToolbar(NavigationToolbar2Tk):
            toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] == 'Pan']

        toolbar = CustomToolbar(canvas, toolbar_frame)
        toolbar.update()

        if self.theme_mode == "dark":
            toolbar.config(background="#2e2e2e", borderwidth=0)
            for child in toolbar.winfo_children():
                child.configure(background="#2e2e2e", foreground="white", activebackground="#3a3a3a")

        def update_plot_from_entry(index):
            x_str = self.entries[index * 2].get().strip()
            y_str = self.entries[index * 2 + 1].get().strip()

            if not x_str or not y_str:
                if point_dots[index]:
                    point_dots[index].remove()
                    point_dots[index] = None
                if point_labels[index]:
                    point_labels[index].remove()
                    point_labels[index] = None
                update_lines()
                canvas.draw()
                return

            try:
                x_val = float(x_str)
                y_val = float(y_str)

                if point_dots[index]:
                    point_dots[index].remove()
                if point_labels[index]:
                    point_labels[index].remove()

                point_dots[index] = ax.plot(x_val, y_val, 'o', color=colors[index])[0]
                point_labels[index] = ax.text(x_val + 0.1, y_val + 0.1, f"P{index+1}", color=colors[index])
                update_lines()
                canvas.draw()
            except ValueError:
                pass

        for i in range(4):
            x_entry = ttk.Entry(input_frame, width=8)
            x_entry.grid(row=3, column=i * 2, padx=(0, 2))
            self.entries.append(x_entry)

            y_entry = ttk.Entry(input_frame, width=8)
            y_entry.grid(row=3, column=i * 2 + 1, padx=(2, 10 if i < 3 else 0))
            self.entries.append(y_entry)

            def make_entry_callback(idx):
                return lambda e: update_plot_from_entry(idx)

            x_entry.bind("<FocusOut>", make_entry_callback(i))
            x_entry.bind("<Return>", make_entry_callback(i))
            y_entry.bind("<FocusOut>", make_entry_callback(i))
            y_entry.bind("<Return>", make_entry_callback(i))

        def update_lines():
            try:
                x1 = float(self.entries[0].get())
                y1 = float(self.entries[1].get())
                x2 = float(self.entries[2].get())
                y2 = float(self.entries[3].get())

                if segment_lines[0]:
                    segment_lines[0].remove()
                segment_lines[0] = ax.plot([x1, x2], [y1, y2], color='gray', linestyle='--')[0]
            except ValueError:
                if segment_lines[0]:
                    segment_lines[0].remove()
                    segment_lines[0] = None

            try:
                x3 = float(self.entries[4].get())
                y3 = float(self.entries[5].get())
                x4 = float(self.entries[6].get())
                y4 = float(self.entries[7].get())

                if segment_lines[1]:
                    segment_lines[1].remove()
                segment_lines[1] = ax.plot([x3, x4], [y3, y4], color='gray', linestyle='--')[0]
            except ValueError:
                if segment_lines[1]:
                    segment_lines[1].remove()
                    segment_lines[1] = None

        def calculate():
            try:
                coords = [float(e.get()) for e in self.entries]
                result = callback(coords)
                messagebox.showinfo(tr("result"), result)
            except Exception as e:
                messagebox.showerror(tr("error"), str(e))

        def save():
            try:
                coords = [float(e.get()) for e in self.entries]
                points = [(coords[i], coords[i+1]) for i in range(0, 8, 2)]

                os.makedirs("saves", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                filename = f"saves/intersection/points_{timestamp}.csv"

                with open(filename, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Point", "X", "Y"])
                    for i, (x, y) in enumerate(points, start=1):
                        writer.writerow([f"P{i}", x, y])

                messagebox.showinfo(tr("saved"), f"{tr('save_success')}\n{filename}")
            except Exception as e:
                messagebox.showerror(tr("error"), f"{tr('save_error')}\n{str(e)}")

        def back_and_close_plot():
            plt.close(fig)
            self.render_main_menu()

        ttk.Button(parent, text=tr("calculate"), command=calculate, width=30).pack(pady=5)
        ttk.Button(parent, text=tr("save"), command=save, width=30).pack(pady=5)
        ttk.Button(parent, text=tr("back"), command=back_and_close_plot, width=30).pack(pady=5)

        def onclick(event):
            if toolbar.mode != '':
                return

            if event.xdata is None or event.ydata is None:
                return

            x, y = round(event.xdata, 2), round(event.ydata, 2)
            index = selected_point_index.get()
            if index < 0 or index >= 4:
                return

            self.entries[index * 2].delete(0, tk.END)
            self.entries[index * 2].insert(0, str(x))
            self.entries[index * 2 + 1].delete(0, tk.END)
            self.entries[index * 2 + 1].insert(0, str(y))

            if point_dots[index]:
                point_dots[index].remove()
            if point_labels[index]:
                point_labels[index].remove()

            point_dots[index] = ax.plot(x, y, 'o', color=colors[index])[0]
            point_labels[index] = ax.text(x + 0.1, y + 0.1, f"P{index+1}", color=colors[index])
            update_lines()
            canvas.draw()

            for i in range(index + 1, 4):
                if self.entries[i * 2].get() == "" or self.entries[i * 2 + 1].get() == "":
                    selected_point_index.set(i)
                    break

        canvas.mpl_connect("button_press_event", onclick)

        def redraw_all_points():
            for i in range(4):
                update_plot_from_entry(i)

        self.redraw_all_points = redraw_all_points

    def compute_intersection(self, coords):
        return check_intersection(*coords)

    def compute_convex_hull(self, coords):
        return compute_convex_hull(coords)

def run_app():
    app = AppWindow()
    app.root.mainloop()

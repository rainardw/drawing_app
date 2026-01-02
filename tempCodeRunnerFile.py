import tkinter as tk
from tkinter import colorchooser, simpledialog
from PIL import Image, ImageDraw, ImageFont
import os
import sys

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PinkBrush Pro 💖 - by codingwrann")
        self.root.geometry("1100x800")
        self.root.configure(bg="#FFF8FA")  # pink sangat lembut
        self.root.resizable(False, False)

        # State
        self.current_color = "#FF69B4"
        self.brush_size = 5
        self.is_eraser = False
        self.drawing_tool = "brush"  # "brush", "text", "circle", "square", "triangle"
        self.start_x = None
        self.start_y = None

        # Canvas utama (lebih besar)
        self.canvas = tk.Canvas(
            root, bg="white", cursor="cross",
            width=900, height=550,
            highlightthickness=1, highlightbackground="#E8D0D5"
        )
        self.canvas.pack(pady=15)

        # Gambar virtual untuk simpan
        self.image = Image.new("RGB", (900, 550), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Binding
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.create_toolbar()
        self.create_color_palette()
        self.create_shape_tools()
        self.create_action_buttons()

    # === MOUSE HANDLERS ===
    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

        # Jika mode text
        if self.drawing_tool == "text":
            self.add_text_at(event.x, event.y)
            return

    def on_drag(self, event):
        if self.drawing_tool == "brush":
            if self.start_x and self.start_y:
                color = "white" if self.is_eraser else self.current_color
                # Canvas
                self.canvas.create_line(
                    self.start_x, self.start_y, event.x, event.y,
                    width=self.brush_size, fill=color,
                    capstyle=tk.ROUND, smooth=tk.TRUE
                )
                # Pillow
                self.draw.line(
                    [self.start_x, self.start_y, event.x, event.y],
                    fill=color, width=self.brush_size
                )
                self.start_x, self.start_y = event.x, event.y

    def on_release(self, event):
        if self.drawing_tool in ["circle", "square", "triangle"]:
            self.draw_shape(self.start_x, self.start_y, event.x, event.y)
        self.start_x, self.start_y = None, None

    # === TEXT TOOL ===
    def add_text_at(self, x, y):
        user_text = simpledialog.askstring("Input Teks", "Masukkan teks:", parent=self.root)
        if user_text:
            font_size = simpledialog.askinteger("Ukuran Font", "Ukuran font (8–40):", 
                                              initialvalue=20, minvalue=8, maxvalue=40)
            if font_size:
                # Gambar di canvas
                self.canvas.create_text(x, y, text=user_text, fill=self.current_color, 
                                       font=("Segoe UI", font_size, "normal"))
                # Gambar di Pillow (simulasi sederhana — teks mungkin tidak 100% sama)
                try:
                    # Coba pakai font default
                    self.draw.text((x, y), user_text, fill=self.current_color, 
                                   font=None)  # Pillow tidak support font size langsung tanpa file
                except:
                    self.draw.text((x, y), user_text, fill=self.current_color)

    # === BENTUK GEOMETRIS ===
    def draw_shape(self, x1, y1, x2, y2):
        color = self.current_color
        if self.drawing_tool == "circle":
            # Pastikan jadi lingkaran (bukan oval)
            dx, dy = x2 - x1, y2 - y1
            size = min(abs(dx), abs(dy))
            if dx < 0: x1 -= size
            if dy < 0: y1 -= size
            self.canvas.create_oval(x1, y1, x1+size, y1+size, outline=color, width=self.brush_size)
            self.draw.ellipse([x1, y1, x1+size, y1+size], outline=color, width=self.brush_size)
        elif self.drawing_tool == "square":
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=self.brush_size)
            self.draw.rectangle([x1, y1, x2, y2], outline=color, width=self.brush_size)
        elif self.drawing_tool == "triangle":
            x3 = x1 + (x2 - x1) // 2
            y3 = y1
            self.canvas.create_polygon(x1, y2, x2, y2, x3, y3, outline=color, fill="", width=self.brush_size)
            self.draw.polygon([(x1, y2), (x2, y2), (x3, y3)], outline=color, width=self.brush_size)

    # === TOOLBAR ATAS ===
    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg="#FFF0F3", height=60)
        toolbar.pack(fill=tk.X, padx=20, pady=(0, 8))
        toolbar.pack_propagate(False)

        tk.Label(toolbar, text="🖌️ Alat:", bg="#FFF0F3", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(0,10))

        tools = [
            ("Brush", "brush", "#FFB6C1"),
            ("Text", "text", "#A8E6CF"),
            ("○ Lingkaran", "circle", "#FFD3B6"),
            ("▭ Persegi", "square", "#D4A5A5"),
            ("△ Segitiga", "triangle", "#C1F4C5")
        ]

        for name, tool, bg in tools:
            btn = tk.Button(
                toolbar, text=name, bg=bg, fg="black",
                font=("Segoe UI", 10), width=10,
                command=lambda t=tool: self.set_tool(t)
            )
            btn.pack(side=tk.LEFT, padx=4)

        # Penghapus
        eraser_btn = tk.Button(
            toolbar, text="🖉 Penghapus", bg="#E0E0E0",
            font=("Segoe UI", 10), width=12,
            command=self.toggle_eraser
        )
        eraser_btn.pack(side=tk.RIGHT, padx=4)

    # === PALET WARNA ===
    def create_color_palette(self):
        color_frame = tk.Frame(self.root, bg="#FFF8FA")
        color_frame.pack(pady=5)

        tk.Label(color_frame, text="🎨 Warna:", bg="#FFF8FA", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0,10))

        colors = [
            "#FF69B4", "#7FBF90", "#FF9EB1", "#A29BFE", "#55EFC4",
            "#FFD3B6", "#A8E6CF", "#D4A5A5", "#C1F4C5", "#FFAAA5", "black", "white"
        ]
        for color in colors:
            btn = tk.Button(
                color_frame, bg=color, width=2, height=1,
                command=lambda c=color: self.select_color(c)
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Color picker custom
        tk.Button(
            color_frame, text="🎨 Pilih...", bg="#E8D0D5", width=8,
            command=self.pick_custom_color
        ).pack(side=tk.LEFT, padx=(10, 0))

    # === UKURAN & BENTUK ===
    def create_shape_tools(self):
        shape_frame = tk.Frame(self.root, bg="#FFF8FA")
        shape_frame.pack(pady=5)

        # Ukuran kuas
        tk.Label(shape_frame, text="✏️ Ukuran:", bg="#FFF8FA", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0,5))
        size_var = tk.IntVar(value=5)
        tk.Scale(
            shape_frame, from_=1, to=50, orient=tk.HORIZONTAL,
            variable=size_var, bg="#FFF8FA", highlightthickness=0,
            length=200,
            command=lambda v: setattr(self, 'brush_size', int(v))
        ).pack(side=tk.LEFT, padx=5)

    # === TOMBOL AKSI BAWAH ===
    def create_action_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#FFF8FA")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame, text="🗑️ Hapus Semua", bg="#FFB3BA", fg="white",
            font=("Segoe UI", 11, "bold"), width=10, height=25,
            command=self.clear_all
        ).pack(side=tk.LEFT, padx=12)

        tk.Button(
            btn_frame, text="💾 Simpan Gambar", bg="#7FBF90", fg="white",
            font=("Segoe UI", 11, "bold"), width=10, height=25,
            command=self.save_image
        ).pack(side=tk.LEFT, padx=12)

    # === FUNGSI SET ALAT ===
    def set_tool(self, tool):
        self.drawing_tool = tool
        self.is_eraser = False

    def select_color(self, color):
        self.current_color = color
        self.is_eraser = False

    def pick_custom_color(self):
        color_code = colorchooser.askcolor(title="Pilih Warna")[1]
        if color_code:
            self.current_color = color_code
            self.is_eraser = False

    def toggle_eraser(self):
        self.is_eraser = not self.is_eraser
        self.drawing_tool = "brush"

    def clear_all(self):
        from tkinter import messagebox
        if messagebox.askyesno("Konfirmasi", "Hapus SEMUA? 💔"):
            self.canvas.delete("all")
            self.image = Image.new("RGB", (900, 550), "white")
            self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        try:
            folder = "gambar"
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, "pinkbrush_pro_art.png")
            self.image.save(path)
            from tkinter import messagebox
            messagebox.showinfo("💖 Berhasil!", f"Gambar disimpan di:\n{os.path.abspath(path)}")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("❌ Error", f"Gagal simpan:\n{str(e)}")

# === JALANKAN ===
if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from PIL import Image
from io import BytesIO
import threading
import sys

try:
    from tkinterdnd2 import DND_FILES, DND_TEXT
    HAS_DND = True
except ImportError:
    HAS_DND = False

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass


class HEICConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPG Converter")
        self.root.geometry("700x650")
        self.root.resizable(True, True)

        self.files = []
        self.output_folder = None
        self.converting = False

        # Color scheme
        self.dark_gray = "#2c3e50"
        self.bright_blue = "#3498db"
        self.light_bg = "#f5f5f5"
        self.light_blue_bg = "#e8f4f8"

        # Set window icon
        self.set_window_icon()

        self.setup_ui()
        self.setup_drag_drop()

    def setup_ui(self):
        self.root.configure(bg=self.light_bg)

        # Title bar with branding
        title_frame = tk.Frame(self.root, bg=self.dark_gray, height=100)
        title_frame.pack(fill=tk.X)

        # Try to load and display the branding icon
        try:
            icon_path = self.get_icon_path()
            if icon_path and os.path.exists(icon_path):
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((60, 60), Image.Resampling.LANCZOS)
                self.icon_photo = tk.PhotoImage(file=icon_path) if icon_path.endswith('.gif') else None

                # Convert PIL image to PhotoImage
                icon_img_tk = self.pil_to_photoimage(icon_img)
                icon_label = tk.Label(title_frame, image=icon_img_tk, bg=self.dark_gray)
                icon_label.image = icon_img_tk
                icon_label.pack(side=tk.LEFT, padx=15, pady=10)
        except Exception as e:
            print(f"Could not load icon: {e}")

        title_label = tk.Label(
            title_frame,
            text="HEIC to JPG Converter",
            font=("Segoe UI", 18, "bold"),
            bg=self.dark_gray,
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=20)

        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.light_bg)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Drag and drop area
        self.drop_frame = tk.Frame(content_frame, bg=self.light_blue_bg, height=150, relief=tk.SOLID, borderwidth=2)
        self.drop_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)

        drop_label = tk.Label(
            self.drop_frame,
            text="Drag and drop HEIC files here\nor click to browse",
            bg=self.light_blue_bg,
            font=("Segoe UI", 12, "bold"),
            fg=self.dark_gray,
            cursor="hand2"
        )
        drop_label.pack(expand=True)

        self.drop_frame.bind("<Button-1>", self.browse_files)
        drop_label.bind("<Button-1>", self.browse_files)

        # File list
        list_label = tk.Label(
            content_frame,
            text="Selected Files:",
            font=("Segoe UI", 11, "bold"),
            bg=self.light_bg,
            fg=self.dark_gray
        )
        list_label.pack(anchor="w", padx=20, pady=(10, 5))

        list_frame = tk.Frame(content_frame, bg=self.light_bg)
        list_frame.pack(padx=20, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            height=8,
            font=("Segoe UI", 10),
            bg="white",
            fg=self.dark_gray,
            highlightthickness=1,
            highlightcolor=self.bright_blue
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # Clear button
        clear_btn = ttk.Button(content_frame, text="Clear Files", command=self.clear_files)
        clear_btn.pack(pady=8)

        # Quality slider
        quality_frame = tk.Frame(content_frame, bg=self.light_bg)
        quality_frame.pack(padx=20, pady=12, fill=tk.X)

        quality_label = tk.Label(
            quality_frame,
            text="JPG Quality:",
            font=("Segoe UI", 10, "bold"),
            bg=self.light_bg,
            fg=self.dark_gray
        )
        quality_label.pack(side=tk.LEFT)

        self.quality_var = tk.IntVar(value=75)
        quality_slider = ttk.Scale(
            quality_frame,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.quality_var,
            command=self.update_quality_label
        )
        quality_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        self.quality_label = tk.Label(
            quality_frame,
            text="75",
            width=3,
            font=("Segoe UI", 10, "bold"),
            bg=self.light_bg,
            fg=self.bright_blue
        )
        self.quality_label.pack(side=tk.LEFT)

        # Output folder
        output_frame = tk.Frame(content_frame, bg=self.light_bg)
        output_frame.pack(padx=20, pady=12, fill=tk.X)

        output_label_text = tk.Label(
            output_frame,
            text="Save converted files to:",
            font=("Segoe UI", 10, "bold"),
            bg=self.light_bg,
            fg=self.dark_gray
        )
        output_label_text.pack(side=tk.LEFT)

        self.output_label = tk.Label(
            output_frame,
            text="Same as source files (default)",
            font=("Segoe UI", 10),
            fg=self.bright_blue,
            bg=self.light_bg
        )
        self.output_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        browse_btn = ttk.Button(
            output_frame,
            text="Browse...",
            command=self.choose_output_folder
        )
        browse_btn.pack(side=tk.RIGHT)

        # Convert button
        button_frame = tk.Frame(content_frame, bg=self.light_bg)
        button_frame.pack(pady=15)

        self.convert_btn = tk.Button(
            button_frame,
            text="Convert Files",
            command=self.start_conversion,
            font=("Segoe UI", 11, "bold"),
            bg=self.bright_blue,
            fg="white",
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#2980b9",
            activeforeground="white"
        )
        self.convert_btn.pack()

        # Status
        self.status_label = tk.Label(
            button_frame,
            text="Ready",
            font=("Segoe UI", 9),
            fg=self.dark_gray,
            bg=self.light_bg
        )
        self.status_label.pack(pady=5)

    def set_window_icon(self):
        """Set the window icon to the professional branding icon"""
        try:
            icon_path = self.get_icon_path()
            if icon_path and os.path.exists(icon_path):
                # Load icon and set as window icon
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((64, 64), Image.Resampling.LANCZOS)

                from PIL import ImageTk
                photo = ImageTk.PhotoImage(icon_img)
                self.root.iconphoto(False, photo)
                # Keep a reference to prevent garbage collection
                self.icon_photo = photo
        except Exception as e:
            print(f"Could not set window icon: {e}")

    def pil_to_photoimage(self, pil_image):
        """Convert PIL image to PhotoImage"""
        try:
            from PIL import ImageTk
            return ImageTk.PhotoImage(pil_image)
        except:
            return None

    def get_icon_path(self):
        """Get the path to the icon file"""
        # Try multiple possible locations
        base_dir = os.path.dirname(__file__)
        possible_paths = [
            # For PyInstaller bundled app
            os.path.join(base_dir, 'icon.jpg'),
            os.path.join(base_dir, '..', 'icon.jpg'),
            # For development
            os.path.join(base_dir, 'heic_converter.jpg'),
            os.path.join(base_dir, 'heic_converter.png'),
            # For installed version
            os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Programs', 'HEIC to JPG Converter', 'icon.jpg'),
        ]

        for path in possible_paths:
            full_path = os.path.abspath(path)
            if os.path.exists(full_path):
                return full_path

        return None

    def setup_drag_drop(self):
        """Setup drag and drop for the window"""
        if not HAS_DND:
            return

        try:
            self.drop_frame.drop_target_register(DND_FILES)
            self.drop_frame.dnd_bind('<<Drop>>', self.drop_files)
            self.file_listbox.drop_target_register(DND_FILES)
            self.file_listbox.dnd_bind('<<Drop>>', self.drop_files)
        except Exception as e:
            print(f"Drag and drop setup failed: {e}")

    def drop_files(self, event):
        """Handle dropped files"""
        try:
            import re
            data = event.data.strip()
            files = []

            # Handle tkinterdnd2 format: files wrapped in curly braces
            brace_pattern = r'\{([^}]+)\}'
            brace_files = re.findall(brace_pattern, data)

            if brace_files:
                files = brace_files
            else:
                # Look for drive letters or UNC paths
                path_pattern = r'[A-Z]:\\[^\s]+|\\\\[^\s]+'
                files = re.findall(path_pattern, data)

                if not files:
                    # Fallback: split by space
                    files = [f.strip('"').strip("'") for f in data.split() if f.strip()]

            heic_files = []
            for file_path in files:
                file_path = file_path.strip().strip('"').strip("'")
                if file_path and file_path.lower().endswith(('.heic', '.heif')):
                    if os.path.isfile(file_path):
                        heic_files.append(file_path)

            if heic_files:
                self.files.extend(heic_files)
                self.update_file_list()
            else:
                messagebox.showwarning("Invalid Files", "Please drop HEIC or HEIF files or use Browse")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing dropped files: {e}")

    def browse_files(self, event=None):
        """Browse for HEIC files"""
        files = filedialog.askopenfilenames(
            title="Select HEIC files",
            filetypes=[("HEIC files", "*.heic *.heif"), ("All files", "*.*")]
        )

        if files:
            self.files.extend(files)
            self.update_file_list()

    def update_file_list(self):
        """Update the file listbox display"""
        self.file_listbox.delete(0, tk.END)
        for file in self.files:
            filename = os.path.basename(file)
            self.file_listbox.insert(tk.END, filename)

    def clear_files(self):
        """Clear all selected files"""
        self.files = []
        self.update_file_list()

    def update_quality_label(self, value):
        """Update quality label when slider changes"""
        self.quality_label.config(text=str(int(float(value))))

    def choose_output_folder(self):
        """Choose output folder for converted files"""
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.output_folder = folder
            self.output_label.config(text=folder)

    def start_conversion(self):
        """Start file conversion in a separate thread"""
        if not self.files:
            messagebox.showwarning("No Files", "Please select HEIC files to convert")
            return

        self.converting = True
        self.convert_btn.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()

    def convert_files(self):
        """Convert HEIC files to JPG"""
        quality = self.quality_var.get()
        converted = 0
        failed = 0
        error_details = []

        try:
            for file_path in self.files:
                if not self.converting:
                    break

                try:
                    # Determine output folder
                    if self.output_folder:
                        output_dir = self.output_folder
                    else:
                        output_dir = os.path.dirname(file_path)

                    # Create output filename
                    filename = Path(file_path).stem
                    output_path = os.path.join(output_dir, f"{filename}.jpg")

                    # Handle duplicate filenames
                    counter = 1
                    while os.path.exists(output_path):
                        name = Path(file_path).stem
                        output_path = os.path.join(output_dir, f"{name}_{counter}.jpg")
                        counter += 1

                    # Read file into memory (works better with network paths)
                    with open(file_path, 'rb') as f:
                        file_data = f.read()

                    # Convert image from memory
                    img = Image.open(BytesIO(file_data))

                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            background.paste(img, mask=img.split()[-1])
                        else:
                            background.paste(img)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Save as JPG
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                    converted += 1

                    self.update_status(f"Converting... ({converted}/{len(self.files)})")

                except Exception as e:
                    failed += 1
                    error_msg = f"{os.path.basename(file_path)}: {str(e)}"
                    error_details.append(error_msg)
                    print(f"Error converting {file_path}: {e}")

            # Show completion message
            self.converting = False
            self.root.after(0, self.show_completion, converted, failed, error_details)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Conversion error: {e}"))
        finally:
            self.root.after(0, lambda: self.convert_btn.config(state=tk.NORMAL))

    def show_completion(self, converted, failed, error_details):
        """Show completion message"""
        message = f"Conversion complete!\n\nSuccessful: {converted}\nFailed: {failed}"

        if failed > 0:
            message += f"\n\nErrors:\n"
            for error in error_details[:5]:
                message += f"• {error}\n"
            if len(error_details) > 5:
                message += f"... and {len(error_details) - 5} more"
            messagebox.showwarning("Conversion Complete", message)
        else:
            messagebox.showinfo("Done", message)

        self.update_status("Ready")
        self.files = []
        self.update_file_list()

    def update_status(self, message):
        """Update status label"""
        self.root.after(0, lambda: self.status_label.config(text=message))


if __name__ == "__main__":
    if HAS_DND:
        from tkinterdnd2 import Tk
        root = Tk()
    else:
        root = tk.Tk()
    app = HEICConverterApp(root)
    root.mainloop()

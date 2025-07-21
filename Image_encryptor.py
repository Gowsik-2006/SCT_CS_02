import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import random

# === Load your custom theme ===
ctk.set_default_color_theme("D:/Python materials/python practice/cc/nordic_theme.json")

# === Complex Encrypt ===
def complex_encrypt(input_path, output_path, key, seed):
    img = Image.open(input_path).convert('RGB')
    pixels = list(img.getdata())
    n = len(pixels)

    # XOR pixel values
    pixels = [(r ^ key, g ^ key, b ^ key) for (r, g, b) in pixels]

    # Shuffle pixel positions with seed
    random.seed(seed)
    indices = list(range(n))
    random.shuffle(indices)
    shuffled_pixels = [pixels[i] for i in indices]

    img.putdata(shuffled_pixels)
    img.save(output_path)

def complex_decrypt(input_path, output_path, key, seed):
    img = Image.open(input_path).convert('RGB')
    pixels = list(img.getdata())
    n = len(pixels)

    # Generate shuffle order
    random.seed(seed)
    indices = list(range(n))
    shuffled_indices = indices.copy()
    random.shuffle(shuffled_indices)

    # Build reverse mapping
    reverse_indices = [0] * n
    for i, si in enumerate(shuffled_indices):
        reverse_indices[si] = i

    # Unshuffle
    unshuffled_pixels = [pixels[reverse_indices[i]] for i in range(n)]

    # Reverse XOR
    original_pixels = [(r ^ key, g ^ key, b ^ key) for (r, g, b) in unshuffled_pixels]

    img.putdata(original_pixels)
    img.save(output_path)

# === GUI App ===
class ComplexEncryptorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Complex Image Encryptor")
        self.geometry("600x500")
        self.input_path = ""

        self.label = ctk.CTkLabel(self, text="PIXEL IMAGE ENCRYPTOR TOOL",font=("Bitcount Grid Single Light Open", 30,"bold"))
        self.label.pack(pady=20)

        self.load_button = ctk.CTkButton(self, text="Load Image",font=("courier new", 16,"bold"), command=self.load_image)
        self.load_button.pack(pady=20)

        self.key_entry = ctk.CTkEntry(self, placeholder_text="Enter Key (integer)",font=("Consolas",16),width=200, height=20)
        self.key_entry.pack(pady=20)

        self.seed_entry = ctk.CTkEntry(self, placeholder_text="Enter Seed (integer)",font=("Consolas",16),width=200, height=20)
        self.seed_entry.pack(pady=20)

        self.encrypt_button = ctk.CTkButton(self, text="Encrypt Image",font=("courier new", 16,"bold"), command=self.encrypt)
        self.encrypt_button.pack(pady=20)

        self.decrypt_button = ctk.CTkButton(self, text="Decrypt Image",font=("courier new", 16,"bold"), command=self.decrypt)
        self.decrypt_button.pack(pady=20)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.input_path = path
            messagebox.showinfo("Loaded", f"Image loaded:\n{path}")

    def encrypt(self):
        if self.input_path and self.key_entry.get() and self.seed_entry.get():
            try:
                key = int(self.key_entry.get())
                seed = int(self.seed_entry.get())
                output_path = filedialog.asksaveasfilename(defaultextension=".png")
                if output_path:
                    complex_encrypt(self.input_path, output_path, key, seed)
                    messagebox.showinfo("Success", f"Encrypted and saved:\n{output_path}")
            except ValueError:
                messagebox.showerror("Error", "Key and Seed must be integers.")

    def decrypt(self):
        if self.input_path and self.key_entry.get() and self.seed_entry.get():
            try:
                key = int(self.key_entry.get())
                seed = int(self.seed_entry.get())
                output_path = filedialog.asksaveasfilename(defaultextension=".png")
                if output_path:
                    complex_decrypt(self.input_path, output_path, key, seed)
                    messagebox.showinfo("Success", f"Decrypted and saved:\n{output_path}")
            except ValueError:
                messagebox.showerror("Error", "Key and Seed must be integers.")

if __name__ == "__main__":
    app = ComplexEncryptorApp()
    app.mainloop()

# Written by: Gowsik Raja.S
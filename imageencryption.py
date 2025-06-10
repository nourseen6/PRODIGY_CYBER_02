import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def update_images(original_path, result_path):
   
    original_img = Image.open(original_path)
    original_img.thumbnail((180, 180))
    original_photo = ImageTk.PhotoImage(original_img)

    result_img = Image.open(result_path)
    result_img.thumbnail((180, 180))
    result_photo = ImageTk.PhotoImage(result_img)

    original_label.config(image=original_photo)
    original_label.image = original_photo  

    result_label.config(image=result_photo)
    result_label.image = result_photo  

def encrypt_image(path, shift):
    image = Image.open(path)
    pixels = image.load()

    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = ((r + shift) % 256, (g + shift) % 256, (b + shift) % 256)

    new_path = os.path.splitext(path)[0] + "_encrypted.png"
    image.save(new_path)
    return new_path

def decrypt_image(path, shift):
    image = Image.open(path)
    pixels = image.load()

    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = ((r - shift) % 256, (g - shift) % 256, (b - shift) % 256)

    new_path = os.path.splitext(path)[0] + "_decrypted.png"
    image.save(new_path)
    return new_path

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if filename:
        path_var.set(filename)
        # Show original image
        original_img = Image.open(filename)
        original_img.thumbnail((180,180))
        original_photo = ImageTk.PhotoImage(original_img)
        original_label.config(image=original_photo)
        original_label.image = original_photo

        
        result_label.config(image='')
        result_label.image = None

def encrypt_action():
    try:
        shift = int(shift_entry.get())
        path = path_var.get()
        if not path:
            raise Exception("No image selected")
        new_file = encrypt_image(path, shift)
        messagebox.showinfo("Success", f"Encrypted image saved as:\n{new_file}")
        update_images(path, new_file)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_action():
    try:
        shift = int(shift_entry.get())
        path = path_var.get()
        if not path:
            raise Exception("No image selected")
        new_file = decrypt_image(path, shift)
        messagebox.showinfo("Success", f"Decrypted image saved as:\n{new_file}")
        update_images(path, new_file)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI 
window = tk.Tk()
window.title("Image Encryption Tool")
window.geometry("700x450")

path_var = tk.StringVar()

top_frame = tk.Frame(window)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Select Image File:", font=("Arial", 14)).grid(row=0, column=0, padx=5)
tk.Button(top_frame, text="Browse", command=browse_file, font=("Arial", 12)).grid(row=0, column=1)

tk.Label(window, textvariable=path_var, wraplength=650, fg="blue", font=("Arial", 10)).pack()

tk.Label(window, text="Enter Shift Value:", font=("Arial", 14)).pack(pady=5)
shift_entry = tk.Entry(window, font=("Arial", 14))
shift_entry.pack()

button_frame = tk.Frame(window)
button_frame.pack(pady=10)
tk.Button(button_frame, text="Encrypt", command=encrypt_action, bg="lightgreen", font=("Arial", 14)).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Decrypt", command=decrypt_action, bg="lightblue", font=("Arial", 14)).grid(row=0, column=1, padx=10)

images_frame = tk.Frame(window)
images_frame.pack(pady=10)

tk.Label(images_frame, text="Original Image", font=("Arial", 12)).grid(row=0, column=0, padx=20)
tk.Label(images_frame, text="Result Image", font=("Arial", 12)).grid(row=0, column=1, padx=20)

original_label = tk.Label(images_frame)
original_label.grid(row=1, column=0, padx=20)

result_label = tk.Label(images_frame)
result_label.grid(row=1, column=1, padx=20)

window.mainloop()

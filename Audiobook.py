import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
import PyPDF2

from gtts import gTTS
import os

# Main app window
app = tk.Tk()
app.title("PDF to Audiobook Converter")
app.geometry("400x500")

# Variables
pdf_path = tk.StringVar()
start_page = tk.StringVar(value="1")
end_page = tk.StringVar(value="1")
language = tk.StringVar(value="en")
voice_type = tk.StringVar(value="Male")
speed = tk.IntVar(value=150)

# Functions
def browse_file():
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if path:
        pdf_path.set(path)

def get_text_from_pdf(path, start, end):
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            start = max(0, int(start) - 1)
            end = min(int(end), total_pages)

            text = ""
            for i in range(start, end):
                page = reader.pages[i]
                content = page.extract_text()
                if content:
                    text += content
            return text
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return ""

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed.get())

    # Set voice (Male/Female)
    voices = engine.getProperty('voices')
    if voice_type.get() == "Male":
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

    engine.say(text)
    engine.runAndWait()

def preview_audio():
    if not pdf_path.get():
        messagebox.showwarning("Missing File", "Please select a PDF file.")
        return

    text = get_text_from_pdf(pdf_path.get(), start_page.get(), end_page.get())
    if text.strip():
        speak_text(text[:500])  # Speak first 500 characters for preview
    else:
        messagebox.showinfo("Empty", "No readable text found in the selected page range.")

def save_mp3():
    messagebox.showinfo("Coming Soon", "MP3 save functionality will be added in the next step.")

# GUI Widgets
tk.Label(app, text="Select PDF:").pack(pady=5)
tk.Entry(app, textvariable=pdf_path, width=40).pack()
tk.Button(app, text="Browse", command=browse_file).pack(pady=5)

tk.Label(app, text="Page Range (Start - End):").pack(pady=10)
tk.Entry(app, textvariable=start_page, width=5).pack(side=tk.LEFT, padx=(90, 5))
tk.Entry(app, textvariable=end_page, width=5).pack(side=tk.LEFT)

tk.Label(app, text="Language (for later use):").pack(pady=10)
tk.OptionMenu(app, language, "en", "hi", "es", "fr", "de").pack()

tk.Label(app, text="Voice Type:").pack(pady=10)
tk.OptionMenu(app, voice_type, "Male", "Female").pack()

tk.Label(app, text="Speaking Speed:").pack(pady=10)
tk.Scale(app, from_=100, to=250, variable=speed, orient=tk.HORIZONTAL).pack()

tk.Button(app, text="▶ Preview", command=preview_audio).pack(pady=10)
tk.Button(app, text="💾 Save MP3", command=save_mp3).pack(pady=5)

app.mainloop()


def save_mp3():
    if not pdf_path.get():
        messagebox.showwarning("Missing File", "Please select a PDF file.")
        return

    text = get_text_from_pdf(pdf_path.get(), start_page.get(), end_page.get())
    if not text.strip():
        messagebox.showinfo("Empty", "No readable text found in the selected page range.")
        return

    try:
        lang = language.get()  # Use selected language (e.g., 'en', 'hi', etc.)
        tts = gTTS(text=text, lang=lang)
        
        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if save_path:
            tts.save(save_path)
            messagebox.showinfo("Success", f"MP3 saved to:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
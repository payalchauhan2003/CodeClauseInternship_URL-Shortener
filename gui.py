import tkinter as tk
from tkinter import messagebox
import requests


class URLShortenerGUI:
    def __init__(self, master):
        self.master = master
        master.title("URL Shortener")

        self.label = tk.Label(master, text="URL Shortener")
        self.label.pack()

        self.long_url_label = tk.Label(master, text="Long URL:")
        self.long_url_label.pack()

        self.long_url_entry = tk.Entry(master, width=50)
        self.long_url_entry.pack()

        self.shorten_button = tk.Button(master, text="Shorten URL", command=self.shorten_url)
        self.shorten_button.pack()

        self.short_url_label = tk.Label(master, text="Shortened URL:")
        self.short_url_label.pack()

        self.short_url_entry = tk.Entry(master, width=50)
        self.short_url_entry.pack()

        self.expand_button = tk.Button(master, text="Expand URL", command=self.expand_url)
        self.expand_button.pack()

        self.expanded_url_label = tk.Label(master, text="Expanded URL:")
        self.expanded_url_label.pack()

        self.expanded_url_entry = tk.Entry(master, width=50)
        self.expanded_url_entry.pack()

    def shorten_url(self):
        long_url = self.long_url_entry.get()

        if not long_url:
            messagebox.showwarning("Warning", "Please enter a long URL")
            return

        # Send a POST request to the server to shorten the URL
        response = requests.post("http://localhost:5000/shorten", json={'url': long_url})

        if response.status_code == 200:
            short_url = response.json()['short_url']
            self.short_url_entry.delete(0, tk.END)
            self.short_url_entry.insert(0, short_url)
        else:
            messagebox.showerror("Error", "Failed to shorten URL")

    def expand_url(self):
        short_url = self.short_url_entry.get()

        if not short_url:
            messagebox.showwarning("Warning", "Please enter a short URL")
            return

        # Send a GET request to the server to expand the URL
        response = requests.get(short_url)

        if response.status_code == 200:
            long_url = response.url
            self.expanded_url_entry.delete(0, tk.END)
            self.expanded_url_entry.insert(0, long_url)
        else:
            messagebox.showerror("Error", "Failed to expand URL")


if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortenerGUI(root)
    root.mainloop()


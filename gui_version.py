# Author:  Luke Moll
# Date:    2024-02-01

import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox


class WebScraper:
    # A class to scrape multiple websites.
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def is_response_successful(self):
        # Check if the request was successful.
        return self.response.status_code == 200

    def get_title(self):
        # Get the title of the webpage.
        return self.soup.find("h1").get_text()

    def get_links(self):
        # Get all links from the webpage that do not contain '#'.
        return [link.attrs["href"] for link in self.soup.find_all("a") if '#' not in link.attrs["href"]]

    @staticmethod
    def save_links(links):
        # Save the links to a text file.
        with open('links.txt', 'w') as f:
            for link in links:
                f.write("%s\n" % link)  # puts every link in a separate line
        messagebox.showinfo("success", "links saved 'links.txt'")

    @staticmethod
    def get_user_input(valid_inputs):
        # Get user input and validate it.
        while True:
            user_input = int(input())
            if user_input in valid_inputs:
                return user_input


class GUI:
    # A class to create a GUI for the web scraper.
    def __init__(self, root):
        self.root = root
        self.scraper = None
        self.links_frame = None

        label = tk.Label(root, text="Enter url to scrape")
        label.pack()
        entry = tk.Entry(root)
        entry.pack()

        self.output = tk.Text(root, state='disabled')
        self.output.pack()

        scrollbar = tk.Scrollbar(root, command=self.output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.config(yscrollcommand=scrollbar.set)

        actions = {1: "Request response", 2: "Get the title", 3: "Get every link", 4: "End program"}
        for key, value in actions.items():
            button = tk.Button(root, text=value, command=lambda k=key: self.start_scraping(entry.get(), k))
            button.pack()

    def link_window(self, links):
        # Display the links in the output text box.
        for link in links:
            self.output.insert(tk.END, link + "\n")
        if not hasattr(self, 'save_button'):
            self.save_button = tk.Button(self.links_frame, text="save links", command=lambda: self.scraper.save_links(links))
            self.save_button.pack()

    def start_scraping(self, url, action):
        # Start the web scraping process based on the user's action.
        if action == 4:
            self.root.destroy()
        else:
            self.scraper = WebScraper(url)
            self.output.config(state='normal')
            if action == 1:
                self.output.insert(tk.END, "Request successful\n" if self.scraper.is_response_successful() else "Request failed\n")
            elif action == 2:
                self.output.insert(tk.END, self.scraper.get_title() + "\n")
            elif action == 3:
                links = self.scraper.get_links()
                self.link_window(links)
                messagebox.showinfo("information", str(len(links)) + " links found\n")
            else:
                self.output.insert(tk.END, "Wrong selection, try again\n")
            self.output.config(state='disabled')


def main():
    # Create the GUI and start the Tkinter event loop.
    root = tk.Tk()
    root.geometry('800x600')
    gui = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

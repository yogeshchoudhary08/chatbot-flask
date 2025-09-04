import tkinter as tk
import webbrowser

projects = [
    {'budget': '$1000', 'description': 'Web development project to create an e-commerce site.', 'url': 'https://example.com/project1'},
    {'budget': '$500', 'description': 'Python script automation for data scraping from websites.', 'url': 'https://example.com/project2'},
    {'budget': '$750', 'description': 'Design and implement a chatbot using AI techniques.', 'url': 'https://example.com/project3'},
    # Add more projects with URLs
]

def open_url(url):
    webbrowser.open(url)

root = tk.Tk()
root.title("Freelance Projects")

for i, project in enumerate(projects):
    text = f"{project['description']} (Budget: {project['budget']})"
    link = tk.Label(root, text=text, fg="blue", cursor="hand2", wraplength=500, justify="left")
    link.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    link.bind("<Button-1>", lambda e, url=project['url']: open_url(url))

root.mainloop()

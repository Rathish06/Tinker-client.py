import tkinter as tk
import requests

def send_query():
    query = query_entry.get()
    if query:
        response = requests.post("http://127.0.0.1:5000/query", json={"query": query})
        if response.status_code == 200:
            result = response.json().get("response", "No response received")
            output_label.config(text=result)
        else:
            output_label.config(text="Error communicating with the web service.")
    else:
        output_label.config(text="Please enter a query.")

# Create Tkinter GUI
root = tk.Tk()
root.title("Assistant Client")

tk.Label(root, text="Enter your query:").pack(pady=10)
query_entry = tk.Entry(root, width=50)
query_entry.pack(pady=5)
tk.Button(root, text="Send", command=send_query).pack(pady=10)
output_label = tk.Label(root, text="", wraplength=400, justify="left")
output_label.pack(pady=10)

root.mainloop()

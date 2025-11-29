import json #JavaScript Object Notation 
import difflib #Differeance Library 
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# Load FAQs File
with open("faqs.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

# Save updated FAQ
def save_faqs():
    with open("faqs.json", "w", encoding="utf-8") as f:
        json.dump(faqs, f, indent=4)

# Chatbot Logic (SAFE matching)
def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # 1) EXACT MATCH ONLY (safe)
    if user_input in faqs:
        return faqs[user_input]

    # 2) FUZZY MATCH (ONLY if input has 2+ words)
    questions = list(faqs.keys())
    if len(user_input.split()) >= 2:  
        match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.50)
        if match:
            return faqs[match[0]]

    # 3) LEARNING MODE
    response = simpledialog.askstring(
        "Learning Mode",
        f"I don't know the answer to:\n'{user_input}'\nPlease enter the correct answer:")

    if response:
        faqs[user_input] = response
        save_faqs()
        return "Got it! I'll remember that for next time."
    else:
        return "Okay, I’ll skip learning this one."

# SEND MESSAGE (GUI)
def send_message():
    user_msg = entry.get().strip()
    if not user_msg:
        return

    chatbox.insert(tk.END, "You: " + user_msg + "\n", "user")
    entry.delete(0, tk.END)

    bot_reply = chatbot_response(user_msg)
    chatbox.insert(tk.END, "Bot: " + bot_reply + "\n\n", "bot")
    chatbox.see(tk.END)

# GUI WINDOW
window = tk.Tk()
window.title("FAQ Chatbot (Safe Matching Version)")
window.geometry("530x500")
window.resizable(False, False)

# Chat Display
chatbox = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 11))
chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chatbox.tag_config("user", foreground="blue")
chatbox.tag_config("bot", foreground="green")

# Input Box
entry = tk.Entry(window, font=("Arial", 12))
entry.pack(padx=10, pady=5, fill=tk.X)
entry.focus()

# Send Button
tk.Button(window, text="Send", font=("Arial", 12), command=send_message).pack(pady=5)

# Intro Message
chatbox.insert(tk.END,"🤖 Welcome to your Safe & Smart FAQ Chatbot!\nType your question below.\n\n","bot")

# Run GUI
window.mainloop()

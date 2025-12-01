import json  #JavaScript Object Notation 
import difflib #Differeance Library 
import tkinter as tk #GUI toolkit
from tkinter import scrolledtext, simpledialog #text widget with scroll bar used for chat display | used to display the dialoge box when the bot doesnt know the answer

# Open faqs file 
with open("faqs.json", "r", encoding="utf-8") as f:
    faqs = json.load(f) #reads and converts the file into a python object (list/dictionaries)

# Save updated faqs (Learning Mode)
def save_faqs():
    with open("faqs.json", "w", encoding="utf-8") as f:
        json.dump(faqs, f, indent=4) #storing the python object into a json file (does opposite of json.load)

# chatbot logic (fuzzy matching + learning mode)
def chatbot_response(user_input):
    user_input = user_input.lower().strip() #converts the user input to all lowercase and removes whitespace

    # exact & partial keyword match
    for question, answer in faqs.items(): 
        q_words = question.lower().split() #creates a list of the string questions in the json file
        if all(word in user_input for word in q_words): #checks weather the user input is in the json file as a question
            return answer

    # fuzzy match for short questions to avoid wrong matches
    questions = list(faqs.keys()) #makes a list of all the questions from the json file
    if len(user_input.split()) >= 2:
        match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.70) #finds the strings (n amt) that are similar the entered string(based on a score bw 0 and 1)
        if match:
            return faqs[match[0]] #return the first match found from the list

    # learning mode: to learn the ans form user when doesnt know ans already
    response = simpledialog.askstring("Learning Mode", f"I don't know the answer to:\n'{user_input}'\nPlease enter the correct answer:")

    if response:
        faqs[user_input] = response
        save_faqs() #saves the response to the faqs json file
        return "Got it! I'll remember that for next time."
    else:
        return "Okay, I’ll skip learning this one."

# GUI - Tkinter Interface
#comes here first after hitting send button
def send_message():
    user_msg = entry.get().strip() 
    if not user_msg:
        return

    chatbox.insert(tk.END, "You: " + user_msg + "\n", "user") #adds the message to the bottom of the chatbox, default is top
    entry.delete(0, tk.END) #clears the entry field from start to ending

    bot_reply = chatbot_response(user_msg) 
    chatbox.insert(tk.END, "Bot: " + bot_reply + "\n\n", "bot") #will apply the config for " " for the entire line
    chatbox.see(tk.END) #scrolls the chatbox viewport so the end of the text can b seen 

# Build GUI
window = tk.Tk()
window.title("FAQ Chatbot - Advanced Version")
window.geometry("530x500")
window.resizable(False, False) 

# Chat Display
chatbox = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 11)) #textbox with scrollbacr is created 
chatbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True) #places the widget in the window in the next available space
chatbox.tag_config("user", foreground="blue") #makes the text appears in specific color
chatbox.tag_config("bot", foreground="green") 

# Input Field
entry = tk.Entry(window, font=("Arial", 12))
entry.pack(pady=5, padx=10, fill=tk.X) #leaves that amt of pixels worth of space | to expand the entry box in the x direction
entry.focus() #puts the cursor at the entry box on opening 

# Send Button
tk.Button(window, text="Send", font=("Arial", 12), command=send_message).pack(pady=5)

# Intro message
chatbox.insert(tk.END, "🤖 Welcome to the Advanced FAQ Chatbot!\nType your question below.\n\n", "bot")

# Run GUI loop
window.mainloop()

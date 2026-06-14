import tkinter as tk
from tkinter import scrolledtext
import re
import random

BOT_NAME = "DecodeBot"

exact_intents = {
    "hello": "greeting",
    "hi": "greeting",
    "hey": "greeting",
    "good morning": "greeting",
    "good evening": "greeting",
    "bye": "farewell",
    "goodbye": "farewell",
    "see you": "farewell",
    "thanks": "thanks",
    "thank you": "thanks",
    "help": "help",
    "menu": "help",
    "what is your name": "name",
    "who are you": "name",
    "how are you": "status"
}

keyword_rules = {
    "greeting": ["hello", "hi", "hey", "greetings"],
    "farewell": ["bye", "goodbye", "later"],
    "thanks": ["thanks", "thank"],
    "name": ["name", "who are you"],
    "status": ["how are you", "fine", "doing"],
    "help": ["help", "support", "menu", "options"],
    "college_fees": ["fees", "fee", "payment", "cost"],
    "college_admission": ["admission", "apply", "enroll", "registration"],
    "college_hostel": ["hostel", "room", "mess", "accommodation"],
    "college_exam": ["exam", "test", "schedule", "paper"],
    "college_contact": ["contact", "phone", "email", "office"]
}

responses = {
    "greeting": [
        f"Hello! I am {BOT_NAME}. How can I help you today?",
        f"Hi there! {BOT_NAME} is ready to assist you."
    ],
    "farewell": [
        "Goodbye! Have a great day!",
        "Bye! See you soon."
    ],
    "thanks": [
        "You're welcome!",
        "Glad I could help."
    ],
    "help": [
        "You can ask about fees, admission, hostel, exam, contact, or ask my name."
    ],
    "name": [
        f"My name is {BOT_NAME}.",
        f"I am {BOT_NAME}, a rule-based AI chatbot."
    ],
    "status": [
        "I am functioning perfectly and ready to assist you."
    ],
    "college_fees": [
        "For fee details, please contact the college office or official website."
    ],
    "college_admission": [
        "Admissions usually require registration and document submission."
    ],
    "college_hostel": [
        "For hostel details, contact the hostel administration office."
    ],
    "college_exam": [
        "Please check your department notice board or exam cell for schedules."
    ],
    "college_contact": [
        "Refer to the official contact section for phone, email, or office details."
    ],
    "fallback": [
        "I do not understand that yet. Please try another phrase."
    ]
}

def sanitize(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def exact_match_intent(clean_input):
    return exact_intents.get(clean_input)

def keyword_match_intent(clean_input):
    words = clean_input.split()
    for intent, keywords in keyword_rules.items():
        for keyword in keywords:
            if keyword in clean_input or keyword in words:
                return intent
    return None

def detect_special_cases(clean_input):
    if "your name" in clean_input or "who are you" in clean_input:
        return "name"
    if "how are you" in clean_input:
        return "status"
    if "thank" in clean_input:
        return "thanks"
    return None

def get_response(user_input):
    clean_input = sanitize(user_input)

    if clean_input in ["exit", "quit", "stop"]:
        return "Goodbye! Session terminated successfully.", True

    if clean_input == "":
        return "Please type something so I can process it.", False

    intent = exact_match_intent(clean_input)

    if not intent:
        intent = detect_special_cases(clean_input)

    if not intent:
        intent = keyword_match_intent(clean_input)

    if intent and intent in responses:
        return random.choice(responses[intent]), False

    return random.choice(responses["fallback"]), False

def send_message(event=None):
    user_input = entry_box.get()
    if not user_input.strip():
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "You: " + user_input + "\n", "user")
    entry_box.delete(0, tk.END)

    bot_reply, should_exit = get_response(user_input)
    chat_area.insert(tk.END, BOT_NAME + ": " + bot_reply + "\n\n", "bot")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

    if should_exit:
        root.after(1000, root.destroy)

root = tk.Tk()
root.title("DecodeBot - Rule Based Chatbot")
root.geometry("600x500")
root.configure(bg="#1e1e2f")

title_label = tk.Label(
    root,
    text="DecodeBot Chatbot",
    font=("Arial", 18, "bold"),
    bg="#1e1e2f",
    fg="white"
)
title_label.pack(pady=10)

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 12),
    bg="#2b2b3c",
    fg="white",
    state=tk.DISABLED
)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_area.tag_config("user", foreground="#00ffcc")
chat_area.tag_config("bot", foreground="#ffd166")

input_frame = tk.Frame(root, bg="#1e1e2f")
input_frame.pack(fill=tk.X, padx=10, pady=10)

entry_box = tk.Entry(
    input_frame,
    font=("Arial", 12),
    bg="white",
    fg="black"
)
entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry_box.bind("<Return>", send_message)

send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    command=send_message
)
send_button.pack(side=tk.RIGHT)

chat_area.config(state=tk.NORMAL)
chat_area.insert(tk.END, f"{BOT_NAME}: Hello! Type 'help' to begin or 'exit' to close.\n\n", "bot")
chat_area.config(state=tk.DISABLED)

root.mainloop()
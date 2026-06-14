import tkinter as tk
from tkinter import ttk
import re
import random
from datetime import datetime

BOT_NAME = "DecodeBot"
TAGLINE = "DecodeLabs | Global Internship & Project Learning"

responses = {
    "about": [
        "DecodeLabs is a global internship platform focused on hands-on project learning, mentor guidance, and career-ready outcomes.",
        "DecodeLabs helps learners build practical skills through guided projects and structured internship-style learning."
    ],
    "internship": [
        "DecodeLabs offers internship programs with real projects, mentorship, and flexible learning.",
        "Its internship model is designed for practical experience and portfolio building."
    ],
    "training": [
        "DecodeLabs training is project-based and mentor-led.",
        "Training is structured to help learners gain practical, job-oriented skills."
    ],
    "mentor": [
        "DecodeLabs emphasizes mentor guidance, support, and feedback during learning.",
        "Mentors help learners stay on track with projects and outcomes."
    ],
    "project": [
        "The platform focuses on real projects and portfolio-ready work.",
        "Projects are a central part of the learning experience."
    ],
    "learners": [
        "DecodeLabs highlights a large learner community with practical, guided learning.",
        "The platform supports learners from beginner to project-ready stages."
    ],
    "contact": [
        "Please use the official DecodeLabs website contact or support channel for direct communication."
    ],
    "privacy": [
        "The website includes privacy-related policies for user data, retention, and security."
    ],
    "greeting": [
        f"Hello! I am {BOT_NAME}. Welcome to DecodeLabs.",
        f"Hi there! {BOT_NAME} is ready to help you."
    ],
    "farewell": [
        "Goodbye! Have a great day.",
        "Bye! Thanks for chatting."
    ],
    "thanks": [
        "You're welcome!",
        "Glad I could help."
    ],
    "help": [
        "Ask me about internships, training, mentors, projects, learners, contact, privacy, or DecodeLabs itself."
    ],
    "name": [
        f"My name is {BOT_NAME}.",
        f"I am {BOT_NAME}, a rule-based chatbot for DecodeLabs."
    ],
    "status": [
        "I am functioning perfectly and ready to assist you."
    ],
    "fallback": [
        "I do not understand that yet. Please try another phrase.",
        "Sorry, I could not match that to my current rule base."
    ]
}

def sanitize(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def detect_intent(clean):
    if clean in ["exit", "quit", "close"]:
        return "farewell"
    if clean in ["hello", "hi", "hey", "good morning", "good evening"]:
        return "greeting"
    if clean in ["thanks", "thank you"]:
        return "thanks"
    if clean in ["help", "menu"]:
        return "help"
    if clean in ["what is your name", "who are you"]:
        return "name"
    if clean in ["how are you"]:
        return "status"
    if "internship" in clean or "internships" in clean or "apply for internship" in clean:
        return "internship"
    if "training" in clean or "course" in clean or "classes" in clean or "program" in clean:
        return "training"
    if "mentor" in clean or "mentorship" in clean or "guidance" in clean:
        return "mentor"
    if "project" in clean or "projects" in clean or "portfolio" in clean:
        return "project"
    if "learners" in clean or "students" in clean or "community" in clean or "outcomes" in clean:
        return "learners"
    if "contact" in clean or "email" in clean or "phone" in clean or "reach" in clean:
        return "contact"
    if "privacy" in clean or "policy" in clean or "data" in clean or "security" in clean:
        return "privacy"
    if "about" in clean or "decodelabs" in clean or "decode labs" in clean:
        return "about"
    return None

def get_reply(user_text):
    clean = sanitize(user_text)
    if clean == "":
        return "Please type something so I can process it.", False
    intent = detect_intent(clean)
    if intent in responses:
        return random.choice(responses[intent]), intent == "farewell"
    return random.choice(responses["fallback"]), False

class BubbleChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DecodeBot | DecodeLabs")
        self.root.geometry("1080x760")
        self.root.minsize(960, 680)
        self.colors = {
            "bg": "#07111f",
            "panel": "#0f172a",
            "header": "#101827",
            "bubble_user": "#2563eb",
            "bubble_bot": "#1f2937",
            "text": "#e5e7eb",
            "muted": "#94a3b8",
            "accent": "#22c55e",
            "accent2": "#38bdf8",
            "border": "#223046"
        }
        self.root.configure(bg=self.colors["bg"])
        self.build_ui()
        self.add_bot_message("Welcome to DecodeBot. Ask me about internships, training, mentorship, projects, learners, contact, or privacy.")
        self.entry.focus_set()

    def build_ui(self):
        header = tk.Frame(self.root, bg=self.colors["header"], height=92)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=self.colors["header"])
        left.pack(side="left", padx=20, pady=16)
        tk.Label(left, text="DecodeBot", bg=self.colors["header"], fg=self.colors["text"], font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(left, text=TAGLINE, bg=self.colors["header"], fg=self.colors["muted"], font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 0))

        right = tk.Frame(header, bg=self.colors["header"])
        right.pack(side="right", padx=20, pady=16)
        self.clock = tk.Label(right, text=self.time_text(), bg=self.colors["header"], fg=self.colors["accent"], font=("Segoe UI", 10, "bold"))
        self.clock.pack(anchor="e")
        self.status = tk.Label(right, text="Online • Rule-based mode", bg=self.colors["header"], fg=self.colors["accent2"], font=("Segoe UI", 10))
        self.status.pack(anchor="e", pady=(4, 0))
        self.root.after(1000, self.update_clock)

        outer = tk.Frame(self.root, bg=self.colors["bg"])
        outer.pack(fill="both", expand=True, padx=14, pady=14)

        main = tk.Frame(outer, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1)
        main.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main, bg=self.colors["panel"], highlightthickness=0, bd=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(main, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.chat_frame = tk.Frame(self.canvas, bg=self.colors["panel"])
        self.chat_window = self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.chat_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.resize_canvas)

        input_bar = tk.Frame(self.root, bg=self.colors["bg"])
        input_bar.pack(fill="x", padx=14, pady=(0, 14))

        self.entry = tk.Entry(
            input_bar, font=("Segoe UI", 12), bg="#0f172a", fg="white",
            insertbackground="white", relief="flat", highlightthickness=1,
            highlightbackground=self.colors["border"], highlightcolor=self.colors["accent2"]
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 12))
        self.entry.bind("<Return>", self.send_message)

        clear_btn = tk.Button(
            input_bar, text="Clear Chat", bg="#ef4444", fg="white",
            font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=10,
            command=self.clear_chat
        )
        clear_btn.pack(side="right", padx=(0, 10))

        send_btn = tk.Button(
            input_bar, text="Send", bg=self.colors["accent2"], fg="white",
            font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=10,
            command=self.send_message
        )
        send_btn.pack(side="right")

    def resize_canvas(self, event):
        self.canvas.itemconfig(self.chat_window, width=event.width)

    def time_text(self):
        return datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")

    def update_clock(self):
        self.clock.config(text=self.time_text())
        self.root.after(1000, self.update_clock)

    def add_bubble(self, speaker, text, side):
        row = tk.Frame(self.chat_frame, bg=self.colors["panel"])
        row.pack(fill="x", pady=8, padx=10)

        if side == "right":
            row.columnconfigure(0, weight=1)
            container = tk.Frame(row, bg=self.colors["panel"])
            container.grid(row=0, column=1, sticky="e")
        else:
            container = tk.Frame(row, bg=self.colors["panel"])
            container.grid(row=0, column=0, sticky="w")

        tk.Label(container, text=speaker, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=8, pady=(0, 3))
        bubble_color = self.colors["bubble_user"] if side == "right" else self.colors["bubble_bot"]
        bubble = tk.Frame(container, bg=bubble_color, highlightthickness=1, highlightbackground=self.colors["border"])
        bubble.pack(anchor="e" if side == "right" else "w")
        label = tk.Label(bubble, text=text, bg=bubble_color, fg="white", font=("Segoe UI", 11), wraplength=560, justify="left", padx=14, pady=10)
        label.pack()
        self.canvas.after(20, lambda: self.canvas.yview_moveto(1.0))

    def add_user_message(self, text):
        self.add_bubble("You", text, "right")

    def add_bot_message(self, text):
        self.type_text("DecodeBot", text)

    def type_text(self, speaker, text):
        row = tk.Frame(self.chat_frame, bg=self.colors["panel"])
        row.pack(fill="x", pady=8, padx=10)
        container = tk.Frame(row, bg=self.colors["panel"])
        container.pack(anchor="w")
        tk.Label(container, text=speaker, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=8, pady=(0, 3))
        bubble_color = self.colors["bubble_bot"]
        bubble = tk.Frame(container, bg=bubble_color, highlightthickness=1, highlightbackground=self.colors["border"])
        bubble.pack(anchor="w")
        label = tk.Label(bubble, text="", bg=bubble_color, fg="white", font=("Segoe UI", 11), wraplength=560, justify="left", padx=14, pady=10)
        label.pack()

        def animate(i=0):
            if i <= len(text):
                label.config(text=text[:i])
                self.canvas.yview_moveto(1.0)
                self.root.after(14, lambda: animate(i + 1))

        animate()

    def send_message(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.add_user_message(text)
        self.entry.delete(0, tk.END)
        reply, should_close = get_reply(text)
        self.root.after(200, lambda: self.add_bot_message(reply))
        if should_close:
            self.root.after(1500, self.root.destroy)

    def clear_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.add_bot_message("Chat cleared. Ask me again about internships, training, mentorship, projects, learners, contact, or privacy.")

root = tk.Tk()
app = BubbleChatApp(root)
root.mainloop()

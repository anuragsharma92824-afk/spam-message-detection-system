import tkinter as tk
from tkinter import messagebox
import re
import pyttsx3

from dataset import load_dataset
from model import SpamModel
from history import save_history, load_history, clear_history
from graph import (
    show_dataset_graph,
    show_confusion_matrix,
    show_user_detection_graph
)
from dashboard import create_dashboard
from phishing import check_phishing
from url_checker import  extract_url, check_url_online 
from dotenv import load_dotenv 
import os

# load environment variables 

load_dotenv( )
VIRUSTOTAL_API_KEY=os.getenv("VIRUSTOTAL_API_KEY"," ")


# ==================================================
# COLORS
# ==================================================

BG = "#eef4ff"
CARD = "#ffffff"
NAVY = "#102a56"
BLUE = "#1769ff"
BLUE_DARK = "#0d47c9"
LIGHT_BLUE = "#e8f0ff"
TEXT = "#17233c"
MUTED = "#667085"
GREEN = "#16803c"
RED = "#d92d20"
BORDER = "#d7e2f5"



# ==================================================
# INITIAL SETUP
# ==================================================

df = load_dataset()

spam_total = int((df["label"] == 1).sum())
ham_total = int((df["label"] == 0).sum())
total_messages = len(df)

spam_model = SpamModel()
metrics = spam_model.get_metrics()

session_spam = 0
session_ham = 0

voice_enabled = True

engine = pyttsx3.init()


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()

root.title("Spam Message Detection System")
root.geometry("1100x700")
root.minsize(900, 600)
root.configure(bg=BG)


# ==================================================
# FUNCTIONS
# ==================================================

def speak(text):
    if voice_enabled:
        engine.say(text)
        engine.runAndWait()


def validate_email(email):

    if email == "":
        return True

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


def clear_message():

    sender_entry.delete(0, tk.END)
    message_box.delete("1.0", tk.END)

    result_label.config(
        text="Result will appear here",
        fg=MUTED,
        bg=LIGHT_BLUE
    )

    phishing_label.config(
        text="Phishing result will appear here",
        fg=MUTED,
        bg=LIGHT_BLUE
    )


def check_message():

    global session_spam, session_ham

    sender = sender_entry.get().strip()
    message = message_box.get("1.0", tk.END).strip()

    # Empty message check
    if not message:

        messagebox.showwarning(
            "Warning",
            "Please enter a message."
        )

        return

    # Email validation
    if sender and "@" not in sender:

        messagebox.showwarning(
            "Warning",
            "Please enter a valid sender email."
        )

        return

    # ==========================================================
    # SPAM DETECTION
    # ==========================================================

    result = spam_model.predict(message)

    # ==========================================================
    # PHISHING DETECTION
    # ==========================================================

    phishing_status, phishing_reasons = check_phishing(message)

    # ==========================================================
    # ONLINE URL VERIFICATION
    # ==========================================================

    url = extract_url(message)

    if url:

        url_status, url_details = check_url_online(
            url,
            VIRUSTOTAL_API_KEY
        )

    else:

        url_status = "No URL Found"
        url_details = "Message me koi URL nahi mila."

    # ==========================================================
    # DISPLAY ONLINE URL VERIFICATION RESULT
    # ==========================================================

    if url_status == "Malicious":

        url_color = RED

    elif url_status == "Suspicious":

        url_color = "#D97706"

    elif url_status == "Safe":

        url_color = GREEN

    else:

        url_color = MUTED

    url_label.config(
        text=f"ONLINE URL VERIFICATION\n\n{url_details}",
        fg=url_color,
        bg=LIGHT_BLUE
    )

    # ==========================================================
    # SPAM RESULT
    # ==========================================================

    if result == "Spam":

        session_spam += 1

        result_label.config(
            text="⚠️  SPAM MESSAGE",
            fg=RED,
            bg="#fff1f0"
        )

        speak(
            "Warning. This message is spam."
        )

    else:

        session_ham += 1

        result_label.config(
            text="✓  HAM MESSAGE",
            fg=GREEN,
            bg="#ecfdf3"
        )

        speak(
            "This message is not spam."
        )

    # ==========================================================
    # PHISHING DETECTION RESULT
    # ==========================================================

    if phishing_status == "Possible Phishing":

        phishing_text = "⚠️  POSSIBLE PHISHING\n\n"

        for reason in phishing_reasons:

            phishing_text += "• " + reason + "\n"

        phishing_label.config(
            text=phishing_text,
            fg=RED,
            bg="#fff1f0"
        )

    else:

        phishing_label.config(
            text="✓  NO SUSPICIOUS PHISHING PATTERN DETECTED",
            fg=GREEN,
            bg="#ecfdf3"
        )

    # ==========================================================
    # SAVE HISTORY
    # ==========================================================

    save_history(
        message,
        result,
        sender,
        phishing_status,
        phishing_reasons,
        url,
        url_status,
        url_details
    )


# ==================================================
# HOME
# ==================================================

def show_home():

    clear_pages()

    home_frame = tk.Frame(
        content_frame,
        bg=BG
    )

    home_frame.pack(
        fill="both",
        expand=True
    )

    title = tk.Label(
        home_frame,
        text="Spam Message Detection",
        font=("Arial", 28, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=(25, 5)
    )

    subtitle = tk.Label(
        home_frame,
        text="Machine Learning Based Spam Detection System",
        font=("Arial", 13),
        bg=BG,
        fg=MUTED
    )

    subtitle.pack(
        pady=(0, 20)
    )

    # ==================================================
    # SCROLLABLE MAIN CARD
    # ==================================================

    scroll_container = tk.Frame(
        home_frame,
        bg=BG
    )

    scroll_container.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    # Canvas

    canvas = tk.Canvas(
        scroll_container,
        bg=BG,
        highlightthickness=0,
        borderwidth=0
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    # Scrollbar

    scrollbar = tk.Scrollbar(
        scroll_container,
        orient="vertical",
        command=canvas.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    # ==================================================
    # INPUT FRAME
    # ==================================================

    input_frame = tk.Frame(
        canvas,
        bg=CARD,
        padx=28,
        pady=22,
        relief="solid",
        borderwidth=1,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=input_frame,
        anchor="nw"
    )

    # ==================================================
    # SCROLL REGION UPDATE
    # ==================================================

    def update_scroll_region(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

        canvas.itemconfig(
            canvas_window,
            width=canvas.winfo_width()
        )

    input_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        update_scroll_region
    )

    # ==================================================
    # SENDER
    # ==================================================

    sender_label = tk.Label(
        input_frame,
        text="Sender Email",
        font=("Arial", 12, "bold"),
        bg=CARD,
        fg=TEXT
    )

    sender_label.pack(
        anchor="w"
    )

    global sender_entry

    sender_entry = tk.Entry(
        input_frame,
        font=("Arial", 12),
        bg="#f8faff",
        fg=TEXT,
        relief="solid",
        borderwidth=1
    )

    sender_entry.pack(
        fill="x",
        pady=(7, 18),
        ipady=8
    )

    # ==================================================
    # MESSAGE
    # ==================================================

    message_label = tk.Label(
        input_frame,
        text="Enter Message",
        font=("Arial", 12, "bold"),
        bg=CARD,
        fg=TEXT
    )

    message_label.pack(
        anchor="w"
    )

    global message_box

    message_box = tk.Text(
        input_frame,
        height=7,
        font=("Arial", 12),
        wrap="word",
        bg="#f8faff",
        fg=TEXT,
        relief="solid",
        borderwidth=1
    )

    message_box.pack(
        fill="x",
        pady=(7, 10)
    )

    # ==================================================
    # BUTTONS
    # ==================================================

    button_frame = tk.Frame(
        input_frame,
        bg=CARD
    )

    button_frame.pack(
        pady=15
    )

    check_button = tk.Button(
        button_frame,
        text="🔍  Check Message",
        command=check_message,
        font=("Arial", 11, "bold"),
        bg=BLUE,
        fg="white",
        activebackground=BLUE_DARK,
        activeforeground="white",
        relief="flat",
        padx=22,
        pady=10,
        cursor="hand2"
    )

    check_button.pack(
        side="left",
        padx=7
    )

    clear_button = tk.Button(
        button_frame,
        text="🧹 Clear",
        command=clear_message,
        font=("Arial", 11, "bold"),
        bg="#e53935",
        fg="white",
        activebackground="#b71c1c",
        activeforeground="white",
        relief="flat",
        padx=24,
        pady=10,
        cursor="hand2"
    )

    clear_button.pack(
        side="left",
        padx=7
    )

    # ==================================================
    # RESULT
    # ==================================================

    global result_label

    result_label = tk.Label(
        input_frame,
        text="Result will appear here",
        font=("Arial", 17, "bold"),
        bg=LIGHT_BLUE,
        fg=MUTED,
        padx=20,
        pady=15
    )

    result_label.pack(
        fill="x",
        pady=(10, 0)
    )

    # ==================================================
    # PHISHING RESULT
    # ==================================================

    global phishing_label, url_label

    phishing_label = tk.Label(
        input_frame,
        text="Phishing result will appear here",
        font=("Arial", 15, "bold"),
        bg=LIGHT_BLUE,
        fg=MUTED,
        padx=20,
        pady=15,
        justify="left",
        anchor="w"
    )

    phishing_label.pack(
        fill="x",
        pady=(12, 0)
    )

    # ==================================================
    # ONLINE URL VERIFICATION
    # ==================================================

    url_label = tk.Label(
        input_frame,
        text="Online URL verification result will appear here",
        font=("Arial", 13, "bold"),
        bg=LIGHT_BLUE,
        fg=MUTED,
        padx=20,
        pady=15,
        justify="left",
        anchor="w"
    )

    url_label.pack(
        fill="x",
        pady=(5, 12)
    )


# ==================================================
# DASHBOARD
# ==================================================

def show_dashboard_page():

    clear_pages()

    page = tk.Frame(
        content_frame,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    create_dashboard(
        page,
        metrics,
        total_messages,
        spam_total,
        ham_total
    )


# ==================================================
# GRAPHS
# ==================================================

def show_graph_page():

    clear_pages()

    page = tk.Frame(
        content_frame,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    title = tk.Label(
        page,
        text="Graphs & Visualization",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=28
    )

    dataset_button = tk.Button(
        page,
        text="📊  Dataset Distribution",
        command=lambda: show_dataset_graph(
            ham_total,
            spam_total
        ),
        font=("Arial", 12, "bold"),
        bg=BLUE,
        fg="white",
        activebackground=BLUE_DARK,
        activeforeground="white",
        relief="flat",
        padx=30,
        pady=11,
        cursor="hand2"
    )

    dataset_button.pack(
        pady=8
    )

    confusion_button = tk.Button(
        page,
        text="🔲  Confusion Matrix",
        command=lambda: show_confusion_matrix(
            metrics["confusion_matrix"]
        ),
        font=("Arial", 12, "bold"),
        bg=NAVY,
        fg="white",
        activebackground="#1c3e73",
        activeforeground="white",
        relief="flat",
        padx=30,
        pady=11,
        cursor="hand2"
    )

    confusion_button.pack(
        pady=8
    )

    user_button = tk.Button(
        page,
        text="📈  Current Session Detection",
        command=lambda: show_user_detection_graph(
            session_spam,
            session_ham
        ),
        font=("Arial", 12, "bold"),
        bg="#475467",
        fg="white",
        activebackground="#344054",
        activeforeground="white",
        relief="flat",
        padx=30,
        pady=11,
        cursor="hand2"
    )

    user_button.pack(
        pady=8
    )


# ==================================================
# HISTORY
# ==================================================

def show_history_page():

    clear_pages()

    page = tk.Frame(
        content_frame,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    title = tk.Label(
        page,
        text="Message History",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=18
    )

    history_data = load_history()

    # Text + scrollbar container

    history_frame = tk.Frame(
        page,
        bg=BG
    )

    history_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=5
    )

    scrollbar = tk.Scrollbar(
        history_frame,
        orient="vertical"
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    text_area = tk.Text(
        history_frame,
        font=("Arial", 11),
        wrap="word",
        bg=CARD,
        fg=TEXT,
        relief="solid",
        borderwidth=1,
        yscrollcommand=scrollbar.set
    )

    text_area.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=text_area.yview
    )

    if history_data.empty:

        text_area.insert(
            tk.END,
            "No message history available."
        )

    else:

        for _, row in history_data.iterrows():

            text_area.insert(
                tk.END,
                f"Date: {row.get('date_time', '')}\n"
            )

            text_area.insert(
                tk.END,
                f"Sender: {row.get('sender', '')}\n"
            )

            text_area.insert(
                tk.END,
                f"Message: {row.get('message', '')}\n"
            )

            text_area.insert(
                tk.END,
                f"Result: {row.get('result', '')}\n"
            )

            phishing_status = str(
                row.get("phishing_status", "")
            ).strip()

            if phishing_status and phishing_status != "nan":

                text_area.insert(
                    tk.END,
                    f"Phishing: {phishing_status}\n"
                )

            phishing_reasons = str(
                row.get("phishing_reasons", "")
            ).strip()

            if phishing_reasons and phishing_reasons != "nan":

                text_area.insert(
                    tk.END,
                    "Phishing Reasons:\n"
                )

                reasons = phishing_reasons.split(";")

                for reason in reasons:

                    reason = reason.strip()

                    if reason:

                        text_area.insert(
                            tk.END,
                            f"  • {reason}\n"
                        )
# url verification history
            url_value = str(
                row.get("url","")
            ).strip()

            url_status = str(
                row.get("url_status","")
            ).strip()

            url_detsils = str(
                 row.get("url_details","")
            ).strip()

            if url_value and url_value !="nan":

             text_area.insert(
                tk.END,
                f"URL:{url_value}\n"
            )
            text_area.insert(
                            tk.END,
                            f"URL Status:{url_status}\n"
                        )
            if url_detsils and url_detsils !="nan":

                text_area.insert(
                                            tk.END,
                                            f"URL Details:{url_detsils}\n"
                                        )
            

            text_area.insert(
                tk.END,
                "\n------------------------------\n\n"
            )

    delete_button = tk.Button(
        page,
        text="🗑️  Clear History",
        command=delete_history,
        font=("Arial", 11, "bold"),
        bg="#c62828",
        fg="white",
        activebackground="#8e0000",
        activeforeground="white",
        relief="flat",
        padx=30,
        pady=11,
        cursor="hand2"
    )

    delete_button.pack(
        pady=10
    )


def delete_history():

    answer = messagebox.askyesno(
        "Clear History",
        "Are you sure you want to delete all history?"
    )

    if answer:

        clear_history()

        messagebox.showinfo(
            "History",
            "History cleared successfully."
        )

        show_history_page()
 
# ==================================================
# SETTINGS
# ==================================================

def show_settings_page():

    clear_pages()

    page = tk.Frame(
        content_frame,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    title = tk.Label(
        page,
        text="Settings",
        font=("Arial", 26, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=(25, 15)
    )

    # Voice card

    voice_card = tk.Frame(
        page,
        bg=CARD,
        padx=25,
        pady=20,
        relief="solid",
        borderwidth=1,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    voice_card.pack(
        padx=70,
        fill="x"
    )

    voice_title = tk.Label(
        voice_card,
        text="🔊 Voice Output",
        font=("Arial", 15, "bold"),
        bg=CARD,
        fg=TEXT
    )

    voice_title.pack(
        anchor="w"
    )

    voice_description = tk.Label(
        voice_card,
        text="Enable or disable voice feedback after message detection.",
        font=("Arial", 10),
        bg=CARD,
        fg=MUTED
    )

    voice_description.pack(
        anchor="w",
        pady=(3, 15)
    )

    global voice_enabled

    voice_var = tk.BooleanVar(
        value=voice_enabled
    )

    # Large ON/OFF button

    def change_voice():

        global voice_enabled

        voice_enabled = voice_var.get()

        if voice_enabled:

            voice_button.config(
                text="  ●  ON  ",
                bg=GREEN,
                activebackground="#126b32"
            )

            voice_status.config(
                text="Voice output is ON",
                fg=GREEN
            )

        else:

            voice_button.config(
                text="  ●  OFF  ",
                bg="#667085",
                activebackground="#475467"
            )

            voice_status.config(
                text="Voice output is OFF",
                fg=MUTED
            )

    voice_button = tk.Button(
        voice_card,
        text="  ●  ON  ",
        command=lambda: (
            voice_var.set(not voice_var.get()),
            change_voice()
        ),
        font=("Arial", 13, "bold"),
        bg=GREEN,
        fg="white",
        activebackground="#126b32",
        activeforeground="white",
        relief="flat",
        padx=30,
        pady=10,
        cursor="hand2"
    )

    voice_button.pack(
        side="left",
        padx=(0, 15)
    )

    voice_status = tk.Label(
        voice_card,
        text="Voice output is ON",
        font=("Arial", 11, "bold"),
        bg=CARD,
        fg=GREEN
    )

    voice_status.pack(
        side="left"
    )


    # System information

    info_title = tk.Label(
        page,
        text="System Information",
        font=("Arial", 17, "bold"),
        bg=BG,
        fg=NAVY
    )

    info_title.pack(
        anchor="w",
        padx=70,
        pady=(25, 10)
    )

    info_card = tk.Frame(
        page,
        bg=CARD,
        padx=30,
        pady=20,
        relief="solid",
        borderwidth=1,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    info_card.pack(
        padx=70,
        fill="x"
    )

    info = tk.Label(
        info_card,
        text=(
            "Spam Message Detection System\n\n"
            "Machine Learning     : Multinomial Naive Bayes\n"
            "Feature Extraction   : CountVectorizer\n"
            "GUI                   : Tkinter\n"
            "Dataset               : SMS Spam Collection"
        ),
        font=("Arial", 11),
        bg=CARD,
        fg=TEXT,
        justify="left"
    )

    info.pack(
        anchor="w"
    )
   

# ==================================================
# CLEAR PAGES
# ==================================================

def clear_pages():

    for widget in content_frame.winfo_children():
        widget.destroy()


# ==================================================
# SIDEBAR
# ==================================================

sidebar = tk.Frame(
    root,
    bg=NAVY,
    width=220
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


app_title = tk.Label(
    sidebar,
    text="SPAM\nDETECTOR",
    font=("Arial", 20, "bold"),
    bg=NAVY,
    fg="white"
)

app_title.pack(
    pady=30
)


def create_menu_button(text, command):

    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg="#183766",
        fg="white",
        activebackground=BLUE,
        activeforeground="white",
        relief="flat",
        padx=10,
        pady=11,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        padx=15,
        pady=5
    )


create_menu_button(
    "🏠  Home",
    show_home
)

create_menu_button(
    "📊  Dashboard",
    show_dashboard_page
)

create_menu_button(
    "📈  Graphs",
    show_graph_page
)

create_menu_button(
    "📜  History",
    show_history_page
)

create_menu_button(
    "⚙️  Settings",
    show_settings_page
)


# ==================================================
# SIDEBAR FOOTER
# ==================================================

footer = tk.Label(
    sidebar,
    text="Smarter Messages\nSafer You",
    font=("Arial", 10, "bold"),
    bg=NAVY,
    fg="#a9c7ff"
)

footer.pack(
    side="bottom",
    pady=30
)


# ==================================================
# CONTENT AREA
# ==================================================

content_frame = tk.Frame(
    root,
    bg=BG
)

content_frame.pack(
    side="right",
    fill="both",
    expand=True
)


# ==================================================
# START
# ==================================================

show_home()

root.mainloop()
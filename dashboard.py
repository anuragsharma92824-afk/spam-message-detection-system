import tkinter as tk


def create_stat_card(parent, title, value, row, column, bg_color):
    """Create a simple dashboard statistic card."""

    card = tk.Frame(
        parent,
        bg=bg_color,
        width=200,
        height=120,
        relief="solid",
        borderwidth=1
    )

    card.grid(
        row=row,
        column=column,
        padx=10,
        pady=10
    )

    card.grid_propagate(False)

    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 12),
        bg=bg_color,
        fg="#555555"
    )

    title_label.pack(pady=(20, 5))

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 24, "bold"),
        bg=bg_color,
        fg="#222222"
    )

    value_label.pack()


def create_dashboard(parent, metrics, total_messages, spam_count, ham_count):
    """Create the complete dashboard."""

    for widget in parent.winfo_children():
        widget.destroy()

    title = tk.Label(
        parent,
        text="Dashboard",
        font=("Arial", 24, "bold"),
        bg="#f5f5f5",
        fg="#222222"
    )

    title.pack(
        anchor="w",
        padx=30,
        pady=(25, 10)
    )

    cards_frame = tk.Frame(
        parent,
        bg="#f5f5f5"
    )

    cards_frame.pack(
        fill="x",
        padx=20
    )

    accuracy = f"{metrics['accuracy'] * 100:.2f}%"
    precision = f"{metrics['precision'] * 100:.2f}%"
    recall = f"{metrics['recall'] * 100:.2f}%"
    f1 = f"{metrics['f1'] * 100:.2f}%"

    create_stat_card(
        cards_frame,
        "Total Messages",
        total_messages,
        0,
        0,
        "#DDEEFF"
    )

    create_stat_card(
        cards_frame,
        "Spam Messages",
        spam_count,
        0,
        1,
        "#FFE0E0"
    )

    create_stat_card(
        cards_frame,
        "Ham Messages",
        ham_count,
        0,
        2,
        "#DFF5E1"
    )

    create_stat_card(
        cards_frame,
        "Accuracy",
        accuracy,
        1,
        0,
        "#E8DFFF"
    )

    create_stat_card(
        cards_frame,
        "Precision",
        precision,
        1,
        1,
        "#FFE8CC"
    )

    create_stat_card(
        cards_frame,
        "Recall",
        recall,
        1,
        2,
        "#DDF5F5"
    )

    create_stat_card(
        cards_frame,
        "F1 Score",
        f1,
        2,
        0,
        "#FFF2CC"
    )

    info = tk.Label(
        parent,
        text="Multinomial Naive Bayes + CountVectorizer",
        font=("Arial", 13),
        bg="#f5f5f5",
        fg="#555555"
    )

    info.pack(
        anchor="w",
        padx=30,
        pady=20
    )
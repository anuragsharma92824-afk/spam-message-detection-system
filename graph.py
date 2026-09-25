import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


def show_dataset_graph(ham_count, spam_count):
    """Show ham vs spam message distribution."""

    labels = ["Ham", "Spam"]
    values = [ham_count, spam_count]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values)

    plt.title("Dataset Distribution")
    plt.xlabel("Message Type")
    plt.ylabel("Number of Messages")

    plt.tight_layout()
    plt.show()


def show_confusion_matrix(confusion):
    """Show confusion matrix."""

    display = ConfusionMatrixDisplay(
        confusion_matrix=confusion,
        display_labels=["Ham", "Spam"]
    )

    display.plot()

    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.show()


def show_user_detection_graph(spam_count, ham_count):
    """Show current session detection results."""

    labels = ["Spam", "Ham"]
    values = [spam_count, ham_count]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values)

    plt.title("Current Session Detection")
    plt.xlabel("Message Type")
    plt.ylabel("Number of Messages")

    plt.tight_layout()
    plt.show()
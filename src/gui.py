import tkinter as tk
# from src.api import RequestInfo, RequestParameters


class MainFrame:
    def __init__(self) -> None:
        self.root = tk.Tk()

        self.label = tk.Label(self.root, text="My message", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)
        self.textbox = tk.Text(self.root, font=('Aial', 16))
        self.textbox.pack(padx=10, pady=10)
        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(
            self.root, text="Show Messagebox", font=('Arial', 18),
            variable=self.check_state)
        self.check.pack(pady=10, padx=10)

        self.button = tk.Button(self.root, text="Show message", font=('Arial', 18), command=self.showMessage)
        self.root.mainloop()

    def showMessage(self):
        pass
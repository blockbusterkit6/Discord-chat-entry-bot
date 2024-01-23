import tkinter
import customtkinter
import requests

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Discord Spam Bot")
        self.geometry(f"{700}x{300}")

        # create entry widgets for "content", "authorization", and "Your_URL_Here"
        self.content_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Content", width=600, height=15)
        self.content_entry.pack(pady=10)

        self.authorization_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Authorization", width=600, height=15)
        self.authorization_entry.pack(pady=10)

        self.url_entry = customtkinter.CTkEntry(self, placeholder_text="Enter URL", width=600, height=15)
        self.url_entry.pack(pady=10)

        # create checkbox for message repetition
        self.repeat_checkbox_var = tkinter.BooleanVar()
        self.repeat_checkbox = customtkinter.CTkCheckBox(self, text="Repeat Message", variable=self.repeat_checkbox_var)
        self.repeat_checkbox.pack(pady=5)

        # create title for the time interval entry box
        self.interval_title_label = customtkinter.CTkLabel(self, text="Enter Time Interval (seconds):")
        self.interval_title_label.pack(pady=5)

        # create entry box for time interval between messages
        self.interval_entry = customtkinter.CTkEntry(self, placeholder_text="", width=20)
        self.interval_entry.pack(pady=10)

        # create button to execute the code
        self.execute_button = customtkinter.CTkButton(self, text="Spam Away", command=self.execute_code)
        self.execute_button.pack(pady=10)

        # Variable to keep track of the repeating state
        self.is_repeating = False

    def execute_code(self):
        # Get values from the entry widgets
        content = self.content_entry.get()
        authorization = self.authorization_entry.get()
        url = self.url_entry.get()
        repeat_message = self.repeat_checkbox_var.get()
        interval = self.interval_entry.get()

        # Prepare payload and headers
        payload = {
            'content': content
        }

        header = {
            'authorization': authorization
        }

        def send_request():
            try:
                # Send the POST request
                r = requests.post(url, data=payload, headers=header)
                # Print the response status code
                print("Response Status Code:", r.status_code)
            except requests.exceptions.RequestException as e:
                # Handle exceptions here if needed
                print("Error:", e)

            # If repeat_message is True, schedule the next execution
            if self.is_repeating:
                self.after(int(float(interval) * 1000), send_request)

        # Execute the code immediately
        send_request()

        # If repeat_message is True, set the repeating state and schedule the next execution
        if repeat_message:
            try:
                interval = float(interval)
                if interval > 0:
                    self.is_repeating = True
                    self.after(int(interval * 1000), send_request)
                else:
                    print("Interval must be a positive number.")
            except ValueError:
                print("Invalid interval. Please enter a valid number.")

if __name__ == "__main__":
    app = App()
    app.mainloop()

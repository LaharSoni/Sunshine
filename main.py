import tkinter as tk
from tkinter import messagebox
import openai
import pygame

pygame.mixer.init()
pygame.init()

openai.api_key = "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"

pygame.mixer.music.load('neon222.mpeg')
pygame.mixer.music.play()
class ChatboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("sunshine")
        self.root.geometry("1920x1080")

        self.name = ""
        self.partner = ""
        self.init_first_window()


    def init_first_window(self):
        self.background_image = tk.PhotoImage(file="pxfuel (2).png")
        # self.background_image.config(height=1920,width=1080)
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1,bordermode="outside")

        self.name_label = tk.Label(self.root, text=" Your Name ", font=("comic sans", 30), border=2, background="peachpuff4", foreground="black", relief="solid")
        self.name_entry = tk.Entry(self.root, borderwidth=5, font=("Comic Sans", 25), background="light cyan", foreground="midnight blue")
        self.partner_label = tk.Label(self.root, text="Chat With", font=("comic sans", 30), border=2, background="peachpuff4", foreground="black", relief="solid")
        self.partner_entry = tk.Entry(self.root, borderwidth=5, font=("Comic Sans", 25),background="light cyan",foreground="midnight blue")
        self.ok_button = tk.Button(self.root, text="OK", command=self.open_chat_window,font=("comic sans", 16), height=2, width=10,
                                   borderwidth=7,background="azure4",foreground="black")

        self.name_label.place(relx=0.3, rely=0.2, anchor="center")
        self.name_entry.place(relx=0.3, rely=0.3, anchor="center")
        self.partner_label.place(relx=0.3, rely=0.4, anchor="center")
        self.partner_entry.place(relx=0.3, rely=0.5, anchor="center")
        self.ok_button.place(relx=0.3, rely=0.6, anchor="center")


    def open_chat_window(self):
        self.name = self.name_entry.get()
        self.partner = self.partner_entry.get()

        if not self.name or not self.partner:
            messagebox.showerror("Error", "Please enter your name and the person you want to talk to.")
            return

        self.first_window_destroy()
        self.init_second_window()

    def first_window_destroy(self):
        self.name_label.destroy()
        self.name_entry.destroy()
        self.partner_label.destroy()
        self.partner_entry.destroy()
        self.ok_button.destroy()


    def init_second_window(self):
        self.second_window = tk.Toplevel(self.root)
        self.second_window.title(f"Chat with {self.partner}")
        self.second_window.geometry("1200x1200")

        self.chat_display = tk.Text(self.second_window, state=tk.DISABLED,font=("comic sans",16),background="lightblue1")
        self.user_input = tk.Entry(self.second_window, font=("comic sans", 16), borderwidth=5,background="light cyan",foreground="midnight blue")
        self.send_button = tk.Button(self.second_window, text="➤",relief="solid", font=(70), command=self.send_message,
                                     width=10, foreground="white", borderwidth=2,bg="green",border="2")


        self.chat_display.pack(padx=10, pady=10, expand=True, fill='both')
        self.user_input.pack(padx=20, pady=10, fill='both', expand=True)
        self.send_button.pack(pady=10)

        self.emojis = ["😄", "😊", "🤖", "❤", "👍", "🎉", "🙂", "😂", "😎", "🥰"]
        self.emoji_frame = tk.Frame(self.second_window)
        for emoji in self.emojis:
            emoji_button = tk.Button(self.emoji_frame, text=emoji, font=("Bold", 15),background="white",border="2",relief="sunken",
                                     command=lambda e=emoji: self.insert_emoji(e))
            emoji_button.pack(side="left", padx=5,)

        self.emoji_frame.pack(pady=10)

    def insert_emoji(self, emoji):
        self.user_input.insert(tk.END, emoji)

    def send_message(self):
        user_message = self.user_input.get()
        self.update_chat_display(f"\n{self.name}: {user_message}")
        bot_response = self.get_bot_response(user_message)
        self.update_chat_display(f"\n{self.partner}: {bot_response}")
        self.user_input.delete(0, tk.END)

    def get_bot_response(self, message: str) -> str:
        prompt = f"{self.name}: {message}\n{self.partner}: "
        try:
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=prompt,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[self.name, self.partner]
            )

            choices = response.choices[0]
            return choices.text.strip()

        except Exception as e:
            print('ERROR:', e)
            return 'Something went wrong...'

    def update_chat_display(self, message):
        message_frame = tk.Frame(self.chat_display, bd=2, relief="groove",borderwidth=2,border="2",background="white")
        message_label = tk.Label(message_frame, text=message, anchor="w", padx=5, pady=2,font=("arial",18),background="lightskyblue1",foreground="black",wraplength=1290)

        message_frame.pack(fill="x", padx=11, pady=(5,0))
        message_label.pack(fill="x")

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.window_create(tk.END, window=message_frame)
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatboxApp(root)
    root.mainloop()

    app.run()

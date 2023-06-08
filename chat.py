import random
import json
import torch
import tkinter as tk
from tkinter import messagebox
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from messages_to_db import insert_user_message

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

try:
    with open('intents.json', 'r') as f:
        intents = json.load(f)
except FileNotFoundError:
    messagebox.showerror("Error", "Could not find 'intents.json'")
    exit()

try:
    FILE = "data.pth"
    data = torch.load(FILE)
except FileNotFoundError:
    messagebox.showerror("Error", "Could not find 'data.pth'")
    exit()

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "ITECH_BOT"

class ChatWindow:
    def __init__(self, model, device, intents, all_words, tags, bot_name):
        self.window = tk.Tk()
        self.window.title("Chat with ITECH_Bot")
        
        self.text_area = tk.Text(self.window)
        self.text_area.pack()
        
        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(self.window, textvariable=self.entry_text)
        self.entry.bind("<Return>", self.send_message)
        self.entry.pack()
        
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack()
        
        self.model = model
        self.device = device
        self.intents = intents
        self.all_words = all_words
        self.tags = tags
        self.bot_name = bot_name
        
    def send_message(self, event=None):
        message = self.entry_text.get()
        self.text_area.insert(tk.END, "\nYou: " + message)

        if message.lower() == 'quit':
            self.window.quit()
            return
        
        sentence = tokenize(message)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        
        if tag != "uncertain" and prob.item() > 0.75:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    bot_message = f"{self.bot_name}: {random.choice(intent['responses'])}"
        else:
            # TODO: save in DB
            insert_user_message("User1", message, "Couldn't solve this")
            for intent in self.intents['intents']:
                if intent['tag'] == 'uncertain':
                    uncertainAnswer = intent
            bot_message = f"{self.bot_name}: {random.choice(uncertainAnswer['responses'])}"

        self.text_area.insert(tk.END, "\n" + bot_message)
        self.entry_text.set('')

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    chat_window = ChatWindow(model, device, intents, all_words, tags, bot_name)
    chat_window.run()
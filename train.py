import json 
from nltk_utils import tokenize, stem, bag_of_words
from nltk.corpus import stopwords
import numpy as np
import sys
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ChatDataset import ChatDataset 

from model import NeuralNet



try:
    with open('intents.json', 'r') as f:
        intents = json.load(f)
except FileNotFoundError:
    print("The file 'intents.json' was not found. Please ensure the file exists in the correct location.")
    sys.exit(1)



all_words = []
tags = []
xy = []


for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)

    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))


ignore_words = ['?', '!', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '*', '"', "'", 
                '``', "''", '--', '...', '@', '#', '$', '%', '^', '&', '_', '=', '+', '`', '~', 'html', 'body', 'p', 
                'br', '/p', 'div', '/div', 'strong', '/strong', 'em', '/em', 'u', '/u']

ignore_words += stopwords.words('english')



all_words = [stem(w) for w in all_words if w not in ignore_words]

all_words = sorted(set(all_words))
tags = sorted(set(tags))




X_train = []
Y_train = []

for(pattern_sentece, tag) in xy:
    bag = bag_of_words(pattern_sentece, all_words)
    X_train.append(bag)

    label = tags.index(tag)
    Y_train.append(label)

X_train = np.array(X_train)
Y_train = np.array(Y_train)

# Hyper-parameters 
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
# print(input_size, output_size)
# print(output_size, tags)

dataset = ChatDataset(X_train,Y_train)
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)


criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.15f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
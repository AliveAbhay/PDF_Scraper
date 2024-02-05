import os
import glob
import numpy as np
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder

# Assuming you have a folder with labeled text files (one file per language)
data_folder = 'Pdf_scraper/Update_pdf'
pdf_files = glob.glob(os.path.join(data_folder, '*.txt'))

# Read text data and labels
texts = []
labels = []

for file_path in pdf_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        language_label = file_path.split(os.path.sep)[-1].split('.')[0]  # Extract language label from filename
        texts.append(text)
        labels.append(language_label)

# Label encoding
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Tokenization and Padding
word_index = {}  # Create or load your word_index mapping
tokenized_texts = [
    [word_index[word] for word in text.split() if word in word_index]
    for text in texts
]

# Print tokenization results for debugging
for i, (text, tokens) in enumerate(zip(texts, tokenized_texts)):
    print(f"Example {i + 1} - Original Text: {text[:50]}... | Tokens: {tokens[:10]}...")

# Check if tokenized_texts is empty
if not tokenized_texts or all(not seq for seq in tokenized_texts):
    print("Error: No valid tokens found. Check your tokenization process.")
    # Handle the error or exit the program
else:
    # Pad sequences
    max_sequence_length = max(len(seq) for seq in tokenized_texts)
    padded_texts = [seq + [0] * (max_sequence_length - len(seq)) for seq in tokenized_texts]

    # Convert to PyTorch tensor
    X = torch.LongTensor(padded_texts)
    y = torch.LongTensor(encoded_labels)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the model
    class LanguageModel(nn.Module):
        def __init__(self, embedding_dim, hidden_dim, output_size, max_words):
            super(LanguageModel, self).__init__()
            self.embedding = nn.Embedding(max_words, embedding_dim)
            self.lstm = nn.LSTM(embedding_dim, hidden_dim)
            self.fc = nn.Linear(hidden_dim, output_size)

        def forward(self, x):
            x = self.embedding(x)
            lstm_out, _ = self.lstm(x)
            output = self.fc(lstm_out[:, -1, :])
            return output

    # Instantiate the model
    embedding_dim = 100
    hidden_dim = 100
    output_size = len(set(labels))
    max_words = len(word_index) + 1  # Add 1 to account for padding token (if used)
    model = LanguageModel(embedding_dim, hidden_dim, output_size, max_words)

    # Define loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Convert data and labels to PyTorch tensors
    class CustomDataset(Dataset):
        def __init__(self, data, labels):
            self.data = data
            self.labels = labels

        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            return self.data[idx], self.labels[idx]

    train_dataset = CustomDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    # Training loop
    epochs = 5
    for epoch in range(epochs):
        model.train()
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

    # Save the trained model
    torch.save(model.state_dict(), 'language_model.pth')

    # Evaluation
    model.eval()
    test_dataset = CustomDataset(X_test, y_test)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, targets in test_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += targets.size(0)
            correct += (predicted == targets).sum().item()

    accuracy = correct / total
    print(f'Accuracy: {accuracy * 100:.2f}%')

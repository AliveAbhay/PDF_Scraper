import os
import glob
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

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

# Tokenization
max_words = 10000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
word_index = tokenizer.word_index

# Padding
max_sequence_length = 1000
data = pad_sequences(sequences, maxlen=max_sequence_length)

# Label encoding
label_index = {label: index for index, label in enumerate(set(labels))}
encoded_labels = [label_index[label] for label in labels]

# Split data
X_train, X_test, y_train, y_test = train_test_split(data, encoded_labels, test_size=0.2, random_state=42)

# Model
embedding_dim = 100
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_sequence_length))
model.add(LSTM(100))
model.add(Dense(len(set(labels)), activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, np.array(y_train), epochs=5, validation_split=0.2)

# Save the trained model
model.save('language_model.h5')

# Evaluate the model
loss, accuracy = model.evaluate(X_test, np.array(y_test))
print(f'Accuracy: {accuracy * 100:.2f}%')

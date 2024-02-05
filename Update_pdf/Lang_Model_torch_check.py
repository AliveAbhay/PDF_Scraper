import torch
from Lang_model_torch import LanguageModel  # Replace 'your_module' with the actual module where LanguageModel is defined
from sklearn.preprocessing import LabelEncoder

# Instantiate the model
embedding_dim = 100
hidden_dim = 100
output_size = len(set(labels))

model = LanguageModel(embedding_dim, hidden_dim, output_size)

# Load the trained weights
model.load_state_dict(torch.load('language_model.pth'))
model.eval()

# Assuming you have a new text to classify
new_text = input("Enter the text you want to classify: ")

# Preprocess the new text (add additional preprocessing steps as needed)
new_text = new_text.lower()

# Tokenize and pad the new text
new_tokens = torch.LongTensor([word_index[word] for word in new_text.split() if word in word_index])

# Ensure the model is in evaluation mode
model.eval()

# Forward pass to get probabilities
with torch.no_grad():
    new_outputs = model(new_tokens.unsqueeze(0))  # Add a batch dimension

# Get the predicted class
_, predicted_class = torch.max(new_outputs, 1)

# Load the label encoder
label_encoder = LabelEncoder()
label_encoder.classes_ = YOUR_CLASSES  # Replace YOUR_CLASSES with the actual classes from training

# Map the predicted class index to the original class label using the label encoder
predicted_label = label_encoder.classes_[predicted_class.item()]

print(f"The predicted language is: {predicted_label}")

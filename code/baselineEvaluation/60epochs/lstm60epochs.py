#LSTM60EPOCHSRIGHTFINAL
# Imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.utils import Sequence
import gc
import matplotlib.pyplot as plt

# Parameters
chunk_size = 1000
max_len_limit = 500
batch_size = 16
epochs = 60
random_state = 42

# File paths
file_paths_train = [
    "/content/ANKRD1_test_CORRECTED.csv",
    "/content/B2MFIX_test_CORRECTED.csv",
    "/content/PPIAFIX2_test_CORRECTED.csv",
    "/content/GADPH_test_CORRECTED.csv",
    "/content/PGK1_test_CORRECTED.csv",
    "/content/RPLA13A_test_CORRECTED.csv",
    "/content/TTN_test_CORRECTED.csv",
    "/content/NEB_test_CORRECTED.csv"
]

# Chunk processing function
def process_chunk(chunk):
    sequences = chunk['sequence'].values
    labels = chunk['exon_intron_flag'].values
    return sequences, labels

# Initializing the tokenizer
tokenizer = Tokenizer(char_level=True)
sequences_list = []
labels_list = []

# Processing CSV files in chunks for training
for file_path in file_paths_train:
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        sequences, labels = process_chunk(chunk)
        tokenizer.fit_on_texts(sequences)
        sequences_list.extend(sequences)
        labels_list.extend(labels)
        gc.collect()

# Tokenization and padding of sequences
encoded_sequences = tokenizer.texts_to_sequences(sequences_list)
max_len = min(max(len(seq) for seq in encoded_sequences), max_len_limit)
padded_sequences = pad_sequences(encoded_sequences, maxlen=max_len, padding='post')
labels = np.array(labels_list, dtype=np.int8)

# Splitting data into train, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(padded_sequences, labels, test_size=0.2, random_state=random_state)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=random_state)

# Building the RNN model with LSTM
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 32

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    LSTM(32, return_sequences=True),  # First LSTM layer
    Dropout(0.2),
    LSTM(32),  # Second LSTM layer
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Data Generator Class
class DataGenerator(Sequence):
    def __init__(self, sequences, labels, batch_size):
        self.sequences = sequences
        self.labels = labels
        self.batch_size = batch_size
        self.indexes = np.arange(len(self.sequences))

    def __len__(self):
        return int(np.ceil(len(self.sequences) / self.batch_size))

    def __getitem__(self, index):
        batch_indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        return self.sequences[batch_indexes], self.labels[batch_indexes]

# Creating data generators
train_generator = DataGenerator(X_train, y_train, batch_size)
validation_generator = DataGenerator(X_val, y_val, batch_size)

# Training the model
model.fit(train_generator, epochs=epochs, validation_data=validation_generator)

# Function to calculate evaluation metrics with 4 decimal precision and standardized from 0 to 1
def evaluate_model(generator, y_true):
    # Generate predictions
    predictions = model.predict(generator)
    predictions = (predictions > 0.5).astype(int).flatten()  # Convert to 1D array

    # Display the length of data in predictions and y_true
    print(f'Number of predictions: {len(predictions)}')
    print(f'Number of true values (y_true): {len(y_true)}')

    # Calculate TP, TN, FP, FN
    tp = np.sum((y_true == 1) & (predictions == 1))
    tn = np.sum((y_true == 0) & (predictions == 0))
    fp = np.sum((y_true == 0) & (predictions == 1))
    fn = np.sum((y_true == 1) & (predictions == 0))

    # Classification metrics
    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) 
    recall = tp / (tp + fn)
    specificity = tn / (tn + fp) 
    f1 = 2 * (precision * recall) / (precision + recall) 
    
    # Return metrics with 4 decimal precision
    return (round(accuracy, 4), round(precision, 4), round(recall, 4),
            round(specificity, 4), round(f1, 4), tp, tn, fp, fn)

# Evaluating on the test set
test_generator = DataGenerator(X_test, y_test, batch_size)
accuracy, precision, sensitivity, specificity, f1, tp, tn, fp, fn = evaluate_model(test_generator, y_test)

# Display metrics
print(f'Test Accuracy: {accuracy:.4f}')
print(f'Test Precision: {precision:.4f}')
print(f'Test Sensitivity (Recall): {sensitivity:.4f}')
print(f'Test Specificity: {specificity:.4f}')
print(f'Test F1-Score: {f1:.4f}')
print(f'True Positives: {tp}')
print(f'True Negatives: {tn}')
print(f'False Positives: {fp}')
print(f'False Negatives: {fn}')

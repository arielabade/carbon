import tensorflow as tf
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
from Bio import SeqIO
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping

# Função para carregar as sequências do arquivo FASTA
def fasta_to_list(file):
   sequences = []
   labels = []
   with open(file, 'r') as fasta_file:
       for record in SeqIO.parse(fasta_file, "fasta"):
           sequences.append(str(record.seq))
           is_exon = "exon" in record.description.lower()
           labels.append(1 if is_exon else 0)
   return sequences, labels

# Carregar as sequências
sequences, labels = fasta_to_list("0X_carbonRascunho/hbb-test.fa")

# Mapeamento de bases para índices
vocab = ["A", "C", "G", "T"]
base_to_index = {base: i for i, base in enumerate(vocab)}

# Função para converter sequências em índices
def sequence_to_indices(sequence):
   return [base_to_index[base] for base in sequence]

# Converter as sequências para índices
indexed_sequences = [sequence_to_indices(seq) for seq in sequences]

# Aplicar padding
max_len = max(len(seq) for seq in indexed_sequences)
padded_sequences = pad_sequences(indexed_sequences, maxlen=max_len, padding='post')

# Definir parâmetros para embedding
vocab_size = len(vocab)
embedding_dim = 4

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, np.array(labels), test_size=0.2, random_state=42)

# Criar e treinar o modelo CNN com embedding
model = Sequential([
   Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
   Conv1D(filters=64, kernel_size=5, activation='relu', padding='same'),
   MaxPooling1D(pool_size=2),
   Dropout(0.5),
   Conv1D(filters=32, kernel_size=5, activation='relu', padding='same'),
   MaxPooling1D(pool_size=2),
   Flatten(),
   Dense(64, activation='relu'),
   Dropout(0.5),
   Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Adicionar EarlyStopping para evitar overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test), callbacks=[early_stopping])

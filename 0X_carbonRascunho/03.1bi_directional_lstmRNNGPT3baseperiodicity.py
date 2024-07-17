import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.models import Sequential
from Bio import SeqIO
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
from scipy.signal import lfilter
from scipy.fft import fft, ifft

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

# Função para detectar periodicidade
def detect_periodicity(sequence, window_size=240, r=0.992):
    if len(sequence) < window_size:
        return []  # Retorna uma lista vazia se a sequência for menor que o tamanho da janela
    eiip_values = {"A": 0.1260, "C": 0.1340, "G": 0.0806, "T": 0.1335, "N": 0.1000}
    numeric_sequence = np.array([eiip_values.get(base, 0.0) for base in sequence])
    b = [1, -2, 1]
    a = [1, -2 * r * np.cos(2 * np.pi / 3), r**2]
    filtered_sequence = lfilter(b, a, numeric_sequence)
    scores = [np.sum(filtered_sequence[i : i + window_size]**2) for i in range(len(sequence) - window_size + 1)]
    return scores

# Função para classificar exons e introns
def classify_exons(sequence, scores, window_size=240, threshold=None):
    if not scores:
        return [], []  # Retorna listas vazias se scores estiver vazio
    if threshold is None:
        threshold = np.mean(scores)
    exons = []
    introns = []
    in_exon = scores[0] > threshold
    for i, score in enumerate(scores):
        if score > threshold:
            if not in_exon:
                exons.append((i, i + window_size))
                in_exon = True
        else:
            if in_exon:
                introns.append((i, i + window_size))
                in_exon = False
    return exons, introns

# Carregar as sequências
sequences, labels = fasta_to_list("0X_carbonRascunho/hbb-test.fa")

# Mapeamento de bases para índices
vocab = ["A", "C", "G", "T"]
base_to_index = {base: i for i, base in enumerate(vocab)}
base_to_index['N'] = len(vocab)

# Função para converter sequências em índices
def sequence_to_indices(sequence):
    return [base_to_index.get(base, len(vocab)) for base in sequence]

# Converter as sequências para índices
indexed_sequences = [sequence_to_indices(seq) for seq in sequences]

# Aplicar padding
max_len = max(len(seq) for seq in indexed_sequences)
padded_sequences = pad_sequences(indexed_sequences, maxlen=max_len, padding='post')

# Definir parâmetros para embedding
vocab_size = len(vocab) + 1
embedding_dim = 4

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, np.array(labels), test_size=0.2, random_state=42)

# Criar e treinar o modelo Bi-LSTM com embedding
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.5),
    Bidirectional(LSTM(32)),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Adicionar EarlyStopping para evitar overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Treinar o modelo
model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test), callbacks=[early_stopping])

# Aplicar a função de periodicidade
sequence = "".join(c for c in sequences[0] if c in "ACGT")
scores = detect_periodicity(sequence)
exons, introns = classify_exons(sequence, scores)

# Calcular e exibir porcentagens
total_regions = len(exons) + len(introns)
if total_regions > 0:
    exon_percentage = (len(exons) / total_regions) * 100
    intron_percentage = (len(introns) / total_regions) * 100
else:
    exon_percentage = intron_percentage = 0

print("Exons:", exons)
print("Introns:", introns)
print(f"\nPercentage of Exons: {exon_percentage:.2f}%")
print(f"Percentage of Introns: {intron_percentage:.2f}%")

# Avaliar o desempenho do modelo
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'\nTest Loss: {loss:.4f}')
print(f'Test Accuracy: {accuracy:.4f}')

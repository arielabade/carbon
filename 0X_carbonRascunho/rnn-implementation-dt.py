import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense


# 1. Carregar o CSV e preparar as sequências e labels
df = pd.read_csv('DATASETS/output_sequencesTTN.csv')
sequences = df['sequence'].values
labels = df['exon_intron_flag'].values

# 2. Tokenização das sequências
tokenizer = Tokenizer(char_level=True)  # Considera cada base (A, T, C, G) como uma unidade
tokenizer.fit_on_texts(sequences)
encoded_sequences = tokenizer.texts_to_sequences(sequences)

# 3. Padronizar o comprimento das sequências
max_len = max(len(seq) for seq in encoded_sequences)
padded_sequences = pad_sequences(encoded_sequences, maxlen=max_len, padding='post')

# 4. Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

# 5. Construção da RNN Bidirecional
vocab_size = len(tokenizer.word_index) + 1  # Inclui espaço para o índice 0
embedding_dim = 64

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    Bidirectional(LSTM(64, return_sequences=True)),
    Bidirectional(LSTM(64)),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 6. Treinamento do modelo
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# 7. Avaliação do modelo
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Acurácia no conjunto de teste: {accuracy*100:.2f}%')

# 8. Inferência em novos dados (exemplo)
new_sequences = ['GCTTCGCTCTCTGCTCCTCCTGTTCGACAGTCAGCCGCATCTTCTTTTGCGTCGCCAG']  # Exemplo
encoded_new_sequences = tokenizer.texts_to_sequences(new_sequences)
padded_new_sequences = pad_sequences(encoded_new_sequences, maxlen=max_len, padding='post')

predictions = model.predict(padded_new_sequences)
print(f'Predições para novas sequências: {predictions}')

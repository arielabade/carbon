import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.utils import Sequence
import gc
import matplotlib.pyplot as plt

# Parâmetros
chunk_size = 1000
max_len_limit = 500
batch_size = 16
epochs = 60
random_state = 42

# Caminhos dos arquivos, incluindo o NEB no treinamento
file_paths_train = [
    "/content/ANKRD1_test_CORRECTED.csv",
    "/content/B2MFIX_test_CORRECTED.csv",
    "/content/PPIAFIX2_test_CORRECTED.csv",
    "/content/GADPH_test_CORRECTED.csv",
    "/content/PGK1_test_CORRECTED.csv",
    "/content/RPLA13A_test_CORRECTED.csv",
    "/content/TTN_test_CORRECTED.csv",
    "/content/NEB_test_CORRECTED.csv"  # Incluindo NEB no treino
]

# Função para processar chunks
def process_chunk(chunk):
    sequences = chunk['sequence'].values
    labels = chunk['exon_intron_flag'].values
    return sequences, labels

# Inicializando o tokenizer apenas uma vez, fora do loop de chunks
tokenizer = Tokenizer(char_level=True)
sequences_list = []  # Inicialização correta das variáveis
labels_list = []

# Processando os arquivos CSV em chunks para treino (incluindo NEB)
for file_path in file_paths_train:
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        sequences, labels = process_chunk(chunk)
        sequences_list.extend(sequences)
        labels_list.extend(labels)
        gc.collect()

# Ajustando o tokenizer apenas após reunir todas as sequências
tokenizer.fit_on_texts(sequences_list)

# Tokenização e padding das sequências
encoded_sequences = tokenizer.texts_to_sequences(sequences_list)
max_len = min(max(len(seq) for seq in encoded_sequences), max_len_limit)
padded_sequences = pad_sequences(encoded_sequences, maxlen=max_len, padding='post')
labels = np.array(labels_list, dtype=np.int8)

# Separando os dados em treino (80%), validação (10%) e teste (10%)
X_train, X_temp, y_train, y_temp = train_test_split(padded_sequences, labels, test_size=0.2, random_state=random_state)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=random_state)

# Construção do modelo Bidirectional LSTM
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 32

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    Bidirectional(LSTM(32, return_sequences=True)),
    Dropout(0.2),
    Bidirectional(LSTM(32)),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Classe Data Generator
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

# Criando os geradores de dados
train_generator = DataGenerator(X_train, y_train, batch_size)
validation_generator = DataGenerator(X_val, y_val, batch_size)

# Treinamento do modelo
history = model.fit(train_generator, epochs=epochs, validation_data=validation_generator)

# Função para calcular métricas de avaliação, incluindo especificidade
def evaluate_model(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    sensitivity = recall_score(y_true, y_pred)  # Sensibilidade é o Recall
    f1 = f1_score(y_true, y_pred)

    # Cálculo da especificidade
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp)

    return accuracy, precision, sensitivity, specificity, f1

# Avaliação nos arquivos de treino/validação
results = {
    "File": [], "Validation ACC": [], "Validation PRE": [], "Validation SEN": [], "Validation SPEC": [], "Validation F1S": [],
    "Test ACC": [], "Test PRE": [], "Test SEN": [], "Test SPEC": [], "Test F1S": []
}

for test_file in file_paths_train:
    test_data = pd.read_csv(test_file)
    test_sequences = test_data['sequence'].values
    test_labels = test_data['exon_intron_flag'].values

    # Tokenização e padding das sequências de teste
    encoded_test_sequences = tokenizer.texts_to_sequences(test_sequences)
    padded_test_sequences = pad_sequences(encoded_test_sequences, maxlen=max_len, padding='post')

    # Avaliação nos dados de validação
    val_predictions = (model.predict(validation_generator) > 0.5).astype(int)
    val_accuracy, val_precision, val_sensitivity, val_specificity, val_f1 = evaluate_model(y_val, val_predictions)

    # Avaliação nos dados de teste
    test_predictions = (model.predict(padded_test_sequences) > 0.5).astype(int)
    test_accuracy, test_precision, test_sensitivity, test_specificity, test_f1 = evaluate_model(test_labels, test_predictions)

    # Armazenando os resultados
    results["File"].append(test_file)
    results["Validation ACC"].append(val_accuracy * 100)
    results["Validation PRE"].append(val_precision)
    results["Validation SEN"].append(val_sensitivity)
    results["Validation SPEC"].append(val_specificity)
    results["Validation F1S"].append(val_f1)
    results["Test ACC"].append(test_accuracy * 100)
    results["Test PRE"].append(test_precision)
    results["Test SEN"].append(test_sensitivity)
    results["Test SPEC"].append(test_specificity)
    results["Test F1S"].append(test_f1)

    print(f'Results for {test_file}:')
    print(f'Validation Accuracy: {val_accuracy * 100:.2f}%')
    print(f'Test Accuracy: {test_accuracy * 100:.2f}%')
    print(f'Test Precision: {test_precision:.2f}')
    print(f'Test Sensitivity: {test_sensitivity:.2f}')
    print(f'Test Specificity: {test_specificity:.2f}')
    print(f'Test F1 Score: {test_f1:.2f}')
    print('---')

# Exibindo todos os resultados
results_df = pd.DataFrame(results)
print(results_df)

# Calculando as médias totais
numeric_columns = results_df.select_dtypes(include=[np.number])
total_avg = numeric_columns.mean(axis=0)

# Adicionando as métricas totais ao DataFrame
total_metrics = pd.DataFrame({
    "File": ["Total"],
    "Validation ACC": [total_avg["Validation ACC"]],
    "Validation PRE": [total_avg["Validation PRE"]],
    "Validation SEN": [total_avg["Validation SEN"]],
    "Validation SPEC": [total_avg["Validation SPEC"]],
    "Validation F1S": [total_avg["Validation F1S"]],
    "Test ACC": [total_avg["Test ACC"]],
    "Test PRE": [total_avg["Test PRE"]],
    "Test SEN": [total_avg["Test SEN"]],
    "Test SPEC": [total_avg["Test SPEC"]],
    "Test F1S": [total_avg["Test F1S"]]
})

# Concatenando as métricas totais ao DataFrame de resultados
results_df = pd.concat([results_df, total_metrics], ignore_index=True)
print("Results with Total Metrics:")
print(results_df)

# Função para plotar gráficos de perda e acurácia
def plot_history(history):
    plt.figure(figsize=(14, 5))

    # Gráfico de Perda (Loss)
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss Over Epochs')
    plt.legend()
    plt.grid(True)

    # Gráfico de Acurácia
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy Over Epochs')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Chamando a função para plotar os gráficos
plot_history(history)


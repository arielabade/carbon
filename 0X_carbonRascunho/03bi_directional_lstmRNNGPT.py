import tensorflow as tf
import numpy as np
from Bio import SeqIO
import pandas as pd

# Abordagem one-hot vector: utiliza vetores binários de 4 dimensões para classificar as bases
def one_hot_encoding(sequence):
    vectors = {'A': [1, 0, 0, 0], 'G': [0, 1, 0, 0], 'C': [0, 0, 1, 0], 'T': [0, 0, 0, 1]}
    onehot = [vectors[base] for base in sequence]
    return np.array(onehot)

def embed_preprocessing(sequence):
    base_to_index = {'A': 0, 'G': 1, 'C': 2, 'T': 3}
    indices = [base_to_index[base] for base in sequence]
    return indices

def fasta_to_list(file):
    sequences = []
    headers = []  # Temos interesse em manter os IDs?
    with open(file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequences.append(str(record.seq))
            headers.append(record.id)
    return sequences, headers

def fasta_to_dict(file, encoding=None):
    sequences_dict = {True: [], False: []}
    with open(file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequence = str(record.seq)
            is_exon = "exon" in record.description.lower()
            if encoding == "ONE_HOT":
                encoded_sequence = one_hot_encoding(sequence)
            sequences_dict[is_exon].append(encoded_sequence)
    return sequences_dict

print(fasta_to_dict("./hbb-test.fa", encoding="ONE_HOT"))

def binary_annotated_fasta(fasta_file, annotation_file):
    annotation = pd.read_csv(annotation_file, sep='\t', header=None)
    start_indexes = annotation[3].to_list()
    end_indexes = annotation[4].to_list()
    cds_regions = list(zip(start_indexes, end_indexes))
    
    fasta_binary = []
    with open(fasta_file, 'r') as file:
        genome = ''.join(line.strip() for line in file.readlines()[1:])

    for i in range(len(genome)):
        is_cds = any(start - 1 <= i < end - 1 for start, end in cds_regions)
        fasta_binary.append('1' if is_cds else '0')
    
    binary_fasta_string = ''.join(fasta_binary)
    return binary_fasta_string
import tensorflow as tf
import numpy as np
from Bio import SeqIO
import pandas as pd

# Abordagem one-hot vector: utiliza vetores binários de 4 dimensões para classificar as bases
def one_hot_encoding(sequence):
    vectors = {'A': [1, 0, 0, 0], 'G': [0, 1, 0, 0], 'C': [0, 0, 1, 0], 'T': [0, 0, 0, 1]}
    onehot = [vectors[base] for base in sequence]
    return np.array(onehot)

def embed_preprocessing(sequence):
    base_to_index = {'A': 0, 'G': 1, 'C': 2, 'T': 3}
    indices = [base_to_index[base] for base in sequence]
    return indices

def fasta_to_list(file):
    sequences = []
    headers = []  # Temos interesse em manter os IDs?
    with open(file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequences.append(str(record.seq))
            headers.append(record.id)
    return sequences, headers

def fasta_to_dict(file, encoding=None):
    sequences_dict = {True: [], False: []}
    with open(file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequence = str(record.seq)
            is_exon = "exon" in record.description.lower()
            if encoding == "ONE_HOT":
                encoded_sequence = one_hot_encoding(sequence)
            sequences_dict[is_exon].append(encoded_sequence)
    return sequences_dict

print(fasta_to_dict("./hbb-test.fa", encoding="ONE_HOT"))


def binary_annotated_fasta(fasta_file, annotation_file):
    annotation = pd.read_csv(annotation_file, sep='\t', header=None)
    start_indexes = annotation[3].to_list()
    end_indexes = annotation[4].to_list()
    cds_regions = list(zip(start_indexes, end_indexes))
    
    fasta_binary = []
    with open(fasta_file, 'r') as file:
        genome = ''.join(line.strip() for line in file.readlines()[1:])

    for i in range(len(genome)):
        is_cds = any(start - 1 <= i < end - 1 for start, end in cds_regions)
        fasta_binary.append('1' if is_cds else '0')
    
    binary_fasta_string = ''.join(fasta_binary)
    return binary_fasta_string

#RNN

class CodanRNN(tf.keras.Model):
    def __init__(self, input_shape, hidden_units, output_units):
        super(CodanRNN, self).__init__()
        self.rnn = tf.keras.layers.SimpleRNN(hidden_units, return_sequences=True)
        self.fc = tf.keras.layers.Dense(output_units, activation='softmax')
    
    def call(self, inputs):
        x = self.rnn(inputs)
        x = self.fc(x[:, -1, :])  # Use only the last time step's output
        return x

def build_rnn(input_shape, hidden_units=64, output_units=4):
    model = CodanRNN(input_shape, hidden_units, output_units)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Caminho para o arquivo FASTA
file_path = './hbb-test.fa'
sequences, headers = fasta_to_list(file_path)

# Converter as sequências para one-hot encoding
one_hot_sequences = [one_hot_encoding(seq) for seq in sequences]

# Converter as sequências para numpy arrays para que o TensorFlow consiga operar sobre elas
X = np.array(one_hot_sequences)

# Usar a primeira sequência para definir a forma de entrada da RNN
input_shape = (X.shape[1], X.shape[2])

# Construir o modelo RNN
model = build_rnn(input_shape)

# Exemplo de treinamento (X_train e y_train precisam ser preparados conforme a tarefa específica)
# model.fit(X_train, y_train, epochs=10)

# TODO
# Transformar os arquivos fasta em numpy arrays para que o TensorFlow consiga operar sobre eles
# One-hot vs

import tensorflow as tf
import numpy as np
from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt


# Abordagem one-hot vector: utiliza vetores binarios de 4 dimensoes para classificar as bases
def one_hot_encoding(sequence):
    """
    Converte cada nucleotideo de uma sequencia em um vetor binario de 4 posicoes, onde 1 eh o valor correspondente.
    Ex.: AAGTC -> [[1,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]]

    Entrada - sequencia de nucleotideos : string
    Saida - lista de vetores de 4 posicoes : list<list<int>>
    """
    vectors = {'A': [1,0,0,0], 'G': [0,1,0,0], 'C': [0,0,1,0], 'T': [0,0,0,1]} # -01,01, 10, -10 | 
    onehot = []
    for base in sequence:
        onehot.append(vectors[base])
    return np.array(onehot)

def embed_preprocessing(sequence):
    """
    Converte uma sequencia de nucleotideos em uma lista de numeros de 0 a 3.
    Ex.: AATCGACTAGG -> [0,0,3,2,1,0,2,3,0,1,1]
    Esse passo eh necessario no uso do metodo 'embedding vectors'

    Entrada - sequencia de nucleotideos : string
    Saida - lista de indices : list<int>
    """
    base_to_index = {'A': 0, 'G': 1, 'C': 2, 'T': 3}
    indices = [base_to_index[base] for base in sequence]
    return indices

def fasta_to_list(file): # transforma os arquivos fasta em listas com as strings
    sequences = []
    headers = [] # temos interesse em manter os IDs?
    with open(file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequences.append(str(record.seq))
            headers.append(record.id)
    return sequences, headers

def fasta_to_dict(file, encoding=None): ##conversão do cabeçalho
    sequences_dict = {True: [], False: []}
    # sequences_dict = {}
    with open(file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequence = str(record.seq)
            is_exon = "exon" in record.description.lower()
            if encoding == "ONE_HOT":
                encoded_sequence = one_hot_encoding(sequence)
            # Use o comando abaixo para agrupar todas as sequencias exons e introns
            sequences_dict[is_exon].append(encoded_sequence)
            # Use o comando abaixo para categorizar todas as sequencias como True ou False
            # sequences_dict[sequence] = is_exon
    return sequences_dict

print(fasta_to_dict("./hbb-test.fa", encoding="ONE_HOT"))
#sequences, headers = fasta_to_list('./bin/models/VERT_full/dataset/train.fa') # exemplo qualquer para fins de teste

def binary_annotated_fasta(fasta_file, annotation_file):
    #fasta_list = fasta_to_list(fasta_file)
    annotation = pd.read_csv(annotation_file, sep='\t', header=None)
    start_indexes = annotation[3].to_list()
    end_indexes = annotation[4].to_list()

    cds_regions = list(zip(start_indexes, end_indexes))
        
    fasta_binary = []

    with open(fasta_file, 'r') as file:
        genome = ''.join(line.strip() for line in file.readlines()[1:])

    for i in range(len(genome)):
        is_cds = any(start-1 <= i < end-1 for start, end in cds_regions)
        fasta_binary.append('1' if is_cds else '0')
    
    binary_fasta_string = ''.join(fasta_binary)


    return binary_fasta_string



# Modelo de RNN utilizando TensorFlow e Keras (falta instanciar/parametrizar)
class CodanRNN(tf.keras.Model):
    def __init__(self, input_shape, hidden_units, output_units):
        super(CodanRNN, self).__init__()
        self.rnn = tf.keras.layers.SimpleRNN(hidden_units, return_sequences=True)
        self.fc = tf.keras.layers.Dense(output_units)
    
    def call(self, inputs):
        x = self.rnn(inputs)
        x = self.fc(x[:, -1, :])  # Use only the last time step's output
        return x
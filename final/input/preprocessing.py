# randomiação de sequencias, pré processamento dos dados para treino e teste, definição de amostragem das cadeias, leitura das cadeias na ordem normal e na ordem inversa.

def binary_annotated_fasta(fasta_file, annotation_file):
    annotation = pd.read_csv(annotation_file, sep='\t', header=None)
    start_indexes = annotation[3].to_list()
    end_indexes = annotation[4].to_list()

    cds_regions = list(zip(start_indexes, end_indexes))
    
    fasta_binary = []

    with open(fasta_file, 'r') as file:
        genome = ''.join(line.strip() for line in file.readlines()[1:])
    # Continuação da função...

    
print(binary_annotated_fasta('genome.fasta', 'annotation.gtf'))


def one_hot_encoding(sequences):
    vectors = {'A': [1,0,0,0], 'G': [0,1,0,0], 'C': [0,0,1,0], 'T': [0,0,0,1]}
    onehot = []
    for seq in sequences:
        for base in seq:
            onehot.append(vectors[base])
    return np.array(onehot)

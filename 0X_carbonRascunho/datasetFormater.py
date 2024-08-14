import re
import pandas as pd

# Função para processar as sequências DNA a partir de um arquivo
def parse_dna_sequences_from_file(file_path):
    sequences = {}
    current_label = ""

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(">"):
                current_label = line.strip()
                sequences[current_label] = ""
            else:
                sequences[current_label] += line.strip()

    return sequences

# Função para identificar se a sequência é exon ou intron
def identify_exon_or_intron(label):
    if re.search(r'\bexon\b', label, re.IGNORECASE):
        return 1  # Exon
    elif re.search(r'\bintron\b', label, re.IGNORECASE):
        return 0  # Intron
    else:
        return None  # Caso não seja identificado

# Função para extrair gene_name e gene_id
def extract_gene_info(label):
    gene_name_match = re.search(r'(\S+)', label)
    gene_id_match = re.search(r'(ENSE\S+)', label)

    gene_name = gene_name_match.group(1) if gene_name_match else None
    gene_id = gene_id_match.group(1) if gene_id_match else None

    return gene_name, gene_id

# Função para identificar posições de exons e introns
def identify_exon_intron_positions(sequences):
    results = []
    current_start_pos = 0

    for label, sequence in sequences.items():
        gene_name, gene_id = extract_gene_info(label)
        exon_or_intron = identify_exon_or_intron(label)

        length = len(sequence)
        end_pos = current_start_pos + length - 1

        results.append({
            'gene_name': gene_name,
            'gene_id': gene_id,
            'exon_intron_flag': exon_or_intron,
            'sequence_length': length,
            'start_position': current_start_pos,
            'end_position': end_pos,
            'sequence': sequence
        })

        current_start_pos = end_pos + 1  # Atualiza a posição inicial para a próxima sequência

    return results

# Função para criar o DataFrame final e salvar como CSV
def create_dataset_and_save_to_csv(file_path, output_csv_path):
    sequences = parse_dna_sequences_from_file(file_path)
    exon_intron_positions = identify_exon_intron_positions(sequences)
    df = pd.DataFrame(exon_intron_positions)
    df.to_csv(output_csv_path, index=False)

# Exemplo de uso
input_file_path = '/home/ariel/carbon/0X_carbonRascunho/ttn-test.fa'  # Substitua pelo caminho do arquivo de entrada
output_csv_path = 'output_sequencesTTN.csv'  # Substitua pelo caminho do arquivo de saída

create_dataset_and_save_to_csv(input_file_path, output_csv_path)

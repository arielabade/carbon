# load fasta, tamanho mínimo do arquivo, tamanho máximo do arquivo, tokenização do arquivo (quebrar ele em partes menores), tratamento de dados do arquivo repassando a máscara.

def fasta_to_list(file): 
    sequences = []
    headers = [] 
    with open(file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequences.append(str(record.seq))
            headers.append(record.id)
    return sequences, headers


import re

def find_codons(sequence):
    start_codons = ['AUG', 'GUG', 'CUG']
    stop_codons = ['UAA', 'UAG', 'UGA']
    
    start_positions = []
    stop_positions = []
    
    for codon in start_codons:
        start_positions += [m.start() for m in re.finditer(codon, sequence)]
    
    for codon in stop_codons:
        stop_positions += [m.start() for m in re.finditer(codon, sequence)]
    
    return start_positions, stop_positions

def find_splicing_sites(sequence):
    donor_site = 'GU'
    acceptor_site = 'AG'
    
    donor_positions = [m.start() for m in re.finditer(donor_site, sequence)]
    acceptor_positions = [m.start() for m in re.finditer(acceptor_site, sequence)]
    
    return donor_positions, acceptor_positions

def classify_and_split_sequence(sequence):
    sequence = sequence.replace('T', 'U')  # Convert to RNA for simplicity
    donor_positions, acceptor_positions = find_splicing_sites(sequence)
    start_positions, stop_positions = find_codons(sequence)
    
    blocks = []
    current_block = []
    in_exon = False
    
    for i in range(len(sequence)):
        codon = sequence[i:i+3]
        
        if codon in ['AUG', 'GUG', 'CUG']:
            if current_block:
                blocks.append((''.join(current_block), in_exon))
                current_block = []
            in_exon = True
        
        elif codon in ['UAA', 'UAG', 'UGA']:
            if current_block:
                blocks.append((''.join(current_block), in_exon))
                current_block = []
            in_exon = False
        
        current_block.append(sequence[i])
        
    if current_block:
        blocks.append((''.join(current_block), in_exon))
    
    return blocks

def process_sequences(sequences):
    total_length = sum(len(seq) for seq in sequences)
    exon_length = 0
    intron_length = 0
    results = []
    
    for sequence in sequences:
        blocks = classify_and_split_sequence(sequence)
        for block, is_exon in blocks:
            classification = 1 if is_exon else 0
            results.append((block, classification))
            
            if classification == 1:
                exon_length += len(block)
            else:
                intron_length += len(block)
    
    exon_percentage = (exon_length / total_length) * 100
    intron_percentage = (intron_length / total_length) * 100
    
    return results, exon_percentage, intron_percentage

def save_to_file(results, exon_percentage, intron_percentage, filename):
    with open(filename, 'w') as f:
        for sequence, classification in results:
            if len(sequence.strip()) > 0:
                f.write(f"{sequence},{classification}\n")
        f.write(f"\nExon percentage: {exon_percentage:.2f}%\n")
        f.write(f"Intron percentage: {intron_percentage:.2f}%\n")

def read_sequences_from_files(filepaths):
    sequences = []
    for filepath in filepaths:
        with open(filepath, 'r') as file:
            sequence = file.read().replace('\n', '')
            sequences.append(sequence)
    return sequences

# Example usage
filepaths = ['0X_carbonRascunho/hbb-test-transcript.fa']  # Adicione os caminhos dos arquivos aqui
sequences = read_sequences_from_files(filepaths)

results, exon_percentage, intron_percentage = process_sequences(sequences)
save_to_file(results, exon_percentage, intron_percentage, 'classified_sequences_hbb-test-transcript.csv')

print(f"Classification complete. Results saved to classified_sequences_hbb-test-transcript.csv")
print(f"Exon percentage: {exon_percentage:.2f}%")
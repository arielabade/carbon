def count_fasta_exons_introns(file_path):
    """Counts the total number of characters, exons, and introns in a FASTA file.
       Also returns the list of exon and intron sequences for further analysis.
    
    Args:
        file_path: The path to the FASTA file.
    
    Returns:
        A dictionary with the total number of characters, exons, introns, and the lists of sequences.
    """
    total_exon_characters = 0
    total_intron_characters = 0
    exon_sequences = []
    intron_sequences = []
    
    with open(file_path, 'r') as fasta_file:
        for line in fasta_file:
            if not line.strip() or line.startswith('gene_name'):
                continue
            
            line = line.strip()[1:]
            columns = line.split(',')
            
            if len(columns) < 7:
                continue
            
            gene_name = columns[0]
            gene_id = columns[1]
            exon_intron_flag = float(columns[2])
            sequence = columns[6]
            
            if exon_intron_flag == 1.0:
                total_exon_characters += len(sequence.strip())
                exon_sequences.append(line)
            elif exon_intron_flag == 0.0:
                total_intron_characters += len(sequence.strip())
                intron_sequences.append(line)
    
    return {
        'total_exon_characters': total_exon_characters,
        'total_intron_characters': total_intron_characters,
        'exon_sequences': exon_sequences,
        'intron_sequences': intron_sequences
    }

def write_balanced_fasta(output_file, balanced_sequences):
    """Writes the balanced exon and intron sequences to a new CSV file.
    
    Args:
        output_file: Path of the file where the balanced sequences will be saved.
        balanced_sequences: List of balanced sequences.
    """
    with open(output_file, 'w') as out_file:
        for sequence in balanced_sequences:
            out_file.write(f">{sequence}\n")
    print(f"Balanced file saved at {output_file}")

if __name__ == '__main__':
    file_path = 'xxxx/xxxxx/..'  # Relative path for input file
    result = count_fasta_exons_introns(file_path)
    
    print(f"Total nucleotide count in exons: {result['total_exon_characters']}")
    print(f"Total nucleotide count in introns: {result['total_intron_characters']}")
    
    balanced_sequences = result['exon_sequences'] + result['intron_sequences']
    
    output_file = 'xxxx/xxxxx/..'  # Relative path for output file
    write_balanced_fasta(output_file, balanced_sequences)

import csv

def process_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        current_label = ""
        exon_count = 0
        intron_count = 0
        
        for row in reader:
            if len(row) == 1 and row[0].startswith(">"):
                if current_label:
                    print(f"{current_label}")
                    print(f"numero de exons nesse rotulo = {exon_count}")
                    print(f"numero de introns nesse rotulo = {intron_count}")
                    print()
                
                current_label = row[0]
                exon_count = 0
                intron_count = 0
            elif len(row) == 2:
                sequence, label = row
                if "exon" in current_label:
                    exon_count += 1
                elif "intron" in current_label:
                    intron_count += 1
        
        # Print the last label counts
        if current_label:
            print(f"{current_label}")
            print(f"numero de exons nesse rotulo = {exon_count}")
            print(f"numero de introns nesse rotulo = {intron_count}")

# Exemplo de uso
file_path = 'classified_sequences.csv'
process_file(file_path)

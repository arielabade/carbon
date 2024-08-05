
def calcular_percentual_exons_introns(sequencias):
    """Calcula o percentual de exons e introns nas sequências.

    Args:
        sequencias: Uma lista de tuplas (label, seq), onde label é o rótulo da sequência e seq é a sequência em si.

    Returns:
        Uma tupla (percentual_exons, percentual_introns) com os percentuais de exons e introns.
    """
    total_sequencias = len(sequencias)
    exon_count = sum(1 for label, _ in sequencias if "exon" in label)
    intron_count = sum(1 for label, _ in sequencias if "intron" in label)

    percentual_exons = (exon_count / total_sequencias) * 100 if total_sequencias > 0 else 0
    percentual_introns = (intron_count / total_sequencias) * 100 if total_sequencias > 0 else 0

    return percentual_exons, percentual_introns

def ler_sequencias_do_arquivo(file_name):
    sequencias = []
    with open(file_name, "r") as file:
        lines = file.readlines()
        label = ""
        sequence = ""
        for line in lines:
            line = line.strip()
            if line.startswith(">"):
                if label and sequence:
                    sequencias.append((label, sequence))
                label = line
                sequence = ""
            else:
                sequence += line
        if label and sequence:  # Add the last sequence
            sequencias.append((label, sequence))
    return sequencias

# Exemplo de uso:
file_name = "0X_carbonRascunho/GADPH_test.fa" # Coloque aqui o nome do seu arquivo
sequencias = ler_sequencias_do_arquivo(file_name)

percentual_exons, percentual_introns = calcular_percentual_exons_introns(sequencias)

print(f"Percentual de exons: {percentual_exons:.2f}%")
print(f"Percentual de introns: {percentual_introns:.2f}%")

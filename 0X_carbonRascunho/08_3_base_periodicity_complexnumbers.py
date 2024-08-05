import numpy as np
from scipy.signal import lfilter

def complex_representation(sequence):
    """Convert DNA sequence to complex numerical representation.
    
    Args:
        sequence: The DNA sequence as a string (e.g., "ATCGGACT...").
    
    Returns:
        A numpy array of complex numbers representing the DNA sequence.
    """
    complex_values = {
        "A": 1 + 1j,
        "C": -1 + 1j,
        "G": -1 - 1j,
        "T": 1 - 1j
    }
    return np.array([complex_values.get(base, 0 + 0j) for base in sequence])  # Default to 0+0j if base not found

def detect_periodicity(sequence, window_size=1000, r=0.992):
    """Detects 3-base periodicity in a DNA sequence using digital filtering with complex representation.

    Args:
        sequence: The DNA sequence as a string (e.g., "ATCGGACT...").
        window_size: The size of the sliding window (default: 240).
        r: The pole radius of the anti-notch filter (default: 0.992).

    Returns:
        A list of scores indicating the likelihood of each position being in an exon.
    """
    # Convert DNA sequence to complex numerical representation
    numeric_sequence = complex_representation(sequence)

    # Design the anti-notch filter
    b = [1, -2, 1]  # Numerator coefficients
    a = [1, -2 * r * np.cos(2 * np.pi / 3), r**2]  # Denominator coefficients

    # Apply the filter to the numeric sequence
    filtered_sequence = lfilter(b, a, numeric_sequence)

    # Calculate scores using a sliding window
    scores = []
    for i in range(len(sequence) - window_size + 1):
        window = filtered_sequence[i : i + window_size]
        score = np.sum(np.abs(window)**2)  # Use the sum of squares of the magnitude in the window as the score
        scores.append(score)

    return scores

def classify_exons(sequence, scores, threshold=None):
    """Classifies exons and introns based on 3-base periodicity scores.

    Args:
        sequence: The DNA sequence as a string.
        scores: A list of periodicity scores for each position in the sequence.
        threshold: The threshold for classifying a position as an exon (default: mean of scores).

    Returns:
        A list of tuples indicating the exon/intron label for each position.
    """

    if threshold is None:
        threshold = np.mean(scores)  # Set threshold to the mean of the scores if not provided

    exons = []
    introns = []
    in_exon = scores[0] > threshold

    for i, score in enumerate(scores):
        if score > threshold:
            if not in_exon:
                exons.append((i, i + 1000))  # Assuming exon length of 240 bases
                in_exon = True
        else:
            if in_exon:
                introns.append((i, i + 1000))
                in_exon = False

    return exons, introns

# Leitura do arquivo FASTA
file_name = "/home/ariel/carbon/0X_carbonRascunho/GADPH_transcript.fa"  # Coloque aqui o nome do seu arquivo
with open(file_name, "r") as file:
    # Ignora a primeira linha de descrição e lê a sequência de DNA
    sequence = "".join(line.strip().upper() for line in file if not line.startswith(">"))

# Remove caracteres inválidos da sequência
sequence = "".join(c for c in sequence if c in "ACGT")

# Detecta a periodicidade e classifica exons e introns
scores = detect_periodicity(sequence)
exons, introns = classify_exons(sequence, scores)

print("Exons:", exons)
print("Introns:", introns)

# Calcular e exibir porcentagens
total_regions = len(exons) + len(introns)
if total_regions > 0:
    exon_percentage = (len(exons) / total_regions) * 100
    intron_percentage = (len(introns) / total_regions) * 100

    print(f"\nPercentage of Exons: {exon_percentage:.2f}%")
    print(f"Percentage of Introns: {intron_percentage:.2f}%")
else:
    print("No regions classified.")

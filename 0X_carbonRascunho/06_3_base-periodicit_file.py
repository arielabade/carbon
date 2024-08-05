import numpy as np
from scipy.signal import lfilter
from scipy.fft import fft, ifft

def read_sequence_from_file(file_path):
    """Reads a DNA sequence from a file."""
    with open(file_path, 'r') as file:
        sequence = file.read().replace('\n', '')
    return sequence

def detect_periodicity(sequence, window_size=240, r=0.992):
    """Detects 3-base periodicity in a DNA sequence using digital filtering.

    Args:
        sequence: The DNA sequence as a string (e.g., "ATCGGACT...").
        window_size: The size of the sliding window (default: 240).
        r: The pole radius of the anti-notch filter (default: 0.992).

    Returns:
        A list of scores indicating the likelihood of each position being in an exon.
    """

    # Convert DNA sequence to numerical representation (EIIP values)
    eiip_values = {"A": 0.1260, "C": 0.1340, "G": 0.0806, "T": 0.1335, "N": 0.1000}  # Add a value for 'N'
    numeric_sequence = np.array([eiip_values.get(base, 0) for base in sequence])

    # Design the anti-notch filter
    b = [1, -2, 1]  # Numerator coefficients
    a = [1, -2 * r * np.cos(2 * np.pi / 3), r**2]  # Denominator coefficients

    # Apply the filter to the numeric sequence
    filtered_sequence = lfilter(b, a, numeric_sequence)

    # Calculate scores using a sliding window
    scores = []
    for i in range(len(sequence) - window_size + 1):
        window = filtered_sequence[i : i + window_size]
        score = np.max(window)  # Use the maximum value in the window as the score
        scores.append(score)

    return scores

def classify_exons(sequence, scores, threshold=0.5):
    """Classifies exons and introns based on 3-base periodicity scores.

    Args:
        sequence: The DNA sequence as a string.
        scores: A list of periodicity scores for each position in the sequence.
        threshold: The threshold for classifying a position as an exon (default: 0.5).

    Returns:
        A list of tuples indicating the exon/intron label for each position.
    """

    exons = []
    introns = []
    for i, score in enumerate(scores):
        if score > threshold:
            exons.append((i, i + 240))  # Assuming exon length of 240 bases
        else:
            introns.append((i, i + 240))

    return exons, introns

# Example usage
file_path = '/home/ariel/carbon/0X_carbonRascunho/GADPH_test.fa'  # Replace with your actual file path
sequence = read_sequence_from_file(file_path)
sequence = "".join(c for c in sequence if c in "ACGT")  # Remove invalid characters


scores = detect_periodicity(sequence)
exons, introns = classify_exons(sequence, scores)

print("Exons:", exons)
print("Introns:", introns)

# Calculate and display percentages
total_regions = len(exons) + len(introns)
exon_percentage = (len(exons) / total_regions) * 100
intron_percentage = (len(introns) / total_regions) * 100

print(f"\nPercentage of Exons: {exon_percentage:.2f}%")
print(f"Percentage of Introns: {intron_percentage:.2f}%")

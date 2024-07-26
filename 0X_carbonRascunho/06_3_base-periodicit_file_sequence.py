import numpy as np
import pandas as pd
import altair as alt
from spectrum import arburg
from scipy.signal import get_window
from scipy.fft import fft

def read_sequence(file_path):
    """Reads and cleans a DNA sequence from a FASTA file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    sequence = "".join(lines[1:]).replace("\n", "")  # Assuming FASTA format
    return "".join(c for c in sequence if c in "ACGT")  # Keep only valid bases

def sequence_to_eiip(sequence):
    """Converts a DNA sequence to a numerical representation using EIIP values."""
    eiip_values = {"A": 0.1260, "C": 0.1340, "G": 0.0806, "T": 0.1335}
    return np.array([eiip_values.get(base, 0) for base in sequence])

def apply_ar_model(numeric_sequence, order=90):
    """Applies an autoregressive (AR) model to the numeric sequence."""
    ar_model = arburg(numeric_sequence, order)
    return ar_model[0], ar_model[3]  # Retorna os coeficientes AR e a variância do ruído

def calculate_periodicity_scores(ar_coeffs, noise_variance, window_size=240):
    """Calculates periodicity scores using AR model and FFT."""
    kaiser_window = get_window(('kaiser', 5), window_size)
    scores = []
    for i in range(len(ar_coeffs) - window_size + 1):
        window_coeffs = ar_coeffs[i: i + window_size]
        window_noise_var = noise_variance[i: i + window_size]
        spectrum = []
        for coeffs, var in zip(window_coeffs, window_noise_var):
            _, psd = arburg(coeffs, len(coeffs) - 1, var)
            spectrum.append(psd)
        spectrum = np.array(spectrum)
        max_peak = np.max(spectrum[10:len(spectrum) // 2])  # Ignora frequências baixas
        scores.append(max_peak)
    return scores

def classify_regions(scores, threshold=0.5, region_size=240):
    """Classifies regions as exons or introns based on periodicity scores."""
    exons = []
    introns = []
    for i, score in enumerate(scores):
        start = i * region_size
        end = start + region_size
        if score > threshold:
            exons.append((start, end))
        else:
            introns.append((start, end))
    return exons, introns

def calculate_percentages(exons, introns):
    """Calculates the percentage of exons and introns."""
    total_regions = len(exons) + len(introns)
    exon_percentage = (len(exons) / total_regions) * 100 if total_regions > 0 else 0
    intron_percentage = (len(introns) / total_regions) * 100 if total_regions > 0 else 0
    return exon_percentage, intron_percentage

def read_fasta(file_path):
    """Lê um arquivo FASTA e retorna um dicionário com as sequências."""
    sequences = {}
    with open(file_path, 'r') as file:
        current_identifier = None
        current_sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if current_identifier is not None:
                    sequences[current_identifier] = current_sequence
                current_identifier = line[1:]
                current_sequence = ""
            else:
                current_sequence += line
        sequences[current_identifier] = current_sequence
    return sequences

def plot_results(sequence, scores, exons, introns, identifier):
    """Plota o espectro de potência e marca as regiões de exons e íntrons."""
    positions = list(range(len(scores)))
    data = pd.DataFrame({
        'Position': positions,
        'Signal': eiip_encode(sequence)[:len(scores)],  # Ajusta o tamanho do sinal
        'AR Power Spectrum': scores,
        'Region': ['Exon' if any(start <= pos < end for start, end in exons) else 'Intron' for pos in positions]
    })

    base = alt.Chart(data).encode(
        x='Position',
        tooltip = ['Position']
    )

    signal_line = base.mark_line(color='blue').encode(
        y='Signal',
        tooltip = ['Position','Signal']
    )

    ar_line = base.mark_line(color='red').encode(
        y='AR Power Spectrum',
        tooltip = ['Position','AR Power Spectrum']
    )

    regions = base.mark_rect().encode(
        y=alt.Y('Region:N', axis=alt.Axis(title='Region')),
        y2=alt.Y2('Region:N'),
        color='Region:N',
        tooltip = ['Region']
    )

    chart = alt.layer(signal_line, ar_line, regions).resolve_scale(
        y = 'independent'
    ).properties(
        title=f'Análise da sequência: {identifier}'
    ).interactive()

    chart.save(f'sequencia_{identifier}_plot.json')

# Main execution
file_path = input("Digite o caminho para o arquivo FASTA: ")  # ou file_path = 'seu_arquivo.fa'
sequences = read_fasta(file_path)
for identifier, sequence in sequences.items():
    numeric_sequence = sequence_to_eiip(sequence)
    ar_coeffs, noise_variance = apply_ar_model(numeric_sequence)
    scores = calculate_periodicity_scores(ar_coeffs, noise_variance)
    exons, introns = classify_regions(scores)
    exon_percentage, intron_percentage = calculate_percentages(exons, introns)

    print(f"Sequência: {identifier}")
    print("Exons:", exons)
    print("Introns:", introns)
    print(f"Percentage of Exons: {exon_percentage:.2f}%")
    print(f"Percentage of Introns: {intron_percentage:.2f}%\n")

    plot_results(sequence, scores, exons, introns, identifier)

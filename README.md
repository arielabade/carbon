Claro! Aqui está o **README reescrito**, incorporando as informações do artigo e detalhando melhor o processo de **ETL (Extract, Transform, Load)** com base no que foi descrito no estudo:

---

# RNN-Based Machine Learning Model for Exon and Intron Classification

This repository implements a Bidirectional LSTM (BI-LSTM) model for classifying exonic and intronic regions in DNA sequences. The project includes the full ETL pipeline, dataset, baseline model comparisons, and hyperparameter optimization inspired by the research presented in the 2025 ICPRAM conference.

## Table of Contents
1. [Model Overview](#model-overview)
2. [ETL Pipeline (Data Preparation)](#etl-pipeline-data-preparation)
3. [Baseline Evaluation](#baseline-evaluation)
4. [Data Description](#data-description)
5. [Conclusion](#conclusion)
6. [License](#license)

---

## Model Overview

The final model is a **Bidirectional Long Short-Term Memory (BI-LSTM)** network optimized for recognizing nucleotide patterns in gene sequences.

### Model Architecture
- **Input**: DNA sequences in CSV format, containing exon/intron binary labels (1 = exon, 0 = intron).
- **Layers**:
  - Three **Bi-LSTM** layers with [64, 64, 32] neurons respectively.
  - **ReLU** activation functions.
  - **Dropout layer** after each Bi-LSTM and Dense layer (dropout rate: 0.2).
- **Optimizer**: **Adam**, with a learning rate of 0.001.
- **Batch Size**: 16
- **Epochs**: 30
- **Loss Function**: Binary cross-entropy

---

## ETL Pipeline (Data Preparation)

The dataset preparation followed a detailed **ETL pipeline**, transforming raw biological data into a structured format suitable for deep learning:

### 1. Extract
- Source: **Ensembl Genome Browser (2024)**
- Format: **FASTA** files containing DNA sequences of 8 human genes
- Genes: ANKRD1, PGK1, B2M, GAPDH, PPIA, RPLA13A, NEB, TTN

### 2. Transform
Conversion of raw FASTA files into a **structured CSV** format, involving:
- **Parsing headers** to extract gene names and exon/intron labels using regex.
- **Segmenting sequences** by exon and intron regions.
- **Metadata inclusion**: gene ID, exon/intron flags, start/end positions.
- **Binary classification labeling**: exon = 1, intron = 0.
- **Sequence length calculation** for each segment.
- **Standardization** of input format for model compatibility.

Example CSV columns:
- `Gene name`, `Gene ID`, `Flag`, `Length`, `Start Position`, `End Position`, `Sequence`

➡️ Data transformation script: [featureExtraction.py](https://github.com/arielabade/carbon/blob/main/code/dataPreparation/featureExtraction.py)

### 3. Load
- Transformed data split into **train (80%)**, **validation (10%)**, and **test (10%)** sets.
- Only the `Sequence` and `Flag` columns are used for model training.

---

## Baseline Evaluation

The BI-LSTM model was compared against three RNN variants: Simple RNN, LSTM, and GRU. Accuracy was the primary metric, but other evaluation metrics were also considered.

| Model        | Accuracy | Precision | Sensitivity (Recall) | Specificity | F1-Score |
|--------------|----------|-----------|----------------------|-------------|----------|
| Simple RNN   | 0.6820   | 0.6216    | 0.9981               | 0.3375      | 0.7661   |
| LSTM         | 0.9860   | 0.9810    | 0.9923               | 0.9790      | 0.9866   |
| GRU          | 0.9960   | 0.9981    | 0.9942               | 0.9979      | 0.9961   |
| **BI-LSTM**  | **0.9980** | **1.0000**  | **0.9961**             | **1.0000**    | **0.9981** |

Model scripts:
- [Simple RNN](https://github.com/arielabade/carbon/blob/main/code/baselineEvaluation/60epochs/simpleRNN60epochs.py)
- [LSTM](https://github.com/arielabade/carbon/blob/main/code/baselineEvaluation/60epochs/lstm60epochs.py)
- [GRU](https://github.com/arielabade/carbon/blob/main/code/baselineEvaluation/60epochs/GRU60epochs.py)
- [BI-LSTM](https://github.com/arielabade/carbon/blob/main/code/baselineEvaluation/60epochs/biLSTM30epochs.py)

---

## Data Description

The dataset includes **9,971 sequences** from 8 human genes:

| Gene     | Exons | Introns | Total Sequences | Exonic Bases | Intronic Bases |
|----------|-------|---------|------------------|---------------|----------------|
| ANKRD1   | 9     | 8       | 17               | 1,790         | 7,202          |
| PGK1     | 37    | 31      | 68               | 9,539         | 339,889        |
| B2M      | 40    | 28      | 68               | 10,553        | 51,222         |
| GAPDH    | 79    | 68      | 147              | 13,269        | 21,371         |
| PPIA     | 80    | 62      | 142              | 34,258        | 80,547         |
| RPLA13A  | 123   | 101     | 224              | 29,782        | 54,231         |
| NEB      | 844   | 823     | 1,667            | 119,394       | 1,106,064      |
| TTN      | 3,822 | 3,807   | 7,629            | 1,247,226     | 2,273,905      |
| **Total**| 5,034 | 4,928   | **9,971**         | 1,469,811     | 3,885,762      |

➡️ Data files: [FASTA and CSV](https://github.com/arielabade/carbon/tree/main/data)

---

## Conclusion

The BI-LSTM model achieved superior performance compared to other RNN-based models in exon and intron classification, reaching an accuracy of **0.9980**. This supports its use as a reliable tool for DNA sequence analysis in bioinformatics and genomic medicine.

The complete ETL process and model training code are available to ensure **reproducibility** and **transparency**, addressing a key limitation in prior studies.

For more information, contact **arielabadebandeira@gmail.com**


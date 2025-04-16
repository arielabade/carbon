Perfeito! Abaixo está a versão atualizada do seu `README.md`, agora incorporando seções e conteúdos sobre **ETL**, **data transformation**, **visualization**, e **machine learning model composition**, todos de forma integrada e objetiva, mantendo o tom científico em inglês.

---

# BI-LSTM Recurrent Neural Network for Exon and Intron Classification Using Nucleotide Sequence Analysis

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#)

## 🔬 Overview

This study implements a **Bidirectional LSTM (BI-LSTM)** model to classify **exonic** and **intronic** regions in DNA sequences. The dataset was sourced from the [Ensembl Genome Browser](https://www.ensembl.org), and the model was compared against Simple RNN, GRU, and LSTM baselines.

> **Top accuracy achieved:** `0.9980` with BI-LSTM.

## 📌 Keywords

Bioinformatics, Sequence Classification, RNN, Genomic Analysis, BI-LSTM, ETL, Data Visualization, Deep Learning

---

## 📖 Introduction

Exon/intron classification is crucial for gene structure analysis, disease prediction, and drug development. Deep learning models such as RNNs, GRUs, LSTMs, and transformer-based approaches (e.g., DNABert, GeneGPT) have shown promising results in identifying genomic patterns.

---

## ⚙️ Methodology

### 1. Data Gathering (ETL Step 1: Extract)

Eight **Homo sapiens** genes were selected from the Ensembl transcript database. Data were retrieved in FASTA format, containing labeled exon and intron regions.

| Gene | Exonic Sequences | Intronic Sequences | Exonic Bases | Intronic Bases |
|------|------------------|--------------------|--------------|----------------|
| ANKRD1-201 | 9 | 8 | 1,790 | 7,202 |
| PGK1-206 | 37 | 31 | 9,539 | 339,889 |
| B2M-212 | 40 | 28 | 10,553 | 51,222 |
| GAPDH-203 | 79 | 68 | 13,269 | 21,371 |
| PPIA-207 | 80 | 62 | 34,258 | 80,547 |
| RPLA13A-222 | 123 | 101 | 29,782 | 54,231 |
| NEB-203 | 844 | 823 | 119,394 | 1,106,064 |
| TTN-201 | 3,822 | 3,807 | 1,247,226 | 2,273,905 |
| **Total** | **5,034** | **4,928** | **1,469,811** | **3,885,762** |

---

### 2. Data Transformation & Preparation (ETL Step 2–3: Transform & Load)

The raw FASTA data was transformed and structured in CSV format for ML processing:

- Metadata extraction (gene ID, region type)
- Binary labeling: `1 = exon`, `0 = intron`
- Sequence segmentation and masking
- Length and position calculation
- Final structure used for modeling:

| Gene | Flag | Length | Start | End | Sequence |
|------|------|--------|-------|-----|----------|
| ANKRD1-201 | 1 | 87 | 0 | 86 | AGGGCCAA... |
| PPIA-207 (intron) | 0 | 1412 | 95411 | 96822 | GTAAGGGT... |

This process ensures compatibility with deep learning frameworks while preserving sequence integrity.

---

### 3. Machine Learning Model Architecture

The classification models were implemented in TensorFlow using Keras. We tested the following RNN-based architectures:

- **Simple RNN** – for baseline sequential modeling
- **GRU** – incorporating update/reset gates
- **LSTM** – handling long-term dependencies
- **BI-LSTM** – bidirectional context for optimal performance

Each model received only the sequence and flag columns as input features.

---

### 4. Hyperparameter Tuning

Grid search was conducted across 324 combinations. The best BI-LSTM configuration:

| Parameter   | Chosen Value |
|-------------|--------------|
| Activation  | ReLU         |
| Optimizer   | Adam         |
| Neurons     | 64           |
| Dropout     | 0.2          |
| Batch Size  | 16           |

Training was limited to 30 epochs, with early stopping based on validation loss convergence.

---

### 5. Evaluation Metrics

| Model       | Accuracy | Precision | Sensitivity | Specificity | F1-score |
|-------------|----------|-----------|-------------|-------------|----------|
| **BI-LSTM** | **0.9980** | **1.0000** | **0.9961**  | **1.0000**  | **0.9981** |
| GRU         | 0.9960   | 0.9981    | 0.9942      | 0.9979      | 0.9961   |
| LSTM        | 0.9860   | 0.9810    | 0.9923      | 0.9790      | 0.9866   |
| Simple RNN  | 0.6820   | 0.6216    | 0.9981      | 0.3375      | 0.7661   |

---

## 📊 Results

The **BI-LSTM model** demonstrated superior performance across all metrics. Its bidirectional design captured long-range dependencies more effectively than other models.

### Training Metrics – BI-LSTM

- **Accuracy across epochs**  
  ![BI-LSTM Accuracy](./images/accuracy.png)

- **Loss across epochs**  
  ![BI-LSTM Loss](./images/loss.png)

These visualizations confirm a stable training process with high convergence and no significant overfitting.

---

## 📉 Data Visualization

To better understand data distribution and model input characteristics, the dataset was also analyzed through graphical summaries:

- Stacked bar plots showing base count distributions across training, validation, and test sets
- Exon/intron proportion analysis by gene
- Visualization of sequence length distributions (not shown here)

These visualizations provide context for dataset balance and feature integrity before model ingestion.

---

## 📈 Comparison with Related Studies

| Model/Study                        | Accuracy | Methodology                       |
|-----------------------------------|----------|-----------------------------------|
| **This Study**                    | **0.9980** | BI-LSTM                          |
| Canatalay & Ucan (2022)           | 0.9610   | BI-LSTM + GRU ensemble            |
| Gunasekaran et al. (2021)         | 0.9316   | CNN                              |
| Barber & Oueslati (2024)          | 0.9160   | ResNet-50 + GoogleNet            |
| Ben Nasr & Oueslati (2021)        | 0.8910   | CNN                              |
| Sudha & Vijaya (2022)             | 0.8488   | LSTM + DNN + BRNN                |

---

## ✅ Conclusions

- The **BI-LSTM** model achieved the highest accuracy in both internal and external benchmarks.
- Its ability to model bidirectional context is well-suited for exon/intron sequence classification.
- Future improvements may include:
  - Ensemble models with GRU/CNN layers
  - Incorporation of biological features (e.g., codon periodicity)

---

## 📁 Dataset & Code

> Dataset and source code are available at:  
> [https://github.com/your-username/your-repo](https://github.com/your-username/your-repo)

---

## 📚 References

For a full list of references and datasets used, consult the publication attached to this repository.

---

Let me know if you want this exported as a `README.md` file or need help creating the graphics mentioned in the visualization section.

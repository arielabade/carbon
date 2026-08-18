## 🧬 Exon & Intron Classification Using BI-LSTM | Genomic Sequence Analysis with Deep Learning

This project implements a Bidirectional LSTM (BI-LSTM) neural network to classify exonic and intronic regions in human DNA sequences using character-level sequence modeling. It includes a complete ETL pipeline, dataset preprocessing from FASTA to CSV, baseline model comparisons (RNN, LSTM, GRU), and visualization of training progress.

Originally developed for a scientific paper accepted at a bioinformatics conference in Portugal, the project focuses on reproducibility and performance benchmarking using real-world genomic data sourced from the Ensembl Genome Browser.

## Table of Contents
1. [Model Overview](#model-overview)
2. [ETL Pipeline (Data Preparation)](#etl-pipeline-data-preparation)
3. [Final BI-LSTM Model Architecture](#final-bi-lstm-model-architecture)
4. [Baseline Evaluation](#baseline-evaluation)
5. [Literature Benchmarking](#literature-benchmarking)
6. [Data Description](#data-description)
7. [Conclusion](#conclusion)
8. [References](#references)
9. [License](#license)

---

## Model Overview

The goal of this project is to accurately distinguish between **exons (coding regions)** and **introns (non-coding regions)** in DNA sequences using deep learning techniques. Among several models tested, the **BI-LSTM** architecture showed the best performance in terms of accuracy and generalization.

---

## ETL Pipeline (Data Preparation)

The ETL pipeline was designed to transform raw biological data from the **FASTA** format into a format compatible with RNN-based models.

### 1. Extract
- **Source**: [Ensembl Genome Browser](https://www.ensembl.org)
- **Genes included**: `ANKRD1`, `PGK1`, `B2M`, `GAPDH`, `PPIA`, `RPLA13A`, `NEB`, `TTN`
- **Format**: FASTA files containing nucleotide sequences labeled by region (exon/intron)

### 2. Transform
Each FASTA file was parsed and transformed into a structured CSV file, following these steps:
- **Gene label extraction** using regex from FASTA headers
- **Binary labeling**: exon = 1, intron = 0
- **Intron masking** for gene IDs not present in intronic regions
- **Feature engineering**: adding metadata such as `start`, `end`, `length`, and `sequence`
- **Cleaning** and standardization to create uniform-length input sequences

🛠️ Code: [featureExtraction.py](data/featureExtraction/featureExtraction.py)

### 3. Load
- After preprocessing, sequences were tokenized (character-level) and padded to a **maximum length of 500** nucleotides.
- Data was split using `train_test_split`:
  - 80% Training
  - 10% Validation
  - 10% Testing
- Sequences were processed in **chunks of 1000** to improve memory efficiency.

![Train/Validation/Test Split](images/trainTestValidation.png)

---

## Final BI-LSTM Model Architecture

The final model was implemented using **TensorFlow and Keras**, with the following structure:

| Layer                  | Configuration                                                      |
|------------------------|--------------------------------------------------------------------|
| **Embedding**          | `input_dim = vocab_size`, `output_dim = 32`, `input_length = 500` |
| **Bi-LSTM Layer 1**    | 32 units, `return_sequences=True`                                 |
| **Dropout Layer**      | Dropout rate = 0.2                                                 |
| **Bi-LSTM Layer 2**    | 32 units                                                           |
| **Dropout Layer**      | Dropout rate = 0.2                                                 |
| **Dense Layer**        | 64 units, `activation='relu'`                                     |
| **Output Layer**       | 1 unit, `activation='sigmoid'`                                     |

### Training Details
- **Epochs**: 60
- **Batch Size**: 16
- **Optimizer**: Adam (default learning rate)
- **Loss Function**: Binary Crossentropy
- **Tokenization**: Character-level (A, T, G, C, etc.)
- **Padding**: Post-padding of sequences up to 500 characters
- **Evaluation Metrics**: Accuracy, Precision, Sensitivity (Recall), Specificity, F1-Score

### Visualization
The training process includes real-time visualization of:
- **Training vs. Validation Loss**
- **Training vs. Validation Accuracy**

![trainingAndLossValidation](images/validationLossBIlstm.png)


📈 These plots confirm that the model generalizes well without overfitting, respecting the converging graphics between validation and loss.

---

## Baseline Evaluation

To validate the BI-LSTM model, it was compared with three other RNN-based architectures: **Simple RNN**, **LSTM**, and **GRU**. All models were trained under the same conditions and evaluated on the same dataset splits.

| Model        | Accuracy | Precision | Sensitivity | Specificity | F1-Score |
|--------------|----------|-----------|-------------|-------------|----------|
| Simple RNN   | 0.6820   | 0.6216    | 0.9981      | 0.3375      | 0.7661   |
| LSTM         | 0.9860   | 0.9810    | 0.9923      | 0.9790      | 0.9866   |
| GRU          | 0.9960   | 0.9981    | 0.9942      | 0.9979      | 0.9961   |
| **BI-LSTM**  | **0.9980** | **1.0000** | **0.9961**   | **1.0000**   | **0.9981** |

📁 Scripts for each model:
- [Simple RNN](code/baselineEvaluation/60epochs/simpleRNN60epochs.py)
- [LSTM](code/baselineEvaluation/60epochs/lstm60epochs.py)
- [GRU](code/baselineEvaluation/60epochs/GRU60epochs.py)
- [BI-LSTM](code/biLSTM/carbonFinalModel.py)

## Literature Benchmarking

The following table compares the proposed BI-LSTM with the local baselines and with related studies identified in the supplied paper source (`Main.tex` and `refs.bib`). Accuracy is the only metric reported consistently enough for a cross-study comparison.

### Controlled benchmark on the project dataset

All local models use the same human-gene dataset, character-level tokenization, 80/10/10 train-validation-test split, and binary exon/intron labels. The values below are the reported test-set results.

| Rank | Model | Accuracy | Precision | Sensitivity | Specificity | F1-score | Local implementation |
|------|-------|----------|-----------|-------------|-------------|----------|----------------------|
| 1 | **Proposed BI-LSTM** | **0.9980** | **1.0000** | **0.9961** | **1.0000** | **0.9981** | [`carbonFinalModel.py`](code/biLSTM/carbonFinalModel.py) |
| 2 | GRU | 0.9960 | 0.9981 | 0.9942 | 0.9979 | 0.9961 | [`GRU60epochs.py`](code/baselineEvaluation/60epochs/GRU60epochs.py) |
| 3 | LSTM | 0.9860 | 0.9810 | 0.9923 | 0.9790 | 0.9866 | [`lstm60epochs.py`](code/baselineEvaluation/60epochs/lstm60epochs.py) |
| 4 | Simple RNN | 0.6820 | 0.6216 | 0.9981 | 0.3375 | 0.7661 | [`simpleRNN60epochs.py`](code/baselineEvaluation/60epochs/simpleRNN60epochs.py) |

### Cross-study literature context

These results must not be interpreted as a strict leaderboard: the studies use different organisms, gene sets, sequence encodings, train/test protocols, and sometimes a related prediction task rather than the same exon/intron classification problem. The external values are reported results, not re-runs of their models in this repository.

| Study / model | Task and representation | Reported accuracy | Comparison status | Reference |
|---------------|------------------------|-------------------|-------------------|-----------|
| **This repository — BI-LSTM** | Human exon/intron classification; Ensembl sequences; character-level encoding | **99.80%** | Reproduced locally | [`carbonFinalModel.py`](code/biLSTM/carbonFinalModel.py) |
| Singh, Nath & Singh (2021) — BI-LSTM-RNN | Human exon/intron prediction using splice-site signals and NCBI data | 96.00% | Related task; reported result | [IJETER paper](https://doi.org/10.30534/ijeter/2021/20932021) |
| Canatalay & Ucan (2022) — BI-LSTM/GRU | Exon prediction using splice-site mapping | 96.10% | Related task; reported result | [Applied Sciences paper](https://doi.org/10.3390/app12094390) |
| Gunasekaran et al. (2021) — CNN | General DNA sequence classification with label/k-mer encoding | 93.16% | Different classification scope; reported result | [Computational and Mathematical Methods in Medicine](https://doi.org/10.1155/2021/1835056) |
| Ben Nasr & Oueslati (2021) — CNN | Human exon/intron classification | ~90.00% | Same broad task; reported result | [SSD conference paper](https://doi.org/10.1109/SSD52085.2021.9429303) |
| Ben Nasr Barber & Oueslati (2024) — ResNet-50 | Human exon/intron classification from FCGR images | 92.00% | Same broad task; reported result | [Journal of Genetic Engineering and Biotechnology](https://doi.org/10.1016/j.jgeb.2024.100359) |
| Akalın & Yumuşak (2024) — SBERT + ANFIS | Exon/intron classification for BCR-ABL and MEFV sequences | 88.88% | Different genes and representation; reported result | [Journal of Polytechnic](https://doi.org/10.2339/politeknik.1187808) |

The local BI-LSTM leads the controlled benchmark at 99.80% accuracy. The literature comparison suggests strong performance relative to the cited studies, but the differences in datasets and experimental protocols mean that the controlled local comparison is the scientifically stronger claim.

---

## Data Description

The final dataset included **9,971 sequences**, evenly distributed between exons and introns, from eight genes. The sequences were balanced in quantity and diversity to ensure generalization.

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

📂 Data files (FASTA and CSV): [Available here](https://github.com/arielabade/carbon/tree/main/data)

---

## Conclusion

The **BI-LSTM** architecture demonstrated superior performance in distinguishing exons from introns, with a final accuracy of **99.80%**. This positions it as a strong candidate for use in bioinformatics pipelines, gene structure analysis, and even medical genomics research.

The project emphasizes:
- 🔍 Transparency via open-source code and data
- 🔁 Reproducibility through complete ETL steps
- 📈 Scientific rigor in metric evaluation and cross-model comparison

## References

The references below were extracted from the `refs.bib` file in the supplied ZIP archive and checked against the linked publisher, DOI, repository, or conference records. The final column records how each reference relates to this repository's files.

| Reference | Contribution to this project | Repository association |
|-----------|-----------------------------|------------------------|
| [Ensembl, *Homo sapiens Ensembl database*](https://www.ensembl.org/) | Source of the human genomic records used by the ETL pipeline. | [`data/fastaData/`](data/fastaData/), [`data/featureExtraction/featureExtraction.py`](data/featureExtraction/featureExtraction.py) |
| [Long & Deutsch (1999), *Intron-exon structures of eukaryotic model organisms*](https://doi.org/10.1093/nar/27.15.3219) | Biological background for exon/intron structure. | README background; no direct implementation. |
| [Abo-Zahhad, Ahmed & Abd-Elrahman (2012), *Genomic Analysis and Classification of Exon and Intron Sequences Using DNA Numerical Mapping Techniques*](https://doi.org/10.5815/ijitcs.2012.08.03) | Motivation for representing nucleotide sequences and classifying exon/intron regions. | [`data/featureExtraction/featureExtraction.py`](data/featureExtraction/featureExtraction.py), [`data/fastaData/`](data/fastaData/), [`data/csvData/`](data/csvData/) |
| [Mabrouk (2014), *A Novel Circular Mapping Technique for Spectral Classification of Exons and Introns in DNA Sequences*](https://doi.org/10.5815/ijitcs.2014.04.02) | Alternative DNA representation discussed in the paper. | Literature context only; no spectral-mapping implementation. |
| [Singh & Srivastava (2020), *The Three Base Periodicity of Protein Coding Sequences and its Application in Exon Prediction*](https://doi.org/10.1109/SPIN48934.2020.9071068) | Candidate biological feature for future feature engineering. | Future-work context; no periodicity feature file. |
| [Singh, Nath & Singh (2021), *Prediction of Eukaryotic Exons Using Bidirectional LSTM-RNN Based Deep Learning Model*](https://doi.org/10.30534/ijeter/2021/20932021) | Prior BI-LSTM-RNN exon-prediction architecture and external benchmark. | [`code/biLSTM/carbonFinalModel.py`](code/biLSTM/carbonFinalModel.py) |
| [Canatalay & Ucan (2022), *A Bidirectional LSTM-RNN and GRU Method to Exon Prediction Using Splice-Site Mapping*](https://doi.org/10.3390/app12094390) | Closest architectural reference for the BI-LSTM/GRU comparison. | [`code/biLSTM/carbonFinalModel.py`](code/biLSTM/carbonFinalModel.py), [`code/baselineEvaluation/60epochs/GRU60epochs.py`](code/baselineEvaluation/60epochs/GRU60epochs.py) |
| [Gunasekaran et al. (2021), *Analysis of DNA Sequence Classification Using CNN and Hybrid Models*](https://doi.org/10.1155/2021/1835056) | CNN and hybrid-model comparison for DNA sequence classification. | Benchmark context; no CNN implementation in this repository. |
| [Ben Nasr & Oueslati (2021), *CNN for Human Exons and Introns Classification*](https://doi.org/10.1109/SSD52085.2021.9429303) | CNN-based exon/intron baseline from the literature. | Benchmark context; no CNN implementation in this repository. |
| [Ben Nasr Barber & Oueslati (2024), *Human Exons and Introns Classification Using Pre-trained ResNet-50 and GoogleNet Models and 13-layers CNN Model*](https://doi.org/10.1016/j.jgeb.2024.100359) | Image-based CNN, ResNet-50, and GoogleNet alternatives. | Benchmark context; no image-model implementation in this repository. |
| [Akalın & Yumuşak (2024), *Classification of Exon and Intron Regions on DNA Sequences with Hybrid Use of SBERT and ANFIS Approaches*](https://doi.org/10.2339/politeknik.1187808) | Hybrid embedding/fuzzy-inference alternative using codon frequencies. | Benchmark context; no SBERT/ANFIS implementation in this repository. |
| [Sudha & Vijaya (2022), *Recurrent Neural Network Based Model for Autism Spectrum Disorder Prediction Using Codon Encoding*](https://doi.org/10.1007/s40031-021-00669-4) | Related recurrent/codon-encoding methodology; its target is gene/ASD classification rather than exon/intron classification. | [`code/baselineEvaluation/60epochs/lstm60epochs.py`](code/baselineEvaluation/60epochs/lstm60epochs.py) as architectural context only. |
| [Hill et al. (2018), *A Deep Recurrent Neural Network Discovers Complex Biological Rules to Decipher RNA Protein-Coding Potential*](https://doi.org/10.1093/nar/gky567) | Background for recurrent models learning biological sequence patterns. | [`code/biLSTM/carbonFinalModel.py`](code/biLSTM/carbonFinalModel.py) as methodological context. |
| [Ji et al. (2021), *DNABERT: Pre-trained Bidirectional Encoder Representations from Transformers Model for DNA-language in Genome*](https://doi.org/10.1093/bioinformatics/btab083) | Transformer-based alternative discussed in the paper. | Literature context only; no DNABERT implementation. |
| [Poddar et al. (2023), *Identifying DNA Sequence Motifs Using Deep Learning: DeepDeCode Model for Splice Site Prediction*](https://arxiv.org/abs/2311.12884) | Attention/deep-learning direction for splice-site prediction. | Literature context only; no DeepDeCode implementation. |

References such as BERT, GPT-4, ResNet-50, GoogleNet, GeneGPT, Ritch et al., and Quazi are retained as broader methodological or biomedical context in the source paper; they are not direct implementations or controlled baselines in this repository.

# 📝 Notes

    This project was developed as part of a research initiative and was accepted for presentation at an international conference in Portugal.
    To access the full paper, feel free to contact me via email: arielabadebandeira@gmail.com

    One of the main challenges during development was finding comparable research papers with similar approaches and consistent evaluation metrics.

    Another significant difficulty was obtaining reliable and publicly available genomic datasets, especially for cross-testing against other models.

    Most related studies used in-house datasets and unfortunately did not provide access to their training or testing data, nor the full implementation details.
    As a result, it was difficult to establish fair comparisons or assess how well those external models actually performed in practice.

📬 For more information, contact: **arielabadebandeira@gmail.com**

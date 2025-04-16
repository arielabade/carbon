# RNN-Based Machine Learning Model for Exon and Intron Classification

This repository provides a Recurrent Neural Network (RNN) model specifically designed to classify exons and introns, including the datasets used and baseline evaluations of multiple model architectures.

## Table of Contents
1. [Model Overview](#model-overview)
2. [Baseline Evaluation](#baseline-evaluation)
3. [Data Description](#data-description)
4. [License](#license)

---

### Model Overview

The final model is a Bidirectional Long Short-Term Memory (BI-LSTM) network, optimized for recognizing sequential patterns within the data.

**Model Architecture**:
- **Input**: A CSV file containing exon/intron sequences with a binary label for classification. Originally, the data was in the FASTA format but it had to be adapted to fit the RNN input format. The link for the data preparation code is [here](https://github.com/arielabade/carbon/blob/main/code/dataPreparation/featureExtraction.py).
- **Layers**: The model includes three bidirectional LSTM layers, each with a specific neuron configuration: 64 neurons in the first layer, 64 in the second, and 32 in the third, doubling the total neurons per layer due to the bidirectional setup.
- **Dropout**: 0.2 Dropout Rate after each Bi-LSTM layer and Dense layer to prevent overfitting by randomly deactivating 20% of the neurons.
- **Activation and Optimzation functions**: the ReLU activation function and Adam optimizator with standard values were used to achieve better results.

### Baseline Evaluation

To evaluate performance, we compared the BI-LSTM with three baseline models (Simple RNN, LSTM, and GRU), selected for their lower computational requirements. The primary evaluation metric was accuracy.

| Model        | Accuracy | Precision | Recall | Specificity | F1-Score |
|--------------|----------|-----------|--------|-------------|----------|
| Simple RNN   | 0.6800   | 0.6206    | 0.9942 | 0.3375      | 0.7642   |
| LSTM         | 0.9910   | 0.9942    | 0.9885 | 0.9937      | 0.9913   |
| GRU          | 0.9970   | 0.9981    | 0.9962 | 0.9979      | 0.9971   |
| BI-LSTM      | 0.9980   | 1.0000    | 0.9961 | 1.0000      | 0.9981   |

- [Simple RNN](https://github.com/arielabade/carbon/blob/main/code/baselineEvaluation/60epochs/simpleRNN60epochs.py).
- [LSTM](https://github.com/arielabade/carbon/blob/main/code/baselineEvaluation/60epochs/lstm60epochs.py).
- [GRU](https://github.com/arielabade/carbon/blob/main/code/baselineEvaluation/60epochs/GRU60epochs.py)
- [BI-LSTM](https://github.com/arielabade/carbon/blob/main/code/baselineEvaluation/60epochs/biLSTM30epochs.py).

### Data Description

The dataset used for training includes exon and intron sequences from eight genes: **Ankyrin Repeat Domain 1 (ANKRD1)**, **Phosphoglycerate Kinase 1 (PGK1)**, **Beta-2-Microglobulin (B2M)**, **Glyceraldehyde-3-Phosphate Dehydrogenase (GADPH)**, **Peptidylprolyl Isomerase A (PPIA)**, **Ribosomal Protein L13A (RPLA13A)**, **Nebulin (NEB)**, and **Titin (TTN)**. Each gene dataset is labeled with *gene name*, *gene identification*, *exon/intron classification*, and *sequence*. Data was sourced from the Ensembl platform.

The data in FASTA format and in the CSV format can be found [here](https://github.com/arielabade/carbon/tree/main/data).


### Conclusion

The BI-LSTM model outperformed the other RNN-based models, making it the preferred choice for exon and intron classification.

For more details, refer to the article:

#hi
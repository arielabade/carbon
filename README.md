# Métodos de Teste para Prevenir Overfitting e Melhorar a Acurácia em Redes Neurais

Estou explorando métodos de teste para prevenir overfitting e melhorar a acurácia em redes neurais, especificamente em redes GRU, que são "featureless". Estou analisando como conseguiram lidar com regiões 3′ UTR, 5′ UTR e CDS em GRUs, usando "Shuffle Analysis" e z-scores para contornar a falta de rotulagem.

## Análise de Mutações

- Utilizo o banco de dados Genecode e analiso mutações específicas.
- Para cada mRNA com comprimento menor que 2000 nt, analiso mutações, incluindo start e stop codons e suas posições.
- Mutações em regiões CDS, 5′ UTR e 3′ UTR são consideradas importantes para a robustez do modelo.

## Métricas e Modelos

- **TIC ("Translation Indicating Codons")** foi uma métrica criada para avaliar exons, focando em codons que indicam a tradução.
- **TIC-score**, uma métrica que considera a ocorrência desses codons dentro de 1000nt após um trinucleotídeo AUG e antes de qualquer stop codon, mostrou-se eficiente em separar mRNAs de lncRNAs.
- Comparei o desempenho de mRNN com outros modelos como CPAT, FEELLnc, e um ensemble de modelos, onde mRNN ensemble teve AUROC de 0.984.

## Motif Scores

- Indicam a probabilidade de uma posição na sequência de DNA ser um sítio de ligação de fator de transcrição (TFBS).
- Pontuações mais altas indicam maior probabilidade de ligação, sendo utilizadas para determinar hits de motivos na sequência de DNA.

## Conclusão

Posso reutilizar os trabalhos existentes sobre mutações e focar na métrica TIC para melhorar as predições no modelo Codan, mantendo a análise detalhada de mutações e codons de parada como base para aumentar a precisão dos modelos preditivos.

Especificação de Software: https://docs.google.com/document/d/1qmJJahj5flkwvH4rx036qLaEHlBHXYmT/edit?usp=sharing&ouid=116786936594225711722&rtpof=true&sd=true 
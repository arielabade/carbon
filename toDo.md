# Organização das Demandas

- [ ] **Arquivo: Sequência Completa**
  - [ ] Identificar onde a sequência é codificante e onde não é.
  - [ ] Localizar os rótulos indicando onde os aminoácidos começam e terminam.
  - [ ] Quebrar o arquivo nas posições necessárias de acordo com a codificação.
  - [ ] Garantir que o teste seja diferente do treino.
  - [ ] Pegar os dados rotulados.

- [ ] **Padding**
  - [ ] Aplicar padding adequado nas sequências para uniformizar os comprimentos.

- [ ] **One Hot Encoding**
  - [ ] Converter as sequências em one hot encoding para preparar os dados para a rede neural.

- [ ] **Embedding**
  - [ ] Adicionar uma camada de embedding para melhorar a representação das sequências.

- [ ] **Configuração da Rede Neural**
  - [ ] Definir o número de camadas da rede neural.
  - [ ] Garantir que os treinamentos incluam exemplos positivos e negativos.
  - [ ] Rodar o modelo DanQ e separar o treinamento para fazer um treinamento balanceado.
  - [ ] Estabelecer onde começam e terminam as sequências.

- [ ] **Treinamento e Avaliação**
  - [ ] Executar treinamentos balanceados com 400 entradas e 100 saídas.
  - [ ] Reconhecer que a rede nunca será melhor que o Codan.

- [ ] **Pré-processamento de Dados**
  - [ ] Realizar o pré-processamento necessário dos dados para otimizar o desempenho da rede.

- [ ] **Branches para Código**
  - [ ] Criar um branch para o código principal.
  - [ ] Criar branches adicionais para operações intermediárias, como data augmentation.

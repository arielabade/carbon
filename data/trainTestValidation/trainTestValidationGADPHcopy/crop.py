import pandas as pd
from sklearn.model_selection import train_test_split

# Passo 1: Ler o arquivo CSV corretamente (supondo que o arquivo já tenha cabeçalhos)
file_path = '/home/ariel/carbon/Data/rnnCSVData/GADPH_test_CORRECTED.csv'  # Substitua pelo caminho do seu arquivo
df = pd.read_csv(file_path)  # Remove header=None, pois estamos assumindo que o CSV tem cabeçalhos

# Adicionar cabeçalhos às colunas, caso eles não estejam no CSV
df.columns = ['gene_name', 'gene_id', 'exon_intron_flag', 'sequence_length', 'start_position', 'end_position', 'sequence']

# Passo 2: Converter colunas específicas para tipos apropriados
df['exon_intron_flag'] = pd.to_numeric(df['exon_intron_flag'], errors='coerce')  # Lida com valores inválidos
df['sequence_length'] = df['sequence_length'].astype(int)
df['start_position'] = df['start_position'].astype(int)
df['end_position'] = df['end_position'].astype(int)

# Verifica se há valores inválidos e os remove (opcional)
df = df.dropna(subset=['exon_intron_flag'])

# As outras colunas podem permanecer como strings (pandas já trata strings por padrão)
df['gene_name'] = df['gene_name'].astype(str)
df['gene_id'] = df['gene_id'].astype(str)
df['sequence'] = df['sequence'].astype(str)

# Passo 3: Dividir os dados em treino (80%) e resto (20%)
train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42)

# Passo 4: Dividir o restante (20%) em teste (10%) e validação (10%)
test_df, val_df = train_test_split(temp_df, test_size=0.5, random_state=42)

# Passo 5: Salvar os três arquivos CSV
train_df.to_csv('/home/ariel/carbon/Data/rnnCSVData/trainTestValidationGADPHcopy/GADPH2train_data.csv', index=False)
test_df.to_csv('/home/ariel/carbon/Data/rnnCSVData/trainTestValidationGADPHcopy/GADPH2test_data.csv', index=False)
val_df.to_csv('/home/ariel/carbon/Data/rnnCSVData/trainTestValidationGADPHcopy/GADPH2val_data.csv', index=False)

print("Divisão concluída e arquivos CSV salvos.")

import pandas as pd
import numpy as np

# ==========================================
# 1. PARÂMETROS FIXOS DO EXPERIMENTO
# ==========================================
C_RES = 4.5          # Capacitância residual em pF (Dados coletados do meu grupo)
SIGMA_C_RES = 0.5    # Incerteza da capacitância residual (Dados coletados do meu grupo)
AREA = 0.02011       # Área das placas em m^2 
SIGMA_AREA = 0.0002  # Incerteza da área 

def calcular_distancia_media(df):
    """Calcula a média das três colunas de distância (d1, d2, d3)."""
    colunas_distancia = df[['d1_mm', 'd2_mm', 'd3_mm']]
    return colunas_distancia.mean(axis=1)

def calcular_incerteza_d(df):
    """
    Calcula o desvio padrão das distâncias medidas.
    O desvio padrão (std) mede o quanto as três medidas (d1, d2, d3) variaram entre si.
    ddof=1 garante que estamos usando a fórmula amostral corretiva.
    """
    colunas_distancia = df[['d1_mm', 'd2_mm', 'd3_mm']]
    return colunas_distancia.std(axis=1, ddof=1)

def calcular_w(distancia_media):
    """Converte a distância para metros inversos (w = 1000 / d)."""
    return 1000 / distancia_media

def calcular_incerteza_w(distancia_media, sigma_d):
    """Aplica a derivada parcial para achar o erro de w: (1000 / d^2) * sigma_d."""
    return (1000 / (distancia_media ** 2)) * sigma_d

def calcular_c_cap(c_medido):
    """Subtrai a capacitância residual do valor medido[cite: 12]."""
    return c_medido - C_RES

def calcular_incerteza_c_cap(sigma_c_medido):
    """Aplica a raiz da soma dos quadrados para propagar o erro de C_cap."""
    return np.sqrt((sigma_c_medido ** 2) + (SIGMA_C_RES ** 2))

def processar_pipeline_dados(caminho_csv):
    """
    Função principal (Pipeline ETL). Carrega o arquivo bruto, aplica as transformações
    físicas e estatísticas, e retorna a tabela final preenchida.
    """
    df = pd.read_csv(caminho_csv, sep=';')
    
    # 1. Tratamento das Distâncias
    df['d_media_mm'] = calcular_distancia_media(df)
    df['sigma_d_mm'] = calcular_incerteza_d(df)
    
    # 2. Transformação para w e sua incerteza
    df['w_m_inv'] = calcular_w(df['d_media_mm'])
    df['sigma_w_m_inv'] = calcular_incerteza_w(df['d_media_mm'], df['sigma_d_mm'])
    
    # 3. Tratamento da Capacitância e sua incerteza
    df['c_cap_pf'] = calcular_c_cap(df['c_medido_pf'])
    df['sigma_c_cap_pf'] = calcular_incerteza_c_cap(df['sigma_c_medido_pf'])
    
    return df
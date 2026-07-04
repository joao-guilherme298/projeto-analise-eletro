import pandas as pd
import numpy as np

# ==========================================
# 1. PARÂMETROS FIXOS DO EXPERIMENTO
# ==========================================
C_RES = 4.5          # Capacitância residual em pF
SIGMA_C_RES = 0.5    # Incerteza da capacitância residual
AREA = 0.02011       # Área das placas em m^2
SIGMA_AREA = 0.0002  # Incerteza da área

def calcular_distancia_media(df):
    """
    Pega as três colunas de distância (d1, d2, d3) e calcula a média.
    """
    colunas_distancia = df[['d1_mm', 'd2_mm', 'd3_mm']]
    return colunas_distancia.mean(axis=1)

def calcular_w(distancia_media):
    """
    Converte a distância de milímetros para metros inversos (w = 1000 / d).
    """
    return 1000 / distancia_media

def calcular_c_cap(c_medido):
    """
    Subtrai a capacitância residual do valor medido no laboratório.
    """
    return c_medido - C_RES

def processar_dados_iniciais(caminho_csv):
    """
    Função principal que carrega os dados e aplica todas as transformações acima.
    Ela retorna um novo DataFrame 'enriquecido' com as colunas que calculamos.
    """
    # Lê o arquivo CSV bruto
    df = pd.read_csv(caminho_csv)
    
    # Cria as novas colunas executando as funções
    df['d_media_mm'] = calcular_distancia_media(df)
    df['w_m_inv'] = calcular_w(df['d_media_mm'])
    df['c_cap_pf'] = calcular_c_cap(df['c_medida_pf'])
    
    return df
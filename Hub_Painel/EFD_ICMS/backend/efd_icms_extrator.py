import pandas as pd
from datetime import datetime

def extrair_periodo_efd(linhas):
    for linha in linhas:
        if linha.startswith('|0000|'):
            partes = linha.strip().split('|')
            if len(partes) > 5:
                dt_ini = partes[4]
                try:
                    return datetime.strptime(dt_ini, '%d%m%Y').date().replace(day=1)
                except ValueError:
                    return 'PERIODO_INVALIDO'
    return 'PERIODO_NAO_ENCONTRADO'

def parse_float(valor):
    try:
        return float(valor.replace(',', '.'))
    except (ValueError, AttributeError):
        return 0.0

def extrair_registros(linhas, periodo):
    registros_e110 = []
    registros_e115 = []

    for linha in linhas:
        partes = linha.strip().split('|')
        if len(partes) < 2:
            continue

        if partes[1] == 'E110':
            dados = partes[2:] + ['0'] * (15 - len(partes[2:]))
            registros_e110.append({
                'REG': 'E110',
                'VL_TOT_DEBITOS': parse_float(dados[0]),
                'VL_AJ_DEBITOS': parse_float(dados[1]),
                'VL_TOT_AJ_DEBITOS': parse_float(dados[2]),
                'VL_ESTORNOS_CRED': parse_float(dados[3]),
                'VL_TOT_CREDITOS': parse_float(dados[4]),
                'VL_AJ_CREDITOS': parse_float(dados[5]),
                'VL_TOT_AJ_CREDITOS': parse_float(dados[6]),
                'VL_ESTORNOS_DEB': parse_float(dados[7]),
                'VL_SLD_CREDOR_ANT': parse_float(dados[8]),
                'VL_SLD_APURADO': parse_float(dados[9]),
                'VL_TOT_DED': parse_float(dados[10]),
                'VL_ICMS_RECOLHER': parse_float(dados[11]),
                'VL_SLD_CREDOR_TRANSPORTAR': parse_float(dados[12]),
                'DEB_ESP': parse_float(dados[13]),
                'PERIODO_REFERENTE': periodo
            })

        elif partes[1] == 'E115':
            dados = partes[2:] + [''] * (4 - len(partes[2:]))
            registros_e115.append({
                'REG': 'E115',
                'COD_INF_ADIC': dados[0],
                'VL_INF_ADIC': parse_float(dados[1]),
                'DESCR_COMPL_AJ': dados[2] if len(dados) > 2 else '',
                'PERIODO_REFERENTE': periodo
            })

    return pd.DataFrame(registros_e110), pd.DataFrame(registros_e115)

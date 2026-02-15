from datetime import datetime


# ----------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------
def extrair_periodo_sped(linhas):
    """
    Procura o |0000| e devolve a data de início do período (DT_INI)
    como datetime.date. Se ausente ou inválida, devolve None.
    """
    for linha in linhas:
        if linha.startswith('|0000|'):
            partes = linha.strip().split('|')
            if len(partes) > 6:
                data_str = partes[6]
                try:
                    return datetime.strptime(data_str, '%d%m%Y').date()
                except ValueError:
                    return None
    return None


def parse_float(valor):
    """
    Converte string numérica (vírgula decimal) p/ float; falha → 0.0
    """
    try:
        return float(valor.replace(',', '.'))
    except (ValueError, AttributeError):
        return 0.0


def _registro_vazio(cod, periodo):
    """
    Cria um dicionário‑sentinela todo zerado para M200 ou M600,
    usando o período informado.
    """
    return {
        'REG': cod,
        'VL_TOT_CONT_NC_PER':   0.0,
        'VL_TOT_CRED_DESC':     0.0,
        'VL_TOT_CRED_DESC_ANT': 0.0,
        'VL_TOT_CONT_NC_DEV':   0.0,
        'VL_RET_NC':            0.0,
        'VL_OUT_DED_NC':        0.0,
        'VL_CONT_NC_REC':       0.0,
        'VL_TOT_CONT_CUM_PER':  0.0,
        'VL_RET_CUM':           0.0,
        'VL_OUT_DED_CUM':       0.0,
        'VL_CONT_CUM_REC':      0.0,
        'VL_TOT_CONT_REC':      0.0,
        'PERIODO_REFERENTE':    periodo,
    }


# ----------------------------------------------------------------------
# Extração dos registros
# ----------------------------------------------------------------------
def extrair_registros_sped(linhas, periodo):
    """
    Percorre as linhas do arquivo e devolve duas listas de dicionários:
    - registros_m200
    - registros_m600

    Se nenhuma linha M200/M600 for encontrada, devolve um registro
    sentinela zerado para cada tipo.
    """
    registros_m200 = []
    registros_m600 = []

    for linha in linhas:
        partes = linha.strip().split('|')
        if len(partes) < 2:
            continue

        reg = partes[1]
        if reg not in ('M200', 'M600'):
            continue

        dados = partes[2:]
        campos = dados + ['0'] * (12 - len(dados))   # garante 12 valores

        registro = {
            'REG': reg,
            'VL_TOT_CONT_NC_PER':   parse_float(campos[0]),   # Campo 2
            'VL_TOT_CRED_DESC':     parse_float(campos[1]),   # Campo 3
            'VL_TOT_CRED_DESC_ANT': parse_float(campos[2]),   # Campo 4
            'VL_TOT_CONT_NC_DEV':   parse_float(campos[3]),   # Campo 5
            'VL_RET_NC':            parse_float(campos[4]),   # Campo 6
            'VL_OUT_DED_NC':        parse_float(campos[5]),   # Campo 7
            'VL_CONT_NC_REC':       parse_float(campos[6]),   # Campo 8
            'VL_TOT_CONT_CUM_PER':  parse_float(campos[7]),   # Campo 9
            'VL_RET_CUM':           parse_float(campos[8]),   # Campo 10
            'VL_OUT_DED_CUM':       parse_float(campos[9]),   # Campo 11
            'VL_CONT_CUM_REC':      parse_float(campos[10]),  # Campo 12
            'VL_TOT_CONT_REC':      parse_float(campos[11]),  # Campo 13
            'PERIODO_REFERENTE':    periodo,
        }

        if reg == 'M200':
            registros_m200.append(registro)
        else:
            registros_m600.append(registro)

    # ➜ Se não encontrou nenhum, devolve sentinela zerado
    if not registros_m200:
        registros_m200.append(_registro_vazio('M200', periodo))
    if not registros_m600:
        registros_m600.append(_registro_vazio('M600', periodo))

    return registros_m200, registros_m600


# ----------------------------------------------------------------------
# Interface principal para vários arquivos
# ----------------------------------------------------------------------
def processar_varios_arquivos(lista_arquivos):
    """
    Recebe uma lista de caminhos .txt, devolve duas listas de dicionários
    agregadas (M200_total, M600_total).
    """
    todos_m200 = []
    todos_m600 = []

    for caminho in lista_arquivos:
        with open(caminho, 'r', encoding='latin1') as f:
            linhas = f.readlines()

        periodo = extrair_periodo_sped(linhas)
        m200, m600 = extrair_registros_sped(linhas, periodo)

        todos_m200.extend(m200)
        todos_m600.extend(m600)

    return todos_m200, todos_m600

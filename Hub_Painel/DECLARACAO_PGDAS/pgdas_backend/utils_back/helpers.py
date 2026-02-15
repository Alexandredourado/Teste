def identificar_natureza_resumida(descricao: str) -> str:
    mapa = {
        "revenda de mercadorias": "Comércio",
        "venda de mercadorias industrializadas": "Indústria",
        "locação de bens móveis": "Locação",
        "prestação de serviços": "Serviços",
        "comunicação": "Serviços",
        "transporte": "Serviços",
        "construção civil": "Construção Civil",
        "ipi e de iss": "IPI + ISS"
    }
    descricao_lower = descricao.lower()
    for chave, valor in mapa.items():
        if chave in descricao_lower:
            return valor
    return "Outros"

def detectar_anexo(natureza: str) -> str:
    match natureza:
        case "Comércio":
            return "Anexo I"
        case "Indústria":
            return "Anexo II"
        case "Locação":
            return "Anexo III ou IV"
        case "Serviços":
            return "Anexo III / IV / V"
        case "Construção Civil":
            return "Anexo IV (ou III em casos específicos)"
        case "IPI + ISS":
            return "Anexo II + Anexo III/IV/V"
        case _:
            return "Indeterminado"

def extrair_particularidades(texto: str) -> list[str]:
    padroes = {
        "Substituição tributária de": "Substituição tributária",
        "Tributação monofásica de": "Tributação monofásica",
        "Isenção": "Isenção",
        "Retenção de ISS": "Retenção de ISS",
        "Exigibilidade suspensa": "Exigibilidade suspensa",
        "Imunidade": "Imunidade",
    }
    achadas = []
    texto_lower = texto.lower()
    for padrao, nome in padroes.items():
        if padrao.lower() in texto_lower:
            achadas.append(nome)
    return achadas

def converter_valor_str_para_float(valor_str: str) -> float | None:
    try:
        return float(valor_str.replace('.', '').replace(',', '.'))
    except ValueError:
        return None

def formatar_float_brl(valor: float) -> str:
    """
    Formata um número float no padrão brasileiro:
    1171.61 -> '1.171,61'
    """
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
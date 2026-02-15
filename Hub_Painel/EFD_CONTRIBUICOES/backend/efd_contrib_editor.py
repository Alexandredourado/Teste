import os

def alterar_linhas_contribuicoes(linhas, novo_cnpj):
    novas_linhas = []
    for linha in linhas:
        if linha.startswith('|0000|'):
            campos = linha.strip().split('|')
            while len(campos) <= 9:
                campos.append('')
            campos[9] = novo_cnpj
            nova_linha = '|'.join(campos) + '\n'
            novas_linhas.append(nova_linha)
        else:
            novas_linhas.append(linha)
    return novas_linhas

def salvar_arquivo_editado(caminho_arquivo, novas_linhas, pasta_destino):
    nome_curto = "<desconhecido>"
    try:
        nome_original = os.path.basename(caminho_arquivo)
        partes_nome = nome_original.split('_')
        if len(partes_nome) >= 3:
            nome_curto = f"EDITADO_{partes_nome[0]}_{partes_nome[1]}_{partes_nome[2]}.txt"
        else:
            nome_curto = f"EDITADO_{nome_original}"

        if not pasta_destino:
            pasta_destino = os.path.dirname(caminho_arquivo)

        os.makedirs(pasta_destino, exist_ok=True)
        novo_caminho = os.path.normpath(os.path.join(pasta_destino, nome_curto))

        with open(novo_caminho, 'w', encoding='latin1') as f:
            f.writelines(novas_linhas)

        return novo_caminho

    except Exception as e:
        raise Exception(f"Erro ao salvar {nome_curto}: {e}")

def processar_arquivo(caminho, novo_cnpj, pasta_destino):
    try:
        with open(caminho, 'r', encoding='latin1') as f:
            linhas = f.readlines()

        linhas_alteradas = alterar_linhas_contribuicoes(linhas, novo_cnpj)
        return salvar_arquivo_editado(caminho, linhas_alteradas, pasta_destino)

    except Exception as e:
        raise Exception(f"Erro ao processar {os.path.basename(caminho)}: {e}")

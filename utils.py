from libs import *

def extrair_valor_texto(texto_valor):
    match = re.search(r"R\$\s*([\d\.,]+)", texto_valor)
    if match:
        valor_str = match.group(1)
        return float(valor_str.replace('.', '').replace(',', '.'))
    raise ValueError("Valor em reais não pôde ser extraído.")

def is_old_date(data_str):
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
    except:
        return True  # Considera antiga se não conseguir interpretar

    agora = datetime.now()
    return (data.year < agora.year) or (data.year == agora.year and data.month < agora.month)

def status_update(df, index, status):
    df.loc[index, 'STATUS'] = status
    df.loc[index, 'Data Atualização FGTS'] = f'{datetime.now().strftime("%d/%m/%Y")}'
    return


def selecionar_arquivo_excel():
    # root = Tk()
    # root.withdraw()  # Esconde a janela principal
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha Excel com os códigos de PIS",
        filetypes=[("Planilhas Excel", "*.xlsx *.xls")]
    )
    return caminho
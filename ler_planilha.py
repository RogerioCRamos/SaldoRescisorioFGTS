from libs import *
from conectividade import *
from utils import *
import os

def salvar_planilha_incremental(df, caminho_original):
    caminho_temp = caminho_original.replace(".xlsx", "_tmp.xlsx")
    try:
        df.to_excel(caminho_temp, index=False)
        os.replace(caminho_temp, caminho_original)
    except Exception as e:
        print(f"Erro ao salvar a planilha: {e}")

def ler_planilha(caminho):

    while True:  # loop externo para reiniciar sessão/navegador

        df = pd.read_excel(caminho, dtype='str')
        df = df.fillna('')
        if 'STATUS' not in df.columns:
            df['STATUS'] = ''
        if not 'Saldo Rescisão' in df.columns:
            df['Saldo Rescisão'] = ''    
        if not 'Data Atualização FGTS' in df.columns:
            df['Data Atualização FGTS'] = ''

        pendentes = df[
            (
                (df['STATUS'] != 'SUCESSO')
                | (df['STATUS'] != 'PIS NÃO LOCALIZADO')
                | is_old_date(df['Data Atualização FGTS'])
            )
        ]

        p, browser, page = access_conectividade()

        try:

            for index, row in pendentes.iterrows():

                if row['STATUS'] != 'SUCESSO' or is_old_date(row['Data Atualização FGTS']):
                    if row['PIS'] not in ('', None):
                        saldo, status = find_fgts_resign_data(page, row['PIS'])

                        if status == "PIS NÃO LOCALIZADO":
                            status_update(df, index, status)
                            print(f'PIS NÃO LOCALIZADO {row['PIS']}')
                            

                        elif status == 'SUCESSO':
                            df.loc[index, 'Saldo Rescisão'] = saldo
                            status_update(df, index, status)

                            print(f'Sucesso')

                        else:
                            status_update(df, index, 'NÃO FOI POSSÍVEL OBTER DADOS')

                            print(f'NÃO FOI POSSIVEL OBTER DADOS {row['PIS']}')

                    else:
                        status_update(df, index, 'NUMERO DO PIS VAZIO')
                        print(f'PIS VAZIO')

                
                salvar_planilha_incremental(df, caminho)

                

            else:
                # Se o for completou sem break (sem falhas ou limite de 100)
                browser.close()
                p.stop()
                print("✅ Processamento finalizado com sucesso.")
                break  # Sai do while e finaliza a função

        except Exception as e:
            print(f"Erro inesperado: {e}")
            browser.close()
            p.stop()
            # Decide reiniciar ou encerrar, conforme necessário

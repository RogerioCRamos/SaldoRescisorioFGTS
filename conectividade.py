from libs import *
from utils import *

def access_conectividade():
    p = sync_playwright().start()
    browser = p.firefox.launch_persistent_context(headless=True, user_data_dir=os.path.expanduser(rf'~\Desktop\fgts\persistente') ,args=["--start-maximized", "--no-startup-window"])
    page = browser.pages[0]
    page.goto("https://conectividadesocialv2.caixa.gov.br/sicns/")
    page.wait_for_load_state("networkidle")

    page.locator("#btnEmpregador").wait_for(state="visible", timeout=50000)
    page.click("#btnEmpregador")
    page.locator("select[name='sltOpcao']").wait_for(state="visible", timeout=30000)

    return p, browser, page

def clicar_pagina_inicial(page, timeout):
    try:
        pagina_inicial = page.get_by_text("Página Inicial", exact=True)
        pagina_inicial.wait_for(state="visible", timeout=timeout)
        pagina_inicial.click()
    except Exception:
        pass

def find_fgts_resign_data(page, pis):
    tentativas = 0
    while tentativas < 3:
        try:
            
            tentativas += 1
            print(f'PIS: {pis} | tentativa: {tentativas}')
    
            clicar_pagina_inicial(page, 1000)

            page.locator("select[name='sltOpcao']").wait_for(state="visible", timeout=10000)
            page.select_option("select[name='sltOpcao']", label="Solicitar Extrato do Trabalhador")

            page.locator("select[name='sltRegiao']").wait_for(state="visible", timeout=5000)
            page.select_option("select[name='sltRegiao']", value="SPD")

            page.once("dialog", lambda dialog: dialog.dismiss())
            campo_pis = page.locator("input[name='txtNumPisPasep']")
            campo_pis.wait_for(state="visible", timeout=5000)
            campo_pis.fill(pis)

            sleep(1)

            botao_localizar = page.locator("a[href='javascript:subm_localizar_trabalhador();']")
            botao_localizar.wait_for(state="visible", timeout=10000)
            botao_localizar.click()

            page.wait_for_load_state("networkidle")

            corpo = page.locator("body").inner_text(timeout=10000)
            if "ERR_NETWORK_CHANGED" in corpo:
                raise Exception("ERR_NETWORK_CHANGED")
            if "PIS/PASEP/NIT não localizado" in corpo:
                clicar_pagina_inicial(page,10000)
                return "", "PIS NÃO LOCALIZADO"

            radio_rows = page.locator("tr:has(input[type='radio'])")
            qtd = radio_rows.count()

            if qtd == 0:
                celula = page.locator("td:has-text('R$')").nth(2)
                celula.wait_for(state="visible", timeout=10000)
                texto_valor = celula.inner_text(timeout=5000)
                clicar_pagina_inicial(page, 10000)
                return extrair_valor_texto(texto_valor), "SUCESSO"

            datas = []
            for i in range(qtd):
                linha_radio = radio_rows.nth(i)
                try:
                    linha_detalhe = linha_radio.evaluate_handle("el => el.nextElementSibling")
                    tem_cells = linha_detalhe.evaluate("el => el.cells && el.cells.length > 3")
                    if tem_cells:
                        data_texto = linha_detalhe.evaluate("el => el.cells[3].innerText.trim()")
                        data_obj = datetime.strptime(data_texto, "%d/%m/%Y")
                        datas.append((data_obj, i))
                except Exception:
                    continue

            if not datas:
                clicar_pagina_inicial(page, 10000)
                raise Exception("Nenhuma data válida encontrada.")

            data_mais_recente = max(datas, key=lambda x: x[0])[0]
            indices_mais_recentes = [i for d, i in datas if d == data_mais_recente]

            valores = []
            for idx in indices_mais_recentes:
                radio = radio_rows.nth(idx).locator("input[type='radio']")
                radio.wait_for(state="visible", timeout=5000)
                radio.click()

                page.get_by_role("cell", name="Empregador").get_by_role("link").first.wait_for(state="visible", timeout=10000)
                page.get_by_role("cell", name="Empregador").get_by_role("link").first.click()

                celula = page.locator("td:has-text('R$')").nth(2)
                celula.wait_for(state="visible", timeout=10000)
                texto_valor = celula.inner_text(timeout=5000)

                clicar_pagina_inicial(page, 10000)

                try:
                    valor_float = extrair_valor_texto(texto_valor)
                    valores.append(valor_float)
                except ValueError:
                    continue

            return sum(valores), "SUCESSO"

        except Exception as e:
            if "ERR_NETWORK_CHANGED" in str(e):
                page.reload()
                continue
            if tentativas >= 3:
                clicar_pagina_inicial(page, 10000)
                return "", "NUMERO DE TENTATIVAS EXCEDIDO"
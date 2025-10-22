from libs import *
from ler_planilha import *

def main():

    caminho = selecionar_arquivo_excel()
    ler_planilha(caminho)

if __name__ == "__main__":
    main()
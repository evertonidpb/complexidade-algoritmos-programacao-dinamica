import sys
import os
import time

def knapsack(M, p, v, n):
    """
    Implementação da Mochila 0-1 baseada fielmente no slide 28 do professor.
    """
    # Criação da tabela k com dimensões (n + 1) x (M + 1)
    k = [[0 for _ in range(M + 1)] for _ in range(n + 1)]
    
    for i in range(0, n + 1):
        for m in range(0, M + 1):
            if i == 0 or m == 0:
                k[i][m] = 0
            elif p[i-1] <= m:
                k[i][m] = max(v[i-1] + k[i-1][m - p[i-1]], k[i-1][m])
            else:
                k[i][m] = k[i-1][m]
                
    return k[n][M], k


def recuperar_itens(k, p, n, M):
    """
    Algoritmo de Backtracking para descobrir os itens extraídos (slides 40-44).
    """
    itens_escolhidos = []
    m = M
    for i in range(n, 0, -1):
        if k[i][m] != k[i-1][m]:
            itens_escolhidos.append(i) # Índice baseado em 1 (Objeto 1, Objeto 2...)
            m = m - p[i-1]
            
    itens_escolhidos.reverse()
    return itens_escolhidos


def carregar_instancia_robusta(caminho_arquivo):
    """
    Lê o arquivo de forma tokenizada, ignorando completamente problemas de 
    quebras de linha (\r\n), espaços extras ou linhas vazias.
    """
    with open(caminho_arquivo, 'r') as f:
        tokens = f.read().split()
        
    if not tokens:
        raise ValueError(f"O arquivo {caminho_arquivo} está vazio.")
        
    n = int(tokens[0])
    M = int(tokens[1])
    
    p = []
    v = []
    
    idx = 2
    for _ in range(n):
        p.append(int(tokens[idx]))      # Peso (pi)
        v.append(int(tokens[idx + 1]))  # Valor (vi)
        idx += 2
        
    return M, p, v, n


def executar_para_um_arquivo(caminho_arquivo):
    """
    Gerencia a execução, cronometra o tempo e exibe o resultado formatado.
    """
    nome_exibicao = os.path.basename(caminho_arquivo)
    print(f"\n" + "="*60)
    print(f"PROCESSANDO: {nome_exibicao}")
    print(f"Caminho: {caminho_arquivo}")
    print("="*60)
    
    try:
        t_inicio_leitura = time.time()
        M, p, v, n = carregar_instancia_robusta(caminho_arquivo)
        
        print(f" -> Itens disponíveis (n): {n}")
        print(f" -> Capacidade máxima (M): {M}")
        
        # Alerta visual para matrizes muito grandes
        if n * M > 50000000:
            print(" [!] Instância grande detectada. Alocando matriz na RAM, aguarde...")
            
        t_inicio_calculo = time.time()
        valor_otimo, tabela_k = knapsack(M, p, v, n)
        
        t_inicio_backtrack = time.time()
        itens_na_mochila = recuperar_itens(tabela_k, p, n, M)
        t_fim = time.time()
        
        # Resultados
        print(f"\n >>> RESULTADO OPTIMAL <<<")
        print(f" * Valor Máximo Alcançado: {valor_otimo}")
        print(f" * Peso Total Utilizado  : {sum(p[i-1] for i in itens_na_mochila)} de {M}")
        
        # Exibe os itens apenas se não forem milhares (para não poluir o terminal)
        if len(itens_na_mochila) <= 30:
            print(f" * ID dos Itens Escolhidos: {itens_na_mochila}")
        else:
            print(f" * Total de Itens Escolhidos: {len(itens_na_mochila)} itens colocados na mochila.")
            print(f" * Primeiros 10 itens escolhidos: {itens_na_mochila[:10]}...")
            
        print(f"\n TEMPOS DE EXECUÇÃO:")
        print(f"  - Carga do Arquivo: {t_inicio_calculo - t_inicio_leitura:.4f}s")
        print(f"  - Resolução da DP : {t_inicio_backtrack - t_inicio_calculo:.4f}s")
        print(f"  - Recuperação (Caminho): {t_fim - t_inicio_backtrack:.4f}s")
        print(f"  - Tempo Total     : {t_fim - t_inicio_leitura:.4f}s")
        
    except Exception as e:
        print(f" [ERRO] Falha ao processar o arquivo {nome_exibicao}: {e}")


if __name__ == "__main__":
    # 1. Descobre dinamicamente onde o mochila.py está para achar a pasta 'instancias' um nível acima (..)
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    pasta_instancias = os.path.abspath(os.path.join(diretorio_script, "..", "instancias"))
    
    # Caso 1: O usuário passou um arquivo específico por argumento (ex: python mochila.py mochila01.txt)
    if len(sys.argv) > 1:
        arquivo_alvo = sys.argv[1]
        caminho_completo = os.path.join(pasta_instancias, arquivo_alvo)
        
        # Tenta ler no caminho exato passado ou procura direto dentro da pasta de instâncias mapeada
        if os.path.exists(arquivo_alvo):
            executar_para_um_arquivo(arquivo_alvo)
        elif os.path.exists(caminho_completo):
            executar_para_um_arquivo(caminho_completo)
        else:
            print(f"Erro: O arquivo '{arquivo_alvo}' não foi encontrado localmente nem em '{pasta_instancias}'.")
            
    # Caso 2: Sem argumentos, o programa varre automaticamente a pasta ../instancias
    else:
        if os.path.exists(pasta_instancias):
            arquivos_na_pasta = [
                os.path.join(pasta_instancias, f) 
                for f in os.listdir(pasta_instancias) 
                if f.startswith('mochila') and f.endswith('.txt')
            ]
            arquivos_na_pasta.sort() # Ordenar sequencialmente (mochila01, mochila02...)
            
            if arquivos_na_pasta:
                print(f"[INFO] Detectamos automaticamente {len(arquivos_na_pasta)} instâncias na pasta externa: '{pasta_instancias}'")
                print("[INFO] Executando todas sequencialmente...\n")
                for caminho_completo in arquivos_na_pasta:
                    executar_para_um_arquivo(caminho_completo)
            else:
                print(f"[AVISO] Nenhum arquivo 'mochila*.txt' encontrado na pasta mapeada: '{pasta_instancias}'.")
        else:
            print(f"[ERRO] A pasta de instâncias não foi encontrada no caminho esperado: '{pasta_instancias}'")
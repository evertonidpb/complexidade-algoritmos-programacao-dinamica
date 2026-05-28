import sys
import os
import time

def knapsack(M, p, v, n):
    """
    Implementação do problam da Mochila 0-1 
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
     Descobrir os itens extraídos.
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
    Lê o arquivo
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


def executar_para_um_arquivo(caminho_arquivo, pasta_saida):
    """
    Gerencia a execução, calcula o tempo, exibe na tela e exporta p/ .txt
    """
    nome_base = os.path.basename(caminho_arquivo)
    print(f"\n" + "="*60)
    print(f"PROCESSANDO: {nome_base}")
    print(f"Caminho: {caminho_arquivo}")
    print("="*60)
    
    try:
        t_inicio_leitura = time.time()
        M, p, v, n = carregar_instancia_robusta(caminho_arquivo)
        
        print(f" -> Itens disponíveis (n): {n}")
        print(f" -> Capacidade máxima (M): {M}")
        
        if n * M > 50000000:
            print(" [!] Instância grande detectada. Alocando matriz na RAM, aguarde...")
            
        t_inicio_calculo = time.time()
        valor_otimo, tabela_k = knapsack(M, p, v, n)
        
        t_inicio_backtrack = time.time()
        itens_na_mochila = recuperar_itens(tabela_k, p, n, M)
        t_fim = time.time()
        
        # Coleta das métricas de tempo
        tempo_carga = t_inicio_calculo - t_inicio_leitura
        tempo_dp = t_inicio_backtrack - t_inicio_calculo
        tempo_backtrack = t_fim - t_inicio_backtrack
        tempo_total = t_fim - t_inicio_leitura
        peso_total = sum(p[i-1] for i in itens_na_mochila)
        
        # --- EXIBIÇÃO NO TERMINAL ---
        print(f"\n >>> RESULTADO OPTIMAL <<<")
        print(f" * Valor Máximo Alcançado: {valor_otimo}")
        print(f" * Peso Total Utilizado  : {peso_total} de {M}")
        
        if len(itens_na_mochila) <= 30:
            print(f" * ID dos Itens Escolhidos: {itens_na_mochila}")
        else:
            print(f" * Total de Itens Escolhidos: {len(itens_na_mochila)} itens.")
            print(f" * Primeiros 10 itens: {itens_na_mochila[:10]}...")
            
        print(f"\n TEMPOS DE EXECUÇÃO: {tempo_total:.4f}s")
        
        # --- GRAVAÇÃO DO ARQUIVO DE TEXTO (RELATÓRIO) ---
        nome_saida = f"resultado_{os.path.splitext(nome_base)[0]}.txt"
        caminho_saida = os.path.join(pasta_saida, nome_saida)
        
        with open(caminho_saida, 'w', encoding='utf-8') as f_out:
            f_out.write("="*60 + "\n")
            f_out.write(f"RELATÓRIO DE EXECUÇÃO - PROBLEMA DA MOCHILA INTEIRA 0-1\n")
            f_out.write(f"Instância de Entrada: {nome_base}\n")
            f_out.write("="*60 + "\n\n")
            
            f_out.write(f"--- DADOS DA INSTÂNCIA ---\n")
            f_out.write(f"Quantidade total de objetos (n): {n}\n")
            f_out.write(f"Capacidade máxima da mochila (M): {M}\n\n")
            
            f_out.write(f"--- RESULTADOS OBTIDOS ---\n")
            f_out.write(f"Valor Ótimo Máximo Solucionado: {valor_otimo}\n")
            f_out.write(f"Peso Total Utilizado na Mochila: {peso_total} de {M}\n")
            f_out.write(f"Total de Objetos Selecionados : {len(itens_na_mochila)}\n\n")
            
            f_out.write(f"--- TEMPOS DE PROCESSAMENTO ---\n")
            f_out.write(f"Leitura e parse do arquivo     : {tempo_carga:.4f} segundos\n")
            f_out.write(f"Processamento Programação Dinâmica: {tempo_dp:.4f} segundos\n")
            f_out.write(f"Backtracking (Recuperar caminho)  : {tempo_backtrack:.4f} segundos\n")
            f_out.write(f"Tempo Total Geral de Execução  : {tempo_total:.4f} segundos\n\n")
            
            f_out.write(f"--- LISTA COMPLETA DOS ÍNDICES SELECIONADOS (1-based) ---\n")
            f_out.write(f"{itens_na_mochila}\n\n")
            
            f_out.write(f"--- DETALHAMENTO DOS ITENS SELECIONADOS ---\n")
            f_out.write(f"{'Item ID':<10}{'Peso (p_i)':<12}{'Valor (v_i)':<12}\n")
            for item in itens_na_mochila:
                idx = item - 1
                f_out.write(f"{item:<10}{p[idx]:<12}{v[idx]:<12}\n")
                
        print(f" [SUCESSO] Relatório salvo em: '{caminho_saida}'")
        
    except Exception as e:
        print(f" [ERRO] Falha ao processar o arquivo {nome_base}: {e}")


if __name__ == "__main__":
    # 1. Mapeamento dinâmico dos diretórios
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    pasta_instancias = os.path.abspath(os.path.join(diretorio_script, "..", "instancias"))
    pasta_resultados = os.path.abspath(os.path.join(diretorio_script, "..", "resultados"))
    
    # Cria a pasta de resultados se ela não existir
    os.makedirs(pasta_resultados, exist_ok=True)
    
    # Caso 1: O usuário passou um arquivo específico por argumento (ex: python mochila.py mochila01.txt)
    if len(sys.argv) > 1:
        arquivo_alvo = sys.argv[1]
        caminho_completo = os.path.join(pasta_instancias, arquivo_alvo)
        
        if os.path.exists(arquivo_alvo):
            executar_para_um_arquivo(arquivo_alvo, pasta_resultados)
        elif os.path.exists(caminho_completo):
            executar_para_um_arquivo(caminho_completo, pasta_resultados)
        else:
            print(f"Erro: O arquivo '{arquivo_alvo}' não foi encontrado localmente nem em '{pasta_instancias}'.")
            
    # Caso 2: Sem argumentos, o programa varre automaticamente toda a pasta ../instancias
    else:
        if os.path.exists(pasta_instancias):
            arquivos_na_pasta = [
                os.path.join(pasta_instancias, f) 
                for f in os.listdir(pasta_instancias) 
                if f.startswith('mochila') and f.endswith('.txt')
            ]
            arquivos_na_pasta.sort()
            
            if arquivos_na_pasta:
                print(f"[INFO] Detectamos {len(arquivos_na_pasta)} instâncias em: '{pasta_instancias}'")
                print("[INFO] Executando e exportando relatórios...\n")
                for caminho_completo in arquivos_na_pasta:
                    executar_para_um_arquivo(caminho_completo, pasta_resultados)
            else:
                print(f"[AVISO] Nenhum arquivo 'mochila*.txt' encontrado em '{pasta_instancias}'.")
        else:
            print(f"[ERRO] A pasta de instâncias não foi encontrada em: '{pasta_instancias}'")
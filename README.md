# Problema da Mochila 0-1 com Programação Dinâmica

Implementação do algoritmo da **Mochila 0-1 (Knapsack Problem)** utilizando **Programação Dinâmica**, com recuperação dos itens escolhidos via **Backtracking**.

O projeto executa automaticamente múltiplas instâncias de teste, mede tempos de execução e apresenta os itens selecionados na solução ótima.

---

# Estrutura do Projeto

```text
.
│   README.md
│
├── instancias/
│   ├── mochila01.txt
│   ├── mochila02.txt
│   ├── mochila1000.txt
│   ├── mochila2500.txt
│   └── mochila5000.txt
│
└── src/
    └── mochila.py
```

---

# Descrição do Problema

Dado um conjunto de objetos, cada um contendo:

- peso `pi`
- valor `vi`

e uma mochila com capacidade máxima `M`, o objetivo é selecionar os objetos que:

✅ maximizem o valor total transportado  
✅ sem ultrapassar a capacidade da mochila

Cada objeto pode ser escolhido apenas uma vez (**problema 0-1**).

---

# Estratégia Utilizada

A implementação utiliza:

- Programação Dinâmica Bottom-Up
- Matriz `k[i][m]`
- Recuperação da solução via Backtracking

---

# Complexidade

## Complexidade Temporal

```text
O(n × M)
```

Onde:

- `n` = número de objetos
- `M` = capacidade máxima da mochila

---

## Complexidade Espacial

```text
O(n × M)
```

Devido ao armazenamento completo da tabela de programação dinâmica.

---

# Formato do Arquivo de Entrada

Cada arquivo `.txt` deve seguir o formato:

```text
n M
p1 v1
p2 v2
...
pn vn
```

Onde:

| Símbolo | Descrição |
|---|---|
| `n` | Quantidade de objetos |
| `M` | Capacidade máxima da mochila |
| `pi` | Peso do objeto |
| `vi` | Valor do objeto |

---

# Exemplo de Entrada

```text
4 30
13 23
23 29
17 27
19 25
```

---

# Exemplo de Saída

```text
instância: mochila01.txt
valor : 107
produtos escolhidos : 1, 2, 6, 7
```

```text
instância: mochila02.txt
valor : 130
produtos escolhidos : 2, 3
```

---

# Funcionalidades Implementadas

- ✅ Leitura robusta de arquivos
- ✅ Execução automática de múltiplas instâncias
- ✅ Recuperação dos itens escolhidos
- ✅ Medição de desempenho
- ✅ Execução individual por argumento
- ✅ Tratamento de erros
- ✅ Compatibilidade com Windows/Linux

---

# Como Executar

## ▶️ Executar todas as instâncias automaticamente

A partir da raiz do projeto:

```bash
cd src
python mochila.py
```

O programa detectará automaticamente todos os arquivos:

```text
mochila*.txt
```

na pasta `../instancias`.

---

## Executar uma instância específica

```bash
cd src
python mochila.py mochila01.txt
```

ou:

```bash
python mochila.py ../instancias/mochila01.txt
```

---

# Exemplo de Execução

```text
[INFO] Detectamos automaticamente 5 instâncias na pasta externa.

============================================================
PROCESSANDO: mochila01.txt
============================================================

 -> Itens disponíveis (n): 7
 -> Capacidade máxima (M): 50

 >>> RESULTADO OPTIMAL <<<
 * Valor Máximo Alcançado: 107
 * Peso Total Utilizado  : 50 de 50
 * ID dos Itens Escolhidos: [1, 2, 6, 7]

 TEMPOS DE EXECUÇÃO:
  - Carga do Arquivo: 0.0001s
  - Resolução da DP : 0.0023s
  - Recuperação (Caminho): 0.0000s
  - Tempo Total     : 0.0024s
```

---

# Principais Funções

## `knapsack(M, p, v, n)`

Resolve o problema da mochila utilizando programação dinâmica.

### Retorna:

- valor ótimo
- matriz de DP completa

---

## `recuperar_itens(k, p, n, M)`

Executa o backtracking na matriz de programação dinâmica para descobrir quais itens foram selecionados.

---

## `carregar_instancia_robusta()`

Realiza leitura tolerante a:

- espaços extras
- linhas vazias
- diferentes padrões de quebra de linha (`\r\n`)

---

# Observações

Para instâncias muito grandes, a matriz de programação dinâmica pode consumir bastante memória RAM devido à complexidade espacial:

```text
O(n × M)
```

O programa já possui alerta automático para grandes alocações.

---

# Conteúdos Estudados

- Programação Dinâmica
- Otimização Combinatória
- Complexidade de Algoritmos
- Problema da Mochila 0-1
- Backtracking

---

# Autor

Projeto acadêmico desenvolvido para fins educacionais e estudos de algoritmos clássicos de otimização.
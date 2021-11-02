import time
import numpy as np
import pandas as pd


def troca_linear(serie):
    """Executa a busca pelo valor mais alto em uma lista e conta a quantidade
    de trocas realizadas entre o maior valor encontrado e a variável temporária
    (item_max) durante todo o processo.
    """
    serie = list(serie)
    k = 0
    item_max = serie[0]

    t_inicio = time.time()
    try:
        for item in range(1, len(serie)):
            if serie[item] > item_max:
                item_max = serie[item]
                k += 1
    except IndexError:
        pass
    t_fim = time.time()

    return k, t_fim-t_inicio


for vezes in range(1,1_001):

    df = pd.DataFrame(np.random.randint(1, 1_001, size=100))

    if vezes != 1:
        for vez in range(vezes):
            df_1 = pd.DataFrame(np.random.randint(1, 1_001, size=100))
            df = pd.concat([df, df_1], axis=1)

    k_time = pd.DataFrame(np.arange(100))
    k_time = df.apply(troca_linear, axis=1)

    t_lista = np.array([item[1] for item in k_time])
    t_medio = t_lista.mean()

    k_lista = np.array([item[0] for item in k_time])
    k_medio = k_lista.mean()

    df = pd.concat([df, k_time], axis=1)

    nomes_colunas = []
    for idx, nome in enumerate(df.columns):
        if idx != len(df.columns) - 1:
            nomes_colunas.append(str(idx))
        else:
            nomes_colunas.append("k, tempo")

    df.columns = nomes_colunas

    path = "./outputs/"
    file_name = "dados" \
                + "_{:0>4d}".format(vezes) \
                + "_k^={:0>2.1f}".format(k_medio) \
                + "_t^={:0>3.3f}_µs".format(t_medio*1e6) \
                + ".csv"
    df.to_csv(path + file_name)
    print(path + file_name, "saved!")

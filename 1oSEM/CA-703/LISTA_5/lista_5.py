#%%

import time
import random
import pandas as pd

#%%
def gera_lista_int(n_elem=1,
    repeticoes=False,
    ordenados=True,
    x_min=1,
    x_max=1000
    ):
    """
    :param n_elem: (int) quantidade de elementos na lista
    :param repeticoes: (bool) se retorna lista com repetições
    :param ordenados: (bool) se retorna lista ordenada
    :param x_min: (int) valor aleatório mínimo a constar na lista
    :param x_max: (int) valor aleatório máximo a constar na lista
    :return: (list) com 'n' elementos com valores aleatórios variando
             entre x_min e x_max
    """

    import random

    lista = []

    while len(lista) <= n_elem:
        sorteio = random.randint(x_min, x_max+1)
        if sorteio not in lista : lista.append(sorteio)

    if ordenados: lista.sort()

    return lista

#%%
def busca_por_salto(vetor, n_buscado, salto=1):
    """
    :param vetor: (list) de (int) onde buscar o valor
    :param n_buscado: (int) número a ser buscado na lista
    :param salto: (int) salto entre as buscas
    :return: (dict)
        'encontrado': (bool) = True se o valor foi encontrado
        'qtd_comparacoes': (int) quantidade de comparações até encontrar ou não
                           o número
        'id_localizado': (int) índice do vetor onde encontra-se o valor buscado
                         retorna None se não encontrado
        'n_buscado': (int) número buscado no vetor
        'vetor': (list) vetor utilizado na busca
        'salto': (int) tamanho do salto
    """


    encontrado = False
    qtd_comparacoes = 0
    ultimo_id = 0
    for id_de_busca in range(salto - 1, len(vetor) + salto, salto):
        if id_de_busca >= len(vetor):
            ultimo_id = len(vetor) - salto
            resultado = busca_linear(vetor, n_buscado, ultimo_id, salto)
            qtd_comp_acum = resultado['qtd_comparacoes']
            resultado['qtd_comparacoes'] = qtd_comparacoes + qtd_comp_acum
            return resultado
        elif n_buscado < vetor[id_de_busca]:
            qtd_comparacoes += 1
            resultado = busca_linear(vetor, n_buscado, ultimo_id, salto)
            qtd_comp_acum = resultado['qtd_comparacoes']
            resultado['qtd_comparacoes'] = qtd_comparacoes + qtd_comp_acum
            return resultado
        elif n_buscado == vetor[id_de_busca]:
            qtd_comparacoes += 1
            encontrado = True
            return {'encontrado': encontrado,
                    'qtd_comparacoes': qtd_comparacoes,
                    'id_localizado': id_de_busca,
                    'n_buscado': n_buscado,
                    'vetor': vetor,
                    'salto': salto}
        else:
            qtd_comparacoes += 1
        ultimo_id = id_de_busca

#%%
def busca_linear(vetor, n_buscado, ultimo_id, salto=1):
    """
    :param vetor: (list) de (int) onde buscar o valor
    :param n_buscado: (int) número a ser buscado na lista
    :param ultimo_id: (int) último índice antes da busca linear
    :param salto: (int) salto entre as buscas
    :return: (dict)
        'encontrado': (bool) = True se o valor foi encontrado
        'qtd_comparacoes': (int) quantidade de comparações até encontrar ou não
                           o número
        'id_localizado': (int) índice do vetor onde encontra-se o valor buscado
                         retorna None se não encontrado
        'n_buscado': (int) número buscado no vetor
        'vetor': (list) vetor utilizado na busca
        'salto': (int) tamanho do salto
    """
    qtd_comparacoes = 0
    for id_de_busca_linear in range(ultimo_id+1, ultimo_id + salto):
        qtd_comparacoes += 1
        if id_de_busca_linear >= len(vetor):
            id_de_busca_linear = len(vetor) - 1
        if n_buscado == vetor[id_de_busca_linear]:
            encontrado = True
            return {'encontrado': encontrado,
                    'qtd_comparacoes': qtd_comparacoes,
                    'id_localizado': id_de_busca_linear,
                    'n_buscado': n_buscado,
                    'vetor': vetor,
                    'salto': salto}
        elif n_buscado < vetor[id_de_busca_linear]:
            break
    return {'encontrado': False,
            'qtd_comparacoes': qtd_comparacoes,
            'id_localizado': None,
            'n_buscado': n_buscado,
            'vetor': vetor,
            'salto': salto}
#%%

def tabela_valores(n_min=20,
                   n_max=100,
                   buscar_da_lista=True):
    """
    :param n_min:
    :param n_max:
    :return:
    """

    colunas = ['encontrado',
               'qtd_comparacoes',
               'id_localizado',
               'n_buscado',
               'vetor',
               'salto',
               'tempo']

    df = pd.DataFrame(columns=colunas)

    for n in range(n_min, n_max+1):
        vetor = gera_lista_int(n)
        if buscar_da_lista:
            n_buscado = random.choice(vetor)
        else:
            n_buscado = random.randint(1, 1001)
        t_inicio = time.time()
        for salto in range(1, len(vetor)):
            # resultado = busca_por_salto(vetor, n_buscado, salto)
            dl = pd.DataFrame([busca_por_salto(vetor, n_buscado, salto)],
                columns=colunas)
            dl['tempo'] = time.time() - t_inicio
            df = df.append(dl, ignore_index=True)

    return df
#%%
df = pd.DataFrame()
df = df.append(tabela_valores(20, 100, False), ignore_index=True)

#%%

path = "/Users/crisdemagalhaes/Programming/PyCharm/lista_5/"
file_name = "dentro_da_lista_outputs.csv"
df.to_csv(path + file_name)

#%%

path = "/Users/crisdemagalhaes/Programming/PyCharm/lista_5/"
file_name = "fora_da_lista_outputs.csv"
df.to_csv(path + file_name)

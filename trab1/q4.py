# João Almir da Costa Junior - 470034

# incompleto

import json

dfa = {'estados': [], 'transicoes': {}, 'inicial': [], 'finais': []}

with open("entrada q4.txt", "r") as arquivo:
	entrada = arquivo.read()
print(entrada)

# #importa o dfa
# with open ('q3.json') as file:
#     tokens = json.load(file)

#separa cada palavra por espaço
def prepare_code(cod):
    codigo = cod.split(' ',)
    return codigo

#percorre as palavras substituindo por tokens
def analise_lexica(tokens):
    estado_atual = dfa['inicial']

    for i in dfa['transicoes'][estado_atual]:
        for j in tokens:
            if j in dfa['transicoes'][estado_atual][i]:
                estado_atual = dfa['transicoes'][estado_atual][i][j]
            elif dfa['transicoes'][estado_atual][i][j] in dfa['finais'][i]:
                tokens[j] = dfa['finais'][i]
            else:
                tokens[j] = 'ERRO'

# transforma quebra de linha em espaço
entrada = entrada.replace('\n', ' ')

#separa os tokens por expaço
tokens = prepare_code(entrada)

print(tokens)

# analise_lexica(tokens)

# João Almir da Costa Junior - 470034
import json


nfa = { "estados": [ 0, 1, 2, 3, 4 ], "transicoes": { 0: { "a": [ 1 ] }, 1: { "": [ 2 ] }, 2: { "": [ 3 ] }, 3: { "b": [ 4 ] } }, "inicial": 0, "finais": [ 4 ] }
#nfa = {'estados': [0,1,2,3,4,5], 'transicoes': {0:{"": [1]},1:{"":[2]},2:{"a":[3]},3:{"":[4,5]} }, 'inicial': 0, 'finais': [4]}

# with open ('q2.json') as file:
#     nfa = json.load(file)

alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '{', '}', ',', '\'', '"', ';', '%', '=', '[', ']', '+', '-', '*', '/', '!', '>', '<', '&', '|']

def closure(estado):
    global nfa
    lista = [estado]

    if estado in nfa['transicoes']:
        if "" in nfa['transicoes'][estado] :
          for i in nfa['transicoes'][estado]['']:
              lista.append(i)
    lista = list(dict.fromkeys(lista)) # remove duplicadas
    return lista

def edge(s, c):
    global nfa

    lista = []
    
    if s in nfa['transicoes']: #impede de percorrer transição que não existe
        for i in nfa['transicoes'][s]:
            if c in nfa['transicoes'][s]:
                lista += nfa['transicoes'][s][i]
    
    return lista

def DFAedge(d, c):
    lista = []

    for i in d:
        lista += edge(i, c)

    for i in lista:
            lista += closure(i)
            lista = list(dict.fromkeys(lista)) # remove duplicadas

    return lista
    

def nfaParaDfa():
    global nfa
    global alfabeto
    dfa = {'estados': [], 'transicoes': {}, 'inicial': [], 'finais': []}
    
    # closure e adicao dos iniciais
    ests_iniciais = closure(nfa['inicial'])

    for i in ests_iniciais:
        ests_iniciais += closure(i)
        ests_iniciais = list(dict.fromkeys(ests_iniciais)) #remove duplicada
    estados_dfa = [ests_iniciais]
    dfa['inicial'] += ests_iniciais
    
    # adiciona os estados do dfa
    for i in nfa['estados']:
        for j in alfabeto:
            if i in nfa['transicoes']:
                estados_dfa += [DFAedge([i], j)]

    estados_dfa = [i for i in estados_dfa if i != []] # remove os [] da lista

    dfa['estados'] = estados_dfa

    # adiciona as transicoes do dfa
    for i in estados_dfa:
        for j in alfabeto:
                dfa_edge = DFAedge(i, j)
                if dfa_edge != []:
                    # print(i , j , dfa_edge)
                    dfa['transicoes'].update({str(i):{j:dfa_edge}})
            
    
    # adiciona os estados finais do dfa
    for i in estados_dfa:
        for j in nfa['finais']:
            if j in i:
                dfa['finais'] += [i]
    return dfa

    


dfa_final = nfaParaDfa()

print(nfa)
print(dfa_final)

with open('q3.json','w') as file:
    json.dump(dfa_final, file, indent=2)


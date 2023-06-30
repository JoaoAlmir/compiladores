# João Almir da Costa Junior - 470034
import json

#variavel global para numerar os estados
numEst = 1

#cria afn com estados representado por inteiros, transicoes, inicial, finais
def cria_afn(estados, transicoes, inicial, finais):
    afn = {'estados':estados, 'transicoes':transicoes, 'inicial':inicial, 'finais':finais}
    return afn

#prepara a lista com o formato [aut1,sinal,aut2]
def preparar_lista(er):
    global numEst
    symbols = ['{', '}', ',', '\'', '"', ';', '[', ']', '+', '=', '-', '*', '/', '%', '!', '>', '<', '&', '']
    lista_er = []
    for simb in er:
        if simb in symbols or str.isalnum(simb):
            # AFN = cria_afn([numEst, numEst+1], [(numEst, simb, numEst+1)], numEst, [numEst + 1])
            AFN = cria_afn([numEst, numEst+1], {}, numEst, [numEst + 1])
            AFN["transicoes"].update({numEst: {simb: [numEst+1]}})
            lista_er.append(AFN)
            numEst = numEst + 3
        else:
            lista_er = lista_er + [simb]
    # print(lista_er)
    return lista_er

#retorna um afn com epsilon transicao entre afn1 e afn2
def concatenacao(AFN1, AFN2):
    transicoes = {}
    transicoes.update(AFN1['transicoes'])
    transicoes.update(AFN2['transicoes'])
    # print(transicoes)
    for finais in AFN1['finais']:
        # AFN['transicoes'].append((finais, '', AFN2['inicial']))
        transicoes.update({finais: {'': [AFN2['inicial']]}})
    AFN = cria_afn(AFN1['estados'] + AFN2['estados'], transicoes, AFN1['inicial'], AFN2['finais'])

    return AFN

#gera um estado inicial novo que faz epsilon transicão com 2 caminhos, AFN1 e ANF2
def uniao(AFN1, AFN2):

    estFinal = AFN1['finais'][-1]+1 if AFN1['finais'][-1] > AFN2['finais'][-1] else AFN2['finais'][-1] +1

    transicoes = {}

    transicoes.update(AFN1['transicoes'])
    transicoes.update(AFN2['transicoes'])
    transicoes[AFN1['inicial']-1] = {}
    transicoes[AFN1['inicial']-1][''] = []
    transicoes[AFN1['inicial']-1][''].append(AFN1['inicial'])
    transicoes[AFN1['inicial']-1][''].append(AFN2['inicial'])
    
    AFN = cria_afn([AFN1['inicial']-1] + AFN1['estados'] +  AFN2['estados'] + [estFinal], transicoes, AFN1['inicial']-1, [estFinal])
    
    for finais in AFN1['finais']:
        AFN['transicoes'].update({finais: {'': [estFinal]}})
    for finais in AFN2['finais']:
        AFN['transicoes'].update({finais: {'': [estFinal]}})
        
    return AFN

#estado final liga com a cabeça e vice versa
def repeticao(AFN1):

    estFinal = AFN1['finais'][-1] + 1
    transicoes = {}
    transicoes.update(AFN1['transicoes'])
    transicoes[AFN1['inicial']-1] = {}
    transicoes[AFN1['inicial']-1][''] = []
    transicoes[AFN1['inicial']-1][''].append(estFinal)
    transicoes[estFinal] = {}
    transicoes[estFinal][''] = []
    transicoes[estFinal][''].append(AFN1['inicial'])

    AFN = cria_afn( [AFN1['inicial']-1] + AFN1['estados'] + [estFinal], transicoes , AFN1['inicial']-1, [estFinal])
    
    for finais in AFN1['finais']:
        AFN['transicoes'][finais] = {}
        AFN['transicoes'][finais][''] = []
        AFN['transicoes'][finais][''].append(estFinal)
    
    return AFN

# cria o afn geral partindo do mesmo estado inicial e indo para todas afns
def junta_afn(afns):
    inicial = -1
    est = []
    finais = {}
    transicoes = {}
    transicoes[inicial] = {}
    transicoes[inicial][''] = []

    for afn in afns:
        transicoes[inicial][''].append(afn['inicial'])
        transicoes.update(afn['transicoes'])
        est += afn['estados']
        finais.update({afn['finais'][0]:afn['finais'][1]})

    return cria_afn(est,transicoes,inicial,finais)

#recebe a pilha com operadores e automatos e retorna o afn
def er_para_afn(pilha):    
    AFN = {}
    ope = []
    aut = []

    if(len(pilha) == 1):
        return pilha.pop()

    for elem in pilha:
        if elem in ['#', '.', '|']:
            ope.append(elem)
        else:
            aut.append(elem)


    while len(ope) > 0:
        simbolo = ope.pop()

        if simbolo == '.':
            AFN1 = aut.pop()
            AFN2 = aut.pop()
            AFN = concatenacao(AFN2, AFN1)
            aut.append(AFN)
        elif simbolo == '|':
            AFN1 = aut.pop()
            AFN2 = aut.pop()
            AFN = uniao(AFN2, AFN1)
            aut.append(AFN)
        elif simbolo == '#':
            AFN1 = aut.pop()
            AFN = repeticao(AFN1)
            aut.append(AFN)
    return AFN

def converter_er_to_afn(er):
    pilha = []
    AFN = []
    lista_er = preparar_lista(er)

    for simb in lista_er:
        if simb != ')':
            pilha.append(simb)
        elif simb == ')':
            aux = []
            while len(pilha) > 0:
                elem = pilha.pop()
                if elem == '(':
                    break
                else:
                    AFN.append(elem)   
                aux.reverse()             
                AFN = er_para_afn(pilha) 
                pilha.append(AFN)
    return AFN

# função final, recebe uma expressao regular e retorna o afn
def converter_er_to_afn(er):
    pilha = []
    AFN = {}
    list_er = preparar_lista(er)

    for simb in list_er:
        if simb != ')':
            pilha.append(simb)
        elif simb == ')':
            aux = []

            while len(pilha) > 0:
                elem = pilha.pop()

                if elem != '(':
                    aux.append(elem)
                else:
                    break
                
            aux.reverse()
            AFN = er_para_afn(aux)
            pilha.append(AFN)

    return AFN
        
with open ('q1.json') as file:
    tokens = json.load(file)

afns = []

for token, er in tokens.items():
    afn = converter_er_to_afn(er)
    afn['finais'].append(token)
    afns.append(afn)

afnFinal = junta_afn(afns)

with open('q2.json','w') as file:
    json.dump(afnFinal, file, indent=2)



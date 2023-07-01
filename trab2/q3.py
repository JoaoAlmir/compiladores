import re

entrada = """1 2
a=a+c
b=4-a
2
2 1
b=20*c
3
3 2
d=a+b
b=0
0"""

entrada = entrada.split("\n")

no = {
    "bloco": -1,
    "expr":[],
    "succ":[],
    "gera":[],
    "mata":[],

}

def no_clear():
    no["bloco"] = -1
    no["expr"] = []
    no["succ"] = -1
    pass


lista_nos = []

#adicionando dados em lista_nos
while no["succ"]!= "0":
    no_clear()

    # bloco
    no["bloco"] = entrada[0][0]

    # expr
    for r in range(int(entrada[0][2])):
        no["expr"].append(entrada[r+1])
        
    # succ
    succ = entrada[int(entrada[0][2])+1]
    no["succ"] = succ

    copia = no.copy()
    lista_nos.append(copia)
    del entrada[0:int(entrada[0][2])+2]




definicoes = []
gen = []
lista_gen = []


# obtendo definicoes
for i in range(len(lista_nos)):
    for j in range(len(lista_nos[i]['expr'])):
        exp = lista_nos[i]['expr'][j]
        gen.append(exp)
        definicoes.append(exp)
    lista_gen.append(gen)
    gen = []


dic_def = {}

#dicionario de morte
for i in range(len(definicoes)):
    dic_def.update({definicoes[i]:"d"+str(i+1)})


dic_mata = {}
aux_mata = []
lista_mata = []

#dicionario mata
for i in range(len(definicoes)):
    for j in range(len(definicoes)):
        if i != j:
            if definicoes[i][0] == definicoes[j][0]:
                aux_mata.append(definicoes[j])
    dic_mata.update({definicoes[i]:aux_mata})
    aux_mata = []

aux_mata = []

# lista mata
for i in range(len(lista_nos)):
    for j in range(len(lista_nos[i]['expr'])):
        exp = lista_nos[i]['expr'][j]
        if dic_mata[exp] != []:
            aux_mata.append(dic_mata[exp])
    lista_mata += aux_mata
    aux_mata = []
            
IN = []
OUT = [] 
ant_IN = []

for _ in range(len(lista_gen)):
    IN.append([])
    OUT.append([])

#obtendo IN e OUT
# while(True):
for _ in range(10):
    ant_IN = OUT.copy()
    for i in range(len(lista_gen)):
        if(i != 0):                     
            IN[i] = OUT[i-1].copy()
        OUT[i] = (list(set(lista_gen[i] + (list(set(IN[i]) - set(lista_mata[i]))))) )
    
    #condição de parada
    if(ant_IN == IN):
        break








# print(dic_def,'\n')

# for i in range(len(lista_nos)):
#     lista_nos[i]['IN'] = IN[i]
#     lista_nos[i]['OUT'] = OUT[i]
#     lista_nos[i]['gera'] = lista_gen[i]
#     lista_nos[i]['mata'] = lista_mata[i]
#     print(lista_nos[i])
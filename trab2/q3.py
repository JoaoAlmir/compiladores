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
    "IN":[],
    "OUT":[],

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


temp_calc = []
filt_calc = []
letras_usadas = []
definicoes = []

#lista de letras usadas na operaçao
for i in range(len(lista_nos)):
    for j in range(len(lista_nos[i]['expr'])):
        exp = lista_nos[i]['expr'][j]
        calc = exp[2:]
        filt_calc = re.sub(r'[^a-zA-Z]', '', calc)
        definicoes.append(calc)
        temp_calc.append(filt_calc)
    letras_usadas.append(temp_calc)
    temp_calc = []

lista_livre_gen = []
lista_gen = []
aux_gen = []
letras_vistas = []


# lista geracao
for i in range(len(lista_nos)):
    for j in reversed(range(len(lista_nos[i]['expr']))):
        letras_vistas+= letras_usadas[i][j]
        exp = lista_nos[i]['expr'][j]
        calc = exp[2:]
        if(exp[0] not in letras_vistas and not calc.isnumeric()):
            aux_gen.append(calc)
            lista_livre_gen.append(exp)
    lista_gen.append(aux_gen)
    aux_gen = []
    letras_vistas = []



aux_kill = []


# lista de letras usadas para kill
for i in range(len(lista_gen)):
    for j in range(len(lista_gen[i])):
        exp = lista_gen[i][j]
        filt_calc = re.sub(r'[^a-zA-Z]', '', exp)
        aux_kill.append(filt_calc)
        

# print(lista_livre_gen)
# print(aux_kill)

lista_kill = []

#preencher lista_kill com vazio
for _ in aux_kill:
    lista_kill.append([])

temp_kill = []


for i in range(len(lista_livre_gen)):
    for j in range(len(aux_kill)):
        if i != j:
            if lista_livre_gen[i][0] in aux_kill[j]:
                temp_kill.append(lista_livre_gen[j])
    lista_kill[i] = temp_kill
    temp_kill = []




dic_def = {}
# dicionario para transformar expressoes em e1, e2, e3...
for i in range(len(definicoes)):

    dic_def.update({definicoes[i]:"e"+str(i+1)})

# print(dic_def)


IN = []
OUT = [] 
ant_IN = []

for _ in range(len(lista_gen)):
    IN.append([])
    OUT.append([])

#obtendo IN e OUT
while(True):
    ant_IN = IN.copy()
    for i in range(len(lista_gen)):
        if(i != 0):                     
            IN[i] = OUT[i-1].copy()
        OUT[i] = (list(set(lista_gen[i] + (list(set(IN[i]) - set(lista_kill[i]))))) )
    
    #condição de parada
    if(ant_IN == IN):
        break

#transformando expressões em e0, e1, e2, ...
for i in range(len(lista_gen)):
    for j in range(len(lista_gen[i])):
        lista_gen[i][j] = dic_def[lista_gen[i][j]]
for i in range(len(lista_kill)):
    for j in range(len(lista_kill[i])):
        df = lista_kill[i][j]
        df = df[2:]
        lista_kill[i][j] = dic_def[df]
for i in range(len(IN)):
    for j in range(len(IN[i])):
        IN[i][j] = dic_def[IN[i][j]]
for i in range(len(OUT)):
    for j in range(len(OUT[i])):
        OUT[i][j] = dic_def[OUT[i][j]]


print(dic_def,'\n')



#preenchendo nos
for i in range(len(lista_nos)):
    lista_nos[i]['IN'] = IN[i]
    lista_nos[i]['OUT'] = OUT[i]
    lista_nos[i]['gera'] = lista_gen[i]
    lista_nos[i]['mata'] = lista_kill[i]
    print(lista_nos[i])
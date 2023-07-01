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
    "def":[],
    "use":[],
    "IN":[],
    "OUT":[]
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





temp_def = []
temp_use = []

lista_def = []
lista_use = []

exp = ""

# obtendo def e use
for i in range(len(lista_nos)):
    for j in range(len(lista_nos[i]['expr'])):
        exp = lista_nos[i]['expr'][j]
        calc = exp[2:]
        calc = re.sub(r'[^a-zA-Z]', '', calc)
        for k in calc:
            if k not in temp_def:
                temp_use.append(k)
        if exp[0] not in temp_use:
                temp_def.append(exp[0])
    temp_use = list(dict.fromkeys(temp_use))
    lista_def.append(temp_def)
    lista_use.append(temp_use)
    temp_def = []
    temp_use = []

for i in range(len(lista_nos)):
    lista_nos[i]['def'] = lista_def[i]
    lista_nos[i]['use'] = lista_use[i]




IN = []
OUT = []
ant_OUT = []

for _ in range(len(lista_use)):
    IN.append([])
    OUT.append([])


rev_def = lista_def.copy()
rev_use = lista_use.copy()

rev_def.reverse()
rev_use.reverse()

#obtendo IN e OUT
while(True):
    ant_OUT = OUT.copy()
    for i in range(len(rev_use)):
        
        if(i != 0):                     
            OUT[i] = IN[i-1].copy()
        IN[i] = (list(set(rev_use[i] + (list(set(OUT[i]) - set(rev_def[i]))))) )
    
    #condição de parada
    if(ant_OUT == OUT):
        break

IN.reverse()
OUT.reverse()

for i in range(len(lista_nos)):
    lista_nos[i]['IN'] = IN[i]
    lista_nos[i]['OUT'] = OUT[i]
    print(lista_nos[i])
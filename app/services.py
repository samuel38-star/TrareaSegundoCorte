"""n=int(input())

numeros=list(map(int,input().split()))

contador=0

for i in numeros:
    while i > contador:
        contador=i
        break

print(contador)


n=int(input())

numeros=list(map(int,input().split()))

suma_final=0

for i in numeros:
    suma_final+=i

print(suma_final)"""



lista=[
    [20,30,3,31,5],
    [5,42,1,65,87]
]

#imprime la lista sin los corchetes
for i in lista:
    for j in i:
        print(j,end=" ")
    print()

#imprime la suma de todos los numeros dentro de la matriz
suma=0

for i in lista:
    for j in i:
        suma += j

print(suma)


#imprime la matriz tal cual 
for i in lista:
    print(i)
#imprime una posicion especifica de la matriz
print(lista[1][0])


#funciones
def saludar():
    print("Hola")
saludar()
#funcion con parametros 
def sumar(a,b):
    print(a+b)
sumar(3,5)

#funcion para encontrar el numero mayor 
def mayor_lista(lista):

    mayor = lista[0]

    for i in lista:
        if i > mayor:
            mayor = i

    return mayor

numeros = [3,8,2,10]

print(mayor_lista(numeros))


def suma_lista(matriz):
    suma_final=0
    for i in lista:
        for j in i:
            suma_final += j
    return suma_final

numeros = [
 [1,2],
 [3,4]
]

print(suma_lista(numeros))

#funcion para buscar por posicion un numero en una matriz 
matriz = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

for i in range(3):
    
    for j in range(3):
        
        if matriz[i][j] == 5:
            print("Fila:",i)
            print("Columna:",j)

#Un programa que busque el número 8 y muestre
matriz = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

for i in range(len(matriz)):
    
    for j in range(len(matriz[i])):
        if matriz[i][j]==8: 
            print("Encontrado en fila",i,"columna",j)
#para buscar por posiciones cercanas a un nunmero de la lista 
matriz = [
 [1,2,3],
 [4,5,6],
 [7,8,9]
]

i = 1
j = 1

dx = [-1,1,0,0]
dy = [0,0,-1,1]

for k in range(4):

    ni = i + dx[k]
    nj = j + dy[k]

    print(matriz[ni][nj])

#buscar mirando los limites de la matriz y que muestre las unicas opciones que tiene dentro de la matriz
matriz = [
 [1,2,3],
 [4,5,6],
 [7,8,9]
]

filas = len(matriz)
columnas = len(matriz[0])

i = 0
j = 0

dx = [-1,1,0,0]
dy = [0,0,-1,1]

for k in range(4):

    ni = i + dx[k]
    nj = j + dy[k]

    if 0 <= ni < filas and 0 <= nj < columnas:
        
        print(matriz[ni][nj])
#busca y cuenta los numeros vecinos mayores a un numero 
matriz = [
 [1,2,3],
 [4,5,6],
 [7,8,9]
]

filas = len(matriz)
columnas = len(matriz[0])

i = 1
j = 1

contador = 0

dx = [-1,1,0,0]
dy = [0,0,-1,1]

for k in range(4):

    ni = i + dx[k]
    nj = j + dy[k]

    if 0 <= ni < filas and 0 <= nj < columnas:

        if matriz[ni][nj] > 5:
            contador += 1

print(contador)

#Desde una posición verificar si algún vecino tiene un valor específico
matriz = [
 [1,2,3],
 [4,5,8],
 [7,8,9]
]

filas = len(matriz)
columnas = len(matriz[0])

i = 1
j = 1
contador=0

dx = [-1,1,0,0]
dy = [0,0,-1,1]

for k in range(4):

    ni = i + dx[k]
    nj = j + dy[k]

    if 0 <= ni < filas and 0 <= nj < columnas:
        if matriz[ni][nj]== 8:
            contador+=1
if contador>=1:
    print("Si")


matriz = [
 [1,1,0],
 [0,1,0],
 [1,0,1]
]

# Cantidad de filas
filas = len(matriz)

# Cantidad de columnas
columnas = len(matriz[0])
contador2=0
def dfs(i,j):
    global contador2 
    # Verifica si se salió de la matriz
    if i < 0 or i >= filas or j < 0 or j >= columnas:
        return
    # Verifica si hay un 0
    # 0 significa:
    # pared o ya visitado
    if matriz[i][j] == 0:
        return
    contador2+=1
    # Muestra la posición actual
    print("Visitando:",i,j)
    # Marca visitado
    matriz[i][j] = 0
    
    
    # Muestra cómo va cambiando la matriz
    
    print("Matriz actual:")

    for fila in matriz:
        print(fila)

    print()
    
    # Arriba
    dfs(i-1,j)

    # Abajo
    dfs(i+1,j)

    # Izquierda
    dfs(i,j-1)

    # Derecha
    dfs(i,j+1)

    


# Empezamos desde la posición (0,0)
dfs(0,0)

print(contador2)

#contar cuantas islas estan conectadas entre si 
matriz = [
 [1,1,0,0],
 [0,1,0,1],
 [1,0,0,1],
 [0,0,1,1]
]

filas = len(matriz)
columnas = len(matriz[0])

islas = 0

matriz3 = [
 [5,3,2],
 [1,8,4],
 [7,6,9]
]

def dfs(i,j):

    if i < 0 or i >= filas or j < 0 or j >= columnas:
        if matriz[ni][nj]== 8:
            return

    if matriz[i][j] == 0:
        return

    matriz[i][j] = 0

    dfs(i-1,j)
    dfs(i+1,j)
    dfs(i,j-1)
    dfs(i,j+1)


for i in range(filas):

    for j in range(columnas):

        if matriz[i][j] == 1:

            islas += 1

            dfs(i,j)


print(islas)


matriz3 = [
 [5,3,2],
 [1,8,4],
 [7,6,9]
]

filas2 = len(matriz3)

# Cantidad de columnas
columnas2 = len(matriz3[0])
def dfs(i,j):
    # Verifica si se salió de la matriz
    if i < 0 or i >= filas2 or j < 0 or j >= columnas2:
            return
    # Verifica si hay un 0
    # 0 significa:
    # pared o ya visitado
    if matriz3[ni][nj]== 8:
        return
    # Muestra la posición actual
    print("Visitando:",i,j)
    # Marca visitado
    matriz3[i][j] = 0
    
    
    # Muestra cómo va cambiando la matriz
    
    print("Matriz actual:")

    for fila in matriz3:
        print(fila)

    print()
    
    # Arriba
    dfs(i-1,j)

    # Abajo
    dfs(i+1,j)

    # Izquierda
    dfs(i,j-1)

    # Derecha
    dfs(i,j+1)

    


# Empezamos desde la posición (0,0)
dfs(0,0)
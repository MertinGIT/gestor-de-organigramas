import os
import pickle
from Funciones_Dependencias import *

class informes():
    def __init__(self, indice):
        self.algo = indice
        self.vec = []
        self.deps = []
        print(indice)
        self.Organigramas_deps = cargar_dependencia_organigrama(self.algo)
        self.name_deps = []
        self.nom_ape = []
        self.nom_ape_extend = []
        self.salarios = []
        self.salarios_extend = []
        self.sucesoras = []
        self.Organigramas = cargar_dependencia_organigrama(self.algo)

    def cargar_datos(self):
        try:
            file_path = os.path.join("archivos_personas", f'organigrama{self.algo}_personas')
            with open(file_path, 'rb') as archivo:
                self.vec = pickle.load(archivo)
        except FileNotFoundError:
              self.vec = []

    #Lista de nombres de personas por dependencia
    def get_nom_ape(self, dep_name):
        aux = ""
        self.nom_ape = []
        for i in range(len(self.vec)):
            for j in range(1):
                aux = self.vec[i][j]
            if self.vec[i][6] == dep_name:
                self.nom_ape.append(self.vec[i][j+1] + " " + aux )
        self.ordenar_nom_ape(self.nom_ape)

        return(self.nom_ape)



    #Lista extendida de personas por dependencia
    def get_nom_ape_extend(self, dep_name):
        aux = ""
        self.nom_ape_extend = []
        file_path = os.path.join("archivos_organigramas", f'organigrama{self.algo}_dependencias')
        with open(file_path, "rb") as archivo:
            self.name_deps = pickle.load(archivo)
        self.Organigramas_deps.raiz = self.name_deps.raiz
        self.name_deps = Enlistar_nom_nodo(self.Organigramas_deps.raiz, [])
        self.sucesoras = mostrar_dependencias_sucesoras(dep_name, self.Organigramas_deps.raiz)
        self.obtener_lista_ordenada(self.vec)

        for i in range(len(self.sucesoras)):
            self.nom_ape_extend.append(self.sucesoras[i])
            for j in range(len(self.vec)):
                if self.vec[j][6] == self.sucesoras[i]:
                    self.nom_ape_extend.append(self.vec[j][1] + " " + self.vec[j][0])
            self.nom_ape_extend.append(" ")

        return self.nom_ape_extend



    def get_salarios_por_dep(self):
        for i in range(len(self.vec)):
            self.salarios.append(self.vec[i][3])
            print(self.salarios)

        print(self.salarios)
    def ordenar_nom_ape(self, VEC):
        N = len(VEC)
        for J in range(N - 1):
            for I in range(N - J - 1):
                if VEC[I + 1] < VEC[I]:
                    VEC[I + 1], VEC[I] = VEC[I], VEC[I + 1]

    #funciones para definir los criterios de ordenamiente en la funcion
    def obtener_primeros_elementos(self):
        return self.vec[0], self.vec[1]

    def obtener_lista_ordenada(self, matriz):
        # Ordenar las dos primeras filas
        # Ordenar las dos primeras columnas
        matriz = sorted(matriz, key=lambda x: (x[0], x[1]))

        # Obtener las posiciones ordenadas de los elementos primeros
        posiciones = sorted(range(len(matriz)),key=lambda x: matriz[x][0])

        # Reordenar la tercera columna en funciÃ³n de las posiciones obtenidas
        columna_tercera = [matriz[i][2] for i in posiciones]

        # Actualizar la matriz con la columna tercera ordenada
        for i in range(len(matriz)):
            matriz[i][2] = columna_tercera[i]
        return matriz

    #Salario por dependencia
    def salario_por_dep(self, dep_name):
        self.salarios = []
        cont = 0
        sum = 0
        for i in range(len(self.vec)):
            aux = self.vec[i][3]
            if aux == "":
                aux = 0

            if self.vec[i][6] == dep_name:
                sum +=  int(aux)
                cont += 1
        self.salarios.append(cont)
        self.salarios.append(sum)
        return self.salarios



    #Salario por dependencia extendida
    def salario_por_dep_extend(self, dep_name):
        aux = ""
        file_path = os.path.join("archivos_organigramas", f'organigrama{self.algo}_dependencias')
        with open(file_path, "rb") as archivo:
            self.name_deps = pickle.load(archivo)
        self.Organigramas_deps.raiz = self.name_deps.raiz
        self.name_deps = Enlistar_nom_nodo(self.Organigramas_deps.raiz, [])
        self.sucesoras = mostrar_dependencias_sucesoras(dep_name, self.Organigramas_deps.raiz)
        self.obtener_lista_ordenada(self.vec)
        self.salarios_extend = []
        for k in range(len(self.sucesoras)):
            self.salarios_extend.append(self.sucesoras[k])

            cont = 0
            sum = 0
            for i in range(len(self.vec)):
                aux = self.vec[i][3]
                if aux == "":
                    aux = 0
                if self.vec[i][6] == self.sucesoras[k] and aux != '.':
                    sum += int(aux)
                    cont += 1
            self.salarios_extend.append(f"La cantidad de personal es: {cont}")
            self.salarios_extend.append(f"El total de salarios es: {sum}")
            self.salarios_extend.append(" ")
        return self.salarios_extend


#informe = informes(43918)

#informe.cargar_datos()
#informe.get_nom_ape("Gerencia")
#informe.get_nom_ape_extend("Gerencia")
#informe.salario_por_dep("Direccion")
#informe.salario_por_dep_extend("Direccion")
#informe.get_salarios_por_dep()
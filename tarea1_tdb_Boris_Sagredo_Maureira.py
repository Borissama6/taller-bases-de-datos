from abc import ABC, abstractmethod
 
class deportista(ABC):
    def __init__(self, nombre, edad, deporte):
        if edad <= 0:
            raise ValueError('Ingreso no válido')
        self.nombre = nombre
        self.edad = edad
        self.deporte = deporte
        self.__puntaje = 0
        self.__cantidad_de_competencias = 0

    @abstractmethod
    def obtener_informacion_basica(self):
        return f"nombre deportista: {self.nombre} deporte que practica: {self.deporte}"

    def obtener_estadisticas(self):
        return f"cantidad de competencias participadas : {self.__cantidad_de_competencias}, cantidad de puntos totales: {self.__puntaje}"

    def reiniciar_puntaje(self):
        self.__puntaje = 0
        self.__cantidad_de_competencias = 0

    def actualizar_puntaje_y_competencias(self, nuevo_puntaje):
        try:
            if nuevo_puntaje >= 0:
                self.__puntaje += nuevo_puntaje
                self.__cantidad_de_competencias += 1
        except ValueError:
            raise ValueError("Error de valor inesperado")

    def obtener_puntaje(self):
        return self.__puntaje
    
    def obtener_deportistas_segun_deporte(self):
        return self.__cantidad_de_competencias

        

class registro:
    def __init__(self):
        self.deportistas = []
    
    def añadir_deportista(self,deportista):
        try:
            if deportista not in self.deportistas:
                self.deportistas.append(deportista)
        except ValueError:
            print("Error al añadirlo o ya existe")

    def mostrar_deportistas(self):
        if not self.deportistas:
            print("No hay deportistas en sistema")
            return
        ordenado = sorted(self.deportistas, key=lambda d: d.obtener_puntaje(), reverse=True)
        
        for sportler in ordenado:
            print(f"{sportler.obtener_informacion_basica()} | Puntos: {sportler.obtener_puntaje()}")

    def mostrar_ranking_por_deporte(self, deporte):
        filtro = [sportler for sportler in self.deportistas if sportler.deporte.lower() == deporte.lower()]
        
        if not filtro:
            print(f"No hay deportistas registrados en {deporte}")
            return
        ranking = sorted(filtro, key=lambda d: d.obtener_puntaje(), reverse=True)

        for sportler in ranking:
            print(f"{sportler.obtener_informacion_basica()} | Puntos: {sportler.obtener_puntaje()}")

    def mostrar_n_mejores_deportistas(self, deporte, n):
        filtro = [d for d in self.deportistas if d.deporte.lower() == deporte.lower()]
        if not filtro:
            print(f"No hay deportistas en: {deporte}")
            return

        ranking = sorted(filtro, key=lambda d: d.obtener_puntaje(), reverse=True)
        for i, d in enumerate(ranking[:n], 1):
            print(f"{i}. {d.obtener_informacion_basica()} | Puntos: {d.obtener_puntaje()}")

    def buscar_deportista(self, nombre):
        for sportler in self.deportistas:
            if sportler.nombre.lower() == nombre.lower():
                return sportler
        return "No encontrado"
            

class Competencia:
    def __init__(self, nombre, fecha, deporte, inscripciones: registro):
        self.nombre = nombre
        self.fecha = fecha
        self.participantes = []
        self.deporte = deporte
        self.resultados = {}
        self.registro = inscripciones

    def inscribir_participante(self, nombre_deportista):
        try:
            deportista_encontrado = self.registro.buscar_deportista(nombre_deportista)
            if deportista_encontrado == "No encontrado":
                raise ValueError(f"El deportista '{nombre_deportista}' no existe en el registro.")
            if deportista_encontrado.deporte.lower() != self.deporte.lower():
                raise ValueError(f"El deportista practica {deportista_encontrado.deporte}, "
                                f"pero la competencia es de {self.deporte}.")
            if deportista_encontrado not in self.participantes:
                self.participantes.append(deportista_encontrado)
                print(f"Inscripción exitosa: {nombre_deportista}")
            else:
                print("El deportista ya está inscrito en esta competencia.")
        except ValueError as e:
            print(f"Error al inscribir: {e}")
    
    def registrar_resultado(self, deportista, puntos):
        if deportista not in self.participantes:
            return "Error - El deportista no está inscrito en la competencia"
            
        if puntos <= 0:
            return "Error - Los puntos deben ser números positivos"
        self.resultados[deportista] = puntos
        deportista.actualizar_puntaje_y_competencias(puntos)

    def mostrar_resultado(self):
        if len(self.resultados) <= 0:
            print('No se registram participantes')
            return
        for participante, puntaje in self.resultados.items():
            print(f' Deportista: {participante.nombre} obtuvo {puntaje} puntos')

    def mostrar_n_posiciones(self, n):
        if n > 0 and n <= len(self.resultados):
            resultados_xd = sorted(self.resultados.items(), key=lambda item: item[1], reverse= True)
            for deportista, puntaje in resultados_xd[:n]:
                print(f' Deportista: {deportista.nombre} obtuvo {puntaje} puntos')
        else:
            print('Error')

                
class Futbolista(deportista):
    def __init__ (self, nombre, edad, equipo, posicion):
        super().__init__(nombre, edad, 'Futbol')
        self.equipo = equipo
        self.__goles = 0
        self.__asistencias = 0
        self.posicion = posicion

    def añadir_goles(self, goles):
        if goles > 0:
            self.__goles += goles
            return
        else:
            print('Error al ingresar goles')
    
    def añadir_asistencias(self, asistencias):
        if asistencias > 0:
            self.__asistencias += asistencias
            return
        else:
            print('Error al ingresar asistencias')
    
    def calcular_rendimiento(self):
        competencias = self.obtener_deportistas_segun_deporte() 
        if competencias == 0:
            return 0
        rendimiento = (self.__goles * 2 + self.__asistencias * 0.7) / competencias
        return rendimiento
    
    def cambiar_de_equipo(self, nuevo_equipo):
        self.equipo = nuevo_equipo
        self.__goles = 0
        self.__cantidad_de_competencias = 0

    def obtener_informacion_basica(self):
        return super().obtener_informacion_basica()

class Tenista(deportista):
    def __init__ (self, nombre, edad, pareja: str, raking_atp: int):
        super().__init__(nombre, edad, 'Tenis')
        self.pareja = pareja
        self.ranking_atp = raking_atp
    
    def actualizar_de_pareja(self, nueva_pareja:str):
        self.pareja = nueva_pareja
        self.reiniciar_puntaje()
    
    def actualizar_ranking(self, nueva_posicion: int):
        if nueva_posicion <= 0:
            return 'Error al ingresar datos'
        else:
            self.ranking_atp = nueva_posicion

    def obtener_informacion_basica(self):
        return f"Tenista: {self.nombre}, Ranking ATP: {self.ranking_atp}, Pareja: {self.pareja}"

class Alteta(deportista):
    def __init__ (self, nombre, edad, disciplina : str):
        super().__init__(nombre, edad, 'Atletismo')
        self.disciplina = disciplina
        self.mejores_tiempos = []
    
    def agregar_mejores_tiempos(self, tiempo):
        if tiempo > 0 and len(self.mejores_tiempos) > 0:
            if tiempo > self.mejores_tiempos[0]:
                self.mejores_tiempos.insert(0, tiempo)
        else:
            print('Datos inválidos')
            return
    
    def obtener_informacion_basica(self):
        return f"Atleta: {self.nombre}, Disciplina: {self.disciplina}"
    

def ejecutar_simulacion():
    # Crear del Registro
    registro_general = registro() 

    # 2. Creación de Deportistas
    f1 = Futbolista("Alexis Sanchez", 35, "Tocopilla FC", "Delantero")
    f2 = Futbolista("Arturo Vidal", 36, "Colo-Colo", "Mediocampista")
    t1 = Tenista("Nicolas Jarry", 28, "Sin Pareja", 20)
    t2 = Tenista("Alejandro Tabilo", 26, "Tomas Barrios", 38)
    a1 = Alteta("Martina Weil", 24, "400m planos")

    # Registro de deportistas
    registro_general.añadir_deportista(f1)
    registro_general.añadir_deportista(f2)
    registro_general.añadir_deportista(t1)
    registro_general.añadir_deportista(t2)
    registro_general.añadir_deportista(a1)
    #print("AÑADIDOS CORRECTAMENTE")

    # Métodos específicos de cada deporte
    f1.añadir_goles(10)
    f1.añadir_asistencias(5)
    t1.actualizar_ranking(19)
    a1.agregar_mejores_tiempos(51.07)
    a1.agregar_mejores_tiempos(51.12)
    print(f"Goles añadidos a {f1.nombre}. Ranking actualizado para {t1.nombre}.")

    print("\nProbar competencia e inscripciones")
    copa_america = Competencia("Copa America 2026", "2026-06-15", "Futbol", registro_general)

    copa_america.inscribir_participante("Alexis Sanchez")
    copa_america.inscribir_participante("Arturo Vidal")
    copa_america.inscribir_participante("Nicolas Jarry") ##Noatr tenista en competencia de futbol

    copa_america.registrar_resultado(f1, 500)
    copa_america.registrar_resultado(f2, 350)

    print("\n[7] Mostrando resultados y posiciones de la competencia...")
    print(f'resultados copa america: {copa_america.mostrar_resultado()}')
    print(f'N posiciones: {copa_america.mostrar_n_posiciones(3)}')

    print(f'Todos los deportistas: {registro_general.mostrar_deportistas()}')
    

    print("\nRanking de Fútbol")
    registro_general.mostrar_ranking_por_deporte("Futbol")

    print(f'Mejor futbolista: {registro_general.mostrar_n_mejores_deportistas("Futbol", 1)}')

    print("\nEstadísticas de la clase madre/rendimiento")
    print(f"Estadísticas Alexis Sanchez: {f1.obtener_estadisticas()}")
    print(f"Rendimiento Alexis Sanchez: {f1.calcular_rendimiento()}")

    print("\nProbando reglas de pérdida de puntos")
    print(f"Puntos de {f2.nombre} ANTES de cambiar equipo: {f2.obtener_puntaje()}")
    f2.cambiar_de_equipo("Boca Juniors")
    print(f"Puntos de {f2.nombre} despues de cambiar equipo: {f2.obtener_puntaje()}")

    t2.actualizar_de_pareja("Cristian Garin")
    print(f"Pareja de {t2.nombre} actualizada con éxito.")

if __name__ == "__main__":
    try:
        ejecutar_simulacion()
    except Exception as e:
        print(f"\nError: {e}")
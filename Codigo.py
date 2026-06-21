#==========================================================================================================================================================================
#Aqui haremos el proyecto de introduccion a la programacion
#==========================================================================================================================================================================
import tkinter as tk
from PIL import Image, ImageTk
import json
from math import hypot

#Creacion de clases
class Usuario:
    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = contraseña
        self.victorias_atacante = 0
        self.victorias_defensor = 0

class Estructura:
    """
    Clase base para todo lo que el atacante puede destruir durante el combate:
    muros, torres y la base central. Centraliza la vida y el daño recibido
    para no repetir la misma lógica en cada subclase.
    """
    def __init__(self, vida, fila, columna):
        self.vida_max = vida
        self.vida = vida
        self.fila = fila
        self.columna = columna

    def recibir_daño(self, daño):
        """Resta vida a la estructura. Devuelve True si quedó destruida."""
        self.vida -= daño
        if self.vida < 0:
            self.vida = 0
        return self.vida <= 0


class Muro(Estructura):
    VIDA_BASE = 40

    def __init__(self, fila, columna):
        super().__init__(Muro.VIDA_BASE, fila, columna)


class BaseCentral(Estructura):
    VIDA_BASE = 200

    def __init__(self, fila, columna):
        super().__init__(BaseCentral.VIDA_BASE, fila, columna)


class Torre(Estructura):
    def __init__(self, valor, daño, vida, alcance, costo, fila=None, columna=None):
        super().__init__(vida, fila, columna)
        self.valor = valor
        self.daño = daño
        self.alcance = alcance
        self.costo = costo
        self.objetivo = None  # enemigo que esta torre está atacando en este momento

    def en_rango(self, enemigo):
        """Revisa si un enemigo está dentro del alcance de esta torre."""
        distancia = hypot(self.fila - enemigo.fila, self.columna - enemigo.columna)
        return distancia <= self.alcance

    def elegir_objetivo(self, enemigos_vivos):
        """
        Si el objetivo actual sigue vivo y en rango, lo conserva.
        Si no, busca entre los enemigos vivos el más cercano que esté en rango.
        """
        if self.objetivo is not None and self.objetivo.vida > 0 and self.en_rango(self.objetivo):
            return self.objetivo

        candidatos = [enemigo for enemigo in enemigos_vivos if self.en_rango(enemigo)]
        if not candidatos:
            self.objetivo = None
            return None

        self.objetivo = min(
            candidatos,
            key=lambda enemigo: hypot(self.fila - enemigo.fila, self.columna - enemigo.columna)
        )
        return self.objetivo

    def atacar(self):
        """
        Le hace daño al objetivo actual de la torre.
        Devuelve al enemigo si murió por este ataque, o None si sigue vivo.
        """
        if self.objetivo is None:
            return None
        destruido = self.objetivo.recibir_daño(self.daño)
        if destruido:
            enemigo_eliminado = self.objetivo
            self.objetivo = None
            return enemigo_eliminado
        return None


class Enemigo:
    def __init__(self, daño, vida, rapidez, costo):
        self.daño = daño
        self.vida_max = vida
        self.vida = vida
        self.rapidez = rapidez
        self.costo = costo
        # Estos atributos se completan cuando el enemigo se coloca en el tablero
        self.fila = None
        self.columna = None
        self.objetivo = None       # Torre o BaseCentral que persigue (en linea recta)
        self.bloqueado_por = None  # Muro que le impide el paso y que debe romper primero

    def recibir_daño(self, daño):
        """Resta vida al enemigo. Devuelve True si quedó destruido."""
        self.vida -= daño
        if self.vida < 0:
            self.vida = 0
        return self.vida <= 0

    def buscar_objetivo(self, estructuras_vivas):
        """
        Busca la estructura más cercana en linea recta para ir a destruirla.
        Solo considera torres y la base central (los muros no son un destino,
        son obstaculos que se atacan unicamente si se interponen en el camino).
        """
        candidatos = [e for e in estructuras_vivas if isinstance(e, (Torre, BaseCentral))]
        if not candidatos:
            self.objetivo = None
            return None
        self.objetivo = min(
            candidatos,
            key=lambda estructura: hypot(self.fila - estructura.fila, self.columna - estructura.columna)
        )
        return self.objetivo

    def _golpear(self, estructura):
        """Le pega a una estructura (muro u objetivo final). Devuelve la estructura si murió."""
        destruido = estructura.recibir_daño(self.daño)
        if destruido:
            if estructura is self.bloqueado_por:
                self.bloqueado_por = None
            if estructura is self.objetivo:
                self.objetivo = None
            return estructura
        return None

    def mover_o_atacar(self, estructuras_vivas):
        """
        Se ejecuta en cada paso del combate (un 'tick' del temporizador):
        - Si hay un muro bloqueando el camino, lo ataca hasta destruirlo.
        - Si ya esta junto a su objetivo (torre o base), lo ataca en vez de moverse.
        - Si no, avanza en linea recta hacia su objetivo, a la velocidad de su tipo.
        Devuelve la estructura destruida en este paso, o None si no destruyó nada.
        """
        if self.objetivo is None:
            return None

        if self.bloqueado_por is not None:
            if self.bloqueado_por.vida <= 0:
                self.bloqueado_por = None
            else:
                return self._golpear(self.bloqueado_por)

        distancia_objetivo = hypot(self.objetivo.fila - self.fila, self.objetivo.columna - self.columna)
        if distancia_objetivo <= 0.6:
            return self._golpear(self.objetivo)

        paso = self.rapidez * FACTOR_VELOCIDAD
        dx = (self.objetivo.columna - self.columna) / distancia_objetivo
        dy = (self.objetivo.fila - self.fila) / distancia_objetivo
        nueva_fila = self.fila + dy * paso
        nueva_columna = self.columna + dx * paso

        # Si en el camino hacia la nueva posicion hay un muro vivo, se detiene a romperlo
        for estructura in estructuras_vivas:
            if isinstance(estructura, Muro) and estructura.vida > 0:
                if hypot(estructura.fila - nueva_fila, estructura.columna - nueva_columna) < 0.5:
                    self.bloqueado_por = estructura
                    return self._golpear(estructura)

        self.fila = nueva_fila
        self.columna = nueva_columna
        return None


torre_basica = Torre(3,15,60,10,2)
torre_ligera = Torre(4,10,50,15,3)
torre_pesada = Torre(5,25,80,5,5)

enemigo_basico = Enemigo(25,350,10,2)
enemigo_rapido = Enemigo(20,230,25,4)
enemigo_fuerte = Enemigo(50,550,5,5)

jugador1_listo = False
jugador2_listo = False
ancho_ventana = 1376
alto_ventana = 768
dinero_jugador1 = 30
dinero_jugador2 = 40

# ----- Variables nuevas para el turno del atacante y el sistema de rondas -----
nombre_jugador1 = None        # nombre del usuario que juega como defensor en esta partida
nombre_jugador2 = None        # nombre del usuario que juega como atacante en esta partida
rondas_ganadas_defensor = 0   # rondas ganadas por el jugador 1 en la partida actual
rondas_ganadas_atacante = 0   # rondas ganadas por el jugador 2 en la partida actual

DINERO_INICIAL = 30           # dinero con el que arranca cada jugador en la ronda 1
BONUS_RONDA = 10              # dinero extra que se suma por cada ronda que ya se jugó
FACTOR_VELOCIDAD = 0.045      # convierte "rapidez" del enemigo en casillas avanzadas por tick
INTERVALO_COMBATE = 150       # milisegundos entre cada paso de la simulacion de combate













#==========================================================================================================================================================================
ventana_principal = tk.Tk()
ventana_principal.geometry("1376x768+300+150")
ventana_principal.title("CLASH OF TEC")
ventana_principal.resizable(False, False)

inicio = tk.Frame(ventana_principal)
menu   = tk.Frame(ventana_principal)

imagen_inicio = Image.open("Imagenes/Portada.PNG")  
imagen_tk = ImageTk.PhotoImage(imagen_inicio)
portada = tk.Label(inicio , image=imagen_tk)
portada.pack()

imagen_inicio2 = Image.open("Imagenes/Menu.PNG")  
imagen_tk2 = ImageTk.PhotoImage(imagen_inicio2)
interfaz = tk.Label(menu , image=imagen_tk2)
interfaz.pack()

def entrar():
    inicio.pack_forget()
    menu.pack(fill="both", expand=True)
tk.Button(portada, text="JUGAR",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=entrar, font=(10)).place(relx=0.43,rely=0.45)

def salir():
    ventana_principal.destroy()
ventana_principal.protocol("WM_DELETE_WINDOW", ventana_principal.destroy)




def actualizar_victoria(nombre, rol_ganador):
    """
    Suma una victoria (como 'atacante' o 'defensor') al usuario indicado
    dentro de usuarios.json. Si el usuario no existe en el archivo (por ejemplo,
    si nombre es None porque algo falló en el login), no hace nada.
    """
    if not nombre:
        return
    try:
        with open("usuarios.json", "r") as archivo:
            usuarios = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    for usuario in usuarios:
        if usuario["nombre"] == nombre:
            if rol_ganador == "defensor":
                usuario["victorias_defensor"] += 1
            else:
                usuario["victorias_atacante"] += 1
            break

    with open("usuarios.json", "w") as archivo:
        json.dump(usuarios, archivo, indent=4)











#===================================Frame donde se empezara el juego=========================================================== 

def iniciar_partida():
    global dinero_jugador1, dinero_jugador2

    menu.pack_forget()

    numero_ronda = rondas_ganadas_defensor + rondas_ganadas_atacante + 1
    # El dinero se hereda de la ronda anterior; solo se le suma un bono al
    # arrancar una ronda nueva (la ronda 1 ya arranca en DINERO_INICIAL,
    # asignado en jugar() cuando se registran los jugadores).
    if numero_ronda > 1:
        dinero_jugador1 += BONUS_RONDA
        dinero_jugador2 += BONUS_RONDA

    juego = tk.Frame(ventana_principal,width=ancho_ventana,height=alto_ventana,bg="#b6a38d")
    juego.pack(fill="both", expand=True)

    tk.Label(juego, text="TURNO DEL JUGADOR 1", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 25, "bold")).place(relx=0.6, rely=0.05)
    tk.Label(juego, text=f"Ronda {numero_ronda}  |  Marcador -> Defensor: {rondas_ganadas_defensor}  Atacante: {rondas_ganadas_atacante}",
            bg="#b6a38d", fg="#462d1c", justify="center",
            font=("Arial", 12, "bold")).place(relx=0.62, rely=0.005)
    tk.Label(juego, text="Coloca la base central y las estructuras para defenderla \n Cada estructura cuesta dinero, asi que utilizalo sabiamente", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 15, "bold")).place(relx=0.55, rely=0.1)
    texto_base_central = tk.Label(juego, text="La base central sera la estructura que tienes que defender \n Colocala en una posicion estrategica!",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 12, "bold"))
    texto_base_central.place(relx=0.6, rely=0.18) 
    tk.Label(juego, text="El muro detiene a los atacantes es \n bueno rodear a la base central con ellos",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 12, "bold")).place(relx=0.65, rely=0.28)  
    tk.Label(juego, text="Costo: 1",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 11, "bold")).place(relx=0.8,rely=0.35)
    tk.Label(juego, text="Las torres defienden la base central, atacando a los intrusos \n Cada torre tiene su caracteristica",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 12, "bold")).place(relx=0.6, rely=0.4)   
    tk.Label(juego, text="Tipo de torre",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 12, "bold")).place(relx=0.65, rely=0.48)   
    tk.Label(juego, text="Daño\n\n\n15\n\n\n\n10\n\n\n\n25",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 12, "bold")).place(relx=0.75, rely=0.48)  
    tk.Label(juego, text="Alcance\n\n\n10\n\n\n\n15\n\n\n\n5",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 12, "bold")).place(relx=0.8, rely=0.48)
    tk.Label(juego, text="Costo\n\n\n2\n\n\n\n3\n\n\n\n5",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 12, "bold")).place(relx=0.85, rely=0.48)
    tk.Label(juego, text="Si cometiste un error y \n quieres tu dinero de vuelta. \n Puedes borrar",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 10, "bold")).place(relx=0.55, rely=0.82)
    
    texto_dinero = tk.Label(juego, text=f"Dinero: {dinero_jugador1}",
            bg="#b6a38d", fg="gold", justify="center",
            font=("Arial", 14, "bold"))
    texto_dinero.place(relx=0.8, rely=0.85)

    img = Image.open("Imagenes/Marco.PNG")
    nuevo_ancho = int(img.width * (768/270))
    nuevo_alto = int(img.height * (768/270))
    img = img.resize(
        (nuevo_ancho, nuevo_alto),
        Image.Resampling.LANCZOS)
    imagen_tk3 = ImageTk.PhotoImage(img)
    imagen_cuadricula = tk.Label(juego, image=imagen_tk3)
    imagen_cuadricula.image = imagen_tk3
    imagen_cuadricula.place(relx=0,rely=0)
    #====================================================================================
    
    tamaño = 40
    tamaño_matriz = 15
    
    matriz_defensa = [[0 for _ in range(tamaño_matriz)] for _ in range(tamaño_matriz)]

    contador_base_central = 0
    item_selecionado = 1

    colores = {
        0:"White",
        1:"Yellow",
        2:"gray",
        3:"blue",
        4:"green",
        5:"purple",}
    
    canvas_defensa = tk.Canvas(juego, width=tamaño*tamaño_matriz, 
                               height=tamaño*tamaño_matriz,bg="white",
                               highlightthickness=0)
    canvas_defensa.place(relx=0.05,rely=0.1)

    def dibujar_cuadricula():
        for fila in range(tamaño_matriz):
            for columna in range(tamaño_matriz):
                x1 = columna * tamaño
                y1 = fila * tamaño

                x2 = x1 + tamaño
                y2 = y1 + tamaño

                canvas_defensa.create_rectangle(
                    x1,y1,x2,y2,
                    fill = "white",outline="Black")        
    dibujar_cuadricula()

    def actualizar_celda(fila,columna):
        x1 = columna * tamaño
        y1 = fila * tamaño

        x2 = x1 + tamaño
        y2 = y1 + tamaño

        color = colores[matriz_defensa[fila][columna]]
        canvas_defensa.create_rectangle(
            x1,y1,x2,y2,
            fill=color, outline="black")
        
    def click_en_cuadricula(event):
        nonlocal contador_base_central
        global dinero_jugador1

        columna = event.x //tamaño
        fila = event.y // tamaño 

        if not (0 <= fila < tamaño_matriz and 0 <= columna < tamaño_matriz):
            return

        if matriz_defensa[fila][columna] == 1 and item_selecionado != 1:
            contador_base_central -= 1

        if item_selecionado == 1:
            if contador_base_central == 0:
                matriz_defensa[fila][columna] = 1
                contador_base_central += 1
        else:
            if item_selecionado == 0:
                if matriz_defensa[fila][columna] != 0 and matriz_defensa[fila][columna] != 1:
                    if matriz_defensa[fila][columna] == 3:
                        dinero_jugador1 += 2
                    elif matriz_defensa[fila][columna] == 4:
                        dinero_jugador1 += 3
                    elif matriz_defensa[fila][columna] == 5:
                        dinero_jugador1 += 5
                    else:
                        dinero_jugador1 += 1
                matriz_defensa[fila][columna] = item_selecionado
                texto_dinero.config(text=f"Dinero: {dinero_jugador1}")
            else:
                if dinero_jugador1 >= 1 and matriz_defensa[fila][columna] == 0:
                    if item_selecionado == 3:
                        dinero_jugador1 -= 2
                    elif item_selecionado == 4:
                        dinero_jugador1 -= 3
                    elif item_selecionado == 5:
                        dinero_jugador1 -= 5
                    else:
                        dinero_jugador1 -= 1
                    matriz_defensa[fila][columna] = item_selecionado
                    texto_dinero.config(text=f"Dinero: {dinero_jugador1}")

        actualizar_celda(fila,columna)
    canvas_defensa.bind("<Button-1>",click_en_cuadricula)

    def seleccionar_herramienta(id_item):
        nonlocal item_selecionado
        item_selecionado = id_item
        texto_herramienta.config(text=f"Estructura actual: {estructuras[item_selecionado]}")


    estructuras = {0:"Borrador",1:"Base central",2:"Muro",3:"Torre basica",4:"Torre ligera",5:"Torre pesada"}
    
    texto_herramienta = tk.Label(juego, text=f"Estructura actual: {estructuras[item_selecionado]}",
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 10, "bold"))
    texto_herramienta.place(relx=0.8, rely=0.83)
    
    tk.Button(juego, text="Borrar",width=8, 
            relief="groove",bd=5, bg="#b6a38d", fg="#462d1c",
        command=lambda: seleccionar_herramienta(0)
    ).place(relx=0.7,rely=0.85)

    tk.Button(juego, text="Base Central",width=10, 
            relief="groove",bd=5, bg="#b6a38d", fg="#462d1c",
        command=lambda: seleccionar_herramienta(1)
    ).place(relx=0.7,rely=0.24)

    tk.Button(juego, text="Muro",width=8, 
            relief="groove",bd=5, bg="#b6a38d", fg="#462d1c",
        command=lambda: seleccionar_herramienta(2)
    ).place(relx=0.7,rely=0.35)

    tk.Button( juego, text="Torre Básica",width=9, 
            relief="groove",bd=5, bg="#b6a38d", fg="#462d1c",
        command=lambda: seleccionar_herramienta(3)
    ).place(relx=0.66,rely=0.55)

    tk.Button( juego, text="Torre Ligera",width=10, 
            relief="groove",bd=5, bg="#b6a38d", fg="#462d1c",
        command=lambda: seleccionar_herramienta(4)
    ).place(relx=0.66,rely=0.65)

    tk.Button(juego, text="Torre Pesada",width=10, 
            relief="groove",bd=5, bg="#b6a38d", fg="#462d1c",
        command=lambda: seleccionar_herramienta(5)
    ).place(relx=0.66,rely=0.75)

    #===================================Frame donde se iniciara el turno del atacante============================================================
    def turno_atacante():
        juego.pack_forget()
        atacar = tk.Frame(ventana_principal,width=ancho_ventana,height=alto_ventana,bg="#b6a38d")
        atacar.pack(fill="both", expand=True)

        tk.Label(atacar, text="TURNO DEL JUGADOR 2",
                bg="#b6a38d", fg="blue", justify="center",
                font=("Arial", 25, "bold")).place(relx=0.6, rely=0.05)
        tk.Label(atacar, text=f"Ronda {numero_ronda}  |  Marcador -> Defensor: {rondas_ganadas_defensor}  Atacante: {rondas_ganadas_atacante}",
                bg="#b6a38d", fg="#462d1c", justify="center",
                font=("Arial", 12, "bold")).place(relx=0.62, rely=0.005)
        tk.Label(atacar, text="Coloca tus unidades unicamente en la zona sombreada del borde \n Cuando termines, presiona 'Iniciar Ataque'",
                bg="#b6a38d", fg="blue", justify="center",
                font=("Arial", 15, "bold")).place(relx=0.55, rely=0.1)
        texto_explicacion_atacante = tk.Label(atacar, text="Cada unidad ira en linea recta hacia la torre o base mas cercana \n Si un muro se interpone en el camino, lo atacara hasta destruirlo antes de seguir",
                bg="#b6a38d", fg="blue", justify="center",
                font=("Arial", 12, "bold"))
        texto_explicacion_atacante.place(relx=0.55, rely=0.18)
        tk.Label(atacar, text="Tipo de unidad",
                bg="#b6a38d", fg="blue", justify="center",
                font=("Arial", 12, "bold")).place(relx=0.63, rely=0.30)
        tk.Label(atacar, text="Daño\n\n\n25\n\n\n\n20\n\n\n\n50",
                bg="#b6a38d", fg="blue", justify="center",
                font=("Arial", 12, "bold")).place(relx=0.72, rely=0.30)
        tk.Label(atacar, text="Velocidad\n\n\n10\n\n\n\n25\n\n\n\n5",
                bg="#b6a38d", fg="blue", justify="center",
                font=("Arial", 12, "bold")).place(relx=0.79, rely=0.30)
        tk.Label(atacar, text="Costo\n\n\n2\n\n\n\n4\n\n\n\n5",
                bg="#b6a38d", fg="blue", justify="center",
                font=("Arial", 12, "bold")).place(relx=0.88, rely=0.30)

        texto_dinero2 = tk.Label(atacar, text=f"Dinero atacante: {dinero_jugador2}",
                bg="#b6a38d", fg="gold", justify="center",
                font=("Arial", 14, "bold"))
        texto_dinero2.place(relx=0.76, rely=0.78)

        texto_dinero1_combate = tk.Label(atacar, text=f"Dinero defensor: {dinero_jugador1}",
                bg="#b6a38d", fg="gold", justify="center",
                font=("Arial", 14, "bold"))
        texto_dinero1_combate.place(relx=0.76, rely=0.82)

        img2 = Image.open("Imagenes/Marco.PNG")
        nuevo_ancho2 = int(img2.width * (768/270))
        nuevo_alto2 = int(img2.height * (768/270))
        img2 = img2.resize((nuevo_ancho2, nuevo_alto2), Image.Resampling.LANCZOS)
        imagen_tk_atacar = ImageTk.PhotoImage(img2)
        marco_atacar = tk.Label(atacar, image=imagen_tk_atacar)
        marco_atacar.image = imagen_tk_atacar
        marco_atacar.place(relx=0, rely=0)

        canvas_ataque = tk.Canvas(atacar, width=tamaño*tamaño_matriz,
                                   height=tamaño*tamaño_matriz, bg="white",
                                   highlightthickness=0)
        canvas_ataque.place(relx=0.05, rely=0.1)

        def es_borde(fila, columna):
            return fila == 0 or fila == tamaño_matriz - 1 or columna == 0 or columna == tamaño_matriz - 1

        def dibujar_cuadricula_ataque():
            for fila in range(tamaño_matriz):
                for columna in range(tamaño_matriz):
                    x1 = columna * tamaño
                    y1 = fila * tamaño
                    x2 = x1 + tamaño
                    y2 = y1 + tamaño
                    if es_borde(fila, columna) and matriz_defensa[fila][columna] == 0:
                        relleno = "#e8d9c0"  # zona habilitada para colocar enemigos
                    else:
                        relleno = "white"
                    canvas_ataque.create_rectangle(x1, y1, x2, y2, fill=relleno, outline="black", tags="grid")
        dibujar_cuadricula_ataque()

        # ---- Construye las estructuras reales (con vida propia) a partir de lo que armo el defensor ----
        def construir_estructuras(matriz):
            plantillas_torres = {3: torre_basica, 4: torre_ligera, 5: torre_pesada}
            nuevas_estructuras = []
            for fila in range(len(matriz)):
                for columna in range(len(matriz[fila])):
                    tipo = matriz[fila][columna]
                    if tipo == 1:
                        nuevas_estructuras.append(BaseCentral(fila, columna))
                    elif tipo == 2:
                        nuevas_estructuras.append(Muro(fila, columna))
                    elif tipo in plantillas_torres:
                        plantilla = plantillas_torres[tipo]
                        nuevas_estructuras.append(Torre(plantilla.valor, plantilla.daño, plantilla.vida,
                                                         plantilla.alcance, plantilla.costo, fila, columna))
            return nuevas_estructuras

        estructuras_vivas = construir_estructuras(matriz_defensa)
        enemigos_colocados = []

        plantillas_enemigos = {1: enemigo_basico, 2: enemigo_rapido, 3: enemigo_fuerte}
        unidades = {0: "Borrador", 1: "Enemigo básico", 2: "Enemigo rápido", 3: "Enemigo fuerte"}
        colores_enemigos = {
            enemigo_basico.costo: "orange",
            enemigo_rapido.costo: "cyan",
            enemigo_fuerte.costo: "black",
        }

        item_seleccionado_atacante = 1
        combate_activo = False

        texto_herramienta_atacante = tk.Label(atacar, text=f"Unidad actual: {unidades[item_seleccionado_atacante]}",
                bg="#b6a38d", fg="blue", justify="center",
                font=("Arial", 10, "bold"))
        texto_herramienta_atacante.place(relx=0.76, rely=0.74)

        def seleccionar_herramienta_atacante(id_item):
            nonlocal item_seleccionado_atacante
            item_seleccionado_atacante = id_item
            texto_herramienta_atacante.config(text=f"Unidad actual: {unidades[item_seleccionado_atacante]}")

        tk.Button(atacar, text="Borrar", width=8,
                relief="groove", bd=5, bg="#b6a38d", fg="#462d1c",
            command=lambda: seleccionar_herramienta_atacante(0)
        ).place(relx=0.7, rely=0.85)

        tk.Button(atacar, text="Enemigo Básico", width=13,
                relief="groove", bd=5, bg="#b6a38d", fg="#462d1c",
            command=lambda: seleccionar_herramienta_atacante(1)
        ).place(relx=0.65, rely=0.42)

        tk.Button(atacar, text="Enemigo Rápido", width=13,
                relief="groove", bd=5, bg="#b6a38d", fg="#462d1c",
            command=lambda: seleccionar_herramienta_atacante(2)
        ).place(relx=0.65, rely=0.52)

        tk.Button(atacar, text="Enemigo Fuerte", width=13,
                relief="groove", bd=5, bg="#b6a38d", fg="#462d1c",
            command=lambda: seleccionar_herramienta_atacante(3)
        ).place(relx=0.65, rely=0.62)

        def hay_enemigo_en(fila, columna):
            return any(enemigo.vida > 0 and round(enemigo.fila) == fila and round(enemigo.columna) == columna
                       for enemigo in enemigos_colocados)

        def redibujar_combate():
            canvas_ataque.delete("dinamico")
            for estructura in estructuras_vivas:
                if estructura.vida <= 0:
                    continue
                x1 = estructura.columna * tamaño
                y1 = estructura.fila * tamaño
                x2 = x1 + tamaño
                y2 = y1 + tamaño
                if isinstance(estructura, BaseCentral):
                    color = colores[1]
                elif isinstance(estructura, Muro):
                    color = colores[2]
                else:
                    color = colores[estructura.valor]
                canvas_ataque.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="dinamico")
                proporcion = max(estructura.vida, 0) / estructura.vida_max
                canvas_ataque.create_rectangle(x1, y2 - 6, x2, y2 - 2, fill="gray", outline="", tags="dinamico")
                canvas_ataque.create_rectangle(x1, y2 - 6, x1 + (x2 - x1) * proporcion, y2 - 2, fill="red", outline="", tags="dinamico")

            for enemigo in enemigos_colocados:
                if enemigo.vida <= 0:
                    continue
                cx = enemigo.columna * tamaño + tamaño / 2
                cy = enemigo.fila * tamaño + tamaño / 2
                radio = tamaño / 2 - 8
                color = colores_enemigos[enemigo.costo]
                canvas_ataque.create_oval(cx - radio, cy - radio, cx + radio, cy + radio, fill=color, outline="black", tags="dinamico")
                proporcion = max(enemigo.vida, 0) / enemigo.vida_max
                canvas_ataque.create_rectangle(cx - radio, cy - radio - 8, cx + radio, cy - radio - 4, fill="gray", outline="", tags="dinamico")
                canvas_ataque.create_rectangle(cx - radio, cy - radio - 8, cx - radio + (2 * radio) * proporcion, cy - radio - 4, fill="red", outline="", tags="dinamico")

        def click_en_cuadricula_ataque(event):
            global dinero_jugador2

            if combate_activo:
                return

            columna = event.x // tamaño
            fila = event.y // tamaño
            if not (0 <= fila < tamaño_matriz and 0 <= columna < tamaño_matriz):
                return
            if not es_borde(fila, columna):
                return
            if matriz_defensa[fila][columna] != 0:
                return

            if item_seleccionado_atacante == 0:
                for enemigo in enemigos_colocados:
                    if enemigo.vida > 0 and round(enemigo.fila) == fila and round(enemigo.columna) == columna:
                        enemigo.vida = 0
                        dinero_jugador2 += enemigo.costo
                        texto_dinero2.config(text=f"Dinero atacante: {dinero_jugador2}")
                        break
            else:
                plantilla = plantillas_enemigos[item_seleccionado_atacante]
                if dinero_jugador2 >= plantilla.costo and not hay_enemigo_en(fila, columna):
                    nuevo_enemigo = Enemigo(plantilla.daño, plantilla.vida_max, plantilla.rapidez, plantilla.costo)
                    nuevo_enemigo.fila = fila
                    nuevo_enemigo.columna = columna
                    enemigos_colocados.append(nuevo_enemigo)
                    dinero_jugador2 -= plantilla.costo
                    texto_dinero2.config(text=f"Dinero atacante: {dinero_jugador2}")

            redibujar_combate()

        canvas_ataque.bind("<Button-1>", click_en_cuadricula_ataque)
        redibujar_combate()

        def lanzar_bola(torre, enemigo):
            """Anima una pequeña bola que viaja de la torre al enemigo que está atacando."""
            x0 = torre.columna * tamaño + tamaño / 2
            y0 = torre.fila * tamaño + tamaño / 2
            x1 = enemigo.columna * tamaño + tamaño / 2
            y1 = enemigo.fila * tamaño + tamaño / 2
            bola = canvas_ataque.create_oval(x0 - 4, y0 - 4, x0 + 4, y0 + 4, fill="black", tags="bola")

            pasos = 6
            dx = (x1 - x0) / pasos
            dy = (y1 - y0) / pasos

            def animar(paso_actual=0):
                if paso_actual >= pasos:
                    canvas_ataque.delete(bola)
                    return
                canvas_ataque.move(bola, dx, dy)
                atacar.after(25, lambda: animar(paso_actual + 1))
            animar()

        def ciclo_combate():
            global dinero_jugador1, dinero_jugador2
            nonlocal combate_activo

            if not combate_activo:
                return

            # --- Fase de ataque de las torres ---
            enemigos_vivos = [e for e in enemigos_colocados if e.vida > 0]
            for estructura in estructuras_vivas:
                if isinstance(estructura, Torre) and estructura.vida > 0:
                    objetivo = estructura.elegir_objetivo(enemigos_vivos)
                    if objetivo is not None:
                        lanzar_bola(estructura, objetivo)
                        enemigo_destruido = estructura.atacar()
                        if enemigo_destruido is not None:
                            dinero_jugador1 += enemigo_destruido.costo
                            texto_dinero1_combate.config(text=f"Dinero defensor: {dinero_jugador1}")
                            enemigos_vivos = [e for e in enemigos_colocados if e.vida > 0]

            # --- Fase de movimiento / ataque de los enemigos ---
            estructuras_en_pie = [s for s in estructuras_vivas if s.vida > 0]
            for enemigo in enemigos_vivos:
                if enemigo.vida <= 0:
                    continue
                if enemigo.objetivo is None or enemigo.objetivo.vida <= 0:
                    enemigo.buscar_objetivo(estructuras_en_pie)
                estructura_destruida = enemigo.mover_o_atacar(estructuras_en_pie)
                if estructura_destruida is not None:
                    if isinstance(estructura_destruida, BaseCentral):
                        redibujar_combate()
                        terminar_ronda("atacante")
                        return
                    elif isinstance(estructura_destruida, Torre):
                        dinero_jugador2 += estructura_destruida.costo
                        texto_dinero2.config(text=f"Dinero atacante: {dinero_jugador2}")
                        estructuras_en_pie = [s for s in estructuras_vivas if s.vida > 0]
                    # Si lo destruido fue un muro, simplemente desaparece (no da dinero)

            redibujar_combate()

            if not any(e.vida > 0 for e in enemigos_colocados):
                terminar_ronda("defensor")
                return

            atacar.after(INTERVALO_COMBATE, ciclo_combate)

        def terminar_ronda(ganador):
            nonlocal combate_activo
            global rondas_ganadas_defensor, rondas_ganadas_atacante
            combate_activo = False

            if ganador == "defensor":
                rondas_ganadas_defensor += 1
                mensaje = "¡El defensor ganó esta ronda!"
            else:
                rondas_ganadas_atacante += 1
                mensaje = "¡El atacante ganó esta ronda!"

            tk.Label(atacar, text=f"{mensaje}\nMarcador -> Defensor: {rondas_ganadas_defensor}   Atacante: {rondas_ganadas_atacante}",
                    bg="#b6a38d", fg="darkred", justify="center",
                    font=("Arial", 18, "bold")).place(relx=0.32, rely=0.45)

            if rondas_ganadas_defensor >= 3 or rondas_ganadas_atacante >= 3:
                ganador_partida = "defensor" if rondas_ganadas_defensor >= 3 else "atacante"
                nombre_ganador = nombre_jugador1 if ganador_partida == "defensor" else nombre_jugador2
                actualizar_victoria(nombre_ganador, ganador_partida)

                def volver_al_menu():
                    atacar.destroy()
                    menu.pack(fill="both", expand=True)

                tk.Button(atacar, text=f"¡{nombre_ganador or 'Jugador'} gana la partida!  Volver al menú",
                        relief="groove", bd=5, bg="#b6a38d", fg="#462d1c",
                    command=volver_al_menu
                ).place(relx=0.30, rely=0.55)
            else:
                tk.Button(atacar, text="Siguiente ronda",
                        relief="groove", bd=5, bg="#b6a38d", fg="#462d1c",
                    command=lambda: iniciar_partida(atacar)
                ).place(relx=0.35, rely=0.55)

        def iniciar_ataque():
            nonlocal combate_activo
            if combate_activo:
                return
            combate_activo = True
            boton_iniciar_ataque.config(state="disabled")
            ciclo_combate()

        boton_iniciar_ataque = tk.Button(atacar, text="Iniciar Ataque", width=12,
                relief="groove", bd=5, bg="#b6a38d", fg="#462d1c",
            command=iniciar_ataque
        )
        boton_iniciar_ataque.place(relx=0.9, rely=0.9)

        def terminar_juego_atacante():
            nonlocal combate_activo
            combate_activo = False
            atacar.pack_forget()
            menu.pack(fill="both", expand=True)

        tk.Button(atacar, text="Terminar juego", width=12,
                relief="groove", bd=5, bg="#b6a38d", fg="#462d1c",
            command=terminar_juego_atacante
        ).place(relx=0.7, rely=0.95)

    #===============================================================================================================================

    def verificar_inicio_partido():
        if contador_base_central == 1:
            turno_atacante()
        else:
            texto_base_central.config(text="La base central sera la estructura que tienes que defender \n Sin una, no se puede pasar el turno")


    tk.Button(juego, text="Listo",width=10, 
            relief="groove",bd=5, bg="#b6a38d", fg="#462d1c",
        command=verificar_inicio_partido
    ).place(relx=0.9,rely=0.9)
    

    def terminar_juego():
        juego.pack_forget()
        menu.pack(fill="both", expand=True)


    tk.Button(juego, text="Terminar juego",width=12, 
            relief="groove",bd=5, bg="#b6a38d", fg="#462d1c",
        command=terminar_juego
    ).place(relx=0.7,rely=0.95)

#===============================================================================================================================









#======================Frame donde se inicia sesion o se crea la cuenta=======================
def jugar():
    global dinero_jugador1, dinero_jugador2, rondas_ganadas_defensor, rondas_ganadas_atacante
    global nombre_jugador1, nombre_jugador2
    dinero_jugador1 = DINERO_INICIAL
    dinero_jugador2 = DINERO_INICIAL + 10
    rondas_ganadas_defensor = 0
    rondas_ganadas_atacante = 0
    nombre_jugador1 = None
    nombre_jugador2 = None
    #=========================Jugador 1===========================
    registrar1 = tk.Frame(menu)
    registrar1.place(relx = 0.31, rely=0.1)

    imagen_inicio3 = Image.open("Imagenes/Marco.PNG")  
    imagen_tk3 = ImageTk.PhotoImage(imagen_inicio3)
    registro1 = tk.Label(registrar1, image=imagen_tk3)
    registro1.image = imagen_tk3
    registro1.pack()

    texto_label1_1 = tk.Label(registrar1, text="Quien sera el jugador 1?", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 13, "bold"))
    texto_label1_1.place(relx=0.11, rely=0.15)

    texto_label1_2 = tk.Label(registrar1, text="Has jugado antes?", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 11, "bold"))
    texto_label1_2.place(relx=0.25, rely=0.25)

    texto_label1_3 = tk.Label(registrar1, text="Eres nuevo?", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 11, "bold"))
    texto_label1_3.place(relx=0.32, rely=0.52)

    def pestaña_iniciar_sesion1():
        texto_label1_1.place_forget()
        texto_label1_2.place_forget()
        texto_label1_3.place_forget()
        boton_iniciar_sesion1.place_forget()
        boton_crear_cuenta1.place_forget()

        texto_label1_4 = tk.Label(registrar1, text="Ingresa tu usuario", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 11, "bold"))
        texto_label1_4.place(relx=0.24, rely=0.15)

        entrada_usuario1 = tk.Entry(registrar1, width=15)
        entrada_usuario1.place(relx=0.3,rely=0.25)

        texto_label1_5 = tk.Label(registrar1, text="Ingresa tu contraseña", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 11, "bold"))
        texto_label1_5.place(relx=0.2, rely=0.4)

        entrada_contraseña1 = tk.Entry(registrar1, width=15)
        entrada_contraseña1.place(relx=0.3,rely=0.51)
        

        def jugador1_preparado(nombre):
            global jugador1_listo, nombre_jugador1
            nombre_jugador1 = nombre
            texto_label1_4.place_forget()
            entrada_usuario1.place_forget()
            texto_label1_5 .place_forget()
            entrada_contraseña1.place_forget()
            boton_ingresar1.place_forget()
            texto_label1_6 = tk.Label(registrar1, text="Jugador 1 listo", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 13, "bold"))
            texto_label1_6.place(relx=0.3, rely=0.4)
            jugador1_listo = True
            if jugador1_listo and jugador2_listo:
                iniciar_partida()


        def iniciar_sesion():

            with open("usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)

            for usuario in usuarios:
                if (usuario["nombre"] == entrada_usuario1.get() and
                    usuario["contrasena"] == entrada_contraseña1.get()):
                    jugador1_preparado(usuario["nombre"])
                    return usuario
            texto_label1_4.config(text="Usuario incorrecto")
            texto_label1_5.config(text="O contraseña incorrecto")
            return None

        boton_ingresar1 = tk.Button(registrar1,text="Ingresar",width=8, 
            relief="groove",bd=5, bg="#b6a38d", 
            fg="#462d1c", command=iniciar_sesion, font=(8))
        boton_ingresar1.place(relx=0.3,rely=0.6)


    def pestaña_crear_cuenta1():
        texto_label1_1.place_forget()
        texto_label1_2.place_forget()
        texto_label1_3.place_forget()
        boton_iniciar_sesion1.place_forget()
        boton_crear_cuenta1.place_forget()

        texto_label1_4 = tk.Label(registrar1, text="Nombra tu usuario", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 11, "bold"))
        texto_label1_4.place(relx=0.24, rely=0.15)

        entrada_usuario1 = tk.Entry(registrar1, width=15)
        entrada_usuario1.place(relx=0.3,rely=0.25)

        texto_label1_5 = tk.Label(registrar1, text="Crea tu contraseña", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 11, "bold"))
        texto_label1_5.place(relx=0.20, rely=0.4)

        entrada_contraseña1 = tk.Entry(registrar1, width=15)
        entrada_contraseña1.place(relx=0.3,rely=0.51)

        def guardar_usuario(usuario):
            try:
                with open("usuarios.json", "r") as archivo:
                    usuarios = json.load(archivo)
            except (FileNotFoundError, json.JSONDecodeError):
                usuarios = []

            for usuario_json in usuarios:
                if usuario_json["nombre"] == entrada_usuario1.get():
                    texto_label1_4.config(text="El nombre de usuario")
                    texto_label1_5.config(text="ya esta en uso")
                    return

            usuarios.append({
                "nombre": usuario.nombre,
                "contrasena": usuario.contraseña,
                "victorias_atacante": usuario.victorias_atacante,
                "victorias_defensor": usuario.victorias_defensor})

            with open("usuarios.json", "w") as archivo:
                json.dump(usuarios, archivo, indent=4)
            jugador1_preparado(usuario.nombre)

        def jugador1_preparado(nombre):
            global jugador1_listo, nombre_jugador1
            nombre_jugador1 = nombre
            texto_label1_4.place_forget()
            entrada_usuario1.place_forget()
            texto_label1_5 .place_forget()
            entrada_contraseña1.place_forget()
            boton_ingresar1.place_forget()
            texto_label1_6 = tk.Label(registrar1, text="Jugador 1 listo", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 13, "bold"))
            texto_label1_6.place(relx=0.3, rely=0.4)
            jugador1_listo = True
            if jugador1_listo and jugador2_listo:
                iniciar_partida()
         
        def crear_cuenta():
            nuevo_usuario = Usuario(entrada_usuario1.get(), entrada_contraseña1.get())
            guardar_usuario(nuevo_usuario)
            

        boton_ingresar1 = tk.Button(registrar1,text="Crear",width=8, 
            relief="groove",bd=5, bg="#b6a38d", 
            fg="#462d1c", command=crear_cuenta, font=(8))
        boton_ingresar1.place(relx=0.3,rely=0.6)


    boton_iniciar_sesion1 = tk.Button(registrar1, text="Iniciar sesion",width=10, 
            relief="groove",bd=5, bg="#b6a38d", 
            fg="#462d1c", command=pestaña_iniciar_sesion1, font=(10))
    boton_iniciar_sesion1.place(relx=0.3,rely=0.35)

    boton_crear_cuenta1 = tk.Button(registrar1, text="Crear cuenta",width=10, 
            relief="groove",bd=5, bg="#b6a38d", 
            fg="#462d1c", command=pestaña_crear_cuenta1, font=(10))
    boton_crear_cuenta1.place(relx=0.3,rely=0.62)


    #=========================Jugador 2===========================
    registrar2 = tk.Frame(menu)
    registrar2.place(relx = 0.5, rely=0.1)

    imagen_inicio4 = Image.open("Imagenes/Marco.PNG")  
    imagen_tk4 = ImageTk.PhotoImage(imagen_inicio4)
    registro2 = tk.Label(registrar2, image=imagen_tk4)
    registro2.image = imagen_tk4
    registro2.pack()

    texto_label2_1 = tk.Label(registrar2, text="Quien sera el jugador 2?", 
            bg="#b6a38d", fg="blue", justify="center",
            font=("Arial", 13, "bold"))
    texto_label2_1.place(relx=0.11, rely=0.15)

    texto_label2_2 = tk.Label(registrar2, text="Has jugado antes?", 
            bg="#b6a38d", fg="blue", justify="center",
            font=("Arial", 11, "bold"))
    texto_label2_2.place(relx=0.25, rely=0.25)

    texto_label2_3 = tk.Label(registrar2, text="Eres nuevo?", 
            bg="#b6a38d", fg="blue", justify="center",
            font=("Arial", 11, "bold"))
    texto_label2_3.place(relx=0.32, rely=0.52)
    
    def pestaña_iniciar_sesion2():
        texto_label2_1.place_forget()
        texto_label2_2.place_forget()
        texto_label2_3.place_forget()
        boton_iniciar_sesion2.place_forget()
        boton_crear_cuenta2.place_forget()

        texto_label2_4 = tk.Label(registrar2, text="Ingresa tu usuario", 
            bg="#b6a38d", fg="Blue", justify="center",
            font=("Arial", 11, "bold"))
        texto_label2_4.place(relx=0.24, rely=0.15)

        entrada_usuario2 = tk.Entry(registrar2, width=15)
        entrada_usuario2.place(relx=0.3,rely=0.25)

        texto_label2_5 = tk.Label(registrar2, text="Ingresa tu contraseña", 
            bg="#b6a38d", fg="Blue", justify="center",
            font=("Arial", 11, "bold"))
        texto_label2_5.place(relx=0.2, rely=0.4)

        entrada_contraseña2 = tk.Entry(registrar2, width=15)
        entrada_contraseña2.place(relx=0.3,rely=0.51)

        def jugador2_preparado(nombre):
            global jugador2_listo, nombre_jugador2
            nombre_jugador2 = nombre
            texto_label2_4.place_forget()
            entrada_usuario2.place_forget()
            texto_label2_5 .place_forget()
            entrada_contraseña2.place_forget()
            boton_ingresar2.place_forget()
            texto_label2_6 = tk.Label(registrar2, text="Jugador 2 listo", 
            bg="#b6a38d", fg="blue", justify="center",
            font=("Arial", 13, "bold"))
            texto_label2_6.place(relx=0.3, rely=0.4)
            jugador2_listo = True
            if jugador1_listo and jugador2_listo:
                iniciar_partida()

        def iniciar_sesion():

            with open("usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)

            for usuario in usuarios:
                if (usuario["nombre"] == entrada_usuario2.get() and
                    usuario["contrasena"] == entrada_contraseña2.get()):
                    jugador2_preparado(usuario["nombre"])
                    return usuario
            texto_label2_4.config(text="Usuario incorrecto")
            texto_label2_5.config(text="O contraseña incorrecto")
            return None

        boton_ingresar2 = tk.Button(registrar2,text="Ingresar",width=8, 
            relief="groove",bd=5, bg="#b6a38d", 
            fg="#462d1c", command=iniciar_sesion, font=(8))
        boton_ingresar2.place(relx=0.3,rely=0.6)

    def pestaña_crear_cuenta2():
        texto_label2_1.place_forget()
        texto_label2_2.place_forget()
        texto_label2_3.place_forget()
        boton_iniciar_sesion2.place_forget()
        boton_crear_cuenta2.place_forget()

        texto_label2_4 = tk.Label(registrar2, text="Nombra tu usuario", 
            bg="#b6a38d", fg="blue", justify="center",
            font=("Arial", 11, "bold"))
        texto_label2_4.place(relx=0.24, rely=0.15)

        entrada_usuario2 = tk.Entry(registrar2, width=15)
        entrada_usuario2.place(relx=0.3,rely=0.25)

        texto_label2_5 = tk.Label(registrar2, text="Crea tu contraseña", 
            bg="#b6a38d", fg="blue", justify="center",
            font=("Arial", 11, "bold"))
        texto_label2_5.place(relx=0.20, rely=0.4)

        entrada_contraseña2 = tk.Entry(registrar2, width=15)
        entrada_contraseña2.place(relx=0.3,rely=0.51)

        def guardar_usuario(usuario):
            try:
                with open("usuarios.json", "r") as archivo:
                    usuarios = json.load(archivo)
            except (FileNotFoundError, json.JSONDecodeError):
                usuarios = []

            for usuario_json in usuarios:
                if usuario_json["nombre"] == entrada_usuario2.get():
                    texto_label2_4.config(text="El nombre de usuario")
                    texto_label2_5.config(text="ya esta en uso")
                    return

            usuarios.append({
                "nombre": usuario.nombre,
                "contrasena": usuario.contraseña,
                "victorias_atacante": usuario.victorias_atacante,
                "victorias_defensor": usuario.victorias_defensor})

            with open("usuarios.json", "w") as archivo:
                json.dump(usuarios, archivo, indent=4)
            jugador2_preparado(usuario.nombre)

        def jugador2_preparado(nombre):
            global jugador2_listo, nombre_jugador2
            nombre_jugador2 = nombre
            texto_label2_4.place_forget()
            entrada_usuario2.place_forget()
            texto_label2_5 .place_forget()
            entrada_contraseña2.place_forget()
            boton_ingresar2.place_forget()
            texto_label2_6 = tk.Label(registrar2, text="Jugador 2 listo", 
            bg="#b6a38d", fg="blue", justify="center",
            font=("Arial", 13, "bold"))
            texto_label2_6.place(relx=0.3, rely=0.4)
            jugador2_listo = True
            if jugador1_listo and jugador2_listo:
                iniciar_partida()
         
        def crear_cuenta():
            nuevo_usuario = Usuario(entrada_usuario2.get(), entrada_contraseña2.get())
            guardar_usuario(nuevo_usuario)
            

        boton_ingresar2 = tk.Button(registrar2,text="Crear",width=8, 
            relief="groove",bd=5, bg="#b6a38d", 
            fg="#462d1c", command=crear_cuenta, font=(8))
        boton_ingresar2.place(relx=0.3,rely=0.6)


    boton_iniciar_sesion2 = tk.Button(registrar2, text="Iniciar sesion",width=10, 
            relief="groove",bd=5, bg="#b6a38d", 
            fg="#462d1c", command=pestaña_iniciar_sesion2, font=(10))
    boton_iniciar_sesion2.place(relx=0.3,rely=0.35)

    boton_crear_cuenta2 = tk.Button(registrar2, text="Crear cuenta",width=10, 
            relief="groove",bd=5, bg="#b6a38d", 
            fg="#462d1c", command=pestaña_crear_cuenta2, font=(10))
    boton_crear_cuenta2.place(relx=0.3,rely=0.62)


    #===========================================================================
    def atras():
        global jugador1_listo, jugador2_listo
        registrar1.place_forget()
        registrar2.place_forget()
        jugador1_listo = False
        jugador2_listo = False
    boton_atras1 =tk.Button(registrar1, text="Atras",width=10, 
                            relief="groove",bd=5, bg="#b6a38d", 
                            fg="#462d1c", command=atras)
    boton_atras1.place(relx=0.35,rely=0.8)
    boton_atras2 = tk.Button(registrar2, text="Atras",width=10, 
                            relief="groove",bd=5, bg="#b6a38d", 
                            fg="#462d1c", command=atras)
    boton_atras2.place(relx=0.35,rely=0.8)
#=========================================================================================





#===================================Frame donde estaran las estadisticas=========================================
def estadisticas():
    pass
#================================================================================================================








tk.Button(portada, text="JUGAR",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=entrar, font=(10)).place(relx=0.43,rely=0.45)
tk.Button(interfaz, text="JUGAR",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=jugar).place(relx=0.45,rely=0.1)
tk.Button(interfaz, text="Estadisticas",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=estadisticas).place(relx=0.45,rely=0.2)

tk.Button(interfaz, text="SALIR",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=salir).place(relx=0.45,rely=0.3)

inicio.pack(fill="both", expand=True)

ventana_principal.mainloop()
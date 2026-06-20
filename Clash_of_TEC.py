#==========================================================================================================================================================================
#Aqui haremos el proyecto de introduccion a la programacion
#==========================================================================================================================================================================
import tkinter as tk
import time
from PIL import Image, ImageTk
import json

#Creacion de clases
class Usuario:
    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = contraseña
        self.victorias_atacante = 0
        self.victorias_defensor = 0

class Torres:
    def __init__(self,valor,daño,alcance,costo):
        self.valor = valor 
        self.daño = daño
        self.alcance = alcance
        self.costo = costo


jugador1_listo = False
jugador2_listo = False
ancho_ventana = 1376
alto_ventana = 768
dinero_jugador1 = 30
dinero_jugador2 = 30

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
#===================================Frame donde se empezara el juego=========================================================== 















def iniciar_partida():
    menu.pack_forget()
    juego = tk.Frame(ventana_principal,width=ancho_ventana,height=alto_ventana,bg="#b6a38d")
    juego.pack(fill="both", expand=True)

    tk.Label(juego, text="TURNO DEL JUGADOR 1", 
            bg="#b6a38d", fg="red", justify="center",
            font=("Arial", 25, "bold")).place(relx=0.6, rely=0.05)
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
                    dinero_jugador1 += 1
                matriz_defensa[fila][columna] = item_selecionado
                texto_dinero.config(text=f"Dinero: {dinero_jugador1}")
            else:
                if dinero_jugador1 >= 1 and matriz_defensa[fila][columna] == 0:
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
    global dinero_jugador1,dinero_jugador2
    dinero_jugador1 = 30
    dinero_jugador2 = 30
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
        

        def jugador1_preparado():
            global jugador1_listo
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
                    jugador1_preparado()
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
            jugador1_preparado()

        def jugador1_preparado():
            global jugador1_listo
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

        def jugador2_preparado():
            global jugador2_listo
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
                    jugador2_preparado()
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
            jugador2_preparado()

        def jugador2_preparado():
            global jugador2_listo
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





tk.Button(portada, text="JUGAR",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=entrar, font=(10)).place(relx=0.43,rely=0.45)
tk.Button(interfaz, text="JUGAR",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=jugar).place(relx=0.45,rely=0.1)
tk.Button(interfaz, text="Estadisticas",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=iniciar_partida).place(relx=0.45,rely=0.2)

tk.Button(interfaz, text="SALIR",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=salir).place(relx=0.45,rely=0.3)

inicio.pack(fill="both", expand=True)

ventana_principal.mainloop()

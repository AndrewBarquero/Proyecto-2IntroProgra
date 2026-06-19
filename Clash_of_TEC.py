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


jugador1_listo = False
jugador2_listo = False
#==========================================================================================================================================================================
ventana_principal = tk.Tk()
ventana_principal.geometry("+300+150")
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

#======================Frame donde se inicia sesion o se crea la cuenta=======================
def jugar():
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

    tk.Label(registrar2, text="Quien sera el jugador 2?", 
            bg="#b6a38d", fg="blue", justify="center",
            font=("Arial", 13, "bold")).place(relx=0.11, rely=0.15)
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
                        fg="#462d1c", command=salir).place(relx=0.45,rely=0.2)

tk.Button(interfaz, text="SALIR",width=15, 
                        relief="groove",bd=15, bg="#b6a38d", 
                        fg="#462d1c", command=salir).place(relx=0.45,rely=0.3)

inicio.pack(fill="both", expand=True)



ventana_principal.mainloop()

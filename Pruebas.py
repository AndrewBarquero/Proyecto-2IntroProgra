"""
import tkinter as tk

root = tk.Tk()
root.geometry("800x600")

inicio = tk.Frame(root)
juego = tk.Frame(root)

# Pantalla inicio
tk.Label(inicio, text="MENÚ PRINCIPAL").pack()

def ir_juego():
    inicio.pack_forget()
    juego.pack(fill="both", expand=True)

tk.Button(inicio, text="Jugar", command=ir_juego).pack()

# Pantalla juego
tk.Label(juego, text="ESTÁS JUGANDO").pack()

def volver():
    juego.pack_forget()
    inicio.pack(fill="both", expand=True)

tk.Button(juego, text="Volver", command=volver).pack()

inicio.pack(fill="both", expand=True)

root.mainloop()
"""
"""
import json
archivo = open("Archivo_pruebas.txt", "r") #Abre el .txt para leerlo
lista_ventas = archivo.readlines() #Hace una lista de strings con las lineas que tiene 
archivo.close()
print(lista_ventas)
usuario1 = json.dumps(lista_ventas[1])
print(usuario1)
"""
import tkinter as tk

root = tk.Tk()

# Menú principal
lbl_titulo = tk.Label(root, text="Mi Juego")
lbl_titulo.pack()

# Frame oculto
frame_login = tk.Frame(root)

tk.Label(frame_login, text="Iniciar Sesión").pack()
tk.Button(frame_login, text="Entrar").pack()

tk.Label(frame_login, text="Crear Cuenta").pack()
tk.Button(frame_login, text="Registrarse").pack()

def jugar():
    frame_login.pack(pady=20)

btn_jugar = tk.Button(root, text="Jugar", command=jugar)
btn_jugar.pack()

root.mainloop()
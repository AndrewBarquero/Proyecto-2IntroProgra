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
mensaje = tk.Label(root, text="Palabra correcta")

entrada = tk.Entry(root)
entrada.pack()
def leer():
    palabra = entrada.get()
    print(palabra)
    print(type(palabra))
    if palabra == "Hola":
        mensaje.pack()
tk.Button(root, text="Boton", command=leer).pack()

root.mainloop()
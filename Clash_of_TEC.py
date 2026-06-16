"""
#==========================================================================================================================================================================
#Aqui haremos el proyecto de introduccion a la programacion
#==========================================================================================================================================================================
import tkinter as tk
import time
from PIL import Image, ImageTk
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
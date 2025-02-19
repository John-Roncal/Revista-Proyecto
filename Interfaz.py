import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc

# Conexión a SQL Server
def conectar_db():
    try:
        conexion = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-R58HSL2K;"
            "DATABASE=RevistaBD;"
            "Trusted_Connection=yes;"
        )
        return conexion
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

# Función para guardar datos en la base de datos
def guardar_datos():
    empresa = entry_empresa.get()
    correo = entry_correo.get()
    categoria = combo_categoria.get()

    if not empresa or not correo or not categoria:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return

    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO Clientes (Empresa, Correo, Categoria) VALUES (?, ?, ?)",
                (empresa, correo, categoria)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Datos guardados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los datos: {e}")
        finally:
            conexion.close()

# Interfaz gráfica mejorada
app = tk.Tk()
app.title("Gestión de Clientes")
app.geometry("350x250")
app.configure(bg="#f4f4f4")

frame = tk.Frame(app, padx=20, pady=20, bg="white", relief=tk.RIDGE, bd=3)
frame.pack(pady=20)

tk.Label(frame, text="Empresa:", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_empresa = tk.Entry(frame, width=30)
entry_empresa.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Correo:", font=("Arial", 10, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_correo = tk.Entry(frame, width=30)
entry_correo.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Categoría:", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
combo_categoria = ttk.Combobox(frame, values=["Gastronomía", "Deportes", "Entretenimiento"], state="readonly", width=27)
combo_categoria.grid(row=2, column=1, padx=10, pady=5)

btn_guardar = tk.Button(frame, text="Guardar", command=guardar_datos, bg="#28a745", fg="white", font=("Arial", 10, "bold"))
btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)

app.mainloop()

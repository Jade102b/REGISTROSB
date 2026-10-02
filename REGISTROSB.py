import customtkinter as ctk
from tkinter import ttk, messagebox

# Configuración del tema general
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Base de datos local temporal
BASEDATOS_PASTELES = [
    {"nombre": "Pastel de Fresas con Crema", "categoria": "Pastel Entero", "precio": 25.00, "descuento": "20% OFF", "precio_final": 20.00, "sabor": "Fresa / Vainilla"},
    {"nombre": "Cupcake de Chocolate Supremo", "categoria": "Cupcake", "precio": 4.00, "descuento": "Sin descuento", "precio_final": 4.00, "sabor": "Chocolate Negro"},
    {"nombre": "Tarta de Frutos Rojos", "categoria": "Tarta", "precio": 18.50, "descuento": "20% OFF", "precio_final": 14.80, "sabor": "Mora y Frambuesa"}
]

# Colores personalizados (Cake Rest Theme)
COLOR_ROSA = "#FF6B8B"
COLOR_ROSA_HOVER = "#FF4F73"
COLOR_CAFE = "#A67C52"
COLOR_CAFE_HOVER = "#8C653E"
COLOR_FONDO = "#FFF8F5"
COLOR_TEXTO = "#4A3525"


# Ventana 1: Formulario de Registro
class VentanaRegistro(ctk.CTkToplevel):
    def __init__(self, parent, callback_actualizacion=None):
        super().__init__(parent)
        self.title("🍰 Registro de Pastel - Cake Rest")
        self.geometry("420x580")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_FONDO)
        self.callback_actualizacion = callback_actualizacion

        # Hacer que la ventana resalte
        self.attributes("-topmost", True)

        self.iniciar_ui()

    def iniciar_ui(self):
        # Título
        lbl_titulo = ctk.CTkLabel(
            self, 
            text="🧁 Registrar Nuevo Pastel", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TEXTO
        )
        lbl_titulo.pack(pady=(20, 2))

        lbl_subtitulo = ctk.CTkLabel(
            self, 
            text="Taste & Enjoy - Sistema de Inventario", 
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        lbl_subtitulo.pack(pady=(0, 15))

        # Marco del formulario
        frame_form = ctk.CTkFrame(self, fg_color="transparent")
        frame_form.pack(fill="both", expand=True, padx=30, pady=5)

        # Campo: Nombre
        ctk.CTkLabel(frame_form, text="Nombre del Pastel:", text_color=COLOR_TEXTO, font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 2))
        self.entry_nombre = ctk.CTkEntry(frame_form, placeholder_text="Ej. Pastel de Fresas", border_color="#E8C3B9")
        self.entry_nombre.pack(fill="x", pady=(0, 10))

        # Campo: Categoría
        ctk.CTkLabel(frame_form, text="Categoría:", text_color=COLOR_TEXTO, font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 2))
        self.combo_categoria = ctk.CTkOptionMenu(
            frame_form, 
            values=["Pastel Entero", "Porción / Rebanada", "Cupcake", "Tarta", "Postre Frío"],
            button_color=COLOR_CAFE,
            button_hover_color=COLOR_CAFE_HOVER,
            dropdown_fg_color="#FFFFFF"
        )
        self.combo_categoria.pack(fill="x", pady=(0, 10))

        # Campo: Sabor / Relleno
        ctk.CTkLabel(frame_form, text="Sabor / Relleno:", text_color=COLOR_TEXTO, font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 2))
        self.entry_sabor = ctk.CTkEntry(frame_form, placeholder_text="Ej. Chocolate y Vainilla", border_color="#E8C3B9")
        self.entry_sabor.pack(fill="x", pady=(0, 10))

        # Campo: Precio
        ctk.CTkLabel(frame_form, text="Precio Base ($):", text_color=COLOR_TEXTO, font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 2))
        self.entry_precio = ctk.CTkEntry(frame_form, placeholder_text="15.00", border_color="#E8C3B9")
        self.entry_precio.pack(fill="x", pady=(0, 10))
        self.entry_precio.bind("<KeyRelease>", lambda event: self.calcular_precio_final())

        # Campo: Descuento
        ctk.CTkLabel(frame_form, text="Descuento Promo:", text_color=COLOR_TEXTO, font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 2))
        self.combo_descuento = ctk.CTkOptionMenu(
            frame_form, 
            values=["Sin descuento", "20% OFF", "10% OFF", "30% OFF"],
            button_color=COLOR_CAFE,
            button_hover_color=COLOR_CAFE_HOVER,
            command=lambda choice: self.calcular_precio_final()
        )
        self.combo_descuento.pack(fill="x", pady=(0, 10))

        # Visualización Precio Final
        self.lbl_precio_final = ctk.CTkLabel(
            frame_form, 
            text="Precio Final: $ 0.00", 
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLOR_ROSA
        )
        self.lbl_precio_final.pack(pady=10)

        # Botón Guardar
        btn_guardar = ctk.CTkButton(
            self, 
            text="💖 Guardar Registro", 
            fg_color=COLOR_ROSA, 
            hover_color=COLOR_ROSA_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.guardar_registro
        )
        btn_guardar.pack(fill="x", padx=30, pady=(10, 20))

    def calcular_precio_final(self):
        try:
            precio = float(self.entry_precio.get())
        except ValueError:
            precio = 0.0

        desc_texto = self.combo_descuento.get()
        porcentaje = 0
        if "20%" in desc_texto:
            porcentaje = 0.20
        elif "10%" in desc_texto:
            porcentaje = 0.10
        elif "30%" in desc_texto:
            porcentaje = 0.30

        precio_final = precio * (1 - porcentaje)
        self.lbl_precio_final.configure(text=f"Precio Final: $ {precio_final:.2f}")
        return precio_final

    def guardar_registro(self):
        nombre = self.entry_nombre.get().strip()
        sabor = self.entry_sabor.get().strip()

        if not nombre or not sabor:
            messagebox.showwarning("Campos Incompletos", "Por favor completa el nombre y el sabor del pastel.")
            return

        try:
            precio = float(self.entry_precio.get())
        except ValueError:
            messagebox.showwarning("Precio Inválido", "Por favor ingresa un precio numérico válido.")
            return

        precio_final = self.calcular_precio_final()

        nuevo_pastel = {
            "nombre": nombre,
            "categoria": self.combo_categoria.get(),
            "precio": precio,
            "descuento": self.combo_descuento.get(),
            "precio_final": precio_final,
            "sabor": sabor
        }

        BASEDATOS_PASTELES.append(nuevo_pastel)
        messagebox.showinfo("¡Éxito!", f"¡El pastel '{nombre}' ha sido registrado correctamente!")

        if self.callback_actualizacion:
            self.callback_actualizacion()

        self.destroy()


# Ventana 2: Tabla de Historial / Lista
class VentanaLista(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📜 Pasteles Registrados - Cake Rest")
        self.geometry("700x480")
        self.configure(fg_color=COLOR_FONDO)

        self.attributes("-topmost", True)
        self.iniciar_ui()

    def iniciar_ui(self):
        # Título
        lbl_titulo = ctk.CTkLabel(
            self, 
            text="🍩 Pasteles Registrados", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXTO
        )
        lbl_titulo.pack(pady=(15, 10))

        # Buscador
        frame_busqueda = ctk.CTkFrame(self, fg_color="transparent")
        frame_busqueda.pack(fill="x", padx=20, pady=5)

        self.entry_buscar = ctk.CTkEntry(
            frame_busqueda, 
            placeholder_text="🔍 Buscar por nombre o sabor...",
            border_color="#E8C3B9"
        )
        self.entry_buscar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_buscar.bind("<KeyRelease>", lambda event: self.cargar_datos())

        btn_refrescar = ctk.CTkButton(
            frame_busqueda, 
            text="🔄 Actualizar", 
            fg_color=COLOR_CAFE, 
            hover_color=COLOR_CAFE_HOVER,
            width=100,
            command=self.cargar_datos
        )
        btn_refrescar.pack(side="right")

        # Tabla con tkinter Treeview personalizado
        frame_tabla = ctk.CTkFrame(self, fg_color="transparent")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        # Estilo para la tabla Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground=COLOR_TEXTO,
            rowheight=28,
            fieldbackground="#FFFFFF",
            font=('Segoe UI', 10)
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_CAFE,
            foreground="white",
            font=('Segoe UI', 10, 'bold')
        )
        style.map("Treeview", background=[('selected', COLOR_ROSA)])

        columnas = ("nombre", "categoria", "precio", "descuento", "p_final", "sabor")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("precio", text="Precio Base")
        self.tabla.heading("descuento", text="Promo")
        self.tabla.heading("p_final", text="Precio Final")
        self.tabla.heading("sabor", text="Sabor")

        self.tabla.column("nombre", width=150)
        self.tabla.column("categoria", width=100)
        self.tabla.column("precio", width=80, anchor="center")
        self.tabla.column("descuento", width=90, anchor="center")
        self.tabla.column("p_final", width=90, anchor="center")
        self.tabla.column("sabor", width=130)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botón Eliminar
        btn_eliminar = ctk.CTkButton(
            self, 
            text="🗑️ Eliminar Seleccionado", 
            fg_color="#E8C3B9", 
            text_color=COLOR_TEXTO,
            hover_color="#DDA89A",
            command=self.eliminar_seleccionado
        )
        btn_eliminar.pack(pady=(0, 15))

        self.cargar_datos()

    def cargar_datos(self):
        # Limpiar filas existentes
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        filtro = self.entry_buscar.get().lower()

        for item in BASEDATOS_PASTELES:
            if filtro in item["nombre"].lower() or filtro in item["sabor"].lower():
                self.tabla.insert("", "end", values=(
                    item["nombre"],
                    item["categoria"],
                    f"${item['precio']:.2f}",
                    item["descuento"],
                    f"${item['precio_final']:.2f}",
                    item["sabor"]
                ))

    def eliminar_seleccionado(self):
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Atención", "Selecciona una fila para eliminar.")
            return

        item_vals = self.tabla.item(selected_item)["values"]
        nombre = item_vals[0]

        BASEDATOS_PASTELES[:] = [p for p in BASEDATOS_PASTELES if p["nombre"] != nombre]
        self.cargar_datos()
        messagebox.showinfo("Eliminado", f"Se eliminó '{nombre}' del registro.")


# Ventana Principal (Menú)
class VentanaMenuPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CAKE REST - Panel Principal 🍰")
        self.geometry("380x420")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_FONDO)

        self.win_registro = None
        self.win_lista = None

        self.iniciar_ui()

    def iniciar_ui(self):
        # Header / Logotipo
        lbl_brand = ctk.CTkLabel(
            self, 
            text="CAKE REST", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLOR_ROSA
        )
        lbl_brand.pack(pady=(35, 2))

        lbl_slogan = ctk.CTkLabel(
            self, 
            text="Taste & Enjoy • Sistema Pastelería", 
            font=ctk.CTkFont(size=12),
            text_color=COLOR_CAFE
        )
        lbl_slogan.pack(pady=(0, 25))

        # Botones Principales
        btn_nuevo = ctk.CTkButton(
            self, 
            text="➕ Registrar Nuevo Pastel", 
            fg_color=COLOR_ROSA, 
            hover_color=COLOR_ROSA_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            corner_radius=15,
            command=self.abrir_registro
        )
        btn_nuevo.pack(fill="x", padx=40, pady=10)

        btn_ver_lista = ctk.CTkButton(
            self, 
            text="📋 Ver Todos los Pasteles", 
            fg_color=COLOR_CAFE, 
            hover_color=COLOR_CAFE_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            corner_radius=15,
            command=self.abrir_lista
        )
        btn_ver_lista.pack(fill="x", padx=40, pady=10)

        # Pie de página
        lbl_footer = ctk.CTkLabel(
            self, 
            text="Desarrollado con CustomTkinter", 
            font=ctk.CTkFont(size=10),
            text_color="#AAAAAA"
        )
        lbl_footer.pack(side="bottom", pady=15)

    def abrir_registro(self):
        if self.win_registro is None or not self.win_registro.winfo_exists():
            cb = self.win_lista.cargar_datos if (self.win_lista and self.win_lista.winfo_exists()) else None
            self.win_registro = VentanaRegistro(self, callback_actualizacion=cb)
        else:
            self.win_registro.focus()

    def abrir_lista(self):
        if self.win_lista is None or not self.win_lista.winfo_exists():
            self.win_lista = VentanaLista(self)
        else:
            self.win_lista.focus()


if __name__ == "__main__":
    app = VentanaMenuPrincipal()
    app.mainloop()
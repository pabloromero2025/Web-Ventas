import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import random

# --- CONFIGURACIÓN DE LA PÁGINA WEB ---
st.set_page_config(
    page_title="Sistema de Gestión Comercial Pro v1.0",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE ESTILOS CSS PERSONALIZADOS (DARK MODE ELEGANTE & SIN FRANJA BLANCA) ---
st.markdown(
    """
    <style>
        @import url('https://googleapis.com');

        html, body, [class*="css"] {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        .stApp, [data-testid="stHeader"], [data-testid="stToolbar"] {
            background-color: #0f172a !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stSidebar"] {
            background-color: #1e293b !important;
            border-right: 1px solid #334155;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF  !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        h1 {
            font-size: 2.2rem !important;
            margin-bottom: 0.5rem !important;
        }

        p, label, span, .stMarkdown, small {
            color: #cbd5e1 !important;
        }

        div[data-testid="stForm"], div[data-testid="stMetric"], .stContainer, div[class*="border"] {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
            padding: 1rem;
        }

        div[data-testid="stMetricValue"] {
            color: #048582 !important;
            font-weight: 700 !important;
            font-size: 1.8rem !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }

        /* --- 🎨 SELECTORES Y CUADROS DE TEXTO CON FONDO NEGRO --- */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #000000 !important; /* Fondo Negro Absoluto para la caja cerrada */
            color: #f8fafc !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
        }
        
        /* Forzado para la lista desplegable interna cuando se abre el menú */
        ul[data-testid="stSelectboxVirtualList"], div[data-baseweb="menu"] {
            background-color: #000000 !important; /* Fondo Negro Absoluto para la lista abierta */
            border: 1px solid #334155 !important;
        }

        /* Color del texto de las opciones dentro de la lista abierta */
        ul[data-testid="stSelectboxVirtualList"] li, div[data-baseweb="menu"] div {
            color: #cbd5e1 !important;
            background-color: #000000 !important;
        }

        /* Efecto de resaltado al pasar el mouse por encima de una opción del menú */
        ul[data-testid="stSelectboxVirtualList"] li:hover, div[data-baseweb="menu"] div:hover {
            background-color: #10b981 !important; /* Resalta en Verde Esmeralda al pasar el cursor */
            color: #000000 !important; /* Texto negro sobre el fondo verde */
        }

        /* Indicador de foco iluminado al escribir */
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #10b981 !important;
            box-shadow: 0 0 0 1px #10b981 !important;
        }

        button[kind="primary"] {
            background-color: #1e9dbd !important;
            color: #1d1f24 !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out;
        }
        button[kind="primary"]:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }

        button[kind="secondary"] {
            background-color: #334155 !important;
            color: #E0D6C3  !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease-in-out;
        }
        button[kind="secondary"]:hover {
            background-color: #475569 !important;
            border-color: #64748b !important;
        }

        /* --- 💎 CONFIGURACIÓN VISUAL SEGURA PARA DATA-EDITORS DE REPOSICIÓN --- */
        [data-testid="stDataFrame"], [data-testid="stDataEditor"], .stDataFrame {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            padding: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
        }

        /* --- 🎨 ESTILO PERSONALIZADO DE TABLA CENTRADA (DISEÑO TIPO HOJA9) --- */
        div[data-testid="stTable"] {
            background-color: #111827 !important;
            border: 2px solid #334155 !important;
            border-radius: 12px !important;
            padding: 10px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important;
            margin-top: 15px !important;
            display: flex !important;
            justify-content: center !important;
        }

        div[data-testid="stTable"] table {
            background-color: transparent !important;
            width: 100% !important;
            margin: 0 auto !important;
        }

        /* Cabecera Verde Azulada - CENTRADO ABSOLUTO */
        div[data-testid="stTable"] table thead tr th {
            background-color: #048582 !important;
            color: #000000 !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            padding: 12px !important;
            text-align: center !important;
            border: none !important;
        }

        div[data-testid="stTable"] table thead {
            border-radius: 8px 8px 0 0 !important;
        }

        /* Fondo del cuerpo de la tabla unificado a tono oscuro */
        div[data-testid="stTable"] table tbody {
            background-color: #0f172a !important;
        }

        /* Celdas de Productos - CENTRADO ABSOLUTO Y LEGIBLE */
        div[data-testid="stTable"] table tbody tr td {
            color: #cbd5e1 !important;
            font-size: 0.95rem !important;
            padding: 12px !important;
            text-align: center !important;
            border-bottom: 1px solid #1f2937 !important;
        }

        /* Estilización de la barra de desplazamiento interna general */
        ::-webkit-scrollbar {
            width: 6px !important;
            height: 6px !important;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a !important;
        }
        ::-webkit-scrollbar-thumb {
            background: #475569 !important;
            border-radius: 4px !important;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #10b981 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #1e293b !important;
            border-radius: 8px 8px 0px 0px;
            border: 1px solid #334155;
            color: #94a3b8 !important;
            padding: 8px 16px;
        }

        .stTabs [aria-selected="true"] {
            background-color: #0f172a !important;
            color: #10b981 !important;
            border-bottom: 2px solid #10b981 !important;
            font-weight: 600;
        }

        hr {
            border-color: #334155 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

DB_NAME = "sistema_gestion.db"

# --- INICIALIZACIÓN DE BASE DE DATOS ---
def inicializar_base_datos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rubros (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nombre TEXT UNIQUE NOT NULL,
            margen_defecto REAL DEFAULT 40.0
        )
    """)
    try:
        cursor.execute("ALTER TABLE rubros ADD COLUMN margen_defecto REAL DEFAULT 40.0")
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articulos (
            codigo TEXT PRIMARY KEY, descripcion TEXT NOT NULL, rubro TEXT,
            proveedor TEXT, vencimiento TEXT, costo REAL DEFAULT 0,
            precio_venta TEXT, fecha_act TEXT, ultima_venta TEXT, stock_actual INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, total REAL, fecha TEXT, metodo_pago TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT, venta_id INTEGER, codigo TEXT,
            descripcion TEXT, cantidad REAL, precio_unitario REAL, subtotal REAL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM rubros")
    if cursor.fetchone()[0] == 0:
        rubros_iniciales = [
            ("- Sin clasificar -", 0.0), 
            ("Almacén", 35.0), 
            ("Bebidas", 40.0), 
            ("Kiosco", 50.0), 
            ("Limpieza", 30.0)
        ]
        cursor.executemany("INSERT OR IGNORE INTO rubros (nombre, margen_defecto) VALUES (?, ?)", rubros_iniciales)
    conexion.commit()
    conexion.close()

inicializar_base_datos()

def generar_codigo_autonumerico(rubro_nombre):
    prefijo = "".join([c for c in rubro_nombre if c.isalnum()]).upper()[:3]
    if not prefijo or len(prefijo) < 3:
        prefijo = "GEN"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM articulos WHERE codigo LIKE ? ORDER BY codigo DESC LIMIT 1", (f"{prefijo}%",))
    res = cursor.fetchone()
    conn.close()
    
    if res:
        ultimo_codigo = res[0]
        try:
            numero_str = "".join([c for c in ultimo_codigo if c.isdigit()])
            siguiente_num = int(numero_str) + 1 if numero_str else 1
        except ValueError:
            siguiente_num = 1
    else:
        siguiente_num = 1
        
    return f"{prefijo}{siguiente_num:04d}"

def simular_datos_prueba():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    metodos = ["Efectivo", "Tarjeta de Débito", "Tarjeta de Crédito", "Transferencia Virtual"]
    for i in range(1, 15):
        total_v = round(random.uniform(500.0, 4500.0), 2)
        dia = random.randint(1, 15)
        fecha_v = f"{dia:02d}/09/2026 14:30"
        cursor.execute("INSERT INTO ventas (total, fecha, metodo_pago) VALUES (?, ?, ?)", (total_v, fecha_v, random.choice(metodos)))

    for i in range(1, 11):
        codigo = f"BEB{i:04d}"
        desc = f"Artículo de Prueba Premium {i}"
        costo = round(random.uniform(50.0, 1200.0), 2)
        precio_venta_str = f"{round(costo * 1.4, 2):.2f}".replace('.', ',')
        cursor.execute("""
            INSERT OR REPLACE INTO articulos (codigo, descripcion, rubro, proveedor, vencimiento, costo, precio_venta, fecha_act, ultima_venta, stock_actual)
            VALUES (?, ?, 'Bebidas', 'Distribuidora Central', '-', ?, ?, '15/09/2026', '-', ?)
        """, (codigo, desc, costo, precio_venta_str, random.randint(3, 45)))
    conexion.commit()
    conexion.close()

# --- 🛠️ CORRECCIÓN CLAVE: INICIALIZACIÓN CONTROLADA DEL ESTADO DE NAVEGACIÓN ---
if "navegacion_actual" not in st.session_state:
    st.session_state.navegacion_actual = "🏠 Inicio / Dashboard"

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #10b981 !important;'>💼 GESTIÓN PRO</h2>", unsafe_allow_html=True)
    st.write("---")
    
    lista_opciones = ["🏠 Inicio / Dashboard", "📦 Artículos (ABM)", "🔄 Reposición & Precios", "🛒 Ventas / POS", "📈 Informes Analíticos"]
    # Forzamos a que el radio escuche y mantenga el índice dinámicamente desde el state
    indice_defecto = lista_opciones.index(st.session_state.navegacion_actual) if st.session_state.navegacion_actual in lista_opciones else 0

    opcion_menu = st.sidebar.radio(
        "Navegación del Sistema:",
        lista_opciones,
        index=indice_defecto,
        label_visibility="collapsed"
    )
    # Sincronizamos el estado
    st.session_state.navegacion_actual = opcion_menu
    
    st.write("---")
    st.markdown("<small style='color: #64748b;'>Servidor Web Local Activo</small>", unsafe_allow_html=True)

# --- INTERRUPTOR VISUAL: OCULTAR SIDEBAR EN VENTAS / POS ---
if "Ventas" in opcion_menu:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            [data-testid="stAppViewBlockContainer"] {
                padding-left: 2rem !important;
                padding-right: 2rem !important;
                max-width: 100% !important;
            }
            [data-testid="stSidebarCollapseButton"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 1. HOME / DASHBOARD ---
if "Inicio / Dashboard" in opcion_menu:
    st.markdown("<h1>🏠 Dashboard General</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 0.95rem;'>Sesión activa: <span style='color: #10b981;'>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</span></p>", unsafe_allow_html=True)
    st.write("")

    conn = sqlite3.connect(DB_NAME)
    df_art = pd.read_sql_query("SELECT stock_actual FROM articulos", conn)
    df_v_hoy = pd.read_sql_query("SELECT total FROM ventas WHERE fecha LIKE ?", conn, params=(f"{datetime.now().strftime('%d/%m/%Y')}%",))
    conn.close()

    total_art = len(df_art)
    bajo_stock = len(df_art[df_art['stock_actual'] <= 5]) if total_art > 0 else 0
    ventas_hoy = df_v_hoy['total'].sum() if not df_v_hoy.empty else 0.0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.container(border=True).metric("💵 Ventas de la Jornada", f"$ {ventas_hoy:,.2f}", delta="En tiempo real", delta_color="normal")
    with m2:
        st.container(border=True).metric("📦 Catálogo de Productos", f"{total_art} un.", delta="Registrados")
    with m3:
        st.container(border=True).metric("⚠️ Alertas de Bajo Stock", f"{bajo_stock} art.", delta="- Crítico" if bajo_stock > 0 else "Estable", delta_color="inverse" if bajo_stock > 0 else "normal")

    st.write("")
    st.write("### ⚡ Acciones Rápidas")
    col_btn1, _ = st.columns([1, 1])
    with col_btn1:
        if st.button("📥 Cargar Datos Demostrativos de Prueba", width='stretch', type="secondary"):
            simular_datos_prueba()
            st.toast("¡Datos demostrativos inyectados con éxito!", icon="🔄")
            st.rerun()

# --- 2. GESTIÓN DE ARTÍCULOS (ABM) ---
elif "Artículos" in opcion_menu:
    st.markdown("<h1>📦 Administración de Productos</h1>", unsafe_allow_html=True)
    st.write("")
    
    tab_lista, tab_alta, tab_mod_del, tab_rubros = st.tabs([
        "📋 Catálogo en Góndola", 
        "➕ Alta de Nuevo Producto", 
        "✏️ Modificar / Eliminar", 
        "🏷️ Gestión de Rubros"
    ])
    
    with tab_lista:
        buscar = st.text_input("🔍 Buscar por código o descripción:", placeholder="Escribe para filtrar...")
        
        conn = sqlite3.connect(DB_NAME)
        query = "SELECT codigo as 'Código', descripcion as 'Descripción', rubro as 'Rubro', precio_venta as 'Precio Venta ($)', stock_actual as 'Stock' FROM articulos"
        if buscar:
            query += " WHERE codigo LIKE ? OR descripcion LIKE ?"
            df = pd.read_sql_query(query, conn, params=(f"%{buscar}%", f"%{buscar}%"))
        else:
            df = pd.read_sql_query(query, conn)
        conn.close()

        # CAMBIO CLAVE: Reemplazamos st.dataframe por st.table para que escuche el CSS de colores planos
        st.table(df)
        
        st.write("") # Espaciador
        csv_data = df.to_csv(index=False, sep=';', encoding='utf-8-sig')
        st.download_button("📥 Descargar Planilla CSV", data=csv_data, file_name="inventario_local.csv", width='stretch')


    with tab_alta:
        st.write("### Formulario de Registro")
        
        conn = sqlite3.connect(DB_NAME)
        rubros_db = conn.execute("SELECT nombre, margen_defecto FROM rubros").fetchall()
        conn.close()
        
        r_list = [r[0] for r in rubros_db]
        margen_dict = {r[0]: r[1] for r in rubros_db}

        def actualizar_valores_por_rubro():
            rubro_actual = st.session_state.alta_rubro
            iteracion = st.session_state.get("alta_form_iter", 0)
            st.session_state[f"txt_alta_cod_{iteracion}"] = generar_codigo_autonumerico(rubro_actual)
            st.session_state[f"num_alta_util_{iteracion}"] = margen_dict.get(rubro_actual, 40.0)

        rubro_seleccionado = st.selectbox(
            "Categoría / Rubro",
            r_list if r_list else ["- Sin clasificar -"],
            key="alta_rubro",
            on_change=actualizar_valores_por_rubro
        )
        
        if "alta_form_iter" not in st.session_state:
            st.session_state.alta_form_iter = 0
            
        i = st.session_state.alta_form_iter

        if f"txt_alta_cod_{i}" not in st.session_state:
            st.session_state[f"txt_alta_cod_{i}"] = generar_codigo_autonumerico(rubro_seleccionado)
        if f"num_alta_costo_{i}" not in st.session_state:
            st.session_state[f"num_alta_costo_{i}"] = 0.0
        if f"num_alta_util_{i}" not in st.session_state:
            st.session_state[f"num_alta_util_{i}"] = margen_dict.get(rubro_seleccionado, 40.0)

        col_form1, col_form2 = st.columns(2)
        with col_form1:
            cod = st.text_input("Código de Barras Interno *", key=f"txt_alta_cod_{i}")
            desc = st.text_input("Nombre / Descripción del Artículo *", key=f"txt_alta_desc_{i}")
            costo = st.number_input("Costo Neto de Compra ($)", min_value=0.0, step=50.0, key=f"num_alta_costo_{i}")
        with col_form2:
            utilidad = st.number_input("Margen de Utilidad Proyectado (%)", min_value=0.0, step=5.0, key=f"num_alta_util_{i}")
            
            precio_sugerido_calc = st.session_state[f"num_alta_costo_{i}"] * (1 + (st.session_state[f"num_alta_util_{i}"] / 100))
            st.session_state[f"num_alta_precio_{i}"] = float(round(precio_sugerido_calc, 2))
            
            precio_local = st.number_input("Precio Venta Local ($) [Modificable]", min_value=0.0, step=50.0, key=f"num_alta_precio_{i}")
            stock = st.number_input("Cantidad / Stock Inicial Físico", min_value=0, step=5, value=0, key=f"num_alta_stock_{i}")

        st.write("")

        if st.button("💾 Guardar y Registrar en Inventario", type="primary", width='stretch'):
            if not cod or not desc:
                st.error("Rellena los campos obligatorios antes de continuar.")
            else:
                pv_str = f"{precio_local:.2f}".replace('.', ',')
                f_act = datetime.now().strftime("%d/%m/%Y")
                conn = sqlite3.connect(DB_NAME)
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO articulos (codigo, descripcion, rubro, costo, precio_venta, fecha_act, ultima_venta, stock_actual)
                        VALUES (?, ?, ?, ?, ?, ?, '-', ?)
                    """, (cod.strip(), desc.strip(), rubro_seleccionado, costo, pv_str, f_act, stock))
                    conn.commit()
                    st.toast(f"¡{desc} registrado correctamente!", icon="🎉")
                    st.session_state.alta_form_iter += 1
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al registrar artículo: {str(e)}")
                finally:
                    conn.close()
    with tab_mod_del:
        st.write("### Seleccionar Artículo para Editar o Eliminar")
        conn = sqlite3.connect(DB_NAME)
        articulos_disponibles = conn.execute("SELECT codigo, descripcion FROM articulos").fetchall()
        conn.close()
        
        if articulos_disponibles:
            opciones_editar = ["-- Seleccionar artículo --"] + [f"{art[1]} (Cód: {art[0]})" for art in articulos_disponibles]
            art_elegido = st.selectbox("Buscador de artículo:", opciones_editar)
            
            if art_elegido != "-- Seleccionar artículo --":
                codigo_editar = art_elegido.split("(Cód: ")[1].replace(")", "").strip()
                
                conn = sqlite3.connect(DB_NAME)
                datos_art = conn.execute("SELECT codigo, descripcion, rubro, costo, precio_venta, stock_actual FROM articulos WHERE codigo = ?", (codigo_editar,)).fetchone()
                conn.close()
                
                if datos_art:
                    _, d_desc, d_rubro, d_costo, d_pv_str, d_stock = datos_art
                    try:
                        d_pv_num = float(str(d_pv_str).replace('.', '').replace(',', '.'))
                    except ValueError:
                        d_pv_num = 0.0
                        
                    ce1, ce2 = st.columns(2)
                    with ce1:
                        nuevo_codigo = st.text_input("Código de Barras", value=codigo_editar)
                        nueva_desc = st.text_input("Descripción", value=d_desc)
                        nuevo_rubro = st.text_input("Rubro (No modificable)", value=d_rubro, disabled=True)
                    with ce2:
                        nuevo_costo = st.number_input("Costo Neto ($)", min_value=0.0, value=float(d_costo), step=50.0)
                        nuevo_pv = st.number_input("Precio Venta Local ($)", min_value=0.0, value=float(d_pv_num), step=50.0)
                        nuevo_stock = st.number_input("Stock Actual", min_value=0, value=int(d_stock))
                    
                    st.write("") 
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        btn_actualizar = st.button("💾 Guardar Cambios", type="primary", width='stretch')
                    with col_m2:
                        btn_eliminar = st.button("🗑️ Eliminar Artículo", type="secondary", width='stretch')
                        
                    if btn_actualizar:
                        conn = sqlite3.connect(DB_NAME)
                        try:
                            pv_str_upd = f"{nuevo_pv:.2f}".replace('.', ',')
                            f_act = datetime.now().strftime("%d/%m/%Y")
                            conn.execute("""
                                UPDATE articulos 
                                SET codigo = ?, descripcion = ?, rubro = ?, costo = ?, precio_venta = ?, stock_actual = ?, fecha_act = ?
                                WHERE codigo = ?
                            """, (nuevo_codigo.strip(), nueva_desc.strip(), nuevo_rubro, nuevo_costo, pv_str_upd, nuevo_stock, f_act, codigo_editar))
                            conn.commit()
                            st.toast("¡Artículo actualizado con éxito!", icon="✅")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al actualizar: {str(e)}")
                        finally:
                            conn.close()

                    if btn_eliminar:
                        conn = sqlite3.connect(DB_NAME)
                        try:
                            conn.execute("DELETE FROM articulos WHERE codigo = ?", (codigo_editar,))
                            conn.commit()
                            st.toast("¡Artículo eliminado del inventario!", icon="🗑️")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al eliminar: {str(e)}")
                        finally:
                            conn.close()
        else:
            st.info("No hay artículos registrados para modificar o eliminar.")

    with tab_rubros:
        st.write("### 🏷️ Gestión de Rubros Comercial (ABM)")
        tab_r1, tab_r2 = st.tabs(["➕ Crear Rubro", "✏️ Modificar / Eliminar Rubro"])
        
        with tab_r1:
            n_rubro = st.text_input("Nombre del Nuevo Rubro comercial:")
            n_margen = st.number_input("Margen de Ganancia por Defecto (%)", min_value=0.0, max_value=500.0, value=40.0, step=5.0)
            
            if st.button("➕ Crear e Incorporar Rubro", type="primary", width='stretch'):
                if n_rubro:
                    conn = sqlite3.connect(DB_NAME)
                    try:
                        conn.execute("INSERT INTO rubros (nombre, margen_defecto) VALUES (?, ?)", (n_rubro.strip(), n_margen))
                        conn.commit()
                        st.toast(f"Rubro '{n_rubro}' disponible con {n_margen}% de utilidad base.", icon="🏷️")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.warning("Esa categoría ya existe.")
                    finally:
                        conn.close()
                else:
                    st.error("El nombre del rubro no puede estar vacío.")
                    
        with tab_r2:
            conn = sqlite3.connect(DB_NAME)
            lista_r_ed = conn.execute("SELECT id, nombre, margen_defecto FROM rubros").fetchall()
            conn.close()
            
            if lista_r_ed:
                opciones_r = ["-- Seleccionar Rubro --"] + [f"{r[1]} (Margen: {r[2]}%)" for r in lista_r_ed if r[1] != "- Sin clasificar -"]
                rubro_elegido_abm = st.selectbox("Seleccione rubro a editar:", opciones_r)
                
                if rubro_elegido_abm != "-- Seleccionar Rubro --":
                    nombre_r_actual = rubro_elegido_abm.split(" (Margen:")[0].strip()
                    datos_r_act = next(r for r in lista_r_ed if r[1] == nombre_r_actual)
                    
                    col_re1, col_re2 = st.columns(2)
                    with col_re1:
                        mod_nombre_r = st.text_input("Editar Nombre de Categoría", value=datos_r_act[1])
                    with col_re2:
                        mod_margen_r = st.number_input("Editar Margen Base (%)", min_value=0.0, max_value=500.0, value=float(datos_r_act[2]), step=5.0)
                        
                    col_rbtn1, col_rbtn2 = st.columns(2)
                    with col_rbtn1:
                        if st.button("💾 Modificar Rubro", type="primary", width='stretch'):
                            conn = sqlite3.connect(DB_NAME)
                            try:
                                conn.execute("UPDATE rubros SET nombre = ?, margen_defecto = ? WHERE id = ?", (mod_nombre_r.strip(), mod_margen_r, datos_r_act[0]))
                                conn.execute("UPDATE articulos SET rubro = ? WHERE rubro = ?", (mod_nombre_r.strip(), datos_r_act[1]))
                                conn.commit()
                                st.toast("¡Categoría actualizada en el sistema!", icon="🔄")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                            finally:
                                conn.close()
                                
                    with col_rbtn2:
                        if st.button("🗑️ Eliminar Rubro Permanente", type="secondary", width='stretch'):
                            conn = sqlite3.connect(DB_NAME)
                            try:
                                conn.execute("DELETE FROM rubros WHERE id = ?", (datos_r_act[0],))
                                conn.execute("UPDATE articulos SET rubro = '- Sin clasificar -' WHERE rubro = ?", (datos_r_act[1],))
                                conn.commit()
                                st.toast("Rubro eliminado. Productos reasignados.", icon="🗑️")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                            finally:
                                conn.close()
            else:
                st.info("No hay rubros registrados modificables.")

# --- 3. NUEVO MÓDULO: REPOSICIÓN DE STOCK & ACTUALIZACIÓN DE PRECIOS ---
elif "Reposición" in opcion_menu:
    st.markdown("<h1>🔄 Módulo de Operaciones Logísticas</h1>", unsafe_allow_html=True)
    st.write("")
    
    tab_repo, tab_precios = st.tabs(["📦 Ingreso de Mercadería (Stock)", "📈 Actualización Global de Precios"])
    
    with tab_repo:
        st.write("### Incrementar Unidades de Inventario")
        conn = sqlite3.connect(DB_NAME)
        articulos_repo = conn.execute("SELECT codigo, descripcion, stock_actual FROM articulos").fetchall()
        conn.close()
        
        if articulos_repo:
            opciones_repo = ["-- Seleccionar Producto --"] + [f"{a[1]} (Cód: {a[0]}) - Stock actual: {a[2]} un." for a in articulos_repo]
            prod_repo_sel = st.selectbox("Buscar artículo para reponer:", opciones_repo)
            
            if prod_repo_sel != "-- Seleccionar Producto --":
                cod_repo = prod_repo_sel.split("(Cód: ")[1].split(")")[0].strip()
                cant_a_sumar = st.number_input("Cantidad de unidades ingresantes:", min_value=1, value=10, step=1)
                
                if st.button("🟢 Confirmar Ingreso de Stock", type="primary", width='stretch'):
                    conn = sqlite3.connect(DB_NAME)
                    try:
                        conn.execute("UPDATE articulos SET stock_actual = stock_actual + ? WHERE codigo = ?", (cant_a_sumar, cod_repo))
                        conn.commit()
                        st.toast("¡Unidades agregadas al inventario físico con éxito!", icon="📦")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al actualizar stock: {str(e)}")
                    finally:
                        conn.close()
        else:
            st.info("No hay artículos en el catálogo para reponer stock.")
            
    with tab_precios:
        st.write("### Modificación Porcentual en Masa")
        
        conn = sqlite3.connect(DB_NAME)
        r_filtros = ["-- Todos los productos --"] + [r[0] for r in conn.execute("SELECT nombre FROM rubros").fetchall()]
        conn.close()
        
        rubro_a_afectar = st.selectbox("Filtrar lote por Rubro/Categoría:", r_filtros)
        porcentaje_cambio = st.number_input("Porcentaje de Ajuste (Positivo aumenta, Negativo rebaja) %:", value=10.0, step=0.5)
        
        st.warning("⚠️ Esta acción es irreversible y recalculará de forma inmediata los valores de venta local del lote seleccionado.")
        
        if st.button("⚡ Ejecutar Actualización Masiva de Precios", type="primary", width='stretch'):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            if rubro_a_afectar == "-- Todos los productos --":
                articulos_cambio = cursor.execute("SELECT codigo, precio_venta FROM articulos").fetchall()
            else:
                articulos_cambio = cursor.execute("SELECT codigo, precio_venta FROM articulos WHERE rubro = ?", (rubro_a_afectar,)).fetchall()
                
            contador_cambios = 0
            for art in articulos_cambio:
                cod_a = art[0]
                try:
                    precio_limpio = str(art[1]).replace('.', '').replace(',', '.')
                    pv_actual = float(precio_limpio)
                except ValueError:
                    pv_actual = 0.0
                    
                nuevo_pv_calc = pv_actual * (1 + (porcentaje_cambio / 100))
                nuevo_pv_str = f"{nuevo_pv_calc:.2f}".replace('.', ',')
                f_act = datetime.now().strftime("%d/%m/%Y")
                
                cursor.execute("UPDATE articulos SET precio_venta = ?, fecha_act = ? WHERE codigo = ?", (nuevo_pv_str, f_act, cod_a))
                contador_cambios += 1
                
            conn.commit()
            conn.close()
            st.success(f"¡Proceso finalizado! Se actualizaron los precios de {contador_cambios} artículos con éxito.")
            st.rerun()
# --- 4. PUNTO DE VENTA (VENTAS / POS) ---
elif "Ventas" in opcion_menu:
    col_titulo_pos, col_salir_pos = st.columns([4, 1])
    with col_titulo_pos:
        st.markdown("<h2 style='margin: 0px; padding-bottom: 10px;'>🛒 Terminal de Cobro (POS)</h2>", unsafe_allow_html=True)
        
    with col_salir_pos:
        # CORRECCIÓN DEFINITIVA: Cambiamos la variable de estado nativa en lugar del script JS que fallaba por el display:none
        if st.button("⬅️ Salir al Menú", type="secondary", width='stretch'):
            st.session_state.navegacion_actual = "🏠 Inicio / Dashboard"
            st.rerun()

    if "carrito_web" not in st.session_state:
        st.session_state.carrito_web = []

    # --- DISEÑO EN 3 COLUMNAS COMPACTAS ---
    c_carga, c_carrito, c_cierre = st.columns([1.1, 1.7, 1.1])

    # --- COLUMNA 1: ESCANEO Y BUSQUEDA ---
    with c_carga:
        st.markdown("<h4 style='font-size: 1.1rem; margin-bottom: 5px;'>🔍 Buscar / Escanear</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            conn = sqlite3.connect(DB_NAME)
            lista_articulos_db = conn.execute("SELECT codigo, descripcion FROM articulos").fetchall()
            conn.close()
            
            opciones_articulos = ["-- Busque o Escanee Aquí --"] + [
                f"{art[0]} - {art[1]}" for art in lista_articulos_db
            ]
            
            articulo_seleccionado = st.selectbox("Producto:", opciones_articulos, index=0, label_visibility="collapsed")
            cant_scan = st.number_input("Cantidad:", min_value=1.0, value=1.0, step=1.0)
            
            st.write("")
            if st.button("📥 Agregar al Pedido", type="secondary", width='stretch'):
                if articulo_seleccionado != "-- Busque o Escanee Aquí --":
                    codigo_a_procesar = articulo_seleccionado.split(" - ")[0].strip()
                    
                    conn = sqlite3.connect(DB_NAME)
                    res = conn.execute("SELECT codigo, descripcion, precio_venta FROM articulos WHERE codigo = ?", (codigo_a_procesar,)).fetchone()
                    conn.close()
                    
                    if res:
                        v_codigo, v_descripcion, v_precio_str = res
                        try:
                            p_f = float(str(v_precio_str).replace('.', '').replace(',', '.'))
                        except ValueError:
                            p_f = 0.0
                            
                        st.session_state.carrito_web.append({
                            "Código": v_codigo,
                            "Descripción": v_descripcion,
                            "Cantidad": float(cant_scan),
                            "Unitario ($)": p_f,
                            "Subtotal ($)": float(cant_scan * p_f)
                        })
                        st.toast(f"Añadido: {v_descripcion}", icon="🛒")
                        st.rerun()
                else:
                    st.warning("Seleccione un artículo válido.")

    # --- COLUMNA 2: DETALLE DEL CARRITO CON MENÚ DE EDICIÓN DE CANTIDAD ---
        # --- COLUMNA 2: DETALLE DEL CARRITO CON FUNCIÓN DE ACTUALIZACIÓN CONTROLADA ---
    with c_carrito:
        st.markdown("<h4 style='font-size: 1.1rem; margin-bottom: 5px;'>📋 Detalle de la Transacción Actual</h4>", unsafe_allow_html=True)
        
        if st.session_state.carrito_web:
            df_carrito = pd.DataFrame(st.session_state.carrito_web)
            
            # --- FUNCIÓN LOGÍSTICA PARA RECALCULAR SUBTOTALES AL INSTANTE SIN BUCLES ---
            def procesar_cambio_cantidad():
                cambios = st.session_state.editor_pos_live.get("edited_rows", {})
                for fila_index, contenido in cambios.items():
                    if "Cantidad" in contenido:
                        nueva_cant = float(contenido["Cantidad"])
                        # Obtenemos el precio unitario guardado en la memoria de esa fila
                        precio_uni = float(st.session_state.carrito_web[fila_index]["Unitario ($)"])
                        # Impactamos los nuevos cálculos directamente sobre el contenedor nativo
                        st.session_state.carrito_web[fila_index]["Cantidad"] = nueva_cant
                        st.session_state.carrito_web[fila_index]["Subtotal ($)"] = nueva_cant * precio_uni

            # Renderizamos la tabla vinculando la función al evento on_change
            st.data_editor(
                df_carrito,
                width='stretch',
                hide_index=True,
                key="editor_pos_live",
                on_change=procesar_cambio_cantidad,
                column_config={
                    "Código": st.column_config.TextColumn(disabled=True),
                    "Descripción": st.column_config.TextColumn(disabled=True),
                    "Cantidad": st.column_config.NumberColumn(min_value=1.0, step=1.0, required=True, disabled=False),
                    "Unitario ($)": st.column_config.NumberColumn(format="$ %.2f", disabled=True),
                    "Subtotal ($)": st.column_config.NumberColumn(format="$ %.2f", disabled=True),
                }
            )

            # Botón de vaciado manual
            if st.button("❌ Vaciar Pedido", type="secondary", width='stretch'):
                st.session_state.carrito_web = []
                st.rerun()
        else:
            st.container(border=True).info("Terminal vacía. Escanee artículos para iniciar la transacción comercial.")

    # --- COLUMNA 3: TOTAL, DESCUENTOS, RECARGOS Y COBRO ---
    with c_cierre:
        st.markdown("<h4 style='font-size: 1.1rem; margin-bottom: 5px;'>💵 Cierre / Ticket</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            subtotal_base = sum(i["Subtotal ($)"] for i in st.session_state.carrito_web) if st.session_state.carrito_web else 0.0
            
            col_desc, col_rec = st.columns(2)
            with col_desc:
                p_desc = st.number_input("Desc. (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            with col_rec:
                p_rec = st.number_input("Rec. (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            
            monto_descuento = subtotal_base * (p_desc / 100)
            monto_recargo = subtotal_base * (p_rec / 100)
            tot_transaccion = subtotal_base - monto_descuento + monto_recargo
            
            st.markdown(
                f"""
                <div style="background-color: #0f172a; padding: 10px; border-radius: 8px; border: 1px solid #10b981; margin-bottom: 10px; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.75rem; font-weight: 600;">TOTAL A COBRAR</span><br>
                    <span style="color: #10b981; font-size: 1.8rem; font-weight: 800;">$ {tot_transaccion:,.2f}</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            m_pago = st.selectbox("Método:", ["Efectivo", "Tarjeta de Débito", "Tarjeta de Crédito", "Transferencia Virtual"])
            
            if m_pago == "Efectivo":
                monto_recibido = st.number_input("Monto Recibido ($):", min_value=0.0, value=float(tot_transaccion), step=100.0)
            else:
                monto_recibido = tot_transaccion
                st.text_input("Monto Recibido ($):", value=f"{tot_transaccion:,.2f}", disabled=True)
                
            vuelto = monto_recibido - tot_transaccion if monto_recibido >= tot_transaccion else 0.0
            
            st.markdown(
                f"""
                <div style="padding: 5px 0px; text-align: center; font-size: 0.95rem; font-weight: 600; color: #cbd5e1;">
                    Vuelto: <span style="color: #f59e0b; font-size: 1.1rem;">$ {vuelto:,.2f}</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("🟢 CONFIRMAR COMPROBANTE", type="primary", width='stretch'):
                if not st.session_state.carrito_web:
                    st.error("No hay ítems cargados.")
                elif monto_recibido < tot_transaccion:
                    st.error("Monto insuficiente.")
                else:
                    f_v = datetime.now().strftime("%d/%m/%Y %H:%M")
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO ventas (total, fecha, metodo_pago) VALUES (?, ?, ?)", (tot_transaccion, f_v, m_pago))
                        v_id = cursor.lastrowid
                        
                        for item in st.session_state.carrito_web:
                            cursor.execute("""
                                INSERT INTO detalle_venta (venta_id, codigo, descripcion, cantidad, precio_unitario, subtotal)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (v_id, item["Código"], item["Descripción"], item["Cantidad"], item["Unitario ($)"], item["Subtotal ($)"]))
                            
                            cursor.execute("UPDATE articulos SET stock_actual = IFNULL(stock_actual, 0) - ? WHERE codigo = ?", (item["Cantidad"], item["Código"]))
                        
                        conn.commit()
                        st.success(f"Emitido N° {v_id}")
                        st.session_state.carrito_web = []
                        st.rerun()
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Error: {str(e)}")
                    finally:
                        conn.close()

# --- 5. INFORMES ANALÍTICOS ---
elif "Informes" in opcion_menu:
    st.markdown("<h1>📈 Módulo de Auditoría y Reportes</h1>", unsafe_allow_html=True)
    st.write("")
    
    rep_sel = st.selectbox("Selecciona la consulta analítica a procesar:", [
        "Historial General de Ventas Facturadas",
        "Análisis de Valorización Física del Inventario"
    ])
    
    conn = sqlite3.connect(DB_NAME)
    
    if "Historial" in rep_sel:
        st.subheader("Historial de Comprobantes Emitidos")
        
        f1, f2 = st.columns(2)
        with f1:
            fecha_desde = st.date_input("Filtrar Desde:", value=date(2026, 1, 1))
        with f2:
            fecha_hasta = st.date_input("Filtrar Hasta:", value=date(2026, 12, 31))
            
        df_ventas_reg = pd.read_sql_query("SELECT id as 'N° Venta', fecha as 'Fecha y Hora', metodo_pago as 'Método Pago', total as 'Total Recaudado ($)' FROM ventas ORDER BY id DESC", conn)
        conn.close()
        
        if not df_ventas_reg.empty:
            # Corrección: procesado seguro de la cadena de texto para extraer la fecha limpia
            df_ventas_reg['fecha_parsed'] = pd.to_datetime(df_ventas_reg['Fecha y Hora'].astype(str).str.split().str[0], format='%d/%m/%Y').dt.date
            df_filtrado = df_ventas_reg[(df_ventas_reg['fecha_parsed'] >= fecha_desde) & (df_ventas_reg['fecha_parsed'] <= fecha_hasta)]
            
            if not df_filtrado.empty:
                st.write("### 📊 Gráfico Analítico de Rendimiento")
                df_agrupado = df_filtrado.groupby('Método Pago')['Total Recaudado ($)'].sum().reset_index()
                st.bar_chart(data=df_agrupado, x='Método Pago', y='Total Recaudado ($)', width="stretch")
                
                st.write("### 📋 Registros Encontrados")
                st.dataframe(df_filtrado.drop(columns=['fecha_parsed']), width="stretch", hide_index=True)
            else:
                st.info("No se encontraron ventas comerciales en el rango de fechas seleccionado.")
        else:
            st.info("No se registran ventas comerciales guardadas en la BD local.")
            
    else:
        st.subheader("Auditoría Contable de Activos en Stock")
        df_stock_val = pd.read_sql_query("SELECT costo, precio_venta, stock_actual FROM articulos", conn)
        conn.close()
        
        if not df_stock_val.empty:
            df_stock_val['pv_num'] = df_stock_val['precio_venta'].astype(str).str.replace('$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
            df_stock_val['Costo Acumulado'] = df_stock_val['costo'] * df_stock_val['stock_actual']
            df_stock_val['Venta Esperada'] = df_stock_val['pv_num'] * df_stock_val['stock_actual']
            
            c_costo = df_stock_val['Costo Acumulado'].sum()
            c_venta = df_stock_val['Venta Esperada'].sum()
            margen = c_venta - c_costo
            
            col_inf1, col_inf2, col_inf3 = st.columns(3)
            with col_inf1:
                with st.container(border=True):
                    st.metric(label="Capital de Costo Invertido", value=f"$ {c_costo:,.2f}")
            with col_inf2:
                with st.container(border=True):
                    st.metric(label="Valor Estimado de Liquidación", value=f"$ {c_venta:,.2f}")
            with col_inf3:
                with st.container(border=True):
                    st.metric(label="Margen Neto de Retorno", value=f"$ {margen:,.2f}",
                              delta=f"{round((margen/c_costo)*100, 2) if c_costo else 0}% Proyectado")
        else:
            st.info("Introduce artículos para ver la valorización contable de tus stocks.")

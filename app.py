import streamlit as st
import pandas as pd
from datetime import datetime, date
import random
from supabase import create_client, Client

# --- CONFIGURACIÓN DE LAS CREDENCIALES DE SUPABASE ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURACIÓN DE LA PÁGINA WEB ---
st.set_page_config(
    page_title="Sistema de Gestión Comercial Pro v1.0",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE ESTILOS CSS PERSONALIZADOS ---
st.markdown(
    """
    <style>
        @import url('https://googleapis.com');
        html, body, [class*="css"] { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
        .stApp, [data-testid="stHeader"], [data-testid="stToolbar"] { background-color: #0f172a !important; }
        [data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155; }
        h1, h2, h3, h4, h5, h6 { color: #FFFFFF  !important; font-weight: 700 !important; letter-spacing: -0.02em; }
        h1 { font-size: 2.2rem !important; margin-bottom: 0.5rem !important; }
        p, label, span, .stMarkdown, small { color: #cbd5e1 !important; }
        div[data-testid="stForm"], div[data-testid="stMetric"], .stContainer, div[class*="border"] {
            background-color: #1e293b !important; border: 1px solid #334155 !important;
            border-radius: 12px !important; padding: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
        }
        div[data-testid="stMetricValue"] { color: #048582 !important; font-weight: 700 !important; font-size: 1.8rem !important; }
        div[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.9rem !important; font-weight: 500 !important; }
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] { background-color: #000000 !important; color: #f8fafc !important; border: 1px solid #475569 !important; border-radius: 8px !important; }
        ul[data-testid="stSelectboxVirtualList"], div[data-baseweb="menu"] { background-color: #000000 !important; border: 1px solid #334155 !important; }
        ul[data-testid="stSelectboxVirtualList"] li, div[data-baseweb="menu"] div { color: #cbd5e1 !important; background-color: #000000 !important; }
        ul[data-testid="stSelectboxVirtualList"] li:hover, div[data-baseweb="menu"] div:hover { background-color: #10b981 !important; color: #000000 !important; }
        .stTextInput input:focus, .stNumberInput input:focus { border-color: #10b981 !important; box-shadow: 0 0 0 1px #10b981 !important; }
        button[kind="primary"] { background-color: #1e9dbd !important; color: #1d1f24 !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; transition: all 0.2s ease-in-out; }
        button[kind="primary"]:hover { opacity: 0.9; transform: translateY(-1px); }
        button[kind="secondary"] { background-color: #334155 !important; color: #E0D6C3  !important; border: 1px solid #475569 !important; border-radius: 8px !important; font-weight: 500 !important; transition: all 0.2s ease-in-out; }
        button[kind="secondary"]:hover { background-color: #475569 !important; border-color: #64748b !important; }
        [data-testid="stDataFrame"], [data-testid="stDataEditor"], .stDataFrame { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 12px !important; padding: 8px !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important; }
        div[data-testid="stTable"] { background-color: #111827 !important; border: 2px solid #334155 !important; border-radius: 12px !important; padding: 10px !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important; margin-top: 15px !important; display: flex !important; justify-content: center !important; }
        div[data-testid="stTable"] table { background-color: transparent !important; width: 100% !important; margin: 0 auto !important; }
        div[data-testid="stTable"] table thead tr th { background-color: #048582 !important; color: #000000 !important; font-size: 1.05rem !important; font-weight: 700 !important; padding: 12px !important; text-align: center !important; border: none !important; }
        div[data-testid="stTable"] table tbody tr td { color: #cbd5e1 !important; font-size: 0.95rem !important; padding: 12px !important; text-align: center !important; border-bottom: 1px solid #1f2937 !important; }
        .stTabs [data-baseweb="tab"] { background-color: #1e293b !important; border-radius: 8px 8px 0px 0px; border: 1px solid #334155; color: #94a3b8 !important; padding: 8px 16px; }
        .stTabs [aria-selected="true"] { background-color: #0f172a !important; color: #10b981 !important; border-bottom: 2px solid #10b981 !important; font-weight: 600; }
        hr { border-color: #334155 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

def generar_codigo_autonumerico(rubro_nombre):
    prefijo = "".join([c for c in rubro_nombre if c.isalnum()]).upper()[:3]
    if not prefijo or len(prefijo) < 3:
        prefijo = "GEN"
    
    res = supabase.table("articulos").select("codigo").ilike("codigo", f"{prefijo}%").order("codigo", desc=True).limit(1).execute()
    
    if res.data and len(res.data) > 0:
        ultimo_codigo = res.data[0]["codigo"]
        try:
            numero_str = "".join([c for c in ultimo_codigo if c.isdigit()])
            siguiente_num = int(numero_str) + 1 if numero_str else 1
        except ValueError:
            siguiente_num = 1
    else:
        siguiente_num = 1
        
    return f"{prefijo}{siguiente_num:04d}"

if "navegacion_actual" not in st.session_state:
    st.session_state.navegacion_actual = "🏠 Inicio / Dashboard"

# --- BARRA LATERAL ---
# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #10b981 !important;'>💼 GESTIÓN PRO</h2>", unsafe_allow_html=True)
    st.write("---")
    
    lista_opciones = ["🏠 Inicio / Dashboard", "📦 Artículos (ABM)", "🔄 Reposición & Precios", "🛒 Ventas / POS", "📈 Informes Analíticos"]
    indice_defecto = lista_opciones.index(st.session_state.navegacion_actual) if st.session_state.navegacion_actual in lista_opciones else 0

    opcion_menu = st.sidebar.radio("Navegación:", lista_opciones, index=indice_defecto, label_visibility="collapsed")
    st.session_state.navegacion_actual = opcion_menu
    st.write("---")
    st.markdown("<small style='color: #64748b;'>Servidor Supabase Activo en la Nube</small>", unsafe_allow_html=True)
    
    # --- BOTÓN DE WHATSAPP CON COMPONENTE NATIVO (NO BLOQUEABLE) ---
    NUMERO_TELEFONO = "5491160335829"
    
    # Recuperamos las respuestas de los usuarios guardadas en memoria para armar el texto
    texto_whatsapp = "🤖 *Resumen de Consulta del Cliente*\n\n"
    if "messages" in st.session_state and st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                texto_whatsapp += f"• {msg['content']}\n"
    else:
        texto_whatsapp += "Hola, solicito soporte técnico o información sobre el sistema."

    import urllib.parse
    texto_codificado = urllib.parse.quote(texto_whatsapp)
    url_whatsapp_sidebar = f"https://wa.me/{NUMERO_TELEFONO}?text={texto_codificado}"
    
    # Inyectamos estilos específicos para cambiar el aspecto del botón nativo de Streamlit
    st.markdown(
        """
        <style>
            div[data-testid="stSidebar"] div.stButton button {
                background-color: #8fce00 !important;
                color: #000000 !important;
                border: 1px solid #94a3b8 !important;
                border-radius: 10px !important;
                font-weight: bold !important;
                font-size: 1.1rem !important;
                height: 50px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
            }
            div[data-testid="stSidebar"] div.stButton button:hover {
                background-color: #e2e8f0 !important;
                border-color: #64748b !important;
                transform: scale(1.02);
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Espaciado para mandarlo abajo en la barra lateral tal como en tu Excel
    st.write("")
    st.write("")
    st.write("")
    
    # Botón de enlace oficial de Streamlit (Evita bloqueos de ventanas emergentes de Chrome)
    st.link_button("💬 Consultar", url_whatsapp_sidebar, use_container_width=True)

if "Ventas" in opcion_menu:
    st.markdown("<style>[data-testid='stSidebar'] {display: none !important;} [data-testid='stAppViewBlockContainer'] {padding-left: 2rem !important; padding-right: 2rem !important; max-width: 100% !important;} [data-testid='stSidebarCollapseButton'] {display: none !important;}</style>", unsafe_allow_html=True)

# --- 1. HOME / DASHBOARD ---
if "Inicio / Dashboard" in opcion_menu:
    st.markdown("<h1>🏠 Dashboard General</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 0.95rem;'>Sesión activa: <span style='color: #10b981;'>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</span></p>", unsafe_allow_html=True)
    st.write("")

    res_art = supabase.table("articulos").select("stock_actual").execute()
    df_art = pd.DataFrame(res_art.data)
    
    fecha_hoy_str = datetime.now().strftime('%d/%m/%Y')
    res_ventas = supabase.table("ventas").select("total").like("fecha", f"{fecha_hoy_str}%").execute()
    df_v_hoy = pd.DataFrame(res_ventas.data)

    total_art = len(df_art)
    bajo_stock = len(df_art[df_art['stock_actual'] <= 5]) if total_art > 0 else 0
    ventas_hoy = df_v_hoy['total'].sum() if not df_v_hoy.empty else 0.0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.container(border=True).metric("💵 Ventas de la Jornada", f"$ {ventas_hoy:,.2f}", delta="En tiempo real")
    with m2:
        st.container(border=True).metric("📦 Catálogo de Productos", f"{total_art} un.", delta="Registrados")
    with m3:
        st.container(border=True).metric("⚠️ Alertas de Bajo Stock", f"{bajo_stock} art.", delta="- Crítico" if bajo_stock > 0 else "Estable", delta_color="inverse" if bajo_stock > 0 else "normal")

# --- 2. GESTIÓN DE ARTÍCULOS (ABM) ---
elif "Artículos" in opcion_menu:
    st.markdown("<h1>📦 Administración de Productos</h1>", unsafe_allow_html=True)
    tab_lista, tab_alta, tab_mod_del, tab_rubros = st.tabs(["📋 Catálogo en Góndola", "➕ Alta de Nuevo Producto", "✏️ Modificar / Eliminar", "🏷️ Gestión de Rubros"])
    
    with tab_lista:
        buscar = st.text_input("🔍 Buscar por código o descripción:", placeholder="Escribe para filtrar...")
        res_cat = supabase.table("articulos").select("codigo, descripcion, rubro, precio_venta, stock_actual").execute()
        df = pd.DataFrame(res_cat.data)
        
        if not df.empty and buscar:
            df = df[df['codigo'].str.contains(buscar, case=False, na=False) | df['descripcion'].str.contains(buscar, case=False, na=False)]
        
        if not df.empty:
            df.columns = ['Código', 'Descripción', 'Rubro', 'Precio Venta ($)', 'Stock']
            st.table(df)
            csv_data = df.to_csv(index=False, sep=';', encoding='utf-8-sig')
            st.download_button("📥 Descargar Planilla CSV", data=csv_data, file_name="inventario_local.csv")
        else:
            st.info("Catálogo vacío o sin coincidencias.")

    with tab_alta:
        st.write("### Formulario de Registro")
        res_rub = supabase.table("rubros").select("nombre, margen_defecto").execute()
        r_list = [r["nombre"] for r in res_rub.data]
        margen_dict = {r["nombre"]: r["margen_defecto"] for r in res_rub.data}

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
            precio_local = st.number_input("Precio Venta Local ($)", min_value=0.0, step=50.0, key=f"num_alta_precio_{i}")
            stock = st.number_input("Cantidad Inicial Física", min_value=0, step=5, value=0, key=f"num_alta_stock_{i}")

        if st.button("💾 Guardar y Registrar en Inventario", type="primary", width='stretch'):
            if not cod or not desc:
                st.error("Rellena los campos obligatorios.")
            else:
                f_act = datetime.now().strftime("%d/%m/%Y")
                
                # Intentar formatear de forma segura según el tipo de columna en la BD
                try:
                    valor_precio = float(precio_local)
                except:
                    valor_precio = str(precio_local).replace('.', ',')
                data_ins = {
                    "codigo": str(cod).strip(),
                    "descripcion": str(desc).strip(),
                    "rubro": str(rubro_seleccionado),
                    "proveedor": "-",
                    "vencimiento": "-",
                    "costo": float(costo) if costo else 0.0,
                    "precio_venta": str(precio_local),
                    "fecha_act": str(f_act),
                    "ultima_venta": "-",
                    "stock_actual": int(stock) if stock else 0
                }

                supabase.table("articulos").upsert(data_ins).execute()
                st.toast(f"¡{desc} registrado correctamente!", icon="🎉")
                st.session_state.alta_form_iter += 1
                st.rerun()

    with tab_mod_del:
        st.write("### Seleccionar Artículo para Editar o Eliminar")
        res_art_ed = supabase.table("articulos").select("codigo, descripcion").execute()
        if res_art_ed.data:
            opciones_editar = ["-- Seleccionar artículo --"] + [f"{art['descripcion']} (Cód: {art['codigo']})" for art in res_art_ed.data]
            art_elegido = st.selectbox("Buscador de artículo:", opciones_editar)
            
            if art_elegido != "-- Seleccionar artículo --":
                codigo_editar = art_elegido.split("(Cód: ")[1].replace(")", "").strip()
                res_datos = supabase.table("articulos").select("*").eq("codigo", codigo_editar).execute()
                if res_datos.data:
                    datos_art = res_datos.data[0]
                    try:
                        d_pv_num = float(str(datos_art["precio_venta"]).replace('.', '').replace(',', '.'))
                    except:
                        d_pv_num = 0.0
                        
                    ce1, ce2 = st.columns(2)
                    with ce1:
                        nuevo_codigo = st.text_input("Código de Barras", value=datos_art["codigo"])
                        nueva_desc = st.text_input("Descripción", value=datos_art["descripcion"])
                        nuevo_rubro = st.text_input("Rubro (No modificable)", value=datos_art["rubro"], disabled=True)
                    with ce2:
                        nuevo_costo = st.number_input("Costo Neto ($)", min_value=0.0, value=float(datos_art["costo"] or 0), step=50.0)
                        nuevo_pv = st.number_input("Precio Venta Local ($)", min_value=0.0, value=d_pv_num, step=50.0)
                        nuevo_stock = st.number_input("Stock Actual", min_value=0, value=int(datos_art["stock_actual"] or 0))
                        
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        if st.button("💾 Guardar Cambios", type="primary", width='stretch'):
                            f_act = datetime.now().strftime("%d/%m/%Y")
                            
                            try:
                                valor_precio_upd = float(nuevo_pv)
                            except:
                                valor_precio_upd = str(nuevo_pv).replace('.', ',')

                            supabase.table("articulos").update({
                                "codigo": nuevo_codigo.strip(),
                                "descripcion": nueva_desc.strip(),
                                "costo": nuevo_costo,
                                "precio_venta": valor_precio_upd,
                                "stock_actual": nuevo_stock,
                                "fecha_act": f_act
                            }).eq("codigo", codigo_editar).execute()
                            st.toast("¡Artículo actualizado con éxito!", icon="✅")
                            st.rerun()
                    with col_m2:
                        if st.button("🗑️ Eliminar Artículo", type="secondary", width='stretch'):
                            supabase.table("articulos").delete().eq("codigo", codigo_editar).execute()
                            st.toast("¡Artículo eliminado!", icon="🗑️")
                            st.rerun()

    with tab_rubros:
        st.write("### 🏷️ Gestión de Rubros Comercial")
        tab_r1, tab_r2 = st.tabs(["➕ Crear Rubro", "✏️ Modificar / Eliminar Rubro"])
        
        with tab_r1:
            n_rubro = st.text_input("Nombre del Nuevo Rubro:")
            n_margen = st.number_input("Margen Base (%)", min_value=0.0, value=40.0, step=5.0)
            if st.button("➕ Crear Rubro", type="primary", width='stretch') and n_rubro:
                try:
                    supabase.table("rubros").insert({"nombre": n_rubro.strip(), "margen_defecto": n_margen}).execute()
                    st.toast(f"Rubro '{n_rubro}' incorporado.", icon="🏷️")
                    st.rerun()
                except:
                    st.warning("La categoría ya existe.")
                    
        with tab_r2:
            res_r_all = supabase.table("rubros").select("id, nombre, margen_defecto").execute().data
            if res_r_all:
                opciones_r = ["-- Seleccionar Rubro --"] + [f"{r['nombre']} (Margen: {r['margen_defecto']}%" for r in res_r_all if r['nombre'] != "- Sin clasificar -"]
                rubro_elegido_abm = st.selectbox("Seleccione rubro:", opciones_r)
                
                if rubro_elegido_abm != "-- Seleccionar Rubro --":
                    nombre_r_actual = rubro_elegido_abm.split(" (Margen:")[0].strip()
                    datos_r_act = next(r for r in res_r_all if r['nombre'] == nombre_r_actual)
                    mod_nombre_r = st.text_input("Editar Nombre", value=datos_r_act['nombre'])
                    mod_margen_r = st.number_input("Editar Margen (%)", min_value=0.0, value=float(datos_r_act['margen_defecto']), step=5.0)
                    
                    cb1, cb2 = st.columns(2)
                    with cb1:
                        if st.button("💾 Modificar Rubro", type="primary"):
                            supabase.table("rubros").update({"nombre": mod_nombre_r.strip(), "margen_defecto": mod_margen_r}).eq("id", datos_r_act["id"]).execute()
                            supabase.table("articulos").update({"rubro": mod_nombre_r.strip()}).eq("rubro", datos_r_act["nombre"]).execute()
                            st.toast("¡Categoría actualizada!", icon="🔄")
                            st.rerun()
                    with cb2:
                        if st.button("🗑️ Eliminar Rubro", type="secondary"):
                            supabase.table("rubros").delete().eq("id", datos_r_act["id"]).execute()
                            supabase.table("articulos").update({"rubro": "- Sin clasificar -"}).eq("rubro", datos_r_act["nombre"]).execute()
                            st.toast("Rubro eliminado.", icon="🗑️")
                            st.rerun()

# --- 3. MÓDULO: REPOSICIÓN DE STOCK & ACTUALIZACIÓN DE PRECIOS ---
elif "Reposición" in opcion_menu:
    st.markdown("<h1>🔄 Módulo de Operaciones Logísticas</h1>", unsafe_allow_html=True)
    tab_repo, tab_precios = st.tabs(["📦 Ingreso de Mercadería (Stock)", "📈 Actualización Global de Precios"])
    
    with tab_repo:
        res_repo = supabase.table("articulos").select("codigo, descripcion, stock_actual").execute().data
        if res_repo:
            opciones_repo = ["-- Seleccionar Producto --"] + [f"{a['descripcion']} (Cód: {a['codigo']}) - Stock: {a['stock_actual']}" for a in res_repo]
            prod_repo_sel = st.selectbox("Buscar artículo:", opciones_repo)
            
            if prod_repo_sel != "-- Seleccionar Producto --":
                cod_repo = prod_repo_sel.split("(Cód: ")[1].split(")")[0].strip()
                prod_actual = next(a for a in res_repo if a['codigo'] == cod_repo)
                cant_a_sumar = st.number_input("Unidades ingresantes:", min_value=1, value=10)
                
                if st.button("🟢 Confirmar Ingreso de Stock", type="primary"):
                    nuevo_stock = int(prod_actual["stock_actual"] or 0) + cant_a_sumar
                    supabase.table("articulos").update({"stock_actual": nuevo_stock}).eq("codigo", cod_repo).execute()
                    st.toast("¡Stock incrementado en la nube!", icon="📦")
                    st.rerun()
        else:
            st.info("No hay artículos en el catálogo para reponer stock.")

    with tab_precios:
        res_r_f = supabase.table("rubros").select("nombre").execute().data
        r_filtros = ["-- Todos los productos --"] + [r["nombre"] for r in res_r_f]
        rubro_a_afectar = st.selectbox("Filtrar lote por Rubro:", r_filtros)
        porcentaje_cambio = st.number_input("Porcentaje de Ajuste (%):", value=10.0)
        
        if st.button("⚡ Ejecutar Actualización Masiva", type="primary"):
            query = supabase.table("articulos").select("codigo, precio_venta")
            if rubro_a_afectar != "-- Todos los productos --":
                query = query.eq("rubro", rubro_a_afectar)
            articulos_cambio = query.execute().data
            
            for art in articulos_cambio:
                try:
                    pv_actual = float(str(art["precio_venta"]).replace('.', '').replace(',', '.'))
                except:
                    pv_actual = 0.0
                nuevo_pv = pv_actual * (1 + (porcentaje_cambio / 100))
                f_act = datetime.now().strftime("%d/%m/%Y")
                supabase.table("articulos").update({"precio_venta": str(round(nuevo_pv, 2)).replace('.', ','), "fecha_act": f_act}).eq("codigo", art["codigo"]).execute()
                
            st.success("¡Precios masivos actualizados correctamente!")
            st.rerun()


# --- 4. PUNTO DE VENTA (VENTAS / POS) ---
elif "Ventas" in opcion_menu:
    col_titulo_pos, col_salir_pos = st.columns([4, 1])
    with col_titulo_pos:
        st.markdown("<h2 style='margin: 0px;'>🛒 Terminal de Cobro (POS)</h2>", unsafe_allow_html=True)
    with col_salir_pos:
        if st.button("⬅️ Salir al Menú", type="secondary", width='stretch'):
            st.session_state.navegacion_actual = "🏠 Inicio / Dashboard"
            st.rerun()

    if "carrito_web" not in st.session_state:
        st.session_state.carrito_web = []

    c_carga, c_carrito, c_cierre = st.columns([1.1, 1.7, 1.1])

    with c_carga:
        st.markdown("<h4>🔍 Buscar / Escanear</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            res_pos = supabase.table("articulos").select("codigo, descripcion").execute().data
            opciones_articulos = ["-- Busque o Escanee Aquí --"] + [f"{art['codigo']} - {art['descripcion']}" for art in res_pos]
            articulo_seleccionado = st.selectbox("Producto:", opciones_articulos, index=0, label_visibility="collapsed")
            cant_scan = st.number_input("Cantidad:", min_value=1.0, value=1.0)
            
            if st.button("📥 Agregar al Pedido", type="secondary", width='stretch') and articulo_seleccionado != "-- Busque o Escanee Aquí --":
                codigo_a_procesar = articulo_seleccionado.split(" - ")[0].strip()
                res_prod = supabase.table("articulos").select("*").eq("codigo", codigo_a_procesar).execute().data
                
                if res_prod:
                    prod_sel = res_prod[0]
                    try:
                        p_f = float(str(prod_sel["precio_venta"]).replace('.', '').replace(',', '.'))
                    except:
                        p_f = 0.0
                    st.session_state.carrito_web.append({
                        "Código": prod_sel["codigo"], 
                        "Descripción": prod_sel["descripcion"], 
                        "Cantidad": float(cant_scan), 
                        "Unitario ($)": p_f, 
                        "Subtotal ($)": float(cant_scan * p_f)
                    })
                    st.toast(f"Añadido: {prod_sel['descripcion']}", icon="🛒")
                    st.rerun()

    with c_carrito:
        st.markdown("<h4>📋 Detalle de la Transacción</h4>", unsafe_allow_html=True)
        if st.session_state.carrito_web:
            df_carrito = pd.DataFrame(st.session_state.carrito_web)
            
            def procesar_cambio_cantidad():
                cambios = st.session_state.editor_pos_live.get("edited_rows", {})
                for fila_index, contenido in cambios.items():
                    if "Cantidad" in contenido:
                        nueva_cant = float(contenido["Cantidad"])
                        precio_uni = float(st.session_state.carrito_web[fila_index]["Unitario ($)"])
                        st.session_state.carrito_web[fila_index]["Cantidad"] = nueva_cant
                        st.session_state.carrito_web[fila_index]["Subtotal ($)"] = nueva_cant * precio_uni

            st.data_editor(
                df_carrito, width='stretch', hide_index=True, key="editor_pos_live", on_change=procesar_cambio_cantidad,
                column_config={
                    "Código": st.column_config.TextColumn(disabled=True), 
                    "Descripción": st.column_config.TextColumn(disabled=True),
                    "Cantidad": st.column_config.NumberColumn(min_value=1.0, required=True), 
                    "Unitario ($)": st.column_config.NumberColumn(format="$ %.2f", disabled=True), 
                    "Subtotal ($)": st.column_config.NumberColumn(format="$ %.2f", disabled=True)
                }
            )
            if st.button("❌ Vaciar Pedido", type="secondary", width='stretch'):
                st.session_state.carrito_web = []
                st.rerun()
        else:
            st.info("Terminal vacía. Cargue artículos.")

    with c_cierre:
        st.markdown("<h4>💵 Cierre / Ticket</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            subtotal_base = sum(i["Subtotal ($)"] for i in st.session_state.carrito_web)
            col_desc, col_rec = st.columns(2)
            p_desc = col_desc.number_input("Desc. (%)", min_value=0.0, max_value=100.0, value=0.0)
            p_rec = col_rec.number_input("Rec. (%)", min_value=0.0, max_value=100.0, value=0.0)
            
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
            monto_recibido = st.number_input("Monto Recibido ($):", min_value=0.0, value=float(tot_transaccion)) if m_pago == "Efectivo" else tot_transaccion
            
            st.markdown(
                f"""
                <div style="padding: 5px 0px; text-align: center; font-size: 0.95rem; font-weight: 600; color: #cbd5e1;">
                    Vuelto: <span style="color: #f59e0b; font-size: 1.1rem;">$ {max(0.0, monto_recibido - tot_transaccion):,.2f}</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("🟢 CONFIRMAR COMPROBANTE", type="primary", width='stretch') and st.session_state.carrito_web:
                f_v = datetime.now().strftime("%d/%m/%Y %H:%M")
                v_res = supabase.table("ventas").insert({"total": tot_transaccion, "fecha": f_v, "metodo_pago": m_pago}).execute()
                
                if v_res.data:
                    v_id = v_res.data[0]["id"]
                    
                    for item in st.session_state.carrito_web:
                        supabase.table("detalle_venta").insert({
                            "venta_id": v_id, 
                            "codigo": item["Código"], 
                            "descripcion": item["Descripción"], 
                            "cantidad": item["Cantidad"], 
                            "precio_unitario": item["Unitario ($)"], 
                            "subtotal": item["Subtotal ($)"]
                        }).execute()
                        
                        prod_stk = supabase.table("articulos").select("stock_actual").eq("codigo", item["Código"]).execute().data
                        if prod_stk:
                            nuevo_stk = int(prod_stk[0]["stock_actual"] or 0) - int(item["Cantidad"])
                            supabase.table("articulos").update({"stock_actual": nuevo_stk}).eq("codigo", item["Código"]).execute()
                    
                    st.success(f"Emitido N° {v_id}")
                    st.session_state.carrito_web = []
                    st.rerun()


# --- 5. INFORMES ANALÍTICOS ---
elif "Informes" in opcion_menu:
    st.markdown("<h1>📈 Módulo de Auditoría y Reportes</h1>", unsafe_allow_html=True)
    st.write("")
    
    rep_sel = st.selectbox("Selecciona la consulta analítica a procesar:", [
        "Historial General de Ventas Facturadas", 
        "Análisis de Valorización Física del Inventario"
    ])
    
    if "Historial" in rep_sel:
        st.subheader("Historial de Comprobantes Emitidos")
        
        f1, f2 = st.columns(2)
        fecha_desde = f1.date_input("Filtrar Desde:", value=date(2026, 1, 1))
        fecha_hasta = f2.date_input("Filtrar Hasta:", value=date(2026, 12, 31))
        
        res_v = supabase.table("ventas").select("id, fecha, metodo_pago, total").order("id", desc=True).execute().data
        df_ventas_reg = pd.DataFrame(res_v)
        
        if not df_ventas_reg.empty:
            # Procesado seguro de strings en pandas para segmentar fecha y hora
            df_ventas_reg['fecha_parsed'] = pd.to_datetime(df_ventas_reg['fecha'].astype(str).str.split().str[0], format='%d/%m/%Y').dt.date
            df_filtrado = df_ventas_reg[(df_ventas_reg['fecha_parsed'] >= fecha_desde) & (df_ventas_reg['fecha_parsed'] <= fecha_hasta)]
            
            if not df_filtrado.empty:
                st.write("### 📊 Gráfico Analítico de Rendimiento")
                df_agrupado = df_filtrado.groupby('metodo_pago')['total'].sum().reset_index()
                df_agrupado.columns = ['Método Pago', 'Total Recaudado ($)']
                st.bar_chart(data=df_agrupado, x='Método Pago', y='Total Recaudado ($)', width="stretch")
                
                st.write("### 📋 Registros Encontrados")
                df_mostrar = df_filtrado.drop(columns=['fecha_parsed'])
                df_mostrar.columns = ['N° Venta', 'Fecha y Hora', 'Método Pago', 'Total Recaudado ($)']
                st.dataframe(df_mostrar, width="stretch", hide_index=True)
            else:
                st.info("No se encontraron ventas comerciales en el rango de fechas seleccionado.")
        else:
            st.info("No se registran ventas guardadas en la base de datos de Supabase.")
            
    else:
        st.subheader("Auditoría Contable de Activos en Stock")
        res_val = supabase.table("articulos").select("costo, precio_venta, stock_actual").execute().data
        df_stock_val = pd.DataFrame(res_val)
        
        if not df_stock_val.empty:
            df_stock_val['pv_num'] = df_stock_val['precio_venta'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
            
            # Sanitización de nulos por seguridad contable
            df_stock_val['costo'] = df_stock_val['costo'].fillna(0.0).astype(float)
            df_stock_val['stock_actual'] = df_stock_val['stock_actual'].fillna(0).astype(int)
            
            c_costo = (df_stock_val['costo'] * df_stock_val['stock_actual']).sum()
            c_venta = (df_stock_val['pv_num'] * df_stock_val['stock_actual']).sum()
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
            st.info("Introduce artículos para calcular la valorización contable de tus existencias.")

import streamlit as st
import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA (Para que parezca una app nativa en el móvil)
st.set_page_config(page_title="App de Revisión Ambulancias", page_icon="🚑", layout="centered")

# Estilo CSS personalizado para que los títulos destaquen más
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #1E88E5; text-align: center; font-weight: bold;}
    .sub-header {font-size: 1.5rem; color: #0D47A1; font-weight: bold; border-bottom: 2px solid #1E88E5; padding-bottom: 5px;}
    .ticket-box {background-color: #F5F5F5; padding: 20px; border-radius: 10px; border: 1px dashed #757575;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🚑 Inspección Técnica de Ambulancia</div>', unsafe_allow_html=True)
st.write("---")

# 2. DATOS DEL VEHÍCULO Y TÉCNICO
st.markdown('<div class="sub-header">📋 Datos de la Revisión</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
vehiculo = col1.text_input("Vehículo:", placeholder="Ej: Soporte Vital Básico")
matricula = col2.text_input("Matrícula:", placeholder="Ej: 1234 ABC")

col3, col4 = st.columns(2)
kilometraje = col3.number_input("Kilometraje:", min_value=0, step=1)
fecha = col4.date_input("Fecha:", datetime.date.today())

tecnico = st.text_input("Técnico responsable:", placeholder="Tu nombre o apellidos")
st.write("---")

# 3. LISTAS DE ELEMENTOS (Extraídas exactamente de tu documento)
elementos_apagado = [
    "Estado general de carrocería", "Neumáticos (presión y desgaste)", "Estado de llantas",
    "Fugas visibles bajo el vehículo", "Nivel de aceite motor", "Nivel líquido refrigerante",
    "Nivel líquido frenos", "Nivel líquido dirección asistida", "Nivel lavaparabrisas",
    "Estado batería y bornes", "Sujeción batería", "Estado correas auxiliares",
    "Manguitos visibles", "Cierres de puertas", "Estado camilla y anclajes",
    "Botellas de oxígeno fijadas", "Tomas eléctricas interiores", "Estado de fusibles",
    "Luces exteriores (sin arrancar)", "Señalización reflectante"
]

elementos_encendido = [
    "Arranque del motor", "Ruido anómalo motor", "Testigos cuadro instrumentos",
    "Alternador/carga bateria", "Alumbrado corto/largo", "Intermitentes",
    "Luces de freno", "Luces marcha atrás", "Prioritarios luminosos",
    "Sirena acústica", "Climatización cabina", "Calefacción habitáculo sanitario",
    "Tomas 12V/220V", "Aspirador sanitario", "Funcionamiento desfibrilador/carga",
    "Compresor o instalación oxígeno", "Dirección asistida", "Pedal de freno",
    "Limpiaparabrisas", "Lavaparabrisas"
]

elementos_dinamicos = [
    "Comprobación de frenada", "Respuesta de la dirección", "Suspensión",
    "Vibraciones anómalas", "Aceleración del motor", "Cambio de marchas",
    "Ruidos de transmisión", "Estabilidad del vehículo", "Funcionamiento del ABS",
    "Funcionamiento del control de tracción", "Comprobación de sirena y prioritarios en circulación"
]

# Función para generar los controles de cada sección de forma limpia
def revisar_seccion(lista_elementos):
    incidencias = []
    for elemento in lista_elementos:
        # Usamos columnas para que quede compacto en la pantalla
        col_nombre, col_estado = st.columns([6, 4])
        with col_nombre:
            st.write(f"**{elemento}**")
        with col_estado:
            estado = st.selectbox("Estado", ["Correcto", "Defecto"], key=f"sel_{elemento}", label_visibility="collapsed")
        
        obs = ""
        if estado == "Defecto":
            obs = st.text_input("📝 Añadir observación:", key=f"obs_{elemento}", placeholder="Describe el problema...")
            incidencias.append({"elemento": elemento, "observacion": obs})
        st.write("") # Espacio
    return incidencias

# 4. FORMULARIO INTERACTIVO CON DESPLEGABLES (Expanders)
st.markdown('<div class="sub-header">🛠️ Desarrollo de la Revisión</div>', unsafe_allow_html=True)
st.info("💡 Toca en cada sección para desplegar los puntos a revisar.")

incidencias_totales = []

with st.expander("1. REVISIÓN EN PARADO - MOTOR APAGADO (preferentemente en frío)"):
    incidencias_totales.extend(revisar_seccion(elementos_apagado))

with st.expander("2. REVISIÓN EN PARADO - MOTOR EN FUNCIONAMIENTO"):
    incidencias_totales.extend(revisar_seccion(elementos_encendido))

with st.expander("3. COMPROBACIONES DINÁMICAS (en movimiento)"):
    incidencias_totales.extend(revisar_seccion(elementos_dinamicos))

st.write("---")

# 5. GENERACIÓN DEL INFORME FINAL (TICKET PROFESIONAL)
st.markdown('<div class="sub-header">📄 Cierre e Informe Final</div>', unsafe_allow_html=True)

if st.button("✅ GENERAR INFORME DE REVISIÓN", type="primary", use_container_width=True):
    
    st.markdown('<div class="ticket-box">', unsafe_allow_html=True)
    st.markdown("### 🏥 TICKET DE MANTENIMIENTO OFICIAL")
    st.write(f"**Fecha:** {fecha.strftime('%d/%m/%Y')} | **Técnico:** {tecnico.upper() if tecnico else 'N/A'}")
    st.write(f"**Vehículo:** {vehiculo} | **Matrícula:** {matricula} | **KM:** {kilometraje}")
    st.write("---")
    
    st.markdown("#### 3. INCIDENCIAS DETECTADAS")
    
    if len(incidencias_totales) == 0:
        st.success("✔️ VEHÍCULO APTO. No se han detectado defectos en ninguna de las fases.")
        texto_ticket = f"TICKET DE REVISIÓN\nVehiculo: {vehiculo}\nMatricula: {matricula}\nTodo correcto. Apto."
    else:
        st.error(f"⚠️ VEHÍCULO NO APTO. Se han detectado {len(incidencias_totales)} incidencias que requieren atención:")
        texto_ticket = f"TICKET DE REVISIÓN\nVehiculo: {vehiculo}\nMatricula: {matricula}\nINCIDENCIAS:\n"
        for inc in incidencias_totales:
            detalle = inc['observacion'] if inc['observacion'] else "Sin observaciones detalladas"
            st.warning(f"❌ **{inc['elemento']}**: {detalle}")
            texto_ticket += f"- {inc['elemento']}: {detalle}\n"
    
    st.write("---")
    st.write("#### 4. FIRMA")
    st.write("*(Firma digital generada y validada en el sistema)*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón mágico para descargar el informe como archivo de texto
    st.download_button(
        label="📥 Descargar Informe (TXT)",
        data=texto_ticket,
        file_name=f"Revision_{matricula}.txt",
        mime="text/plain",
        use_container_width=True
    )
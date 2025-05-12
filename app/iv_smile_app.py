import pandas as pd
import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go

# URLs de tus endpoints
URL_OPCIONES = "https://cyw9gfj3pf.execute-api.us-east-1.amazonaws.com/dev/opciones"
URL_IV = "https://cyw9gfj3pf.execute-api.us-east-1.amazonaws.com/dev/iv"
URL_FUTUROS = "https://cyw9gfj3pf.execute-api.us-east-1.amazonaws.com/dev/futuros"

@st.cache_data
def cargar_opciones():
    resp = requests.get(URL_OPCIONES)
    data = resp.json()
    if isinstance(data, dict) and "body" in data:
        data = json.loads(data["body"])
    return pd.DataFrame(data)

@st.cache_data
def cargar_iv():
    resp = requests.get(URL_IV)
    data = resp.json()
    if isinstance(data, dict) and "body" in data:
        data = json.loads(data["body"])
    return pd.DataFrame(data)

@st.cache_data
def cargar_futuros():
    resp = requests.get(URL_FUTUROS)
    data = resp.json()
    if isinstance(data, dict) and "body" in data:
        data = json.loads(data["body"])
    return pd.DataFrame(data)

opciones_df = cargar_opciones()
iv_df = cargar_iv()
futuros_df = cargar_futuros()

st.header("Futuros disponibles")
st.dataframe(futuros_df)

st.header("Opciones (CALL y PUT) con toda la información e IV")
# Unir opciones y IV por date, strike y type
opciones_iv = opciones_df.merge(
    iv_df[['date', 'strike', 'type', 'iv']],
    on=['date', 'strike', 'type'],
    how='left'
)
# Determinar columnas a mostrar
columnas_opciones = ['date', 'type', 'strike', 'price', 'iv']
for col in ['volume', 'volumen', 'last', 'ultimo']:
    if col in opciones_iv.columns:
        columnas_opciones.append(col)
st.dataframe(opciones_iv[columnas_opciones])

st.header("Smile de volatilidad y datos por fecha de vencimiento")
fechas_vencimiento = sorted(opciones_iv['date'].unique())
fecha_venc_sel = st.selectbox("Selecciona fecha de vencimiento", fechas_vencimiento)
opciones_fecha = opciones_iv[opciones_iv['date'] == fecha_venc_sel]

if not opciones_fecha.empty:
    fig = px.line(
        opciones_fecha,
        x='strike',
        y='iv',
        color='type',
        markers=True,
        title=f"Smile de Volatilidad Implícita para {fecha_venc_sel}"
    )
    st.plotly_chart(fig, key="smile_selector")

    st.subheader("Opciones CALL para la fecha seleccionada")
    st.dataframe(opciones_fecha[opciones_fecha['type'] == 'call'][columnas_opciones])

    st.subheader("Opciones PUT para la fecha seleccionada")
    st.dataframe(opciones_fecha[opciones_fecha['type'] == 'put'][columnas_opciones])
else:
    st.warning("No hay datos de opciones para la fecha seleccionada.")

# El resto de funcionalidades avanzadas pueden ir aquí o en tabs adicionales

# --- TABS PRINCIPALES ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Resumen actual",
    "Tablas históricas",
    "Smile de IV avanzado",
    "Superficie 3D",
    "Descarga de datos"
])

# --- TAB 1: RESUMEN ACTUAL ---
with tab1:
    st.header("Resumen actual: datos y smile más recientes")
    df_scrape = opciones_df.dropna(subset=['scrape_date']) if 'scrape_date' in opciones_df.columns else opciones_df
    if not df_scrape.empty and 'scrape_date' in df_scrape.columns:
        fecha_scraping_actual = df_scrape['scrape_date'].max()
        st.write(f"Fecha de scraping más reciente: {fecha_scraping_actual}")
        opciones_actual = opciones_df[opciones_df['scrape_date'] == fecha_scraping_actual] if 'scrape_date' in opciones_df.columns else opciones_df
        iv_actual = iv_df[iv_df['scrape_date'] == fecha_scraping_actual] if 'scrape_date' in iv_df.columns else iv_df
        futuros_actual = futuros_df[futuros_df['scrape_date'] == fecha_scraping_actual] if 'scrape_date' in futuros_df.columns else futuros_df
        # Unir opciones y IV por date, strike y type para mostrar IV en las tablas de opciones
        opciones_actual_iv = opciones_actual.merge(
            iv_actual[['date', 'strike', 'type', 'iv']],
            on=['date', 'strike', 'type'],
            how='left'
        )
        # Determinar columnas a mostrar
        columnas_opciones = ['strike', 'price', 'iv']
        if 'volume' in opciones_actual_iv.columns:
            columnas_opciones.append('volume')
        elif 'volumen' in opciones_actual_iv.columns:
            columnas_opciones.append('volumen')
        if 'last' in opciones_actual_iv.columns:
            columnas_opciones.append('last')
        elif 'ultimo' in opciones_actual_iv.columns:
            columnas_opciones.append('ultimo')
        st.subheader("Futuros (más recientes)")
        st.dataframe(futuros_actual)
        st.subheader("Opciones CALL (más recientes, con IV)")
        st.dataframe(opciones_actual_iv[opciones_actual_iv['type'] == 'call'][columnas_opciones])
        st.subheader("Opciones PUT (más recientes, con IV)")
        st.dataframe(opciones_actual_iv[opciones_actual_iv['type'] == 'put'][columnas_opciones])
        st.subheader("IV (más recientes)")
        st.dataframe(iv_actual)
        # Gráfico Smile de IV para la fecha de vencimiento más reciente
        if not iv_actual.empty and 'date' in iv_actual.columns:
            fecha_vencimiento_actual = iv_actual['date'].max()
            df_iv_fecha = iv_actual[iv_actual['date'] == fecha_vencimiento_actual]
            if not df_iv_fecha.empty:
                fig = px.line(
                    df_iv_fecha,
                    x='strike',
                    y='iv',
                    color='type',
                    markers=True,
                    title=f"Smile de Volatilidad Implícita para {fecha_vencimiento_actual}"
                )
                st.plotly_chart(fig, key="smile_resumen")
    else:
        st.warning("No hay datos de scraping disponibles.")

# --- TAB 2: TABLAS HISTÓRICAS ---
with tab2:
    st.header("Tablas históricas")
    if 'scrape_date' in opciones_df.columns:
        fechas_scraping = sorted(opciones_df['scrape_date'].dropna().unique())
        fecha_scraping_sel = st.selectbox("Selecciona fecha de scraping", fechas_scraping, key="scrape_date_hist")
        opciones_df_filtrado = opciones_df[opciones_df['scrape_date'] == fecha_scraping_sel]
        iv_df_filtrado = iv_df[iv_df['scrape_date'] == fecha_scraping_sel] if 'scrape_date' in iv_df.columns else iv_df
        futuros_df_filtrado = futuros_df[futuros_df['scrape_date'] == fecha_scraping_sel] if 'scrape_date' in futuros_df.columns else futuros_df
    else:
        opciones_df_filtrado = opciones_df
        iv_df_filtrado = iv_df
        futuros_df_filtrado = futuros_df
    # Unir opciones y IV por date, strike y type para mostrar IV en las tablas de opciones
    opciones_iv = opciones_df_filtrado.merge(
        iv_df_filtrado[['date', 'strike', 'type', 'iv']],
        on=['date', 'strike', 'type'],
        how='left'
    )
    columnas_opciones = ['strike', 'price', 'iv']
    if 'volume' in opciones_iv.columns:
        columnas_opciones.append('volume')
    elif 'volumen' in opciones_iv.columns:
        columnas_opciones.append('volumen')
    if 'last' in opciones_iv.columns:
        columnas_opciones.append('last')
    elif 'ultimo' in opciones_iv.columns:
        columnas_opciones.append('ultimo')
    st.subheader("Futuros")
    st.dataframe(futuros_df_filtrado)
    st.subheader("Opciones CALL (con IV)")
    st.dataframe(opciones_iv[opciones_iv['type'] == 'call'][columnas_opciones])
    st.subheader("Opciones PUT (con IV)")
    st.dataframe(opciones_iv[opciones_iv['type'] == 'put'][columnas_opciones])
    st.subheader("IV")
    st.dataframe(iv_df_filtrado)

# --- TAB 3: SMILE DE IV AVANZADO ---
with tab3:
    st.header("Smile de IV avanzado")
    if not iv_df_filtrado.empty and 'date' in iv_df_filtrado.columns:
        fechas_iv = sorted(iv_df_filtrado['date'].unique())
        fecha_venc_sel = st.selectbox("Selecciona fecha de vencimiento (IV)", fechas_iv, key="exp_iv")
        columnas_iv = ['strike', 'iv', 'type']
        columnas_iv = [col for col in columnas_iv if col in iv_df_filtrado.columns]
        df_iv_fecha = iv_df_filtrado[iv_df_filtrado['date'] == fecha_venc_sel]
        if not df_iv_fecha.empty:
            fig = px.line(
                df_iv_fecha,
                x='strike',
                y='iv',
                color='type',
                markers=True,
                title=f"Smile de Volatilidad Implícita para {fecha_venc_sel}"
            )
            st.plotly_chart(fig, key="smile_avanzado")
    else:
        st.warning("No hay datos de IV para la selección actual.")

# --- TAB 4: SUPERFICIE 3D ---
with tab4:
    st.header("Superficie 3D de volatilidad")
    if not iv_df_filtrado.empty and all(col in iv_df_filtrado.columns for col in ['strike', 'date', 'iv']):
        iv_df_filtrado['date_num'] = pd.to_datetime(iv_df_filtrado['date'], errors='coerce').map(pd.Timestamp.toordinal)
        fig3d = go.Figure(data=[
            go.Mesh3d(
                x=iv_df_filtrado['strike'],
                y=iv_df_filtrado['date_num'],
                z=iv_df_filtrado['iv'],
                color='lightblue',
                opacity=0.5
            )
        ])
        tickvals = iv_df_filtrado['date_num'].unique()
        ticktext = pd.to_datetime(iv_df_filtrado['date'], errors='coerce').dt.strftime('%Y-%m-%d').unique()
        fig3d.update_layout(
            title='Superficie de Volatilidad Implícita',
            scene=dict(
                xaxis_title='Strike',
                yaxis_title='Fecha de Vencimiento',
                zaxis_title='IV',
                yaxis=dict(tickvals=tickvals, ticktext=ticktext)
            )
        )
        st.plotly_chart(fig3d, key="superficie_3d")
    else:
        st.warning("No hay datos suficientes para la superficie 3D.")

# --- TAB 5: DESCARGA DE DATOS ---
with tab5:
    st.header("Descarga de datos filtrados")
    st.write("Puedes descargar los datos filtrados de opciones, IV y futuros en formato CSV.")
    st.download_button("Descargar opciones filtradas (CSV)", opciones_df_filtrado.to_csv(index=False), file_name="opciones_filtradas.csv", mime="text/csv")
    st.download_button("Descargar IV filtrada (CSV)", iv_df_filtrado.to_csv(index=False), file_name="iv_filtrada.csv", mime="text/csv")
    st.download_button("Descargar futuros filtrados (CSV)", futuros_df_filtrado.to_csv(index=False), file_name="futuros_filtrados.csv", mime="text/csv")
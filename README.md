# Práctica Tecnologías Cloud - mIA-13

Aplicación web para visualizar la volatilidad implícita de las opciones MINI IBEX.

## TODO

- [ ] Parte 1: Aplicación Web
  - [ ] Web scraping datos MEFF
  - [ ] Cálculo volatilidad implícita
  - [ ] Gráfico skew de volatilidad
  - [ ] Repositorio GitHub
- [ ] Parte 2: Servicios Cloud
  - [ ] Despliegue app
  - [ ] Workflows GitHub (CI/CD)
  - [ ] Función scraping diario + DB
  - [ ] Función cálculo volatilidad + DB
  - [ ] Workflow despliegue funciones
  - [ ] Conectar app a DB
  - [ ] API
  - [ ] UI: Skews históricos y comparación
  - [ ] Superficie de volatilidad
  - [ ] Terraform
  - [ ] Diagrama arquitectura 

## Ejecución local

Para ejecutar la app principal de Streamlit:

```sh
streamlit run app/iv_smile_app_v3.py
```

## Despliegue público

La app está disponible públicamente en:

https://iguazsmile.streamlit.app/

## Despliegue en Streamlit Cloud

- En el formulario de Streamlit Cloud, usa como "Main file path":
  ```
  app/iv_smile_app_v3.py
  ```
- Asegúrate de que todas las dependencias estén en `requirements.txt` en la raíz del repositorio. 
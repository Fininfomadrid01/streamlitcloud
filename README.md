# Arquitectura Serverless para Análisis de Opciones y Futuros

> **Documento profesional completo:** Consulta también el informe detallado en [Informe_Arquitectura_IV_Smile.docx](./Informe_Arquitectura_IV_Smile.docx)

## Resumen Ejecutivo

Se ha desarrollado una arquitectura serverless en AWS para la automatización del scraping, almacenamiento, cálculo y visualización de datos financieros (opciones y futuros del Mini Ibex), con trazabilidad diaria y visualización profesional en una app Streamlit Cloud.

---

## Objetivos del Proyecto
- Automatizar la recolección diaria de datos de opciones y futuros.
- Calcular la volatilidad implícita (IV) de las opciones.
- Almacenar todos los datos con trazabilidad por fecha de scraping.
- Exponer los datos mediante una API REST.
- Visualizar y analizar los datos en una app web moderna y accesible.

---

## Arquitectura General

### Componentes Principales
- **AWS Lambda:** Funciones serverless para scraping, cálculo de IV y API.
- **Amazon EventBridge:** Triggers programados para la ejecución automática de los procesos.
- **Amazon DynamoDB:** Almacenamiento NoSQL de opciones, futuros e IV, con campo `scrape_date` para trazabilidad.
- **Amazon API Gateway:** Exposición de endpoints REST para consulta de datos.
- **Streamlit Cloud:** App web pública para visualización y análisis.
- **Docker & ECR:** Empaquetado y despliegue de Lambdas en contenedores.
- **Terraform:** Infraestructura como código para gestión y despliegue reproducible.

---

## Diagrama de Arquitectura

![Diagrama de arquitectura serverless de IV Smile](./arquitectura_iv_smile.png)

*Diagrama general de la arquitectura serverless: automatización de scraping, cálculo y visualización de datos financieros usando AWS Lambda, EventBridge, DynamoDB, API Gateway y Streamlit Cloud.*

---

## Flujos y Automatizaciones

### Scraping y Cálculo Automático
- **EventBridge** lanza diariamente:
  - **Lambda Scraper Opciones** (`cron(0 23 ? * MON-FRI *)`)
  - **Lambda Scraper Futuros** (`cron(0 23 *? * MON-FRI *)`)
  - **Lambda IV Calc** (`cron(20 23 * ? * MON-FRI *)`)
- Cada Lambda guarda los datos en **DynamoDB** con la fecha de scraping (`scrape_date`).

### Exposición de Datos vía API
- **API Gateway** expone los endpoints:
  - `/opciones` — Devuelve opciones
  - `/futuros` — Devuelve futuros
  - `/iv` — Devuelve volatilidad implícita
- **Lambda API Embudo** procesa las peticiones y consulta DynamoDB.

### Visualización
- **App Streamlit** **App Streamlit** https://iguazsmile.streamlit.app/  permite:
  - Seleccionar la fecha de scraping.
  - Visualizar tablas y gráficos de opciones, futuros e IV.
  - Analizar la superficie de volatilidad y otros indicadores.

---

## Trazabilidad y Auditoría
- Todos los registros en DynamoDB incluyen el campo `scrape_date`.
- Es posible consultar cualquier snapshot histórico de los datos.
- El sistema es auditable y permite análisis evolutivo.

---

## Despliegue y Mantenimiento
- **Terraform** gestiona toda la infraestructura (Lambdas, triggers, tablas, API Gateway).
- **Docker** y **ECR** facilitan el versionado y despliegue de las Lambdas.
- **GitHub** centraliza el control de versiones y la colaboración.

---

## Endpoints y Triggers

### Triggers de EventBridge

| Trigger/EventBridge           | Cron/Regla                | Lambda destino                | Descripción                                      |
|------------------------------|---------------------------|-------------------------------|--------------------------------------------------|
| Scraper de futuros diario    | `cron(0 23 ? * MON-FRI *)`      | scraper_futuros_lambda        | Scraping de futuros cada día de lunes a viernes a las 23:00 UTC     |
| Scraper de opciones diario   | `cron(0 23 ? * MON-FRI *))`      | dev-scraper-lambda-v2         | Scraping de opciones cada día de lunes a viernes a las 23:00 UTC    |
| Cálculo de IV diario         | `cron(20 23 * ? * MON-FRI *))`     | iv_calc_lambda                | Cálculo de IV cada día de lunes a viernea las 23:20 UTC                    |

### Endpoints (URLs)

| Endpoint (URL)                                                      | Método | Lambda destino         | Descripción                  |
|---------------------------------------------------------------------|--------|-----------------------|------------------------------|
| `/opciones`<br>https://cyw9gfj3pf.execute-api.us-east-1.amazonaws.com/dev/opciones | GET    | api-embudo-lambda     | Devuelve opciones            |
| `/futuros`<br>https://cyw9gfj3pf.execute-api.us-east-1.amazonaws.com/dev/futuros   | GET    | api-embudo-lambda     | Devuelve futuros             |
| `/iv`<br>https://cyw9gfj3pf.execute-api.us-east-1.amazonaws.com/dev/iv             | GET    | api-embudo-lambda     | Devuelve IV                  |
| **App Streamlit** https://iguazsmile.streamlit.app/                              | -      | -                     | Visualización de los datos   |

---

## Contacto y Créditos
- Responsable técnico: Andrés Iguaz
- Repositorio: https://github.com/Fininfomadrid01/streamlitcloud (En abierto para que puedas acceder)
- Fecha: 17/05/2025 

# Práctica Tecnologías Cloud - mIA-13

Aplicación web para visualizar la volatilidad implícita de las opciones MINI IBEX.

## TODO

- [ x] Parte 1: Aplicación Web
  - [x] Web scraping datos MEFF
  - [x ] Cálculo volatilidad implícita
  - [x ] Gráfico skew de volatilidad
  - [x ] Repositorio GitHub
- [x ] Parte 2: Servicios Cloud
  - [x ] Despliegue app
  - [x ] Workflows GitHub (CI/CD)
  - [x ] Función scraping diario + DB
  - [x ] Función cálculo volatilidad + DB
  - [x ] Workflow despliegue funciones
  - [x ] Conectar app a DB
  - [x ] API
  - [x ] UI: Skews históricos y comparación
  - [x ] Superficie de volatilidad
  - [x ] Terraform
  - [x ] Diagrama arquitectura 



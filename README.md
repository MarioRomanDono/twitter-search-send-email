# Twitter-search-send-email

## Descripción

Este repositorio contiene una serie de scripts escritos en Python que realizan una búsqueda en Twitter y envian los resultados mediante email. Para ello, se utiiza la Twitter API v2 y la Gmail API.

El objetivo de este proyecto es, principalmente, prácticar el uso de Python y el manejo de las API anteriormente mencionadas. Aunque este programa es totalmente funcional, de cara al usuario final tal vez es más recomendable utilizar servicios ya existentes y especializados como [IFTTT](https://ifttt.com/)

## Requisitos
- Python 3 y Pip
- Paquetes de Python para utilizar la API de Gmail: `google-api-python-client`, `google-auth-httplib2` y `google-auth-oauthlib`.
- Seguir los pasos para tener [acceso a la API de Twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) y obtener un Bearer Token
- [Crear un proyecto en Google Cloud Platform](https://developers.google.com/workspace/guides/create-project) con la API de Gmail activada y [obtener credenciales para una aplicación de escritorio](https://developers.google.com/workspace/guides/create-credentials)
- Establecer las siguientes variables de entorno:
    - `BEARER_TOKEN` - Token utilizado para realizar las búsquedas en Twitter
    - `QUERY` -  Consulta que se quiere hacer a la API de Twitter. Debe seguir el formato indicado en la [documentación de la API](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)
    - `HOURS` - Número de horas previas a la actual sobre los que se quiere realizar la búsqueda. Por ejemplo, si se quieren buscar los tweets publicados en las últimas 24 horas, debe ser igual a 24. Debe estar entre 0 y 168, debido a que la API de Twitter (en su versión Standard) limita las búsquedas de tweets a los últimos siete días.
    - `FROM_EMAIL` - Dirección de email del remitente
    - `TO_EMAIL` - Dirección de email del destinatario
    - `SUBJECT_EMAIL` - Asunto de los emails enviados
    - `GMAIL_CREDENTIALS` - Cadena JSON codificada en Base64 que se encuentra en el fichero `credentials.json`, obtenido tras haber creado las credenciales de Gmail.
    - `GMAIL_TOKEN` - Cadena JSON codificada en Base64 que se encuentra en el fichero `token.json`, creado tras haber autorizado la aplicación.
- Si no se han establecido las variables `GMAIL_CREDENTIALS` o `GMAIL_TOKEN`, se deben encontrar los ficheros `token.json` y/o `credentials.json` en la raíz del repositorio.

## Instalación y uso
1. Clonar el repositorio: `git clone https://github.com/MarioRomanDono/twitter-search-send-email.git && cd twitter-search-send-email/`
2. Instalar los paquetes requeridos: `pip install -r requirements.txt`
3. Establecer las variables de entorno y ejecutar el programa: `python3 main.py`

Este proyecto puede ser desplegado en plataformas como Heroku o AWS Lambda para que sea ejecutado periódicamente.

También puede ejecutarse en un contenedor de Docker utilizando el Dockerfile disponible en el repositorio.

## Licencia
Todo el código se encuentra bajo la [licencia Apache License 2.0](LICENSE). Se han utilizado fragmentos de código disponibles en las documentaciones de la [API de Twitter](https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py) y de la [API de Gmail](https://github.com/googleworkspace/python-samples/blob/master/gmail/quickstart/quickstart.py).

## Contribuciones
Tanto si deseas añadir como modificar cualquier funcionalidad de los scripts, ¡todos las contribuciones son bienvenidas!
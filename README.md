<h1 align='center'> VideoGameRecommender </h1>
<p align='center'>Video game recommendation system (Sistema de recomendación de videojuegos)<P>

<h2 align='center' id='introduccion'>Descripción del proyecto</h2>

Este proyecto consiste en el desarrollo de un sistema de recomendación de videojuegos para usuarios, diseñado desde cero para un MVP (Minimum Viable Product). Se enfoca en leer y procesar un conjunto de datos crudos, transformándolos y estructurándolos de manera eficiente para facilitar su uso en análisis de datos y aprendizaje automático.

### Tabla de contenido
1. [Introducción](#introduccion)
2. [Instalación y Requisitos](#instalacion-y-requisitos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Uso y Ejecución](#uso-y-ejecucion)
5. [Datos y Fuentes](#datos-y-fuentes)
6. [Metodología](#metodologia)
7. [Resultados y Conclusiones](#resultados-y-conclusiones)
8. [Contribución y Colaboración](#contribución-y-colaboracion)
9. [Licencia](#licencia)

<h2 align='center' id='instalacion-y-requisitos'>Instalación y Requisitos</h2>
<ul>
    <li><b>Lenguaje:</b> Python.</li>
    <li><b>Framework:</b> FastAPI.</li>
    <li><b>NLP (Procesamiento de Lenguaje Natural):</b> Librerías de Machine Learning para el análisis de sentimientos.</li>
    <li><b>Entorno de Despliegue:</b> Render.</li>
</ul>

Todas las librerías y dependencias se encuentran en el archivo requirements.txt. Todo lo que se tiene que hacer es asegurarse de que la consola se encuentra en la misma carpeta en la que el archivo se encuentra y escribir:

    - `pip install requirements.txt`

<h3 align='center'>Objetivos</h3>
<ul>
    <li><b>Extracción y preparación de datos:</b> Se realiza un trabajo de Data Engineering para limpiar y estructurar los datos, eliminando columnas innecesarias y optimizando el rendimiento del modelo y la API.</li>
    <li><b>Análisis de Sentimientos:</b> Se aplica procesamiento de lenguaje natural (NLP) para analizar las reseñas de los usuarios, generando una nueva columna de análisis de sentimientos que reemplaza las reseñas originales.</li>
    <li><b>Desarrollo de API:</b> Se construye una API RESTful utilizando FastAPI, permitiendo a los usuarios consultar datos relevantes a través de varios endpoints. Las funciones incluyen:</li>
    <ul>
        <li>Análisis de desarrolladores por año.</li>
        <li>Datos de gasto y recomendaciones personalizadas por usuario.</li>
        <li>Identificación de usuarios más activos por género de juego.</li>
        <li>Análisis de los mejores desarrolladores por año.</li>
        <li>Evaluación de reseñas por desarrollador según el análisis de sentimiento.</li>
    </ul>
    <li><b>Exploración de Datos (EDA):</b> Se realiza un análisis exploratorio de los datos para identificar patrones, relaciones y anomalías, evitando el uso de librerías automáticas para aplicar manualmente los conceptos y técnicas de EDA.</li>
    <li><b>Modelo de Aprendizaje Automático:</b> Se entrena un modelo de machine learning para el sistema de recomendación, implementando al menos uno de los siguientes enfoques:</li>
    <ul>
        <li><b>Sistema de recomendación item-item:</b> Sugerencias de juegos similares basadas en la similitud del coseno.</li>
        <li><b>Sistema de recomendación user-item:</b> Sugerencias personalizadas para usuarios específicos.</li>
    </ul>
</ul>

<h2 align='center' id='estructura-del-proyecto'>Estructura del Proyecto</h2>

- data/: Contiene los datos en crudo.
- ETL/: Contiene los archivos con el procesamiento de los datos.
- EDA/: Contiene las visualizaciones de los datos. El archivo EDA.ipynb realiza procesamientos adicionales de ETL en función de las tablas unificadas para el entrenamiento del modelo de Machine Lerning.
- Feature Engineering/: Contiene el análisis de sentimientos.
- functions/: Contiene funciones utilitarias catalogadas por ETL y EDA dependiendo su uso.
- ML/: Contiene un archivo para el procesamiento de los datos para entrenar el modelo de Machine Learning, su entrenamiento y el modelo pre entrenado para ser utilizado.
- src/:
    - CSV/: contiene los datos procesados en formato CSV.
    - Parquet/: contiene los datos procesados en formato Parquet.
- main.py: Funciones de API consumibles.
- README.md: Información del proyecto.
- requirements.txt: Contiene las librerías necesarias para ejecutar todo el proyecto.

<h3 align='center' id='uso-y-ejecucion'>Uso y Ejecución</h3>

Si bien, se sube el modelo de Machine Learning pre entrenado, en el caso de querer ver el proceso completo del código, deben respetarse todas las etapas de ejecución del proyecto para que los resultados sean óptimos:

<ol>
    <li><b>ETL (Extraction - Transform - Load):</b> En la carpeta ETL se pueden encontrar los distintos archivos de tipo Jupyter Notebook que se encargan de extraer la data de los DataSets en la carpeta data. Los archivos no tienen un orden específico para ejecutarse, ya que su función es abrir y limpiar los DataSets para luego exportarlos listos para el proceso de EDA. Cada paso está detallado en los markdowns.</li>
    <li><b>Feature Egineering:</b> Ejecutarlo para realizar el análisis de sentimientos en el DataSet user_reviews y exportar un archivo fácilmente trabajable en los prcesos de EDA y Machine Learning.</li>
    <li><b>EDA (Análisis Exploratorio de Datos):</b> Pueden ejecutarse en cualquier orden pero, se recomienda dejar el archivo EDA.ipynb para el final, ya que incluye visualizaciones de la relación entre todos los DataSets procesados y un último proceso de ETL que se enfoca en el procesamiento de datos para entrenar el modelo de Machine Learning.</li>
    <li><b>ML/dummies.ipynb:</b> Este archivo se encarga de generar los valores dummies con los que el modelo de Machine Learning será entrenado.</li>
    <li><b>ML/training.ipynb:</b> Este archivo se encarga de procesar los datos creados luego de generar las columnas dummies entrenando el modelo de Machine Learning que será utilizado para el sistema de recomendación que al final del archivo es exportado.</li>
    <li><b>Consola (`uvicorn main:app --reload`):</b> Este proceso levanta un servidor local en el puerto 8000, lo que permite al usuario acceder a `localhost:8000` y visualizar la información. En caso de querer visualizar todo desde una interfaz gráfica interactiva se puede acceder a `localhost:8000/docs` donde se puede interactuar de forma más interactiva con la API.</li>
</ol>

<b>Nota: </b> Si se desea probar directamente la API con el modelo de Machine Learning pre entrenado se puede avanzar directamente al último paso, dado que el modelo de Machine Learning pre entrenado ha sido subido para optimizar los tiempos de respuesta.

<h2 align='center' id='datos-y-fuentes'>Datos y Fuentes</h2>

Todos los datos utilizados en este proyecto han sido extraídos de las APIs de usuarios, comentarios y juegos de la plataforma Steam Games.

<h2 align='center' id='metodologia'>Metodología</h2>

- <b>Modelo de Machine Learning:</b> Para el modelo de Machine Learning se utilizó el algoritmo de `Similitud del Coseno` que se encarga de identificar el ángulo entre dos vectores n-dimensionales en un espacio n-dimensional (vectoriza los datos) obteniendo un producto escalar entre ambos vectores dividido por el producto de las magnitudes de los vectores obtenidos según los patrones de los datos.
- <b>API:</b> Para el desarrollo de la API se utilizó la tecnología de FastAPI y, para la ejecución en un servidor local se utilizó uvicorn.

<h2 align='center' id='resultados-y-conclusiones'>Resultados y Conclusiones</h2>
<h2 align='center' id='contribución-y-colaboracion'>Contribución y Colaboración</h2>

Se invita a colaboradores a contribuír en la mejora del análisis, así como a proporcionar retroalimentación sobre el proyecto.

<h2 align='center' id='licencia'>Licencia</h2>

Agostina Ailén Fernández Rodríguez - Contacto: [LinkedIn](https://www.linkedin.com/in/agostina-fern%C3%A1ndez-aab4a8323/)
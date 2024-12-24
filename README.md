![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Google](https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Static Badge](https://img.shields.io/badge/By_Charles_-blue)

# AIris - Flask

Bienvenido a **AIris**, una aplicación de código abierto construida con Flask e impulsada por Google Generative AI. Esta aplicación permite interactuar con un chatbot basado en inteligencia artificial de manera sencilla y eficiente.

## Características
- **Minimalismo**: Diseño simple y limpio para una experiencia de usuario intuitiva.
- **Chat impulsado por IA**: Utiliza Google Generative AI para generar respuestas realistas y útiles.
- **Panel de administración**: Gestiona y supervisa las conversaciones y usuarios desde un panel de control.
  - Contador de mensajes enviados por cada usuario.
  - Visualización del modelo de IA que está usando cada usuario.
  - Estadísticas detalladas del uso de la IA.
- **Código abierto**: Modifica y adapta la aplicación según tus necesidades.

## Requisitos
- Python 3.8 o superior
- Flask
- Google Generative AI API Key

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/frensby11/AIris.git
   ```
2. Ingresa al directorio del proyecto:
   ```bash
   cd AIris
   ```
3. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Configura las claves de entorno necesarias:
   ```bash
   export AIRISU="user"
   export AIRISP="password"
   export API_KEY="clave de google"
   ```
   - **AIRISU**: Nombre de usuario para acceder al panel de administración.
   - **AIRISP**: Contraseña para el panel de administración.
   - **API_KEY**: Clave de API de Google Generative AI.

   Asegúrate de que las variables de entorno estén configuradas correctamente antes de iniciar la aplicación.

## Ejecución
Para iniciar la aplicación, ejecuta:
```bash
flask run
```
Accede al chat desde [http://localhost:5000](http://localhost:5000).
Para acceder al panel de administración, visita:
```bash
http://<IP_DEL_SERVIDOR>:5000/admin
```
El panel de administración permite:
- Visualizar el número de mensajes enviados por usuario.
- Ver el modelo de IA en uso.
- Acceder a informes detallados de la actividad del chatbot.

## Contribución
Las contribuciones son bienvenidas. Si deseas colaborar, por favor abre un issue o envía un pull request.

## Licencia
Este proyecto no se puede vender.


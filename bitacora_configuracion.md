# Bitácora de Configuración: Entorno Virtual, Git y GitHub en VS Code

Esta bitácora documenta paso a paso el proceso realizado para configurar el entorno de desarrollo en Python, la automatización de terminales, la inicialización del control de versiones con Git y la vinculación exitosa con GitHub.

---

## 1. Configuración del Entorno Virtual y Terminal en VS Code

Para evitar tener que activar manualmente el entorno virtual (`entorno310`) cada vez que se abriera una nueva terminal o proyecto, se estableció una configuración global en Visual Studio Code.

* **Paso 1:** Abrir la configuración de VS Code presionando `Ctrl + ,`.
* **Paso 2:** Buscar la opción **`Activate Environment`**.
* **Paso 3:** Marcar la casilla **"Python › Terminal: Activate Environment: Activate Python Environment in all Terminals created"** bajo la pestaña **User** (Usuario). Esto asegura que se aplique de forma global en cualquier proyecto futuro.

* **Pero si falla:** activarlo de forma manual: c:\Py310\entorno310\Scripts\activate.bat

---

## 2. Inicialización del Repositorio Local (Git)

Una vez estructurado el proyecto `gestor-tiempo` con su archivo principal `app_tiempo.py`, se procedió a configurar Git localmente.

* **Paso 1:** Abrir la terminal integrada en VS Code y verificar que el entorno virtual esté activo (`(entorno310)` al inicio de la línea).
* **Paso 2:** Inicializar el repositorio Git dentro de la carpeta del proyecto:
  ```cmd
  git init
  ```
* **Paso 3:** Configurar la identidad del usuario en Git (necesaria la primera vez en el equipo):
  ```cmd
  git config --global user.email "tu_correo@example.com"
  git config --global user.name "TuNombre"
  ```
* **Paso 4:** Agregar los archivos del proyecto al área de preparación (*staging area*):
  ```cmd
  git add .
  ```
* **Paso 5:** Realizar el primer commit local (*commit inicial*):
  ```cmd
  git commit -m "Commit inicial: aplicacion de tiempo con vistas V1, V2 y V3"
  ```

---

## 3. Vinculación y Subida a GitHub (Repositorio Remoto)

Para respaldar el código en la nube y habilitar el trabajo colaborativo con herramientas como Copilot, se conectó el repositorio local con GitHub.

* **Paso 1:** Crear un repositorio vacío en [GitHub](https://github.com/) (sin marcar opciones de README ni `.gitignore`).
* **Paso 2:** Vincular el repositorio local con la URL remota proporcionada por GitHub:
  ```cmd
  git remote add origin https://github.com/TU_USUARIO/gestor-tiempo.git
  ```
* **Paso 3:** Asegurar que la rama principal se denomine `main`:
  ```cmd
  git branch -M main
  ```
* **Paso 4:** Enviar los cambios por primera vez utilizando el parámetro `-u` para establecer el seguimiento (*tracking*):
  ```cmd
  git push -u origin main
  ```
* **Paso 5:** Autorizar el acceso en la ventana emergente del navegador haciendo clic en **"Sign in with your browser"**.

---

## 4. Flujo Diario para Futuros Proyectos o Cambios

Una vez completada esta configuración inicial, el flujo de trabajo diario se simplifica considerablemente:

1. **Crear carpeta y abrir en VS Code:** La terminal activará el entorno automáticamente gracias a la configuración global de usuario.
2. **Guardar cambios y preparar:**
   ```cmd
   git add .
   ```
3. **Guardar localmente (Commit):**
   ```cmd
   git commit -m "Descripción de los cambios realizados"
   ```
4. **Enviar a la nube (Push):** Como la rama ya está vinculada, solo se requiere:
   ```cmd
   git push
   ```

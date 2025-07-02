# IVACOL

IVACOL es una aplicación web desarrollada en Django para la gestión y control del estado de declaración del IVA en Colombia. Permite a los usuarios registrar, consultar y administrar facturas, así como visualizar estadísticas, reportes en PDF y gestionar usuarios (incluyendo panel de administración)
Caracteristicas:

- Registro y autenticación de usuarios.
- Subida, edición, eliminación y consulta de facturas.
- Generación de reportes PDF de facturas.
- Visualización de gráficas y estadísticas.
- Administración de usuarios (CRUD para administradores).
- Soporte para modo claro/oscuro.
- Protección de datos personales y restablecimiento de contraseña vía email.

1. **Clona el repositorio y navega al directorio del proyecto:**
   ```sh
   git clone https://github.com/tuusuario/ivacol.git
   cd ivacol
   ```

2. **Crea un entorno virtual (opcional pero recomendado):**
   ```sh
   python -m venv venv
   venv\Scripts\activate

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

6. **Ejecuta el servidor:**
   ```sh
   python manage.py runserver --insecure
   ```

7. **Accede a la aplicación:**
   - Sitio principal: [http://localhost:8000/](http://localhost:8000/)


## Licencia

Este proyecto es propiedad de IVACOL S.A.S. Todos los derechos reservados.

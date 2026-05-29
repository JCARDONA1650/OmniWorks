# OmniWorks — Guía de Usuario
**OnmiTek Solutions**  
**Versión:** 1.0 · 2026  
**Acceso:** `http://localhost:4200`

---

## Contenido

1. [Acceso al sistema](#1-acceso-al-sistema)
2. [Panel principal — Dashboard](#2-panel-principal--dashboard)
3. [Transcripción de Reuniones](#3-transcripción-de-reuniones)
4. [Generador de Documentos](#4-generador-de-documentos)
5. [Envíos Corporativos](#5-envíos-corporativos)
6. [Gestión de Usuarios (Administrador)](#6-gestión-de-usuarios-administrador)
7. [Preguntas frecuentes](#7-preguntas-frecuentes)

---

## 1. Acceso al sistema

### Cómo iniciar sesión

1. Abre el navegador y ve a `http://localhost:4200`
2. Verás la pantalla de login de OmniWorks
3. Ingresa tu correo y contraseña
4. Haz clic en **Iniciar sesión**

**Credenciales del administrador inicial:**
```
Correo:     admin@omniteksolutions.com
Contraseña: Admin2026!
```

> Si el botón muestra "Iniciando sesión..." y no avanza, verifica que el servidor backend esté corriendo en el puerto 8001.

### Cómo cerrar sesión

- En la barra lateral izquierda, al fondo, haz clic en el ícono de salida (flecha hacia la derecha) junto a tu nombre.

---

## 2. Panel principal — Dashboard

Después de iniciar sesión llegarás al **Dashboard** — el centro de control de OmniWorks.

### Qué verás

- **Saludo personalizado** con tu nombre (Buenos días / Buenas tardes / Buenas noches según la hora)
- **Cards de módulos** — acceso rápido a cada herramienta habilitada para tu cuenta
- **Sección Administración** (solo si eres admin) — acceso directo a la gestión de usuarios

### Cómo navegar a un módulo

1. Haz clic en la card del módulo que deseas usar
2. O usa la **barra lateral izquierda** — los módulos aparecen listados con ícono y nombre

### Barra lateral (Sidebar)

La barra lateral siempre está visible y contiene:

| Elemento | Descripción |
|----------|-------------|
| Logo OmniWorks | Regresa al dashboard |
| Inicio | Panel principal |
| Usuarios | Gestión de usuarios (solo admin) |
| Módulos | Links a cada módulo activo |
| Tu avatar | Muestra tus iniciales y rol |
| Botón salir | Cierra la sesión |

---

## 3. Transcripción de Reuniones

Accede desde el dashboard o la barra lateral → **Notas** (`/notes`)

### ¿Para qué sirve?

Esta herramienta graba el audio de una reunión en tiempo real, convierte la voz en texto y puede estructurar automáticamente ese texto en un informe con objetivos, temas tratados y compromisos. Todo funciona en el navegador, sin servicios externos.

> **Navegador requerido:** Google Chrome o Microsoft Edge. Firefox no soporta reconocimiento de voz.

---

### Cómo grabar una reunión

1. Haz clic en **"Iniciar grabación"**
2. El navegador pedirá permiso para usar el micrófono — haz clic en **Permitir**
3. Habla con claridad en español — el texto aparece en pantalla en tiempo real:
   - **Texto negro** = palabras ya confirmadas
   - **Texto gris en cursiva** = palabras que se están procesando
4. Cuando la reunión termine, haz clic en **"Detener grabación"**
5. El timer en rojo muestra el tiempo transcurrido: `⏺ 00:34`

> El sistema retoma automáticamente si el navegador pausa la grabación (ocurre cada ~60 segundos en Chrome).

---

### Filtro de lenguaje inapropiado

Las groserías son reemplazadas automáticamente por `***` en el momento en que se detectan.

---

### Exportar la transcripción

Haz clic en **"Exportar TXT"** para descargar el texto completo como archivo `.txt`.

---

### Generar Informe de Reunión

1. Con la transcripción lista, haz clic en **"Generar Informe"**
2. El sistema analiza el texto usando reglas locales (sin conexión a internet adicional)
3. Se muestra el panel **"Informe de Reunión"** con 4 secciones:

| Sección | Qué contiene |
|---------|-------------|
| **Objetivos** | Oraciones que mencionan metas, propósitos o la razón de la reunión |
| **Compromisos y Acuerdos** | Oraciones con tareas asignadas, pendientes o fechas comprometidas |
| **Temas Tratados** | Todo lo demás discutido durante la reunión |
| **Resumen Ejecutivo** | Un párrafo breve con los puntos más relevantes |

---

### Exportar el Informe

Haz clic en **"Exportar Informe"** para descargar el informe estructurado como `.txt`.

---

### Limpiar y empezar de nuevo

Haz clic en **"Limpiar"** para borrar la transcripción actual. Si hay grabación activa, se detiene automáticamente.

---

## 4. Generador de Documentos

Accede desde el dashboard → **Generador de Documentos** (`/doc-generator`)

### ¿Qué hace?

Permite crear documentos Word (.docx) en masa usando una plantilla con variables dinámicas. Ideal para:
- Certificados laborales
- Contratos
- Cartas personalizadas
- Paz y salvos
- Constancias

---

### Paso 1: Preparar la plantilla Word

En Microsoft Word, crea tu documento con variables entre llaves dobles:

```
Bogotá, {{fecha}}

Señor(a): {{nombre}}
Identificación: {{cedula}}
Cargo: {{cargo}}

La empresa {{empresa}} certifica que el colaborador mencionado
ha trabajado con nosotros desde {{fecha_ingreso}}.

Atentamente,
{{firmante}}
```

Guarda el archivo como `.docx`.

---

### Paso 2: Subir la plantilla

1. En la pantalla del Generador, haz clic en **"Nueva plantilla"**
2. Escribe un nombre descriptivo, ej: `Certificado Laboral 2026`
3. Arrastra tu archivo `.docx` al área marcada, o haz clic para seleccionarlo
4. Haz clic en **"Subir plantilla"**
5. El sistema detecta automáticamente las variables: `nombre`, `cedula`, `cargo`, etc.
6. Verás la plantilla en el grid con sus variables listadas como chips celestes

---

### Paso 3a: Generar un documento individual

1. Haz clic sobre la plantilla que deseas usar
2. Selecciona el modo **"Manual"**
3. Verás un campo de texto por cada variable detectada:
   ```
   {{nombre}}        → Juan Carlos Pérez
   {{cedula}}        → 1234567890
   {{cargo}}         → Analista de Sistemas
   {{empresa}}       → OnmiTek Solutions
   {{fecha}}         → 29 de mayo de 2026
   {{fecha_ingreso}} → 15 de enero de 2024
   {{firmante}}      → María López, Gerente RRHH
   ```
4. El panel derecho muestra las variables con el valor que asignaste (preview en tiempo real)
5. Haz clic en **"Generar DOCX"**
6. El documento se descarga automáticamente en tu equipo

---

### Paso 3b: Generación masiva desde Excel

1. Prepara un archivo Excel donde la **primera fila** son los nombres de las variables:

   | nombre | cedula | cargo | empresa | fecha |
   |--------|--------|-------|---------|-------|
   | Juan Pérez | 1234567890 | Analista | OnmiTek | 29/05/2026 |
   | María López | 9876543210 | Coordinadora | OnmiTek | 29/05/2026 |
   | Carlos Ruiz | 5555555555 | Desarrollador | OnmiTek | 29/05/2026 |

2. En el generador, selecciona la plantilla
3. Cambia el modo a **"Desde Excel"**
4. Arrastra o selecciona tu archivo `.xlsx`
5. Verás una previsualización de los primeros 5 registros
6. Haz clic en **"Generación masiva → ZIP"**
7. Se descarga un archivo `.zip` con un documento Word por cada fila

---

### Historial de generaciones

Haz clic en **"Historial"** para ver todas las generaciones anteriores:
- Nombre de la operación
- Plantilla usada
- Estado (Completado / Error)
- Cantidad de documentos generados
- Fecha

---

## 5. Envíos Corporativos

Accede desde el dashboard → **Envíos Corporativos** (`/email-campaigns`)

El módulo tiene 3 secciones accesibles por tabs en la parte superior.

---

### Tab: SMTP — Configurar el servidor de correo

Antes de enviar cualquier campaña, debes configurar un servidor SMTP.

1. Ve a la tab **SMTP**
2. Haz clic en el formulario de la izquierda:
   ```
   Nombre:             Gmail OnmiTek
   Host SMTP:          smtp.gmail.com
   Puerto:             587
   TLS:                ✓ (marcado)
   Usuario:            correo@empresa.com
   Contraseña:         tu-contraseña-de-app
   Nombre remitente:   OnmiTek Solutions
   Email remitente:    no-reply@onmiteksolutions.com
   ```
3. Haz clic en **"Guardar"**
4. Para verificar que funciona, haz clic en **"Test"** — el sistema enviará un correo de prueba a tu cuenta

> Para Gmail, usa una **contraseña de aplicación** (no la contraseña normal). Ve a tu cuenta Google → Seguridad → Contraseñas de aplicación.

---

### Tab: Plantillas — Crear la plantilla del correo

1. Ve a la tab **Plantillas**
2. Completa el formulario:
   ```
   Nombre:   Newsletter mayo 2026
   Asunto:   {{nombre}}, tenemos novedades para ti
   
   Cuerpo HTML:
   <h2>Hola {{nombre}},</h2>
   <p>Esperamos que estés muy bien.</p>
   <p>Este mes en <strong>{{empresa}}</strong> tenemos:</p>
   <ul>
     <li>Nuevos productos disponibles</li>
     <li>Descuentos especiales</li>
   </ul>
   <p>Saludos,<br>El equipo de {{empresa}}</p>
   ```
3. Haz clic en **"Crear plantilla"**
4. Las variables detectadas (`nombre`, `empresa`) aparecen como chips en la lista

---

### Tab: Campañas — Crear y enviar

#### Crear la campaña

1. Haz clic en **"Nueva campaña"**
2. Completa la configuración:
   ```
   Nombre de la campaña:  Newsletter Mayo 2026
   Plantilla de correo:   Newsletter mayo 2026  (la que creaste)
   Configuración SMTP:    Gmail OnmiTek          (la que configuraste)
   Correos por lote:      10
   Pausa entre lotes:     5 segundos
   ```
3. Haz clic en **"Crear campaña"**
4. La campaña aparece en la tabla con estado **"Borrador"**

> **Lotes y pausas:** Si configuras 10 correos por lote y 5 segundos de pausa, el sistema envía 10 correos, espera 5 segundos, envía otros 10, y así sucesivamente. Esto previene que tu servidor SMTP te bloquee por envíos masivos.

---

#### Importar destinatarios

1. Haz clic sobre la campaña en la tabla para abrir el **panel de envío**
2. Verás la sección de importación (la campaña está en estado "Borrador" o "Lista")
3. Tienes dos modos:

**Modo Excel:**
```
Columna email: email   ← nombre de la columna en tu Excel

Tu Excel debe tener estas columnas:
| email                    | nombre       | empresa     |
|--------------------------|--------------|-------------|
| juan@empresa.com         | Juan Pérez   | OnmiTek     |
| maria@empresa.com        | María López  | OnmiTek     |
| carlos@empresa.com       | Carlos Ruiz  | OnmiTek     |
```

Selecciona tu archivo Excel y haz clic en **"Importar destinatarios"**.

**Modo Manual:**
```
Escribe un email por línea:
juan@empresa.com
maria@empresa.com
carlos@empresa.com
```
Haz clic en **"Importar destinatarios"**.

4. Verás la confirmación: `3 destinatarios importados.`
5. El estado de la campaña cambia a **"Lista"**

---

#### Iniciar el envío

1. Con la campaña en estado **"Lista"**, haz clic en **"Iniciar envío"**
2. El estado cambia a **"Enviando"** y verás:
   - **Barra de progreso** animada que avanza con cada correo enviado
   - **Contadores** en tiempo real: Total / Enviados / Errores / Pendientes
   - **Registro de envíos** — log en tiempo real con cada correo:
     ```
     ✓ Enviado a juan@empresa.com
     ✓ Enviado a maria@empresa.com
     ✗ Error en carlos@empresa.com: Connection refused
     ```

---

#### Controles durante el envío

| Botón | Efecto |
|-------|--------|
| **Pausar** | Detiene el envío al terminar el lote actual. Puedes reanudarlo. |
| **Reanudar** | Continúa desde donde se detuvo |
| **Detener** | Para el envío permanentemente (quedan pendientes sin enviar) |

---

#### Exportar resultados

Cuando la campaña se completa (estado **"Completada"**):
1. Aparece el botón **"Exportar resultados Excel"**
2. Haz clic para descargar un Excel con el estado de cada destinatario:
   - Email
   - Estado (Enviado / Error / Pendiente)
   - Fecha y hora de envío
   - Mensaje de error (si aplica)

---

## 6. Gestión de Usuarios (Administrador)

Accede desde el dashboard → **Usuarios** en la barra lateral, o desde la sección de administración en el dashboard. Solo visible para cuentas con rol **Administrador**.

URL: `/admin/users`

---

### Ver todos los usuarios

La pantalla muestra una tabla con todos los usuarios del sistema:
- Avatar con iniciales
- Nombre completo y email
- Rol (Administrador / Usuario)
- Estado activo/inactivo con toggle
- Fecha de registro
- Botones de acción

---

### Buscar y filtrar usuarios

**Búsqueda:** Escribe en el campo de búsqueda — filtra por nombre, email o username en tiempo real.

**Por rol:**
- `Todos` — muestra todos
- `Admins` — solo administradores
- `Usuarios` — solo usuarios regulares

**Por estado:**
- `Todos` — activos e inactivos
- `Activos` — solo cuentas activas
- `Inactivos` — solo cuentas desactivadas

---

### Crear un nuevo usuario

1. Haz clic en **"Nuevo usuario"** (botón azul, esquina superior derecha)
2. Completa el formulario:
   ```
   Nombre:              Ana
   Apellido:            Martínez
   Correo electrónico:  ana.martinez@empresa.com
   Nombre de usuario:   anamartinez
   Rol:                 Usuario  (o Administrador)
   Contraseña:          MiClave2026!
   Confirmar:           MiClave2026!
   ```
3. Haz clic en **"Crear usuario"**
4. El nuevo usuario aparece al inicio de la tabla y ya puede iniciar sesión

---

### Editar un usuario

1. En la fila del usuario, haz clic en el ícono de lápiz (editar)
2. Modifica los campos necesarios:
   - Nombre, apellido, username
   - Cambiar el rol de Usuario a Administrador (o viceversa)
   - Activar/desactivar la cuenta
3. Haz clic en **"Guardar cambios"**

---

### Cambiar la contraseña de un usuario

1. En la fila del usuario, haz clic en el ícono de candado
2. Escribe la nueva contraseña (mínimo 8 caracteres)
3. Confirma la contraseña
4. Haz clic en **"Actualizar contraseña"**
5. Aparece el mensaje: `Contraseña actualizada correctamente.` y el modal se cierra solo

> El usuario no recibe notificación automática. Comunica la nueva contraseña por otro medio.

---

### Activar o desactivar un usuario

**Desde la tabla (forma rápida):**
- Haz clic directamente en el badge de estado (`Activo` / `Inactivo`) de cualquier usuario
- El cambio aplica inmediatamente sin confirmación

> No puedes desactivar tu propia cuenta desde esta pantalla.

**Desde el modal de edición:**
- Abre el modal de editar → desmarca la casilla "Cuenta activa" → guardar

---

### Gestionar permisos de módulos

Los administradores ven todos los módulos automáticamente. Para usuarios regulares:

1. En la fila del usuario, haz clic en el ícono de grilla (4 cuadros)
2. Se abre el panel de permisos con todos los módulos disponibles:
   ```
   Envíos Corporativos   [●  activado]
   Notas                 [●  activado]
   Generador de Docs     [○  desactivado]
   ```
3. Usa el **toggle switch** para activar o desactivar cada módulo
4. Los cambios aplican de inmediato — no hay botón de guardar
5. Haz clic en **"Listo"** para cerrar el panel

Cuando ese usuario inicie sesión, solo verá los módulos que tiene habilitados en su dashboard y barra lateral.

---

## 7. Preguntas frecuentes

**¿El login gira y no entra?**
Verifica que el backend esté corriendo:
```bash
cd backend
python manage.py runserver 8001
```
Si el frontend está en un puerto diferente al 4200, el CORS está configurado para aceptar cualquier puerto de localhost.

**¿La transcripción se guarda automáticamente?**
No. La transcripción vive en el navegador durante la sesión. Para conservarla, usa **"Exportar TXT"** antes de cerrar o navegar a otra página.

**¿Por qué no funciona el micrófono?**
- Verifica que estés usando Google Chrome o Microsoft Edge
- El navegador pedirá permiso la primera vez — haz clic en **Permitir**
- En configuración del navegador, verifica que el sitio `localhost:4200` tiene permiso de micrófono

**¿El generador de informes es IA conectada a internet?**
No. El análisis del texto se hace completamente en el navegador, sin enviar datos a ningún servidor externo. Funciona offline.

**¿Cuántos destinatarios puedo enviar por campaña?**
No hay límite técnico en el sistema. El límite real lo impone tu servidor SMTP. Para Gmail, el límite es ~500 por día en cuentas personales y mayor en Google Workspace.

**¿Qué pasa si hay un error de envío?**
El destinatario queda marcado como **"Error"** con el mensaje exacto del problema. Los demás destinatarios continúan el proceso. Puedes ver todos los errores en el registro de envíos y exportarlos en Excel.

**¿Cómo agrego más variables a una plantilla del generador?**
Edita tu archivo Word para agregar `{{nueva_variable}}` y vuelve a subir la plantilla. El sistema detectará las nuevas variables automáticamente.

---

*OmniWorks — OnmiTek Solutions · info@onmiteksolutions.com*

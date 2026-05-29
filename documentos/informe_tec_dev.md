# OmniWorks — Informe Técnico de Desarrollo
**Empresa:** OnmiTek Solutions  
**Proyecto:** OmniWorks — Suite Empresarial Modular  
**Ruta base:** `C:\Users\JC\Desktop\Proyectos_Onmitek`

---

## CÓMO CORRER EL APLICATIVO

### Paso 1 — Activar el entorno virtual (Backend)

Abrir terminal en la carpeta `backend`:

```bash
cd C:\Users\JC\Desktop\Proyectos_Onmitek\backend

# Activar entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1

# Activar entorno virtual (CMD)
venv\Scripts\activate.bat

# Activar entorno virtual (Git Bash)
source venv/Scripts/activate
```

Una vez activo, verás `(venv)` al inicio del prompt.

---

### Paso 2 — Aplicar migraciones (solo si hay cambios en modelos)

```bash
# Crear archivos de migración
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate
```

---

### Paso 3 — Levantar el servidor Backend

> **IMPORTANTE:** OmniWorks usa el puerto **8001** porque el 8000 está reservado para otro proyecto en este equipo.

```bash
cd C:\Users\JC\Desktop\Proyectos_Onmitek\backend

# Con entorno virtual activado:
python manage.py runserver 8001

# Sin activar el venv (alternativa):
venv\Scripts\python.exe manage.py runserver 8001
```

El backend quedará disponible en: `http://localhost:8001`

---

### Paso 4 — Levantar el servidor Frontend

Abrir **otra terminal**:

```bash
cd C:\Users\JC\Desktop\Proyectos_Onmitek\omniworks-ui

# Servidor de desarrollo Angular
npx @angular/cli serve --port 4200

# Alternativa si Angular CLI está instalado globalmente:
ng serve --port 4200
```

El frontend quedará disponible en: `http://localhost:4200`
El frontend quedará disponible en: `http://localhost:'
---

### Credenciales de acceso (desarrollo)

| Campo    | Valor                          |
|----------|-------------------------------|
| Email    | admin@omniteksolutions.com     |
| Password | Admin2026!                    |
| Rol      | Administrador                 |

---

### Comandos de utilidad

```bash
# Crear superusuario admin automáticamente
python manage.py create_admin

# Cargar módulos iniciales en la BD
python manage.py seed_modules

# Crear superusuario manualmente
python manage.py createsuperuser

# Ver panel de administración Django
# http://localhost:8001/django-admin/

# Instalar dependencias del backend
pip install -r requirements.txt

# Instalar dependencias del frontend
cd omniworks-ui && npm install
```

---

---

## GUÍA METODOLÓGICA DE DESARROLLO

---

## ARQUITECTURA GENERAL

```
Proyectos_Onmitek/
├── backend/                    ← Django + DRF (API REST)
│   ├── venv/                   ← Entorno virtual Python 3.12.3
│   ├── apps/
│   │   ├── users/              ← Autenticación, usuarios, roles
│   │   └── core/               ← Módulos, permisos por módulo
│   ├── omniworks/
│   │   ├── settings/
│   │   │   ├── base.py         ← Configuración base compartida
│   │   │   └── local.py        ← Configuración local (SQLite, CORS, DEBUG)
│   │   ├── urls.py             ← Enrutador principal (/api/ prefix)
│   │   └── wsgi.py
│   ├── manage.py
│   ├── .env                    ← Variables de entorno (SECRET_KEY, etc.)
│   └── requirements.txt
│
├── omniworks-ui/               ← Angular 21 (Frontend SPA)
│   └── src/
│       ├── app/
│       │   ├── core/           ← Servicios, guards, interceptors, modelos
│       │   ├── auth/           ← Login
│       │   ├── layout/         ← Shell, Sidebar, Topbar
│       │   ├── dashboard/      ← Página principal
│       │   └── admin/          ← Gestión de usuarios (pendiente)
│       ├── environments/       ← URLs de API por entorno
│       └── styles.scss         ← Design system global (variables CSS)
│
└── documentos/                 ← Este archivo y bitácora
```

---

## STACK TECNOLÓGICO

| Capa       | Tecnología                  | Versión   |
|------------|-----------------------------|-----------|
| Backend    | Python                      | 3.12.3    |
| Backend    | Django                      | 6.0.5     |
| Backend    | Django REST Framework       | 3.17.1    |
| Backend    | SimpleJWT                   | 5.5.1     |
| Backend    | django-cors-headers         | 4.9.0     |
| Backend    | python-dotenv               | 1.2.2     |
| Backend    | Pillow                      | 12.2.0    |
| Frontend   | Angular                     | 21.2.7    |
| Frontend   | Node.js                     | 22.15.1   |
| Base datos | SQLite (local) → PostgreSQL | —         |

---

## BACKEND — DESARROLLO DETALLADO

### Modelo de usuarios (`apps/users/models.py`)

Se creó un `CustomUser` que extiende `AbstractUser` de Django con:
- Login por **email** (no por username)
- Campo `role` con opciones: `admin` / `user`
- Campo `avatar` para foto de perfil
- Propiedad calculada `is_admin`

```python
AUTH_USER_MODEL = 'users.User'
```

### Autenticación JWT

- Se usa `djangorestframework-simplejwt`
- **Access token:** 15 minutos de vida
- **Refresh token:** 7 días de vida
- **Blacklist:** al hacer logout el refresh token se invalida
- El login retorna: `{ access, refresh, user: {...datos completos} }`

### Endpoints del API

| Método | Endpoint                         | Acceso    | Descripción                        |
|--------|----------------------------------|-----------|------------------------------------|
| POST   | `/api/auth/login/`               | Público   | Login → tokens + datos usuario     |
| POST   | `/api/auth/logout/`              | Auth      | Invalida el refresh token          |
| POST   | `/api/auth/refresh/`             | Público   | Renueva el access token            |
| GET    | `/api/auth/me/`                  | Auth      | Perfil del usuario autenticado     |
| PATCH  | `/api/auth/me/`                  | Auth      | Actualizar perfil propio           |
| GET    | `/api/users/`                    | Admin     | Listar todos los usuarios          |
| POST   | `/api/users/`                    | Admin     | Crear nuevo usuario                |
| GET    | `/api/users/:id/`                | Admin     | Detalle de un usuario              |
| PATCH  | `/api/users/:id/`                | Admin     | Editar usuario                     |
| DELETE | `/api/users/:id/`                | Admin     | Desactivar usuario (soft delete)   |
| POST   | `/api/users/:id/change-password/`| Admin     | Cambiar contraseña de usuario      |
| GET    | `/api/modules/`                  | Auth      | Módulos habilitados para el usuario|
| GET    | `/api/admin/users/:id/modules/`  | Admin     | Ver permisos de módulos del usuario|
| POST   | `/api/admin/users/:id/modules/`  | Admin     | Habilitar/deshabilitar módulo      |

### Sistema de módulos (`apps/core/`)

- Tabla `Module`: define cada módulo del sistema (key, nombre, ruta, ícono)
- Tabla `ModulePermission`: relación usuario ↔ módulo con `is_enabled`
- Los **admins** ven todos los módulos activos automáticamente
- Los **usuarios regulares** solo ven los módulos que el admin les habilitó

### Comandos de gestión personalizados

- `python manage.py create_admin` → crea el usuario administrador inicial
- `python manage.py seed_modules` → carga los módulos en la base de datos

### Configuración de settings dividida

Se usa `settings/base.py` + `settings/local.py` para separar configuración compartida de configuración local. En producción se crearía `settings/production.py`.

---

## FRONTEND — DESARROLLO DETALLADO

### Design System (`src/styles.scss`)

Se implementó un sistema de diseño completo con variables CSS:
- **Paleta:** negro (`#050a12`), azul oscuro (`#0c1424`), azul primario (`#1e6fff`), celeste (`#38bdf8`)
- **Componentes globales:** `.btn`, `.card`, `.form-group`, `.badge`, `.page`, `.spinner`
- **Animación:** `fadeIn` para entradas de página
- **Scrollbar** personalizado

### Autenticación en Angular

**`AuthService`** — Gestiona el estado de autenticación:
- Almacena tokens en `localStorage`
- Expone `currentUser$` (Observable) para reactividad
- Métodos: `login()`, `logout()`, `refreshToken()`

**`AuthInterceptor`** — Interceptor HTTP:
- Agrega `Authorization: Bearer <token>` a todas las peticiones
- Si recibe 401, intenta renovar el token automáticamente con el refresh token
- Si el refresh también falla, hace logout y redirige al login
- **Corrección Fase 7:** Se resolvió un deadlock donde múltiples peticiones con 401 simultáneo podían quedar bloqueadas indefinidamente si el refresh fallaba. Se usa `BehaviorSubject<string|null|false>` donde `false` señala fallo y desbloquea todas las peticiones en cola

**Guards:**
- `AuthGuard` — bloquea rutas privadas si no está autenticado
- `GuestGuard` — redirige al dashboard si ya está autenticado (evita ver login de nuevo)

### Estructura de rutas

```
/login             → LoginComponent         (GuestGuard)
/                  → ShellComponent         (AuthGuard)
  /home            → DashboardComponent
  /notes           → VoiceNotesComponent    (Transcripción por voz)
  /doc-generator   → DocGeneratorComponent
  /email-campaigns → CampaignsMainComponent
  /admin/users     → AdminUsersComponent    (AdminGuard)
```

### Componentes creados

| Componente             | Ruta                          | Descripción                                    |
|------------------------|-------------------------------|------------------------------------------------|
| `LoginComponent`       | `auth/login/`                 | Formulario de login con validación reactiva    |
| `ShellComponent`       | `layout/shell/`               | Contenedor principal con sidebar + topbar      |
| `SidebarComponent`     | `layout/sidebar/`             | Navegación lateral con módulos dinámicos       |
| `TopbarComponent`      | `layout/topbar/`              | Barra superior con título y datos de usuario   |
| `DashboardComponent`   | `dashboard/`                  | Cards de módulos + accesos rápidos admin       |
| `VoiceNotesComponent`  | `notes/voice-notes/`          | Transcripción por voz + generador de informes  |
| `DocGeneratorComponent`| `doc-generator/generator/`    | Generador de documentos Word desde plantillas  |
| `CampaignsMainComponent`| `email-campaigns/list/`      | Módulo completo de campañas de email           |
| `AdminUsersComponent`  | `admin/users/`                | Panel de gestión de usuarios (solo admin)      |

### Flujo de módulos en el Frontend

1. Al entrar al dashboard, se llama `GET /api/modules/`
2. Los módulos retornados se renderizan como cards con gradiente
3. La sidebar también consulta los módulos para mostrar links de navegación
4. Si el usuario es admin, se muestra la sección de administración

---

## DECISIONES DE DISEÑO

| Decisión | Razón |
|----------|-------|
| Puerto 8001 para backend | El puerto 8000 está ocupado por otro proyecto en el equipo |
| Settings divididos base/local | Preparación para múltiples entornos sin duplicar config |
| Soft delete en usuarios | Se desactiva con `is_active=False` para no perder histórico |
| Login por email en vez de username | Más empresarial y natural para usuarios corporativos |
| JWT con blacklist | Permite invalidar sesiones al hacer logout correctamente |
| NgModule (no standalone) | El proyecto se generó con `--standalone=false` para compatibilidad |

---

## MÓDULOS IMPLEMENTADOS

| Módulo                     | Key              | Estado       | Notas                            |
|----------------------------|------------------|--------------|----------------------------------|
| Transcripción de Reuniones | notes            | ✅ Completo  | Reemplaza el módulo de notas     |
| Generador de Documentos    | doc_generator    | ✅ Completo  | Word templates + Excel bulk      |
| Envíos Corporativos        | email_campaigns  | ✅ Completo  | SMTP + polling + export Excel    |
| Gestión de Usuarios        | —                | ✅ Completo  | Admin only, ruta /admin/users    |

---

## MÓDULO TRANSCRIPCIÓN — DETALLES TÉCNICOS (Fase 7)

### Tecnología: Web Speech API
- `SpeechRecognition` nativo del navegador (Chrome/Edge)
- Sin dependencias externas — funciona 100% en el cliente
- Configuración: `lang='es-CO'`, `continuous=true`, `interimResults=true`
- Reinicio automático en `onend` para sesiones largas

### Generador de informes local
- Archivo: `omniworks-ui/src/app/core/utils/meeting-report.ts`
- Algoritmo: detección de palabras clave por categoría
  - Objetivos: `objetivo`, `meta`, `proposito`, `vamos a hablar`, `nos reunimos`, etc.
  - Compromisos: `compromiso`, `acuerdo`, `pendiente`, `responsable`, `hay que`, etc.
  - Temas: todo lo demás
- Sin red, sin backend, sin API

### Filtro de groserías
- Archivo: `omniworks-ui/src/app/core/utils/offensive-filter.ts`
- Lista de términos en español, aplicada con regex en `onresult` del recognition
- Las palabras filtradas se reemplazan por `***` antes de acumularse en el transcript

### Backend (notes Django app)
- El app `apps/notes/` permanece en el backend pero no es consumido por el frontend
- El registro del módulo `notes` en BD sigue activo con `route: /notes`

---

*Documento mantenido por el equipo de desarrollo — OnmiTek Solutions*

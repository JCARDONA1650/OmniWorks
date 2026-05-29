# OmniWorks — Bitácora de Desarrollo
**Empresa:** OnmiTek Solutions  
**Proyecto:** OmniWorks — Suite Empresarial Modular

---

## FASE 1 — Backend base
**Fecha:** 2026-05-28  
**Estado:** ✅ Completada

### Qué se hizo

**Estructura del proyecto:**
- Se creó el proyecto Django `omniworks` dentro de `backend/`
- Se configuró `settings/base.py` y `settings/local.py` (settings divididos)
- Se eliminó el `settings.py` generado por defecto
- Se creó archivo `.env` con `SECRET_KEY` y `DJANGO_SETTINGS_MODULE`
- Se generó `requirements.txt` con todas las dependencias

**App `users`:**
- Modelo `User` extendiendo `AbstractUser` con login por email, campo `role` (admin/user) y avatar
- `CustomTokenObtainPairSerializer` — el login retorna tokens + datos completos del usuario
- Serializers: `UserSerializer`, `UserCreateSerializer`, `UserUpdateSerializer`, `ChangePasswordSerializer`
- Views: Login, Logout (blacklist), Me, ListCreate, Detail, ChangePassword
- Permiso personalizado `IsAdminUser`
- URLs bajo prefijo `/api/`

**App `core`:**
- Modelo `Module` con campos: key, nombre, descripción, ícono, ruta, orden, activo
- Modelo `ModulePermission` — relación usuario ↔ módulo con `is_enabled`
- Views: módulos del usuario autenticado, permisos por usuario (admin)
- Comando `seed_modules` — carga módulos iniciales
- Comando `create_admin` — crea usuario administrador

**Base de datos:**
- Se aplicaron todas las migraciones (SQLite local)
- Se crearon 2 módulos: Envíos Corporativos y Notas
- Se creó el admin inicial: `admin@omniteksolutions.com` / `Admin2026!`

**Paquetes instalados (ya estaban en venv):**
- Django 6.0.5, DRF 3.17.1, SimpleJWT 5.5.1, CORS Headers 4.9.0, Pillow 12.2.0, python-dotenv 1.2.2

---

## FASE 2 — Frontend Angular (Login, Layout, Dashboard)
**Fecha:** 2026-05-28  
**Estado:** ✅ Completada

### Qué se hizo

**Proyecto Angular:**
- Se creó el proyecto `omniworks-ui` con Angular CLI 21.2.7
- Flags: `--routing=true --style=scss --skip-git=true --standalone=false`
- Se instaló `@angular/cdk`
- Se definió `environment.ts` con `apiUrl: http://localhost:8001/api`

> Nota: El backend usa el puerto **8001** porque el 8000 está ocupado por otro proyecto del equipo.

**Design System (`styles.scss`):**
- Variables CSS para toda la paleta de colores (negro, azul oscuro, azul primario, celeste)
- Componentes globales: `.btn`, `.card`, `.form-group`, `.badge`, `.page`, `.spinner`
- Animación `fadeIn` para entradas de página
- Scrollbar personalizado

**Core — Servicios y guardias:**
- `AuthService` — login, logout, refresh, almacenamiento de tokens en localStorage, `currentUser$`
- `ModulesService` — consulta los módulos disponibles del usuario
- `AuthInterceptor` — agrega JWT en cada request + renovación silenciosa en 401
- `AuthGuard` — protege rutas privadas
- `GuestGuard` — redirige al dashboard si ya está logueado

**Componentes creados:**
- `LoginComponent` — formulario reactivo, validaciones, toggle mostrar/ocultar contraseña, diseño premium con grid y glows de fondo
- `ShellComponent` — contenedor layout con sidebar + topbar + footer + `<router-outlet>`
- `SidebarComponent` — navegación lateral fija, módulos dinámicos desde el API, avatar con iniciales, badge de rol, logout
- `TopbarComponent` — barra superior con título dinámico según ruta y datos del usuario
- `DashboardComponent` — cards de módulos con gradientes únicos, acceso rápido a administración para admins

**Routing:**
- `/login` → LoginComponent (GuestGuard)
- `/home` → DashboardComponent dentro de ShellComponent (AuthGuard)
- Redirección `**` → `/home`

**Email de contacto corregido:** `info@onmiteksolutions.com`

**Build exitoso:** `Application bundle generation complete`  
**API verificada:** Login, tokens JWT y endpoint de módulos respondiendo correctamente en `http://localhost:8001`

---

---

## FASE 3 — Módulo de Notas
**Fecha:** 2026-05-28  
**Estado:** ✅ Completada

### Qué se hizo

**Backend — App `notes`:**
- Modelos creados: `NoteCategory` (categorías por usuario), `Note` (nota con tipo quick/report, pin, soft delete, detección ofensiva), `NoteHistory` (historial de versiones, máx 20 por nota)
- `offensive.py` — detector de lenguaje inapropiado basado en lista de palabras clave en español
- Serializers: `NoteListSerializer` (preview), `NoteSerializer` (completo), `NoteCreateSerializer`, `NoteUpdateSerializer`, `NoteCategorySerializer`, `NoteHistorySerializer`
- Cada serializer valida automáticamente el contenido y actualiza el flag `has_offensive_content`
- Views: CRUD de notas y categorías, filtros (búsqueda, tipo, categoría, fijadas), historial, restaurar versión, papelera, toggle pin
- Historial guarda la versión anterior automáticamente antes de cada edición
- URLs bajo prefijo `/api/notes/`
- Admin Django con listados y filtros para las 3 tablas
- Migración aplicada correctamente

**Endpoints nuevos:**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET/POST | `/api/notes/` | Listar (con filtros) / Crear nota |
| GET/PATCH/DELETE | `/api/notes/:id/` | Detalle / Editar / Eliminar (soft) |
| POST | `/api/notes/:id/pin/` | Toggle fijar/desfijar |
| GET | `/api/notes/:id/history/` | Historial de versiones |
| POST | `/api/notes/:id/history/:hid/restore/` | Restaurar versión |
| GET | `/api/notes/trash/` | Papelera |
| POST | `/api/notes/:id/restore/` | Restaurar desde papelera |
| GET/POST | `/api/notes/categories/` | Categorías del usuario |
| GET/PATCH/DELETE | `/api/notes/categories/:id/` | Detalle categoría |

**Frontend Angular:**
- Modelo `Note`, `NoteCategory`, `NoteHistory`, `NoteFilters` en `core/models/note.model.ts`
- `NotesService` — todos los métodos del API (categorías, notas, historial, papelera)
- `NotesListComponent` — lista con sidebar de filtros (tipo, categorías, fijadas, papelera), búsqueda con debounce 350ms, grid de cards responsivo, cards con actions (pin, eliminar)
- `NoteEditorComponent` — editor full-screen con:
  - Autosave por debounce de 1500ms
  - Indicador de estado: Editando / Guardando... / ✓ Guardado
  - Toggle tipo quick/report
  - Selector de categoría
  - Panel lateral de historial de versiones con restauración
  - Conteo de palabras y caracteres
  - Alerta visual si detecta lenguaje ofensivo
- Rutas registradas: `/notes` → lista, `/notes/:id` → editor
- `FormsModule` agregado al `AppModule` para `[(ngModel)]` en formulario de categorías
- Build exitoso sin errores

**Verificaciones:**
- API de notas responde correctamente en `http://localhost:8001`
- Detección de lenguaje ofensivo funcional (probado con título que contiene palabra clave)
- Compilación Angular exitosa (1.72 MB bundle)

---

---

## FASE 4 — IA Empresarial en Notas + Generador de Documentos
**Fecha:** 2026-05-28  
**Estado:** ✅ Completada

### Correcciones y mejoras
- **Emoji eliminado** del saludo del dashboard — reemplazado por saludo profesional con punto
- **Views reorganizadas** en todos los apps con carpeta `views/` e `__init__.py`:
  - `apps/users/views/`: `auth.py`, `management.py`
  - `apps/core/views/`: `modules.py`, `permissions.py`
  - `apps/notes/views/`: `categories.py`, `crud.py`, `history.py`, `trash.py`, `ai.py`
  - `apps/doc_generator/views/`: `templates.py`, `generation.py`
- **CORS** actualizado para aceptar cualquier puerto de `localhost` (regex), resolviendo conflicto de puertos entre procesos
- **Bug login** corregido: `loading = false` antes de `router.navigate()`, y mensaje de error cuando el backend no está disponible

### IA Empresarial en Notas
- **`apps/notes/ai_service.py`** — Servicio desacoplado con abstracción de proveedor (`AI_PROVIDER` env var). Soporta Claude; arquitectura lista para otros proveedores
- 6 acciones: Resumir, Mejorar redacción, Convertir a informe, Extraer tareas, Puntos clave, Acta de reunión
- **Modelo `NoteAIResult`** — guarda resultado, acción, tokens usados, proveedor y fecha
- **Endpoints**: `POST /api/notes/:id/ai/process/` y `GET /api/notes/:id/ai/`
- **Frontend — Editor con panel dividido**:
  - Barra de acciones IA con chips seleccionables
  - Toggle vista: Editor / Dividido / Historial IA
  - Panel derecho muestra resultado IA con metadatos (fecha, tokens, proveedor)
  - Botón "Aplicar a la nota" para reemplazar contenido
  - **Exportación**: TXT original, JSON original, TXT(IA), JSON(IA)
- **`NlToBrPipe`** — pipe compartido para renderizar Markdown básico y saltos de línea del resultado IA
- Variables de entorno en `.env`: `ANTHROPIC_API_KEY`, `AI_PROVIDER`, `AI_MODEL`

### Generador de Documentos (nuevo módulo)
**Backend:**
- Nueva app `apps/doc_generator` con modelos `DocumentTemplate` y `DocumentGeneration`
- **`doc_service.py`**: detección de variables `{{var}}`, reemplazo en DOCX preservando formato, generación individual y masiva en ZIP, lectura de Excel con openpyxl
- Dependencias instaladas: `python-docx`, `openpyxl`, `reportlab`
- Endpoints:
  - `GET/POST /api/docs/templates/` — listar y subir plantillas
  - `GET /api/docs/templates/:id/variables/` — variables detectadas
  - `POST /api/docs/templates/:id/generate/` — generar documento único → descarga DOCX
  - `POST /api/docs/templates/:id/bulk/` — generación masiva (Excel o JSON) → descarga ZIP
  - `POST /api/docs/import/preview/` — previsualizar Excel antes de generar
  - `GET /api/docs/generations/` — historial de generaciones

**Frontend:**
- `DocGeneratorComponent` con 3 vistas: plantillas, datos y historial
- **Plantillas**: grid de cards con variables detectadas, chips con cada variable, upload de .docx
- **Datos**: modo manual (campo por variable) y modo Excel (drag & drop, preview de primeras 5 filas)
- **Generación**: individual descarga DOCX, masiva descarga ZIP
- Panel preview muestra variables con el valor que se asignará en tiempo real
- Ruta registrada: `/doc-generator`
- Módulo registrado en BD como `doc_generator`
- `requirements.txt` actualizado

---

---

## FASE 5 — Módulo de Envíos Corporativos
**Fecha:** 2026-05-28  
**Estado:** ✅ Completada

### Backend — `apps/email_campaigns/`
- **Modelos**: `SMTPConfig`, `EmailTemplate`, `EmailCampaign`, `EmailRecipient`, `CampaignLog`
- **`email_service.py`**: envío en thread separado, reemplazo de `{{variables}}` por destinatario, lotes con pausa configurable, manejo de pausa/reanudación/stop con evento threading, logging por cada acción, cierre correcto del backend SMTP
- **Views divididas** en `views/smtp.py`, `views/templates.py`, `views/campaigns.py`, `views/sending.py`
- **Test SMTP**: endpoint que envía correo de prueba al email del usuario autenticado
- **Importación**: Excel (.xlsx) o JSON con detección de campo email configurable
- **Exportación de resultados**: genera Excel con estado de cada destinatario (openpyxl con estilos)
- **Polling de logs**: endpoint `GET /api/campaigns/:id/logs/?since_id=X` para logs incrementales
- 14 endpoints bajo `/api/campaigns/`
- Migración aplicada

### Frontend Angular
- **Modelos**: `SMTPConfig`, `EmailTemplate`, `EmailCampaign`, `EmailRecipient`, `CampaignLog`, `CAMPAIGN_STATUS_LABELS`
- **`EmailCampaignsService`**: 18 métodos cubriendo SMTP, plantillas, campañas, destinatarios, control y exportación
- **`CampaignsMainComponent`**: componente único con 4 vistas via tabs internas:
  - **Campañas**: tabla con progreso visual, estado, contadores y acceso al panel de envío
  - **Nueva campaña**: formulario con plantilla, SMTP, tamaño de lote y delay
  - **Panel de envío**: 4 contadores (total/enviados/errores/pendientes), barra de progreso animada con pulse en ejecución, controles (iniciar/pausar/reanudar/detener/exportar), importación de destinatarios inline, log en tiempo real con colores por nivel
  - **Plantillas**: editor WYSIWYG de texto con soporte de `{{variables}}`, lista con chips de variables
  - **SMTP**: formulario completo con test de conexión, lista de configuraciones
- Polling automático cada 2.5s cuando la campaña está activa (estado + logs nuevos)
- Parada del polling al salir de la vista de envío
- Ruta: `/email-campaigns`
- Build exitoso (1.93 MB)

---

## FASE 6 — Panel de Gestión de Usuarios (Admin)
**Fecha:** 2026-05-29  
**Estado:** ✅ Completada

### Backend (ya existía desde Fase 1)
Endpoints: `GET/POST /api/users/`, `PATCH/DELETE /api/users/:id/`, `POST /api/users/:id/change-password/`, `GET/POST /api/admin/users/:id/modules/`

### Frontend Angular
- **`UsersAdminService`** — listar, crear, actualizar, desactivar, cambiar contraseña, permisos de módulos por usuario
- **`AdminGuard`** — solo admins pueden acceder; redirige a `/home` si no tiene rol admin
- **`AdminUsersComponent`** — panel completo:
  - Tabla con avatar de iniciales, nombre completo, email, rol, toggle activo/inactivo, fecha y botones de acción
  - Filtros: búsqueda en tiempo real, filtro por rol (admin/user/todos), filtro por estado (activo/inactivo/todos)
  - Contadores en header: total / activos / admins
  - **Modal Crear**: grilla de campos, validación de contraseñas coincidentes, feedback de error del API
  - **Modal Editar**: nombre, apellido, username, rol, checkbox activo
  - **Modal Cambiar contraseña**: nueva + confirmación, mensaje de éxito con auto-cierre
  - **Modal Permisos de módulos**: toggle switch individual por módulo; solo visible para usuarios no-admin
  - Protección: no se puede desactivar la propia cuenta
- Ruta `/admin/users` protegida con `AdminGuard` (doble protección: AuthGuard + AdminGuard)
- Build exitoso (2.02 MB)

---

---

## CORRECCIÓN — Interceptor HTTP (Deadlock en refresh de token)
**Fecha:** 2026-05-29
**Estado:** ✅ Corregido

### Problema
Cuando el access token expiraba con múltiples peticiones HTTP en vuelo simultáneamente, el interceptor `AuthInterceptor` quedaba en deadlock:

1. La primera petición con 401 iniciaba el refresh (`isRefreshing = true`) y emitía `null` en `refreshTokenSubject`
2. Las demás peticiones entraban al branch de espera → `filter(token => token !== null)`
3. Si el **refresh fallaba**, el `catchError` solo resolvía la primera petición (lanzando error), pero **nunca emitía un valor en `refreshTokenSubject`**
4. Las peticiones en cola quedaban bloqueadas indefinidamente (el timeout de 15s solo cubría `next.handle()`, no el path de espera)

### Solución
- Cambio de tipo del subject: `BehaviorSubject<string | null>` → `BehaviorSubject<string | null | false>`
- `false` es el nuevo valor de señal de fallo: cuando el refresh falla se emite `false` para desbloquear todas las peticiones en cola
- Las peticiones en cola detectan `false` y retornan `throwError(401)` limpiamente
- Se agregó `/auth/refresh/` a la exclusión del 401 handler para evitar recursión

### Archivos modificados
- `omniworks-ui/src/app/core/interceptors/auth.interceptor.ts`

---

## FASE 7 — Módulo de Transcripción de Reuniones (reemplaza Notas)
**Fecha:** 2026-05-29
**Estado:** ✅ Completada

### Contexto
El módulo de Notas original (editor de texto, categorías, historial, papelera, IA por API) fue reemplazado completamente. La nueva herramienta es una **grabadora de voz con transcripción en tiempo real** orientada a reuniones de trabajo.

### Qué se hizo

**Eliminados:**
- `apps/notes/views/ai.py`, `apps/notes/ai_service.py`, `apps/notes/offensive.py` (no se usan desde el frontend)
- `omniworks-ui/src/app/notes/list/` — `NotesListComponent`
- `omniworks-ui/src/app/notes/editor/` — `NoteEditorComponent`
- `omniworks-ui/src/app/shared/pipes/nl-to-br.pipe.ts` — ya no se usa
- Import `NlToBrPipe` y los dos componentes eliminados del `AppModule`

**Nuevos archivos:**
- `omniworks-ui/src/app/notes/voice-notes/voice-notes.component.ts` — componente principal
- `omniworks-ui/src/app/notes/voice-notes/voice-notes.component.html` — template completo
- `omniworks-ui/src/app/notes/voice-notes/voice-notes.component.scss` — estilos profesionales
- `omniworks-ui/src/app/core/utils/meeting-report.ts` — generador de informes (reglas locales JSON)
- `omniworks-ui/src/app/core/utils/offensive-filter.ts` — filtro de groserías del lado del cliente

**Funcionalidades implementadas:**
- **Grabación por voz** via Web Speech API (`SpeechRecognition` nativo del navegador)
  - Idioma: `es-CO`
  - Reconocimiento continuo (`continuous: true`) con reinicio automático (Chrome se detiene cada ~60s)
  - Resultados intermedios en tiempo real (texto gris cursiva mientras se habla)
  - Resultados finales acumulados en el transcript
- **Filtro de lenguaje inapropiado** — lista de términos en español aplicada en el cliente, las palabras detectadas se reemplazan por `***` antes de añadirse al transcript
- **Exportar TXT** — descarga el transcript completo como archivo `.txt`
- **Generador de informe** — procesamiento local sin IA externa:
  - Divide el transcript en oraciones
  - Clasifica cada oración por palabras clave en tres categorías: Objetivos, Compromisos/Acuerdos, Temas Tratados
  - Genera Resumen Ejecutivo con las primeras oraciones relevantes
  - **Exportar Informe TXT** — descarga el informe formateado como `.txt`
- **Timer** de grabación con pulso animado
- Contador de palabras en tiempo real
- Detección de navegador no compatible (solo Chrome/Edge soportan Web Speech API)

**Rutas actualizadas:**
- `/notes` → `VoiceNotesComponent` (antes apuntaba a `NotesListComponent`)
- Se eliminó la ruta `/notes/:id` (editor de texto)

**Build:** exitoso, 2.02 MB sin errores

### Notas técnicas
- El `notes` Django app en el backend permanece intacto pero ya no es consumido por el frontend
- El módulo `notes` sigue registrado en BD con `route: /notes` — la nueva UI lo usa correctamente
- Web Speech API solo funciona en HTTPS o localhost (cumple con el entorno de desarrollo)
- El generador de informe es completamente offline (no requiere backend ni API)

---

---

## REVISIÓN — Pulido de UX general (post Fase 7)
**Fecha:** 2026-05-29
**Estado:** ✅ Completado

### Problemas identificados y resueltos

**1. Voice Notes — texto desaparecía al parar la grabación**
- Causa: `stopRecording()` limpiaba `interimText` antes de guardarlo, y Chrome no siempre convierte el interim a final al llamar `recognition.stop()`
- Fix: se confirma el `interimText` al transcript inmediatamente antes de detener la sesión
- Archivo: `voice-notes.component.ts`

**2. Generador de informes — no detectaba objetivos ni compromisos**
- Causa: El algoritmo anterior dividía por puntuación (`.!?;`), pero el speech-to-text no genera puntuación → todos los textos quedaban sin separar
- Fix completo: nuevo algoritmo en `meeting-report.ts`:
  - Busca keywords directamente en el texto continuo (sin depender de puntuación)
  - Extrae el contexto alrededor de cada keyword con ventana de 180–200 caracteres
  - Retrocede ~4 palabras para incluir el sujeto antes del keyword de compromiso
  - Para temas: si no hay markers explícitos, divide el texto en bloques de 30 palabras
  - Listas más amplias de keywords en español (incluyendo variantes con/sin tilde)

**3. Navegación — spinner bloqueaba las secciones al entrar al módulo**
- Causa: El campaigns component usaba `forkJoin` esperando los 3 requests simultáneamente → si el más lento tardaba, toda la UI bloqueada
- Fix: se carga `getCampaigns()` primero (más importante para la vista), `getTemplates()` y `getSMTPConfigs()` en paralelo sin bloquear
- Timeout del interceptor reducido de 15s → 8s para fallos más rápidos
- Archivos: `campaigns-main.component.ts`, `auth.interceptor.ts`

**4. Generador de Documentos — sin orientación para el usuario nuevo**
- Se agregó panel de onboarding "¿Cómo funciona?" (3 pasos) que aparece cuando no hay plantillas
- Se agregó sección "Biblioteca de Plantillas" con 5 plantillas de ejemplo descargables:
  - Certificado Laboral
  - Carta de Presentación
  - Paz y Salvo
  - Constancia de Ingresos
  - Invitación a Reunión
- Backend: nueva función `generate_sample_template(key)` en `doc_service.py` que genera .docx con python-docx
- Nuevos endpoints: `GET /api/docs/samples/` y `GET /api/docs/samples/<key>/download/`
- Archivos: `doc_service.py`, `views/templates.py`, `urls.py`, `doc-generator.component.html/.scss/.ts`, `doc-generator.service.ts`

**5. Envíos Corporativos — sin guía de inicio**
- Se agregó panel de onboarding con los 3 pasos recomendados (SMTP → Plantilla → Campaña)
- El panel solo aparece cuando no hay campañas creadas aún
- Archivo: `campaigns-main.component.html/.scss`

---

*Bitácora mantenida por el equipo de desarrollo — OnmiTek Solutions*

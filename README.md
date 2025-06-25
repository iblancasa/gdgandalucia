# GDG Andalucía - Sitio Web

Un sitio web estático de una sola página (SPA) para las comunidades de desarrolladores de Google (GDG) en Andalucía.

## 🎯 Propósito

Este sitio web sirve como página de aterrizaje para representar las comunidades GDG en Andalucía y mostrar una cuadrícula de logos de las diferentes comunidades locales.

## 🚀 Características

- **Diseño Material Design**: Interfaz moderna y limpia siguiendo los principios de Material Design
- **Colores de Andalucía**: Paleta de colores inspirada en la bandera de Andalucía (verde y blanco)
- **Responsive**: Diseño completamente adaptable a todos los dispositivos
- **Accesibilidad**: Cumple con estándares de accesibilidad web
- **Interactividad**: Animaciones suaves y efectos de hover
- **Navegación fluida**: Scroll suave entre secciones
- **Contenido en español**: Todo el contenido está en español
- **Generador dinámico**: Script Python para generar la sección de comunidades desde YAML

## 📁 Estructura del Proyecto

```
gdgandalucia/
├── index.html              # Página principal
├── styles.css              # Estilos CSS
├── script.js               # Funcionalidad JavaScript
├── communities.yaml        # Datos de comunidades en YAML
├── generate_communities.py # Generador de sección de comunidades
├── test_generator.py       # Script de prueba del generador
├── requirements.txt        # Dependencias de Python
└── README.md               # Documentación
```

## 🎨 Diseño

### Colores
- **Verde principal**: `#008751` (Verde de Andalucía)
- **Verde secundario**: `#00a651` (Verde más claro)
- **Verde de acento**: `#4caf50` (Verde Material)
- **Blanco**: `#ffffff`
- **Grises**: Varios tonos para texto y fondos

### Tipografía
- **Fuente principal**: Roboto (Google Fonts)
- **Pesos**: 300 (light), 400 (regular), 500 (medium), 700 (bold)

## 📱 Secciones

### 1. Header
- Logo y título del sitio
- Navegación principal
- Efectos de scroll

### 2. Hero Section
- Mensaje de bienvenida
- Botones de acción
- Fondo con gradiente verde

### 3. Comunidades
- Cuadrícula responsive de tarjetas
- Placeholders para logos de comunidades
- Información de cada comunidad GDG
- Animaciones de entrada
- **Generado dinámicamente desde YAML**

### 4. Eventos (Placeholder)
- Sección preparada para futuros eventos
- ID: `eventos`

### 5. Contacto (Placeholder)
- Sección preparada para información de contacto
- ID: `contacto`

### 6. Footer
- Enlaces de navegación
- Redes sociales
- Información de copyright

## 🔧 Funcionalidades JavaScript

### Navegación
- Scroll suave entre secciones
- Efectos de header al hacer scroll
- Actualización de navegación activa

### Interactividad
- Efectos hover en tarjetas de comunidades
- Animaciones de botones
- Sistema de notificaciones

### Accesibilidad
- Navegación por teclado
- Skip links
- ARIA labels
- Soporte para lectores de pantalla

### Rendimiento
- Debouncing para eventos de scroll
- Lazy loading de animaciones
- Optimizaciones de rendimiento

## 🐍 Generador de Comunidades (Python)

### Descripción
El script `generate_communities.py` permite generar dinámicamente la sección de comunidades desde un archivo YAML, facilitando la gestión y actualización de la información de las comunidades.

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Uso del Generador

#### Comandos Básicos
```bash
# Generar y actualizar la sección de comunidades
python generate_communities.py

# Previsualizar el HTML generado sin actualizar el archivo
python generate_communities.py --preview

# Solo validar los datos YAML
python generate_communities.py --validate-only

# Usar archivos personalizados
python generate_communities.py --yaml-file mi-comunidades.yaml --html-file template.html
```

#### Opciones Disponibles
- `--yaml-file`: Archivo YAML con datos de comunidades (por defecto: `communities.yaml`)
- `--html-file`: Archivo HTML a actualizar (por defecto: `index.html`)
- `--output-file`: Archivo de salida (por defecto: mismo que html-file)
- `--validate-only`: Solo validar datos sin actualizar HTML
- `--preview`: Previsualizar HTML generado

### Estructura del YAML

```yaml
communities:
  - name: "GDG Sevilla"
    slug: "sevilla"
    description: "Comunidad de desarrolladores de Google en Sevilla"
    members: "500+"
    logo_path: "images/gdg-sevilla-logo.png"
    website: "https://gdg.community.dev/gdg-sevilla/"
    social:
      twitter: "@gdgsevilla"
      linkedin: "gdg-sevilla"
      meetup: "gdg-sevilla"
    location: "Sevilla"
    province: "Sevilla"
    active: true
    featured: true

config:
  sort_by: "members"        # Opciones: name, members, location, featured
  sort_order: "desc"        # Opciones: asc, desc
  show_inactive: false      # Mostrar comunidades inactivas
  max_communities: 12       # Máximo número de comunidades
  logo_placeholder: true    # Usar iconos placeholder si no hay logo
```

### Campos Requeridos
- `name`: Nombre de la comunidad
- `slug`: Identificador único
- `description`: Descripción de la comunidad
- `members`: Número de miembros (ej: "500+")

### Campos Opcionales
- `logo_path`: Ruta al logo de la comunidad
- `website`: URL del sitio web de la comunidad
- `social`: Enlaces a redes sociales
- `location`: Ciudad de la comunidad
- `province`: Provincia
- `active`: Si la comunidad está activa
- `featured`: Si es una comunidad destacada

### Pruebas
```bash
# Ejecutar pruebas del generador
python test_generator.py
```

## 🚀 Instalación y Uso

### Requisitos
- Navegador web moderno
- Python 3.7+ (para el generador)
- Servidor web local (opcional, para desarrollo)

### Instalación
1. Clona o descarga el proyecto
2. Instala las dependencias de Python: `pip install -r requirements.txt`
3. Abre `index.html` en tu navegador
4. ¡Listo! El sitio está funcionando

### Desarrollo Local
Para desarrollo con un servidor local:

```bash
# Con Python 3
python -m http.server 8000

# Con Node.js (si tienes http-server instalado)
npx http-server

# Con PHP
php -S localhost:8000
```

Luego visita `http://localhost:8000`

## 📝 Personalización

### Agregar Logos de Comunidades
Para agregar los logos reales de las comunidades:

1. Coloca las imágenes en una carpeta `images/`
2. Actualiza el archivo `communities.yaml` con las rutas correctas
3. Ejecuta el generador: `python generate_communities.py`

### Modificar Colores
Los colores están definidos como variables CSS en `styles.css`:

```css
:root {
    --primary-green: #008751;
    --secondary-green: #00a651;
    /* ... otros colores */
}
```

### Agregar Nuevas Secciones
El código está preparado para extensiones futuras. Cada sección tiene:
- ID único para navegación
- Comentarios descriptivos
- Estructura consistente

### Agregar Nuevas Comunidades
1. Edita el archivo `communities.yaml`
2. Agrega la nueva comunidad con todos los campos requeridos
3. Ejecuta: `python generate_communities.py`

## 🔮 Extensiones Futuras

El sitio está diseñado para ser extensible. Algunas ideas para futuras versiones:

- **Sistema de eventos**: Integración con APIs de eventos
- **Blog**: Sección de noticias y artículos
- **Galería**: Fotos de eventos pasados
- **Formulario de contacto**: Integración con servicios de email
- **PWA**: Funcionalidades de aplicación web progresiva
- **Analytics**: Integración con Google Analytics
- **CMS**: Sistema de gestión de contenido
- **API REST**: Endpoint para obtener datos de comunidades
- **Automatización**: CI/CD para actualización automática

## 🛠️ Tecnologías Utilizadas

- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con variables CSS
- **JavaScript ES6+**: Funcionalidad interactiva
- **Python 3.7+**: Generador de contenido dinámico
- **YAML**: Configuración de datos
- **Material Design Icons**: Iconografía
- **Google Fonts**: Tipografía Roboto

## 📊 Compatibilidad

- ✅ Chrome (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Dispositivos móviles
- ✅ Tablets

## 🤝 Contribución

Este proyecto está diseñado para ser iterativo. Para contribuir:

1. Identifica una sección o funcionalidad a mejorar
2. Crea una rama para tu feature
3. Implementa los cambios
4. Prueba en diferentes dispositivos
5. Documenta los cambios
6. Ejecuta las pruebas: `python test_generator.py`

## 📄 Licencia

Este proyecto es parte de las comunidades GDG de Andalucía.

## 📞 Contacto

Para preguntas o sugerencias sobre el sitio web:
- Comunidades GDG de Andalucía
- GitHub: [Enlace al repositorio]

---

**Desarrollado con ❤️ para las comunidades GDG de Andalucía** 
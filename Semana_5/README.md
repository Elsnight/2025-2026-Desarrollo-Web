# 🖼️ Galería Interactiva con JavaScript

## 📋 Descripción del Proyecto

Aplicación web dinámica que permite crear y gestionar una galería de imágenes interactiva utilizando JavaScript para manipular el DOM y manejar eventos.

## ✨ Características

- ➕ **Agregar imágenes**: Ingresa URLs de imágenes y agrégalas dinámicamente a la galería
- 🖱️ **Seleccionar imágenes**: Haz clic en cualquier imagen para seleccionarla (se resalta con borde especial)
- 🗑️ **Eliminar imágenes**: Elimina la imagen seleccionada con un botón o con atajos de teclado
- ⌨️ **Atajos de teclado**:
  - `Enter`: Agregar imagen
  - `Delete` / `Supr`: Eliminar imagen seleccionada
- 📱 **Diseño responsive**: Se adapta a dispositivos móviles, tablets y escritorio
- 🎨 **Animaciones suaves**: Efectos visuales al agregar, seleccionar y eliminar imágenes

## 🛠️ Tecnologías Utilizadas

- HTML5
- CSS3 (Grid Layout, Flexbox, Animaciones)
- JavaScript (Vanilla JS - Manipulación del DOM)

## 📁 Estructura del Proyecto

```
Semana 05/
├── index.html          # Estructura principal de la aplicación
├── styles.css          # Estilos y diseño responsive
├── script.js           # Lógica de la aplicación
├── assets/
│   └── img/           # Carpeta para imágenes (opcional)
└── README.md          # Documentación del proyecto
```

## 🚀 Cómo Usar

1. **Agregar una imagen**:
   - Ingresa una URL válida de imagen en el campo de texto
   - Haz clic en "Agregar Imagen" o presiona `Enter`

2. **Seleccionar una imagen**:
   - Haz clic en cualquier imagen de la galería
   - La imagen seleccionada se resaltará con un borde azul y una marca de verificación

3. **Eliminar una imagen**:
   - Selecciona una imagen
   - Haz clic en "Eliminar Imagen Seleccionada" o presiona `Delete`/`Supr`

## 🌐 URLs de Imágenes de Ejemplo

Puedes probar la galería con estas URLs:

```
https://picsum.photos/400/300?random=1
https://picsum.photos/400/300?random=2
https://picsum.photos/400/300?random=3
https://picsum.photos/400/300?random=4
https://picsum.photos/400/300?random=5
```

## 💻 Requisitos Técnicos Implementados

### Manipulación del DOM

- ✅ `document.getElementById()` - Para obtener elementos por ID
- ✅ `document.querySelector()` - Para seleccionar elementos
- ✅ `document.createElement()` - Para crear nuevos elementos dinámicamente
- ✅ `element.appendChild()` - Para agregar elementos al DOM
- ✅ `element.remove()` - Para eliminar elementos del DOM

### Manejo de Eventos

- ✅ `addEventListener('click')` - Para seleccionar y eliminar imágenes
- ✅ `addEventListener('keydown')` - Para atajos de teclado
- ✅ `addEventListener('input')` - Para validación en tiempo real

### Validaciones

- ✅ Validación de URL de imagen
- ✅ Manejo de errores de carga de imágenes
- ✅ Validación en tiempo real del input

## 🎨 Características de Diseño

- **Layout**: Grid responsive con columnas automáticas
- **Colores**: Paleta moderna con gradientes
- **Tipografía**: Segoe UI para mejor legibilidad
- **Animaciones**:
  - Fade in al cargar la página
  - Zoom in al agregar imágenes
  - Zoom out al eliminar imágenes
  - Efecto de hover en las imágenes
  - Animación del checkmark al seleccionar

## 📱 Responsive Design

- **Desktop**: Grid de 4 columnas
- **Tablet** (768px): Grid de 3 columnas
- **Mobile** (480px): Grid de 2 columnas

## 🌐 Publicación en GitHub Pages

### Paso 1: Subir el código a GitHub

```bash
# Inicializar repositorio (si no existe)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Agregar Galería Interactiva - Semana 05"

# Conectar con el repositorio remoto (si no está conectado)
git remote add origin https://github.com/Elsnight/2025-2026-Desarrollo-Web.git

# Subir cambios
git push origin main
```

### Paso 2: Activar GitHub Pages

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** (Configuración)
3. En el menú lateral, busca **Pages**
4. En **Source**, selecciona la rama `main`
5. Haz clic en **Save**

### Paso 3: Acceder a tu sitio

Después de unos minutos, tu sitio estará disponible en:

```
https://elsnight.github.io/2025-2026-Desarrollo-Web/Semana%2005/
```

o

```
https://elsnight.github.io/2025-2026-Desarrollo-Web/Semana%2005/index.html
```

> **Nota**: Los espacios en las rutas se convierten en `%20` en las URLs

## 👨‍💻 Autor

Desarrollado para el curso de **Desarrollo de Aplicaciones Web**  
Universidad Estatal Amazónica  
Cuarto Semestre - 2025-2026

## 📝 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

**¡Disfruta creando tu galería de imágenes! 🎉**

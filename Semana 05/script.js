// ========================================
// Elementos del DOM
// ========================================
const imageUrlInput = document.getElementById("imageUrl");
const addImageBtn = document.getElementById("addImageBtn");
const deleteImageBtn = document.getElementById("deleteImageBtn");
const gallery = document.getElementById("gallery");
const emptyState = document.getElementById("emptyState");

// Variable para rastrear la imagen actualmente seleccionada
let selectedImage = null;

// ========================================
// Función para actualizar el estado vacío
// ========================================
function updateEmptyState() {
  const hasImages = gallery.children.length > 0;

  if (hasImages) {
    emptyState.classList.remove("show");
  } else {
    emptyState.classList.add("show");
  }
}

// ========================================
// Función para validar URL de imagen
// ========================================
function isValidImageUrl(url) {
  // Verificar que la URL no esté vacía
  if (!url || url.trim() === "") {
    return false;
  }

  // Verificar extensiones de imagen
  const imageExtensions = /\.(jpg|jpeg|png|gif|bmp|svg|webp|ico)$/i;

  // Permitir rutas locales (relativas)
  const isLocalPath =
    url.startsWith("assets/") || url.startsWith("./") || url.startsWith("../");

  // Si es ruta local, solo verificar extensión
  if (isLocalPath) {
    return imageExtensions.test(url);
  }

  // Para URLs externas, verificar que sea una URL válida
  try {
    new URL(url);
    const imageServices =
      /(picsum\.photos|unsplash\.com|pexels\.com|pixabay\.com|imgur\.com|flickr\.com)/i;
    return imageExtensions.test(url) || imageServices.test(url);
  } catch (e) {
    return false;
  }
}

// ========================================
// Función para agregar imagen
// ========================================
function addImage() {
  const imageUrl = imageUrlInput.value.trim();

  // Validar URL
  if (!isValidImageUrl(imageUrl)) {
    alert(
      "⚠️ Por favor, ingresa una URL válida de imagen.\n\nEjemplos:\n• https://picsum.photos/400/300\n• https://ejemplo.com/imagen.jpg",
    );
    imageUrlInput.focus();
    return;
  }

  // Crear contenedor de imagen
  const galleryItem = document.createElement("div");
  galleryItem.classList.add("gallery-item");

  // Crear elemento de imagen
  const img = document.createElement("img");
  img.src = imageUrl;
  img.alt = "Imagen de la galería";
  img.loading = "lazy";

  // Manejar error de carga de imagen
  img.onerror = function () {
    alert(
      "❌ No se pudo cargar la imagen. Verifica la URL e intenta nuevamente.",
    );
    galleryItem.remove();
    updateEmptyState();
  };

  // Manejar carga exitosa
  img.onload = function () {
    console.log("✅ Imagen cargada exitosamente:", imageUrl);
  };

  // Agregar evento de clic para seleccionar imagen
  galleryItem.addEventListener("click", function () {
    selectImage(galleryItem);
  });

  // Agregar imagen al contenedor y este a la galería
  galleryItem.appendChild(img);
  gallery.appendChild(galleryItem);

  // Limpiar input y actualizar estado
  imageUrlInput.value = "";
  imageUrlInput.focus();
  updateEmptyState();

  console.log("🖼️ Imagen agregada a la galería");
}

// ========================================
// Función para seleccionar imagen
// ========================================
function selectImage(galleryItem) {
  // Si hay una imagen previamente seleccionada, deseleccionarla
  if (selectedImage) {
    selectedImage.classList.remove("selected");
  }

  // Si se hace clic en la misma imagen, deseleccionarla
  if (selectedImage === galleryItem) {
    selectedImage = null;
    deleteImageBtn.disabled = true;
    console.log("❌ Imagen deseleccionada");
  } else {
    // Seleccionar la nueva imagen
    selectedImage = galleryItem;
    selectedImage.classList.add("selected");
    deleteImageBtn.disabled = false;
    console.log("✅ Imagen seleccionada");
  }
}

// ========================================
// Función para eliminar imagen seleccionada
// ========================================
function deleteSelectedImage() {
  if (!selectedImage) {
    return;
  }

  // Agregar animación de eliminación
  selectedImage.classList.add("removing");

  // Esperar a que termine la animación antes de eliminar
  setTimeout(() => {
    selectedImage.remove();
    selectedImage = null;
    deleteImageBtn.disabled = true;
    updateEmptyState();
    console.log("🗑️ Imagen eliminada de la galería");
  }, 400); // Duración de la animación
}

// ========================================
// Event Listeners
// ========================================

// Agregar imagen al hacer clic en el botón
addImageBtn.addEventListener("click", addImage);

// Agregar imagen al presionar Enter en el input
imageUrlInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    addImage();
  }
});

// Eliminar imagen al hacer clic en el botón
deleteImageBtn.addEventListener("click", deleteSelectedImage);

// Eliminar imagen con teclado (Delete o Supr)
document.addEventListener("keydown", function (event) {
  if ((event.key === "Delete" || event.key === "Supr") && selectedImage) {
    event.preventDefault();
    deleteSelectedImage();
  }
});

// Prevenir comportamiento por defecto del input para evitar submit
imageUrlInput.addEventListener("input", function () {
  // Opcional: validación en tiempo real
  const url = this.value.trim();
  if (url && !isValidImageUrl(url)) {
    this.style.borderColor = "var(--danger-color)";
  } else {
    this.style.borderColor = "";
  }
});

// ========================================
// Inicialización
// ========================================

// Mostrar estado vacío al cargar la página
updateEmptyState();

// Imágenes locales de ejemplo (en la carpeta assets/img)
const localImages = [
  "assets/img/IMG_20201120_100153164.jpg",
  "assets/img/IMG_20201120_102630323.jpg",
  "assets/img/IMG_20201120_103745038.jpg",
  "assets/img/IMG_20201120_114028024.jpg",
  "assets/img/IMG_20201120_115924129.jpg",
];

// Imágenes de ejemplo de servicios externos (opcional)
const exampleImages = [
  "https://picsum.photos/400/300?random=1",
  "https://picsum.photos/400/300?random=2",
  "https://picsum.photos/400/300?random=3",
  "https://picsum.photos/400/300?random=4",
];

// Función para cargar imágenes de ejemplo
function loadExampleImages(useLocal = true) {
  const imagesToLoad = useLocal ? localImages : exampleImages;

  imagesToLoad.forEach((url, index) => {
    setTimeout(() => {
      imageUrlInput.value = url;
      addImage();
    }, index * 200); // Agregar con un pequeño retraso para animación
  });
}

// Cargar imágenes locales automáticamente al iniciar
loadExampleImages(true);

console.log("✨ Galería Interactiva inicializada");
console.log("📝 Funcionalidades disponibles:");
console.log("  • Agregar imágenes desde URL");
console.log("  • Seleccionar imágenes con clic");
console.log("  • Eliminar imágenes seleccionadas");
console.log("  • Atajos de teclado: Enter (agregar), Delete/Supr (eliminar)");

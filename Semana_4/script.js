// Script personalizado para Semana 4
// Funcionalidades interactivas y mejoramientos

document.addEventListener("DOMContentLoaded", function () {
  console.log("🚀 Página cargada correctamente");

  // ============================================
  // 1. VALIDACIÓN DE FORMULARIO
  // ============================================
  const formulario = document.querySelector(".form-contact");
  if (formulario) {
    formulario.addEventListener("submit", function (e) {
      e.preventDefault();

      const nombre = document.getElementById("nombre").value.trim();
      const email = document.getElementById("email").value.trim();
      const mensaje = document.getElementById("mensaje").value.trim();

      // Validaciones básicas
      if (!nombre || !email || !mensaje) {
        mostrarAlerta("Por favor completa todos los campos", "warning");
        return;
      }

      // Validar email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        mostrarAlerta("Por favor ingresa un email válido", "warning");
        return;
      }

      // Si todo es válido
      mostrarAlerta(
        "¡Mensaje enviado correctamente! Nos pondremos en contacto pronto.",
        "success",
      );

      // Limpiar formulario
      setTimeout(() => {
        formulario.reset();
      }, 1500);
    });
  }

  // ============================================
  // 2. FUNCIÓN PARA MOSTRAR ALERTAS
  // ============================================
  function mostrarAlerta(mensaje, tipo = "info") {
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${tipo} alert-dismissible fade show`;
    alertDiv.setAttribute("role", "alert");
    alertDiv.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

    // Insertar en el formulario
    const formulario = document.querySelector(".form-contact");
    if (formulario) {
      formulario.parentElement.insertBefore(alertDiv, formulario);

      // Auto-eliminar después de 5 segundos
      setTimeout(() => {
        alertDiv.remove();
      }, 5000);
    }
  }

  // ============================================
  // 3. ANIMACIÓN AL SCROLL (Fade-in)
  // ============================================
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -100px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.animation = "fadeInUp 0.8s ease forwards";
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Aplicar a cards
  document.querySelectorAll(".card").forEach((card) => {
    observer.observe(card);
  });

  // ============================================
  // 4. EFECTO HOVER EN BOTONES
  // ============================================
  const botones = document.querySelectorAll(".btn");
  botones.forEach((boton) => {
    boton.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-3px)";
    });

    boton.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });

  // ============================================
  // 5. NAVBAR ACTIVA AL SCROLL
  // ============================================
  window.addEventListener("scroll", function () {
    const scrollPosition = window.scrollY;
    const links = document.querySelectorAll(".navbar-nav .nav-link");

    // Cambiar estilo del navbar
    if (scrollPosition > 100) {
      document.querySelector(".navbar").style.boxShadow =
        "0 4px 12px rgba(0,0,0,0.3)";
    } else {
      document.querySelector(".navbar").style.boxShadow =
        "0 4px 8px rgba(0,0,0,0.2)";
    }

    // Actualizar enlaces activos
    let current = "";
    document.querySelectorAll("section").forEach((section) => {
      const sectionTop = section.offsetTop;
      if (scrollPosition >= sectionTop - 200) {
        current = section.getAttribute("id");
      }
    });

    links.forEach((link) => {
      link.classList.remove("active");
      if (link.getAttribute("href").slice(1) === current) {
        link.classList.add("active");
      }
    });
  });

  // ============================================
  // 6. CONTADOR DE CARACTERES EN TEXTAREA
  // ============================================
  const textarea = document.getElementById("mensaje");
  if (textarea) {
    textarea.addEventListener("input", function () {
      const maxLength = 500;
      const currentLength = this.value.length;

      if (currentLength > maxLength) {
        this.value = this.value.substring(0, maxLength);
      }

      // Opcional: mostrar contador
      console.log(`Caracteres: ${currentLength}/${maxLength}`);
    });
  }

  // ============================================
  // 7. EFECTO PARALLAX EN HERO
  // ============================================
  const hero = document.querySelector(".hero-section");
  if (hero) {
    window.addEventListener("scroll", function () {
      const scrollPosition = window.scrollY;
      hero.style.backgroundPosition = `0 ${scrollPosition * 0.5}px`;
    });
  }

  // ============================================
  // 8. CLICK EN BOTONES "MÁS DETALLES" DE CARDS
  // ============================================
  document.querySelectorAll(".card .btn").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const cardTitle =
        this.closest(".card").querySelector(".card-title").textContent;
      mostrarAlerta(`Más información sobre: ${cardTitle}`, "info");
    });
  });

  // ============================================
  // 9. SMOOTH SCROLL PARA LINKS INTERNOS
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // ============================================
  // 10. EFECTO RIPPLE EN BOTONES
  // ============================================
  function createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement("span");

    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + "px";
    ripple.style.left = x + "px";
    ripple.style.top = y + "px";
    ripple.classList.add("ripple");

    // Agregar estilos de ripple si no existen
    if (!document.querySelector("style[data-ripple]")) {
      const style = document.createElement("style");
      style.setAttribute("data-ripple", "true");
      style.innerHTML = `
                .btn {
                    position: relative;
                    overflow: hidden;
                }
                .ripple {
                    position: absolute;
                    border-radius: 50%;
                    background-color: rgba(255, 255, 255, 0.6);
                    transform: scale(0);
                    animation: ripple-animation 0.6s ease-out;
                    pointer-events: none;
                }
                @keyframes ripple-animation {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
      document.head.appendChild(style);
    }

    button.appendChild(ripple);
  }

  document.querySelectorAll(".btn").forEach((button) => {
    button.addEventListener("click", createRipple);
  });

  // ============================================
  // 11. PRELOAD DE IMÁGENES
  // ============================================
  console.log("✅ Todas las funcionalidades cargadas correctamente");
});

// ============================================
// FUNCIÓN GLOBAL PARA DESARROLLADORES
// ============================================
function abrirEnlace(url) {
  window.open(url, "_blank");
}

// Log de información
console.log("🎨 Página de Desarrollo Web Moderno - Semana 4");
console.log("📱 Bootstrap 5 + CSS3 Personalizado");
console.log("✨ Diseño Responsivo y Animaciones");

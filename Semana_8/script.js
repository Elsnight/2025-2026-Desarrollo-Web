// JavaScript para Semana 8 - Interactividad y Validación

// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {
  // ========== BOTÓN DE ALERTA ==========
  const btnAlerta = document.getElementById("btnAlerta");

  btnAlerta.addEventListener("click", function () {
    // Crear una alerta personalizada con SweetAlert-style usando Bootstrap
    const alertHTML = `
            <div class="modal fade" id="modalAlerta" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header bg-warning">
                            <h5 class="modal-title">
                                <i class="fas fa-exclamation-triangle"></i> ¡Alerta Personalizada!
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p class="mb-0">¡Bienvenido a mi página web interactiva! Esta es una alerta personalizada creada con JavaScript y Bootstrap.</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Entendido</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

    // Insertar el modal en el body
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = alertHTML;
    document.body.appendChild(tempDiv.firstElementChild);

    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById("modalAlerta"));
    modal.show();

    // Limpiar el modal después de cerrarlo
    document
      .getElementById("modalAlerta")
      .addEventListener("hidden.bs.modal", function () {
        this.remove();
      });
  });

  // ========== VALIDACIÓN DEL FORMULARIO ==========
  const formulario = document.getElementById("formularioContacto");
  const nombre = document.getElementById("nombre");
  const email = document.getElementById("email");
  const mensaje = document.getElementById("mensaje");
  const mensajeExito = document.getElementById("mensajeExito");

  // Validación en tiempo real para cada campo
  nombre.addEventListener("input", function () {
    validarCampo(this);
  });

  email.addEventListener("input", function () {
    validarEmail(this);
  });

  mensaje.addEventListener("input", function () {
    validarCampo(this);
  });

  // Función para validar campos de texto
  function validarCampo(campo) {
    if (campo.value.trim() === "") {
      campo.classList.add("is-invalid");
      campo.classList.remove("is-valid");
      return false;
    } else {
      campo.classList.remove("is-invalid");
      campo.classList.add("is-valid");
      return true;
    }
  }

  // Función para validar email
  function validarEmail(campo) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (campo.value.trim() === "") {
      campo.classList.add("is-invalid");
      campo.classList.remove("is-valid");
      campo.nextElementSibling.textContent =
        "Por favor, ingresa un correo electrónico.";
      return false;
    } else if (!emailRegex.test(campo.value)) {
      campo.classList.add("is-invalid");
      campo.classList.remove("is-valid");
      campo.nextElementSibling.textContent =
        "Por favor, ingresa un correo electrónico válido (ejemplo@correo.com).";
      return false;
    } else {
      campo.classList.remove("is-invalid");
      campo.classList.add("is-valid");
      return true;
    }
  }

  // Manejo del envío del formulario
  formulario.addEventListener("submit", function (event) {
    event.preventDefault();
    event.stopPropagation();

    // Validar todos los campos
    const nombreValido = validarCampo(nombre);
    const emailValido = validarEmail(email);
    const mensajeValido = validarCampo(mensaje);

    // Si todos los campos son válidos
    if (nombreValido && emailValido && mensajeValido) {
      // Mostrar mensaje de éxito
      mensajeExito.classList.remove("d-none");

      // Crear datos del formulario
      const datosFormulario = {
        nombre: nombre.value,
        email: email.value,
        mensaje: mensaje.value,
        fecha: new Date().toLocaleString("es-EC"),
      };

      // Mostrar en consola (simulación de envío)
      console.log("Formulario enviado exitosamente:", datosFormulario);

      // Limpiar el formulario
      formulario.reset();

      // Quitar las clases de validación
      nombre.classList.remove("is-valid");
      email.classList.remove("is-valid");
      mensaje.classList.remove("is-valid");

      // Ocultar el mensaje de éxito después de 5 segundos
      setTimeout(function () {
        mensajeExito.classList.add("d-none");
      }, 5000);

      // Scroll suave hacia el mensaje de éxito
      mensajeExito.scrollIntoView({ behavior: "smooth", block: "center" });
    } else {
      // Si hay campos inválidos, hacer scroll al primer campo con error
      const primerCampoInvalido = formulario.querySelector(".is-invalid");
      if (primerCampoInvalido) {
        primerCampoInvalido.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
        primerCampoInvalido.focus();
      }
    }
  });

  // ========== ANIMACIÓN DEL NAVBAR AL HACER SCROLL ==========
  const navbar = document.querySelector(".navbar");
  let lastScroll = 0;

  window.addEventListener("scroll", function () {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
      navbar.style.boxShadow = "0 8px 16px rgba(0, 0, 0, 0.2)";
    } else {
      navbar.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
    }

    lastScroll = currentScroll;
  });

  // ========== NAVEGACIÓN SUAVE ==========
  const navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href");

      if (href.startsWith("#")) {
        e.preventDefault();
        const targetId = href.substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });

          // Cerrar el menú en móviles
          const navbarCollapse = document.querySelector(".navbar-collapse");
          if (navbarCollapse.classList.contains("show")) {
            const bsCollapse = new bootstrap.Collapse(navbarCollapse);
            bsCollapse.hide();
          }
        }
      }
    });
  });

  // ========== EFECTOS ADICIONALES ==========

  // Contador de caracteres para el mensaje
  mensaje.addEventListener("input", function () {
    const maxLength = 500;
    const currentLength = this.value.length;

    // Crear o actualizar contador si no existe
    let contador = this.parentElement.querySelector(".char-counter");
    if (!contador) {
      contador = document.createElement("small");
      contador.className = "char-counter text-muted";
      this.parentElement.appendChild(contador);
    }

    contador.textContent = `${currentLength} / ${maxLength} caracteres`;

    if (currentLength > maxLength) {
      this.value = this.value.substring(0, maxLength);
    }
  });

  // Mensaje de bienvenida en consola
  console.log(
    "%c¡Bienvenido a mi proyecto web!",
    "color: #667eea; font-size: 24px; font-weight: bold;",
  );
  console.log(
    "%cSemana 8 - Bootstrap & JavaScript",
    "color: #764ba2; font-size: 16px;",
  );
  console.log(
    "%cDesarrollo de Aplicaciones Web 2026",
    "color: #666; font-size: 14px;",
  );
});

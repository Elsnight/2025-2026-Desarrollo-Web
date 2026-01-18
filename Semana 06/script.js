// Obtenemos los elementos del formulario
const form = document.getElementById("registroForm");
const inputNombre = document.getElementById("nombre");
const inputEmail = document.getElementById("email");
const inputPassword = document.getElementById("password");
const inputConfirmPassword = document.getElementById("confirmPassword");
const inputEdad = document.getElementById("edad");
const submitBtn = document.getElementById("submitBtn");
const resetBtn = document.getElementById("resetBtn");
const togglePasswordBtn = document.getElementById("togglePassword");
const toggleConfirmPasswordBtn = document.getElementById(
  "toggleConfirmPassword"
);
const successContainer = document.getElementById("successContainer");

// Estado de validación
const validationState = {
  nombre: false,
  email: false,
  password: false,
  confirmPassword: false,
  edad: false,
};

// ==================== Validaciones ====================

/**
 * Valida el nombre
 * Requisito: Mínimo 3 caracteres
 */
function validarNombre(valor) {
  const errorElement = document.getElementById("errorNombre");
  const successElement = document.getElementById("successNombre");

  if (valor.trim().length === 0) {
    mostrarError(inputNombre, errorElement, "El nombre es requerido");
    validationState.nombre = false;
    return false;
  }

  if (valor.trim().length < 3) {
    mostrarError(
      inputNombre,
      errorElement,
      "El nombre debe tener al menos 3 caracteres"
    );
    validationState.nombre = false;
    return false;
  }

  mostrarExito(inputNombre, successElement, "✓ Nombre válido");
  validationState.nombre = true;
  return true;
}

/**
 * Valida el correo electrónico
 * Usa expresión regular para validar el formato
 */
function validarEmail(valor) {
  const errorElement = document.getElementById("errorEmail");
  const successElement = document.getElementById("successEmail");
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (valor.trim().length === 0) {
    mostrarError(inputEmail, errorElement, "El correo es requerido");
    validationState.email = false;
    return false;
  }

  if (!emailRegex.test(valor)) {
    mostrarError(
      inputEmail,
      errorElement,
      "Ingresa un correo válido (ejemplo@correo.com)"
    );
    validationState.email = false;
    return false;
  }

  mostrarExito(inputEmail, successElement, "✓ Correo válido");
  validationState.email = true;
  return true;
}

/**
 * Valida la contraseña
 * Requisitos:
 * - Mínimo 8 caracteres
 * - Al menos un número
 * - Al menos un carácter especial (!@#$%^&*)
 */
function validarPassword(valor) {
  const errorElement = document.getElementById("errorPassword");
  const passwordReqs = document.querySelector(".password-requirements");

  // Mostrar requirements
  passwordReqs.classList.add("show");

  // Requisito: longitud mínima 8
  const lengthReq = document.getElementById("req-length");
  const hasLength = valor.length >= 8;
  updateRequirement(lengthReq, hasLength);

  // Requisito: al menos un número
  const numberReq = document.getElementById("req-number");
  const hasNumber = /\d/.test(valor);
  updateRequirement(numberReq, hasNumber);

  // Requisito: al menos un carácter especial
  const specialReq = document.getElementById("req-special");
  const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(valor);
  updateRequirement(specialReq, hasSpecial);

  // Validación general
  if (valor.trim().length === 0) {
    mostrarError(inputPassword, errorElement, "La contraseña es requerida");
    validationState.password = false;
    return false;
  }

  if (!hasLength || !hasNumber || !hasSpecial) {
    mostrarError(
      inputPassword,
      errorElement,
      "La contraseña no cumple todos los requisitos"
    );
    validationState.password = false;
    return false;
  }

  limpiarError(inputPassword, errorElement);
  validationState.password = true;
  return true;
}

/**
 * Valida la confirmación de contraseña
 * Requisito: Debe coincidir con la contraseña
 */
function validarConfirmPassword(valor) {
  const errorElement = document.getElementById("errorConfirmPassword");
  const successElement = document.getElementById("successConfirmPassword");

  if (valor.trim().length === 0) {
    mostrarError(
      inputConfirmPassword,
      errorElement,
      "Debe confirmar la contraseña"
    );
    validationState.confirmPassword = false;
    return false;
  }

  if (valor !== inputPassword.value) {
    mostrarError(
      inputConfirmPassword,
      errorElement,
      "Las contraseñas no coinciden"
    );
    validationState.confirmPassword = false;
    return false;
  }

  mostrarExito(inputConfirmPassword, successElement, "✓ Contraseñas coinciden");
  validationState.confirmPassword = true;
  return true;
}

/**
 * Valida la edad
 * Requisito: Mayor o igual a 18 años
 */
function validarEdad(valor) {
  const errorElement = document.getElementById("errorEdad");
  const successElement = document.getElementById("successEdad");

  if (valor.trim().length === 0) {
    mostrarError(inputEdad, errorElement, "La edad es requerida");
    validationState.edad = false;
    return false;
  }

  const edad = parseInt(valor);

  if (isNaN(edad)) {
    mostrarError(inputEdad, errorElement, "Ingresa un número válido");
    validationState.edad = false;
    return false;
  }

  if (edad < 18) {
    mostrarError(inputEdad, errorElement, "Debes ser mayor de 18 años");
    validationState.edad = false;
    return false;
  }

  mostrarExito(inputEdad, successElement, "✓ Edad válida");
  validationState.edad = true;
  return true;
}

// ==================== Funciones Auxiliares ====================

/**
 * Muestra un mensaje de error bajo un campo
 */
function mostrarError(inputElement, errorElement, mensaje) {
  inputElement.classList.remove("valid");
  inputElement.classList.add("invalid");
  errorElement.textContent = mensaje;
  errorElement.classList.add("show");
}

/**
 * Muestra un mensaje de éxito bajo un campo
 */
function mostrarExito(inputElement, successElement, mensaje) {
  inputElement.classList.remove("invalid");
  inputElement.classList.add("valid");
  successElement.textContent = mensaje;
  successElement.classList.add("show");

  // Limpiar error si existe
  const errorElement = successElement.previousElementSibling;
  if (errorElement && errorElement.classList.contains("error-message")) {
    errorElement.classList.remove("show");
  }
}

/**
 * Limpia los estilos de error de un campo
 */
function limpiarError(inputElement, errorElement) {
  inputElement.classList.remove("invalid");
  inputElement.classList.add("valid");
  errorElement.classList.remove("show");
}

/**
 * Actualiza el estado visual de un requisito
 */
function updateRequirement(element, isValid) {
  if (isValid) {
    element.classList.add("valid");
    element.innerHTML =
      '<span class="icon">✓</span> ' + element.textContent.substring(2);
  } else {
    element.classList.remove("valid");
    element.innerHTML =
      '<span class="icon">✗</span> ' + element.textContent.substring(2);
  }
}

/**
 * Verifica si todos los campos son válidos
 */
function verificarFormularioCompleto() {
  const todasValidas =
    validationState.nombre &&
    validationState.email &&
    validationState.password &&
    validationState.confirmPassword &&
    validationState.edad;

  submitBtn.disabled = !todasValidas;
}

/**
 * Alterna la visibilidad de la contraseña
 */
function togglePasswordVisibility(inputElement, buttonElement) {
  const tipo =
    inputElement.getAttribute("type") === "password" ? "text" : "password";
  inputElement.setAttribute("type", tipo);
  buttonElement.textContent = tipo === "password" ? "👁️" : "👁️‍🗨️";
}

// ==================== Event Listeners ====================

// Validación en tiempo real para el nombre
inputNombre.addEventListener("input", (e) => {
  validarNombre(e.target.value);
  verificarFormularioCompleto();
});

inputNombre.addEventListener("blur", (e) => {
  validarNombre(e.target.value);
  verificarFormularioCompleto();
});

// Validación en tiempo real para el email
inputEmail.addEventListener("input", (e) => {
  validarEmail(e.target.value);
  verificarFormularioCompleto();
});

inputEmail.addEventListener("blur", (e) => {
  validarEmail(e.target.value);
  verificarFormularioCompleto();
});

// Validación en tiempo real para la contraseña
inputPassword.addEventListener("input", (e) => {
  validarPassword(e.target.value);
  // Si ya hay confirmación de contraseña, validarla también
  if (inputConfirmPassword.value.length > 0) {
    validarConfirmPassword(inputConfirmPassword.value);
  }
  verificarFormularioCompleto();
});

// Validación en tiempo real para confirmar contraseña
inputConfirmPassword.addEventListener("input", (e) => {
  validarConfirmPassword(e.target.value);
  verificarFormularioCompleto();
});

inputConfirmPassword.addEventListener("blur", (e) => {
  validarConfirmPassword(e.target.value);
  verificarFormularioCompleto();
});

// Validación en tiempo real para la edad
inputEdad.addEventListener("input", (e) => {
  validarEdad(e.target.value);
  verificarFormularioCompleto();
});

inputEdad.addEventListener("blur", (e) => {
  validarEdad(e.target.value);
  verificarFormularioCompleto();
});

// Toggle de visibilidad de contraseña
togglePasswordBtn.addEventListener("click", (e) => {
  e.preventDefault();
  togglePasswordVisibility(inputPassword, togglePasswordBtn);
});

toggleConfirmPasswordBtn.addEventListener("click", (e) => {
  e.preventDefault();
  togglePasswordVisibility(inputConfirmPassword, toggleConfirmPasswordBtn);
});

// Envío del formulario
form.addEventListener("submit", (e) => {
  e.preventDefault();

  // Validar todos los campos antes de enviar
  validarNombre(inputNombre.value);
  validarEmail(inputEmail.value);
  validarPassword(inputPassword.value);
  validarConfirmPassword(inputConfirmPassword.value);
  validarEdad(inputEdad.value);

  if (
    validationState.nombre &&
    validationState.email &&
    validationState.password &&
    validationState.confirmPassword &&
    validationState.edad
  ) {
    // Mostrar mensaje de éxito
    mostrarMensajeExito();

    // Opcional: limpiar el formulario después de 3 segundos
    setTimeout(() => {
      form.reset();
      limpiarFormulario();
    }, 3000);
  }
});

// Limpiar formulario con el botón reset
resetBtn.addEventListener("click", () => {
  limpiarFormulario();
});

/**
 * Limpia todos los estilos y mensajes del formulario
 */
function limpiarFormulario() {
  // Limpiar inputs
  form.reset();

  // Restablecer estado de validación
  validationState.nombre = false;
  validationState.email = false;
  validationState.password = false;
  validationState.confirmPassword = false;
  validationState.edad = false;

  // Limpiar estilos de los inputs
  [
    inputNombre,
    inputEmail,
    inputPassword,
    inputConfirmPassword,
    inputEdad,
  ].forEach((input) => {
    input.classList.remove("valid", "invalid");
  });

  // Limpiar todos los mensajes de error y éxito
  document.querySelectorAll(".error-message").forEach((msg) => {
    msg.classList.remove("show");
    msg.textContent = "";
  });

  document.querySelectorAll(".success-message").forEach((msg) => {
    msg.classList.remove("show");
    msg.textContent = "";
  });

  // Ocultar requirements
  document.querySelector(".password-requirements").classList.remove("show");

  // Ocultar mensaje de éxito
  successContainer.classList.remove("show");
  successContainer.innerHTML = "";

  // Deshabilitar botón de envío
  submitBtn.disabled = true;

  // Restablecer el tipo de los inputs de contraseña
  inputPassword.setAttribute("type", "password");
  togglePasswordBtn.textContent = "👁️";
  inputConfirmPassword.setAttribute("type", "password");
  toggleConfirmPasswordBtn.textContent = "👁️";

  // Enfocar el primer campo
  inputNombre.focus();
}

/**
 * Muestra un mensaje de éxito al enviar el formulario
 */
function mostrarMensajeExito() {
  successContainer.innerHTML = `
        <h2>¡Registro exitoso! 🎉</h2>
        <p>Tu formulario ha sido validado correctamente.</p>
        <p><strong>Datos registrados:</strong></p>
        <p>Nombre: ${inputNombre.value}</p>
        <p>Email: ${inputEmail.value}</p>
        <p>Edad: ${inputEdad.value} años</p>
    `;
  successContainer.classList.add("show");
}

// Inicializar: deshabilitar el botón de envío al cargar la página
window.addEventListener("load", () => {
  submitBtn.disabled = true;
});

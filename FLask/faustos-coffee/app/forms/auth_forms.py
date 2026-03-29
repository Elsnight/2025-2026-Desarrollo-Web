from dataclasses import dataclass

from app.models import Usuario


@dataclass(slots=True)
class RegisterFormData:
    nombre: str
    email: str
    password: str
    confirm_password: str

    @classmethod
    def from_mapping(cls, form_data) -> "RegisterFormData":
        return cls(
            nombre=form_data.get("nombre", "").strip(),
            email=form_data.get("email", "").strip().lower(),
            password=form_data.get("password", ""),
            confirm_password=form_data.get("confirm_password", ""),
        )

    def validate(self) -> list[str]:
        errores = []

        if not self.nombre:
            errores.append("El nombre es obligatorio.")

        if not self.email:
            errores.append("El correo electronico es obligatorio.")
        elif "@" not in self.email or "." not in self.email.split("@")[-1]:
            errores.append("Debes ingresar un correo electronico valido.")

        if len(self.password) < 6:
            errores.append("La contrasena debe tener al menos 6 caracteres.")

        if self.password != self.confirm_password:
            errores.append("La confirmacion de contrasena no coincide.")

        return errores

    def to_user(self) -> Usuario:
        usuario = Usuario(
            nombre=self.nombre,
            email=self.email,
        )
        usuario.set_password(self.password)
        return usuario


@dataclass(slots=True)
class LoginFormData:
    email: str
    password: str

    @classmethod
    def from_mapping(cls, form_data) -> "LoginFormData":
        return cls(
            email=form_data.get("email", "").strip().lower(),
            password=form_data.get("password", ""),
        )

    def validate(self) -> list[str]:
        errores = []

        if not self.email:
            errores.append("El correo electronico es obligatorio.")

        if not self.password:
            errores.append("La contrasena es obligatoria.")

        return errores


def build_register_user_from_form(form_data) -> tuple[Usuario, list[str]]:
    register_form = RegisterFormData.from_mapping(form_data)
    return register_form.to_user(), register_form.validate()


def build_login_data_from_form(form_data) -> tuple[LoginFormData, list[str]]:
    login_form = LoginFormData.from_mapping(form_data)
    return login_form, login_form.validate()

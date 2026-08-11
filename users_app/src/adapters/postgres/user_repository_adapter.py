from typing import Optional

from sqlalchemy.exc import IntegrityError

from adapters.postgres.models import UserModel
from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort
from errors import UserAlreadyExistsError, UserNotFoundError


def _model_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        email=model.email,
        phoneNumber=model.phoneNumber,
        dni=model.dni,
        fullName=model.fullName,
        password=model.password,
        salt=model.salt,
        token=model.token,
        status=model.status,
        expireAt=model.expireAt,
        createdAt=model.createdAt,
        updatedAt=model.updatedAt,
    )


class PostgresUserRepositoryAdapter(UserRepositoryPort):
    """Implementación del repositorio de usuarios sobre Postgres."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create(self, user: User) -> User:
        """Crea un nuevo usuario."""
        with self.session_factory() as session:  # type: Session
            model = UserModel(
                id=user.id,
                username=user.username,
                email=user.email,
                phoneNumber=user.phoneNumber,
                dni=user.dni,
                fullName=user.fullName,
                password=user.password,
                salt=user.salt,
                token=user.token,
                status=user.status.value,
            )
            session.add(model)
            try:
                session.commit()
            except IntegrityError as err:
                session.rollback()
                raise UserAlreadyExistsError(
                    "El username o el email ya existen"
                ) from err
            session.refresh(model)
            return _model_to_entity(model)

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por su id."""
        with self.session_factory() as session:
            model = session.get(UserModel, user_id)
            return _model_to_entity(model) if model else None

    def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        """Obtiene un usuario por username o email."""
        with self.session_factory() as session:
            model = (
                session.query(UserModel)
                .filter((UserModel.username == username) | (UserModel.email == email))
                .first()
            )
            return _model_to_entity(model) if model else None

    def get_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por su username."""
        with self.session_factory() as session:
            model = (
                session.query(UserModel).filter(UserModel.username == username).first()
            )
            return _model_to_entity(model) if model else None

    def get_by_token(self, token: str) -> Optional[User]:
        """Obtiene un usuario por su token de sesión."""
        with self.session_factory() as session:
            model = session.query(UserModel).filter(UserModel.token == token).first()
            return _model_to_entity(model) if model else None

    def update(self, user: User) -> User:
        """Actualiza un usuario existente."""
        with self.session_factory() as session:
            model = session.get(UserModel, user.id)
            if not model:
                raise UserNotFoundError(f"Usuario con id {user.id} no existe")
            for field in (
                "phoneNumber",
                "dni",
                "fullName",
                "status",
                "token",
                "expireAt",
                "password",
                "salt",
            ):
                value = getattr(user, field)
                if value is not None:
                    setattr(
                        model,
                        field,
                        value.value if hasattr(value, "value") else value,
                    )
            session.commit()
            session.refresh(model)
            return _model_to_entity(model)

    def count(self) -> int:
        """Cuenta cuántos usuarios hay almacenados."""
        with self.session_factory() as session:
            return session.query(UserModel).count()

    def delete_all(self) -> None:
        """Elimina todos los usuarios."""
        with self.session_factory() as session:
            session.query(UserModel).delete()
            session.commit()

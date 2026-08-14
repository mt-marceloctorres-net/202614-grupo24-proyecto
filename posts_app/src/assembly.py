from adapters.postgres.database import SessionLocal
from adapters.postgres.post_repository_adapter import PostgresPostRepositoryAdapter

# Wiring de casos de uso: se completa en la tarjeta #24 junto con los
# endpoints de negocio (creación/consulta/eliminación de publicaciones).
# El repositorio ya queda disponible para que esos casos de uso lo reciban
# por inyección, igual que en users_app/src/assembly.py.
repository: PostgresPostRepositoryAdapter = PostgresPostRepositoryAdapter(SessionLocal)

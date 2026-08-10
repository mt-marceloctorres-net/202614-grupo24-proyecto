from adapters.postgres.database import SessionLocal
from adapters.postgres.user_repository_adapter import PostgresUserRepositoryAdapter

repository: PostgresUserRepositoryAdapter = PostgresUserRepositoryAdapter(SessionLocal)

# Los `build_*_use_case` de creación, actualización, autenticación y consulta
# se agregan en los issues de endpoints (no en el scaffold).

from fastapi import APIRouter

# Los endpoints del contrato (creación, actualización, auth, /me, /count,
# /ping, /reset) se agregan en los issues de endpoints — este scaffold solo
# deja el router listo para que main.py lo incluya.
router = APIRouter(prefix="/users")

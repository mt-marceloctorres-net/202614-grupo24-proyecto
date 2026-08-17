from datetime import datetime

from domain.models.post import Post


def test_post_has_no_updated_at_field():
    """Publicación no tiene `updatedAt`, a diferencia de Usuario y Trayecto."""
    assert "updatedAt" not in Post.model_fields


def test_post_required_fields():
    """`routeId`, `userId` y `expireAt` son obligatorios; `id`/`createdAt` los asigna el repositorio."""
    post = Post(
        routeId="11111111-1111-1111-1111-111111111111",
        userId="22222222-2222-2222-2222-222222222222",
        expireAt=datetime(2026, 12, 31, 23, 59, 59),
    )
    assert post.id is None
    assert post.createdAt is None
    assert post.routeId == "11111111-1111-1111-1111-111111111111"
    assert post.userId == "22222222-2222-2222-2222-222222222222"

import uuid

import pytest
from pydantic import ValidationError

from domain.models.offer import (
    DESCRIPCION_MAX,
    Offer,
    OfferCreate,
    PackageSize,
    es_uuid,
)
from errors import InvalidOfferValueError


class TestEsUuid:
    """La comprobación de formato uuid, que decide entre 400 y 201."""

    def test_acepta_uuid_v4(self):
        assert es_uuid(str(uuid.uuid4()))

    def test_acepta_uuid_v1(self):
        # Los identificadores del curso son uuid v1: exigir v4 rechazaría datos
        # válidos y dejaría el servicio respondiendo 400 donde debe dar 201.
        assert es_uuid("bf8792d2-3097-11ee-be56-0242ac120002")

    @pytest.mark.parametrize("valor", ["invalidToken", "", "1", None, 12345])
    def test_rechaza_lo_que_no_es_uuid(self, valor):
        assert not es_uuid(valor)


class TestOfferCreate:
    """Validación de forma: lo que Pydantic rechaza termina en 400."""

    def test_acepta_un_cuerpo_valido(self, datos_validos):
        assert datos_validos.size == PackageSize.MEDIUM.value

    @pytest.mark.parametrize("campo", ["postId", "userId"])
    def test_rechaza_identificadores_que_no_son_uuid(self, datos_validos, campo):
        # Es la prueba del evaluador que el servicio fallaba: manda
        # postId "invalidToken" y espera 400, no 201.
        cuerpo = datos_validos.model_dump()
        cuerpo[campo] = "invalidToken"
        with pytest.raises(ValidationError):
            OfferCreate(**cuerpo)

    def test_rechaza_un_cuerpo_incompleto(self):
        with pytest.raises(ValidationError):
            OfferCreate(offer=10)

    def test_acepta_un_tamano_desconocido(self, datos_validos):
        # A propósito: `size` es str y no el enum. Si Pydantic lo rechazara, el
        # servicio respondería 400 y el contrato exige 412 para ese caso.
        cuerpo = datos_validos.model_dump() | {"size": "HUGE"}
        assert OfferCreate(**cuerpo).size == "HUGE"


class TestOfferDesdeSolicitud:
    """Validación de valor: lo que el dominio rechaza termina en 412."""

    def test_construye_la_oferta(self, datos_validos):
        oferta = Offer.desde_solicitud(datos_validos)
        assert oferta.size == PackageSize.MEDIUM
        assert oferta.postId == datos_validos.postId
        assert oferta.id is None and oferta.createdAt is None

    def test_rechaza_un_tamano_invalido(self, datos_validos):
        datos = datos_validos.model_copy(update={"size": "HUGE"})
        with pytest.raises(InvalidOfferValueError, match="HUGE"):
            Offer.desde_solicitud(datos)

    def test_rechaza_una_oferta_negativa(self, datos_validos):
        datos = datos_validos.model_copy(update={"offer": -0.01})
        with pytest.raises(InvalidOfferValueError, match="negativ"):
            Offer.desde_solicitud(datos)

    def test_acepta_una_oferta_en_cero(self, datos_validos):
        # El contrato prohíbe la oferta negativa, no la gratuita.
        datos = datos_validos.model_copy(update={"offer": 0})
        assert Offer.desde_solicitud(datos).offer == 0

    def test_rechaza_una_descripcion_demasiado_larga(self, datos_validos):
        datos = datos_validos.model_copy(
            update={"description": "x" * (DESCRIPCION_MAX + 1)}
        )
        with pytest.raises(InvalidOfferValueError, match="140"):
            Offer.desde_solicitud(datos)

    def test_acepta_la_descripcion_en_el_limite(self, datos_validos):
        # El límite no debe pasarse de estricto: 140 exactos es válido.
        datos = datos_validos.model_copy(update={"description": "y" * DESCRIPCION_MAX})
        assert len(Offer.desde_solicitud(datos).description) == DESCRIPCION_MAX

    @pytest.mark.parametrize("tamano", ["LARGE", "MEDIUM", "SMALL"])
    def test_acepta_los_tres_tamanos_del_contrato(self, datos_validos, tamano):
        datos = datos_validos.model_copy(update={"size": tamano})
        assert Offer.desde_solicitud(datos).size == PackageSize(tamano)

from pydantic import Field, PositiveFloat
from typing import Annotated
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome do atleta", example="Joao", max_length=50)  # type: ignore
    ]
    cpf: Annotated[
        str, Field(description="CPF do atleta", example="12345678900", max_length=11)  # type: ignore
    ]
    idade: Annotated[
        int, Field(description="Idade do atleta", example="25")  # type: ignore
    ]
    peso: Annotated[
        PositiveFloat, Field(description="Peso do atleta", example="75.5")  # type: ignore
    ]
    altura: Annotated[
        PositiveFloat, Field(description="Altura do atleta", example="1.70")  # type: ignore
    ]
    sexo: Annotated[
        str, Field(description="Sexo do atleta", example="F", max_length=1)  # type: ignore
    ]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do atleta")]  # type: ignore
    centro_treinamento: Annotated[
        CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")
    ]  # type: ignore


class AtletaIn(Atleta): ...


class AtletaOut(AtletaIn, OutMixin): ...

from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from workout_api.atleta.schemas import AtletaIn, AtletaOut
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.atleta.models import AtletaModel

from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()


@router.post(
    "/",
    summary="Criar um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    categoria_nome = atleta_in.categoria.nome

    categoria_result = await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome)
    )
    categoria = categoria_result.scalars().first()  # type: ignore
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria {categoria_nome} não encontrada",
        )

    centro_treinamento_result = await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
    )
    centro_treinamento = centro_treinamento_result.scalars().first()  # type: ignore

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Centro de treinamento {centro_treinamento_nome} não foi encontrado",
        )

    try:
        atleta_out = AtletaOut(
            id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump()
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco",
        )

    return atleta_out

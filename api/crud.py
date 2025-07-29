from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Tuple
from . import models

def get_produtos(db: Session, skip: int = 0, limit: int = 100):
    """Retorna lista de produtos"""
    return db.query(models.Produto).offset(skip).limit(limit).all()

def get_vendas(
    db: Session,
    loja: str = None,
    categoria: str = None,
    data_inicio: datetime = None,
    data_fim: datetime = None
):
    """Retorna vendas com filtros"""
    query = db.query(models.Venda).join(models.Produto)
    
    if loja:
        query = query.filter(models.Venda.loja == loja)
    if categoria:
        query = query.filter(models.Produto.categoria == categoria)
    if data_inicio:
        query = query.filter(models.Venda.data_venda >= data_inicio)
    if data_fim:
        query = query.filter(models.Venda.data_venda <= data_fim)
        
    return query.all()

def get_estoque(db: Session):
    """Retorna status atual do estoque"""
    return db.query(models.Estoque).join(models.Produto).all()

def get_produtos_estoque_baixo(db: Session):
    """Retorna produtos com estoque abaixo do mínimo"""
    return (
        db.query(models.Produto, models.Estoque.quantidade)
        .join(models.Estoque)
        .filter(models.Estoque.quantidade < models.Produto.estoque_minimo)
        .all()
    )

def get_vendas_por_categoria(db: Session) -> List[Tuple[str, float]]:
    """Retorna total de vendas por categoria"""
    return (
        db.query(
            models.Produto.categoria,
            func.sum(models.Venda.valor_total).label("total_vendas")
        )
        .join(models.Venda)
        .group_by(models.Produto.categoria)
        .all()
    )

def get_curva_abc(db: Session) -> List[Tuple[str, float]]:
    """Calcula a Curva ABC de produtos"""
    return (
        db.query(
            models.Produto.nome,
            func.sum(models.Venda.valor_total).label("total_vendas")
        )
        .join(models.Venda)
        .group_by(models.Produto.nome)
        .order_by(func.sum(models.Venda.valor_total).desc())
        .all()
    )

def get_margem_lucro(db: Session) -> List[Tuple[str, float]]:
    """Calcula margem de lucro por produto"""
    return (
        db.query(
            models.Produto.nome,
            ((models.Produto.preco - models.Produto.custo) / models.Produto.preco * 100).label("margem")
        )
        .all()
    )

def get_produtos_mais_vendidos(db: Session, limit: int = 10) -> List[Tuple[str, int]]:
    """Retorna ranking de produtos mais vendidos"""
    return (
        db.query(
            models.Produto.nome,
            func.sum(models.Venda.quantidade).label("total_vendido")
        )
        .join(models.Venda)
        .group_by(models.Produto.nome)
        .order_by(func.sum(models.Venda.quantidade).desc())
        .limit(limit)
        .all()
    )

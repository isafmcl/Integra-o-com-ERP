from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import crud, models, database
from fastapi.middleware.cors import CORSMiddleware

# Criando as tabelas
models.Base.metadata.create_all(bind=database.engine)


app = FastAPI(title="ERP Dashboard API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    return database.get_db()

@app.get("/produtos")
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os produtos"""
    return crud.get_produtos(db, skip=skip, limit=limit)

@app.get("/vendas")
def listar_vendas(
    loja: Optional[str] = None,
    categoria: Optional[str] = None,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Lista vendas com filtros"""
    return crud.get_vendas(db, loja=loja, categoria=categoria, data_inicio=data_inicio, data_fim=data_fim)

@app.get("/estoque")
def status_estoque(db: Session = Depends(get_db)):
    """Retorna status atual do estoque"""
    return crud.get_estoque(db)

@app.get("/alertas/ruptura")
def produtos_estoque_baixo(db: Session = Depends(get_db)):
    """Lista produtos com estoque abaixo do mínimo"""
    return crud.get_produtos_estoque_baixo(db)

@app.get("/analytics/vendas-categoria")
def vendas_por_categoria(db: Session = Depends(get_db)):
    """Retorna total de vendas por categoria"""
    return crud.get_vendas_por_categoria(db)

@app.get("/analytics/curva-abc")
def curva_abc(db: Session = Depends(get_db)):
    """Retorna Curva ABC de produtos"""
    return crud.get_curva_abc(db)

@app.get("/analytics/margem-lucro")
def margem_lucro(db: Session = Depends(get_db)):
    """Retorna margem de lucro por produto"""
    return crud.get_margem_lucro(db)

@app.get("/analytics/mais-vendidos")
def produtos_mais_vendidos(limit: int = 10, db: Session = Depends(get_db)):
    """Retorna ranking de produtos mais vendidos"""
    return crud.get_produtos_mais_vendidos(db, limit=limit)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    categoria = Column(String(50))
    preco = Column(Float)
    custo = Column(Float)
    estoque_minimo = Column(Integer)
    
    # Relacionamentos
    estoque = relationship("Estoque", back_populates="produto")
    vendas = relationship("Venda", back_populates="produto")

class Estoque(Base):
    __tablename__ = "estoque"
    
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    data_atualizacao = Column(DateTime)
    
    # Relacionamento
    produto = relationship("Produto", back_populates="estoque")

class Venda(Base):
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    loja = Column(String(50))
    quantidade = Column(Integer)
    valor_total = Column(Float)
    data_venda = Column(DateTime)
    
    # Relacionamento
    produto = relationship("Produto", back_populates="vendas")

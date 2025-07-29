import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import SessionLocal
from api import crud
from datetime import datetime

def verificar_estoque_e_alertar():
    """Verifica produtos com estoque baixo e simula envio de alerta"""
    db = SessionLocal()
    try:
        produtos_criticos = crud.get_produtos_estoque_baixo(db)
        
        if produtos_criticos:
            print("\n=== ALERTA DE ESTOQUE BAIXO ===")
            print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("\nProdutos com estoque abaixo do mínimo:")
            print("-" * 50)
            
            for produto, quantidade in produtos_criticos:
                print(f"Produto: {produto.nome}")
                print(f"Estoque Atual: {quantidade}")
                print(f"Estoque Mínimo: {produto.estoque_minimo}")
                print("-" * 50)
            
            print("\nE-mail seria enviado para o responsável!")
        else:
            print("\nNenhum produto com estoque crítico encontrado.")
            
    finally:
        db.close()

if __name__ == "__main__":
    verificar_estoque_e_alertar()

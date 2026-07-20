import pandas as pd
import json
import os
from datetime import datetime

# ============================================
# 1. FUNÇÃO PARA CRIAR ARQUIVO DE EXEMPLO
# ============================================

def criar_arquivo_exemplo():
    """
    Cria um arquivo Excel de exemplo com dados financeiros.
    """
    dados = {
        'Data': [
            '2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05',
            '2026-01-06', '2026-01-07'
        ],
        'Descrição': [
            'Salário', 'Supermercado', 'Aluguel', 'Uber', 'Restaurante',
            'Cinema', 'Farmácia'
        ],
        'Categoria': [
            'Salário', 'Alimentação', 'Moradia', 'Transporte', 'Lazer',
            'Lazer', 'Saúde'
        ],
        'Tipo': [
            'Receita', 'Despesa', 'Despesa', 'Despesa', 'Despesa',
            'Despesa', 'Despesa'
        ],
        'Valor': [
            5000.00, 350.00, 1200.00, 45.00, 120.00,
            60.00, 80.00
        ]
    }
    
    df = pd.DataFrame(dados)
    df.to_excel('dashboard.xlsx', index=False)
    print("📁 Arquivo de exemplo criado: dashboard.xlsx")
    return df

# ============================================
# 2. FUNÇÃO PARA CARREGAR OS DADOS
# ============================================

def carregar_dados(caminho_arquivo):
    """
    Carrega os dados financeiros de um arquivo Excel.
    """
    try:
        df = pd.read_excel(caminho_arquivo)
        print(f"✅ Dados carregados: {len(df)} transações")
        
        # Verificar se as colunas necessárias existem
        colunas_necessarias = ['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor']
        colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]
        
        if colunas_faltando:
            print(f"⚠️ Colunas faltando: {colunas_faltando}")
            print("🔄 Criando arquivo de exemplo com o formato correto...")
            return criar_arquivo_exemplo()
        
        return df
    except FileNotFoundError:
        print(f"⚠️ Arquivo '{caminho_arquivo}' não encontrado.")
        print("🔄 Criando arquivo de exemplo...")
        return criar_arquivo_exemplo()
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return None

# ============================================
# 3. FUNÇÕES DE ANÁLISE
# ============================================

def calcular_resumo(df):
    """
    Calcula o resumo financeiro (receitas, despesas, saldo).
    """
    if df is None or df.empty:
        return {}
    
    # Calcular totais
    total_receitas = df[df['Tipo'] == 'Receita']['Valor'].sum()
    total_despesas = df[df['Tipo'] == 'Despesa']['Valor'].sum()
    saldo = total_receitas - total_despesas
    
    return {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'quantidade_transacoes': len(df)
    }

def categorizar_gastos(df):
    """
    Agrupa gastos por categoria.
    """
    if df is None or df.empty:
        return {}
    
    despesas = df[df['Tipo'] == 'Despesa']
    if despesas.empty:
        return {}
    
    return despesas.groupby('Categoria')['Valor'].sum().to_dict()

def gerar_relatorio(df):
    """
    Gera um relatório completo em formato de dicionário.
    """
    if df is None or df.empty:
        return {'erro': 'Dados vazios ou inválidos'}
    
    resumo = calcular_resumo(df)
    gastos_por_categoria = categorizar_gastos(df)
    
    return {
        'data_geracao': datetime.now().isoformat(),
        'resumo': resumo,
        'gastos_por_categoria': gastos_por_categoria,
        'top_5_categorias': dict(sorted(gastos_por_categoria.items(), key=lambda x: x[1], reverse=True)[:5])
    }

# ============================================
# 4. FUNÇÕES PARA SALVAR
# ============================================

def salvar_relatorio_json(relatorio, caminho_saida="outputs/relatorio.json"):
    """
    Salva o relatório em formato JSON.
    """
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Relatório salvo em: {caminho_saida}")

def salvar_relatorio_txt(relatorio, caminho_saida="outputs/relatorio.txt"):
    """
    Salva o relatório em formato TXT legível.
    """
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write("="*50 + "\n")
        f.write("RELATÓRIO FINANCEIRO\n")
        f.write("="*50 + "\n\n")
        
        resumo = relatorio.get('resumo', {})
        f.write(f"📊 Resumo:\n")
        f.write(f"  Total Receitas: R$ {resumo.get('total_receitas', 0):.2f}\n")
        f.write(f"  Total Despesas: R$ {resumo.get('total_despesas', 0):.2f}\n")
        f.write(f"  Saldo: R$ {resumo.get('saldo', 0):.2f}\n")
        f.write(f"  Transações: {resumo.get('quantidade_transacoes', 0)}\n\n")
        
        f.write("📂 Gastos por Categoria:\n")
        for categoria, valor in relatorio.get('gastos_por_categoria', {}).items():
            f.write(f"  {categoria}: R$ {valor:.2f}\n")
    
    print(f"✅ Relatório salvo em: {caminho_saida}")

# ============================================
# 5. FUNÇÃO PRINCIPAL
# ============================================

def main():
    print("="*50)
    print("💰 DASHBOARD DE FINANÇAS PESSOAIS")
    print("="*50 + "\n")
    
    # Carregar dados
    df = carregar_dados("dashboard.xlsx")
    if df is None:
        return
    
    # Gerar relatório
    print("\n📊 Gerando relatório...")
    relatorio = gerar_relatorio(df)
    
    # Exibir resumo na tela
    print("\n" + "="*50)
    print("📊 RESUMO FINANCEIRO")
    print("="*50)
    resumo = relatorio.get('resumo', {})
    print(f"  Total Receitas: R$ {resumo.get('total_receitas', 0):.2f}")
    print(f"  Total Despesas: R$ {resumo.get('total_despesas', 0):.2f}")
    print(f"  Saldo: R$ {resumo.get('saldo', 0):.2f}")
    print(f"  Transações: {resumo.get('quantidade_transacoes', 0)}")
    
    print("\n📂 Gastos por Categoria:")
    for categoria, valor in relatorio.get('gastos_por_categoria', {}).items():
        print(f"  {categoria}: R$ {valor:.2f}")
    
    # Salvar relatórios
    salvar_relatorio_json(relatorio)
    salvar_relatorio_txt(relatorio)
    
    print("\n✅ Análise concluída!")

if __name__ == "__main__":
    main()
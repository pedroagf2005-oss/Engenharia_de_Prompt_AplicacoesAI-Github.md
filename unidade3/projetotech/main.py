"""
Interface de Linha de Comando (CLI)
Menu interativo para usar o assistente financeiro
"""

import sys
from datetime import datetime
from src.finance.account_manager import AccountManager
from src.finance.expense_tracker import ExpenseTracker
from src.finance.portfolio_analyzer import PortfolioAnalyzer
from src.assistant.nlp_engine import NLPEngine
from src.assistant.response_generator import ResponseGenerator
from src.utils.logger import logger

class FinanceAssistantCLI:
    
    def __init__(self):
        self.user_id = "usuario_padrao"
        self.account_manager = AccountManager()
        self.expense_tracker = ExpenseTracker()
        self.portfolio_analyzer = PortfolioAnalyzer()
        self.nlp_engine = NLPEngine()
        self.response_generator = ResponseGenerator()
        
        # Criar conta de demonstração
        self._init_demo_data()
    
    def _init_demo_data(self):
        """Inicializa dados de demonstração"""
        # Criar conta de demonstração
        result = self.account_manager.create_account(
            self.user_id,
            "Conta Corrente",
            "corrente",
            2500.00
        )
        
        if result["status"] == "sucesso":
            account_id = result["conta"]["id"]
            
            # Adicionar algumas transações de exemplo
            self.expense_tracker.add_expense(self.user_id, 150.00, "alimentação", "Supermercado")
            self.expense_tracker.add_expense(self.user_id, 50.00, "transporte", "Uber")
            self.expense_tracker.add_expense(self.user_id, 80.00, "entretenimento", "Cinema")
            
            # Adicionar alguns investimentos de exemplo
            self.portfolio_analyzer.add_investment(
                self.user_id, account_id, "PETR4", "Ação", 100, 28.50
            )
            self.portfolio_analyzer.add_investment(
                self.user_id, account_id, "Tesouro IPCA 2030", "Tesouro", 1000, 85.00
            )
    
    def show_menu(self):
        """Mostra menu principal"""
        print("\n" + "="*50)
        print("💰 ASSISTENTE VIRTUAL DE FINANÇAS 💰")
        print("="*50)
        print("\n🎯 Menu Principal:\n")
        print("  1️⃣  💵 Consultar Saldo")
        print("  2️⃣  📊 Análise de Gastos")
        print("  3️⃣  📈 Investimentos")
        print("  4️⃣  💡 Recomendações Personalizadas")
        print("  5️⃣  ➕ Criar Conta")
        print("  6️⃣  📝 Adicionar Despesa")
        print("  7️⃣  💼 Adicionar Investimento")
        print("  8️⃣  📋 Gerar Relatório Completo")
        print("  9️⃣  🤖 Chat com IA")
        print("  0️⃣  ❌ Sair\n")
        print("="*50)
    
    def run(self):
        """Loop principal da aplicação"""
        print("\n✨ Bem-vindo ao Assistente Virtual de Finanças!")
        print("📱 Digite o número da opção desejada e pressione ENTER\n")
        
        while True:
            self.show_menu()
            choice = input("👉 Escolha uma opção: ").strip()
            
            if choice == "1":
                self._show_balance()
            elif choice == "2":
                self._show_expenses()
            elif choice == "3":
                self._show_investments()
            elif choice == "4":
                self._show_recommendations()
            elif choice == "5":
                self._create_account()
            elif choice == "6":
                self._add_expense()
            elif choice == "7":
                self._add_investment()
            elif choice == "8":
                self._generate_report()
            elif choice == "9":
                self._chat_mode()
            elif choice == "0":
                self._exit()
            else:
                print("\n❌ Opção inválida! Tente novamente.")
    
    def _show_balance(self):
        """Mostra saldo das contas"""
        print("\n💰 SALDO ATUAL")
        print("-" * 40)
        
        result = self.account_manager.get_balance(self.user_id)
        
        if "error" in result:
            print(f"❌ Erro: {result['error']}")
        else:
            print(f"\n✅ Saldo Total: R$ {result['saldo_total']:.2f}\n")
            print("📋 Detalhamento por Conta:")
            for conta in result["contas"]:
                print(f"  • {conta['nome']}: R$ {conta['saldo']:.2f}")
    
    def _show_expenses(self):
        """Mostra análise de gastos"""
        print("\n📊 ANÁLISE DE GASTOS")
        print("-" * 40)
        
        result = self.expense_tracker.get_expenses_by_month(self.user_id)
        
        if "error" in result:
            print(f"❌ Erro: {result['error']}")
        else:
            print(f"\n✅ Gastos do Mês: R$ {result['total_despesas']:.2f}")
            print(f"📝 Número de Transações: {result['numero_transacoes']}\n")
            
            if result['despesas_por_categoria']:
                print("📂 Por Categoria:")
                for categoria, valor in result['despesas_por_categoria'].items():
                    pct = (valor / result['total_despesas'] * 100) if result['total_despesas'] > 0 else 0
                    print(f"  • {categoria.capitalize()}: R$ {valor:.2f} ({pct:.1f}%)")
            
            if result['alertas']:
                print("\n⚠️  Alertas:")
                for alerta in result['alertas']:
                    print(f"  {alerta}")
    
    def _show_investments(self):
        """Mostra análise de investimentos"""
        print("\n📈 MEUS INVESTIMENTOS")
        print("-" * 40)
        
        result = self.portfolio_analyzer.get_portfolio(self.user_id)
        
        if "error" in result:
            print(f"\n✅ Você ainda não possui investimentos registrados.")
        else:
            print(f"\n💼 Portfólio Total: R$ {result['valor_atual']:.2f}")
            print(f"💰 Investido: R$ {result['valor_investido']:.2f}")
            
            emoji = "📈" if result['ganho_perda'] >= 0 else "📉"
            print(f"{emoji} Ganho/Perda: R$ {result['ganho_perda']:.2f} ({result['rendimento_percentual']:+.2f}%)\n")
            
            print("📋 Ativos:")
            for inv in result['investimentos']:
                print(f"  • {inv['nome']}: {inv['quantidade']} un. @ R$ {inv['preco_atual']:.2f}")
    
    def _show_recommendations(self):
        """Mostra recomendações personalizadas"""
        print("\n💡 RECOMENDAÇÕES PERSONALIZADAS")
        print("-" * 40)
        print("\nQual é seu perfil de risco?")
        print("  1. 🟢 Conservador (baixo risco)")
        print("  2. 🟡 Moderado (risco médio)")
        print("  3. 🔴 Agressivo (alto risco)")
        
        profile_choice = input("\n👉 Escolha seu perfil: ").strip()
        
        profiles = {"1": "conservador", "2": "moderado", "3": "agressivo"}
        profile = profiles.get(profile_choice, "conservador")
        
        result = self.portfolio_analyzer.get_recommendations(self.user_id, profile)
        
        print(f"\n✅ Recomendações para Perfil {profile.upper()}:\n")
        
        for i, rec in enumerate(result['recomendacoes'], 1):
            print(f"{i}. 📌 {rec['titulo']}")
            print(f"   {rec['descricao']}")
            print(f"   Alocação: {rec['alocacao']}\n")
    
    def _create_account(self):
        """Cria uma nova conta"""
        print("\n➕ CRIAR NOVA CONTA")
        print("-" * 40)
        
        name = input("\n👉 Nome da conta: ").strip()
        account_type = input("👉 Tipo (corrente/poupança): ").strip()
        
        try:
            balance = float(input("👉 Saldo inicial (R$): ").strip())
        except ValueError:
            print("❌ Valor inválido!")
            return
        
        result = self.account_manager.create_account(self.user_id, name, account_type, balance)
        
        if result["status"] == "sucesso":
            print(f"\n✅ Conta criada com sucesso!")
            print(f"   ID: {result['conta']['id']}")
            print(f"   Nome: {result['conta']['name']}")
            print(f"   Saldo: R$ {result['conta']['balance']:.2f}")
        else:
            print(f"\n❌ Erro: {result.get('error', 'Desconhecido')}")
    
    def _add_expense(self):
        """Adiciona uma despesa"""
        print("\n📝 ADICIONAR DESPESA")
        print("-" * 40)
        
        print("\nCategorias disponíveis:")
        categories = ["alimentação", "transporte", "saúde", "educação", 
                     "entretenimento", "moradia", "utilities", "outro"]
        
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat.capitalize()}")
        
        try:
            cat_choice = int(input("\n👉 Escolha a categoria: ").strip()) - 1
            category = categories[cat_choice]
        except (ValueError, IndexError):
            print("❌ Categoria inválida!")
            return
        
        try:
            amount = float(input("👉 Valor (R$): ").strip())
        except ValueError:
            print("❌ Valor inválido!")
            return
        
        description = input("👉 Descrição: ").strip()
        
        result = self.expense_tracker.add_expense(self.user_id, amount, category, description)
        
        if result["status"] == "sucesso":
            print(f"\n✅ Despesa registrada com sucesso!")
            print(f"   Categoria: {result['despesa']['category']}")
            print(f"   Valor: R$ {result['despesa']['amount']:.2f}")
        else:
            print(f"\n❌ Erro: {result.get('error', 'Desconhecido')}")
    
    def _add_investment(self):
        """Adiciona um investimento"""
        print("\n💼 ADICIONAR INVESTIMENTO")
        print("-" * 40)
        
        name = input("\n👉 Nome do ativo (ex: PETR4): ").strip()
        asset_type = input("👉 Tipo (ação/ETF/tesouro/criptomoeda): ").strip()
        
        try:
            quantity = float(input("👉 Quantidade: ").strip())
            price = float(input("👉 Preço de compra (R$): ").strip())
        except ValueError:
            print("❌ Valores inválidos!")
            return
        
        result = self.portfolio_analyzer.add_investment(
            self.user_id, 1, name, asset_type, quantity, price
        )
        
        if result["status"] == "sucesso":
            print(f"\n✅ Investimento registrado com sucesso!")
            print(f"   Ativo: {result['investimento']['nome']}")
            print(f"   Quantidade: {result['investimento']['quantidade']}")
            print(f"   Preço: R$ {result['investimento']['preco_compra']:.2f}")
        else:
            print(f"\n❌ Erro: {result.get('error', 'Desconhecido')}")
    
    def _generate_report(self):
        """Gera relatório completo"""
        print("\n📋 RELATÓRIO COMPLETO")
        print("=" * 50)
        
        print(f"\n📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print(f"👤 Usuário: {self.user_id}\n")
        
        # Saldo
        balance = self.account_manager.get_balance(self.user_id)
        print(f"💰 Saldo Total: R$ {balance['saldo_total']:.2f}")
        
        # Gastos
        expenses = self.expense_tracker.get_expenses_by_month(self.user_id)
        print(f"📊 Gastos do Mês: R$ {expenses['total_despesas']:.2f}")
        
        # Investimentos
        portfolio = self.portfolio_analyzer.get_portfolio(self.user_id)
        if "error" not in portfolio:
            print(f"📈 Portfólio: R$ {portfolio['valor_atual']:.2f}")
            print(f"   Ganho/Perda: R$ {portfolio['ganho_perda']:.2f} ({portfolio['rendimento_percentual']:+.2f}%)")
        
        print("\n" + "=" * 50)
    
    def _chat_mode(self):
        """Modo chat com IA"""
        print("\n🤖 CHAT COM IA")
        print("-" * 40)
        print("\n💬 Digite sua pergunta sobre finanças (ou 'sair' para voltar)\n")
        
        while True:
            user_input = input("👉 Você: ").strip()
            
            if user_input.lower() == "sair":
                break
            
            if not user_input:
                continue
            
            # Processar com NLP
            parsed = self.nlp_engine.process_input(user_input)
            intent = parsed["intent"]
            
            # Gerar resposta
            if intent == "saldo":
                balance = self.account_manager.get_balance(self.user_id)
                response = self.response_generator.generate_balance_response(balance)
            
            elif intent == "gasto":
                expenses = self.expense_tracker.get_expenses_by_month(self.user_id)
                response = self.response_generator.generate_expense_response(expenses)
            
            elif intent == "investimento":
                portfolio = self.portfolio_analyzer.get_portfolio(self.user_id)
                response = self.response_generator.generate_portfolio_response(portfolio)
            
            elif intent == "recomendacao":
                recommendations = self.portfolio_analyzer.get_recommendations(self.user_id)
                response = self.response_generator.generate_recommendation_response(recommendations)
            
            else:
                response = "🤔 Desculpe, não entendi sua pergunta. Posso ajudar com:\n" \
                          "• Saldo da sua conta\n" \
                          "• Gastos do mês\n" \
                          "• Análise de investimentos\n" \
                          "• Recomendações de investimento"
            
            print(f"\n🤖 Assistente: {response}\n")
    
    def _exit(self):
        """Encerra a aplicação"""
        print("\n👋 Obrigado por usar o Assistente Virtual de Finanças!")
        print("💰 Até logo!\n")
        sys.exit(0)

def main():
    """Função principal"""
    try:
        cli = FinanceAssistantCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Aplicação interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")
        print(f"\n❌ Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
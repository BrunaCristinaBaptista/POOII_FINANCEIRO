import pytest
from datetime import date
from decimal import Decimal
from financeiro.categoria import Categoria
from financeiro.conta import Conta
from financeiro.lancamento import Lancamento
from financeiro.fechamento import Fechamento
from financeiro.conciliacao import Conciliacao

class TestConciliacao:

    def test_conciliacao_com_saldo_inicial_e_movimentacao(self) -> None:

        conta = Conta(nome="Bradesco", saldo=3000.00)
        cat = Categoria("Serviços")
        
        fechamento = Fechamento(mes=8, ano=2026, saldo_inicial=3000.00, lancamentos=[])
        
        l1 = Lancamento("Projeto de Desenvolvimento", date(2026, 8, 24), 4000.00, cat, conta, "pix", "receita")
        fechamento.lancamentos.append(l1)
        
        conciliador = Conciliacao(contas=[conta], fechamento=fechamento)
        
        assert conciliador.conciliar() is True

    def test_conciliacao_furo_de_caixa_lanca_erro(self) -> None:
        conta = Conta(nome="Nubank", saldo=1000.00)
        cat = Categoria("Geral")
        
        fechamento = Fechamento(mes=8, ano=2026, saldo_inicial=1000.00, lancamentos=[])
        
        l1 = Lancamento("Freelance", date(2026, 8, 24), 500.00, cat, conta, "pix", "receita")
        fechamento.lancamentos.append(l1)
        
        conta.retirar_saldo(15.00) 
        
        conciliador = Conciliacao(contas=[conta], fechamento=fechamento)
        
        with pytest.raises(ValueError, match="Falha na conciliação!"):
            conciliador.conciliar()

    def test_conciliacao_com_multiplas_contas(self) -> None:

        conta_corrente = Conta(nome="Corrente", saldo=1000.00)
        conta_poupanca = Conta(nome="Poupança", saldo=2000.00)
        cat = Categoria("Geral")
        
        fechamento = Fechamento(mes=8, ano=2026, saldo_inicial=3000.00, lancamentos=[])
        
        despesa = Lancamento("Conta de Luz", date(2026, 8, 24), 100.00, cat, conta_corrente, "debito", "despesa")
        rendimento = Lancamento("Rendimento", date(2026, 8, 24), 50.00, cat, conta_poupanca, "pix", "receita")
        
        fechamento.lancamentos.extend([despesa, rendimento])
        
        conciliador = Conciliacao(contas=[conta_corrente, conta_poupanca], fechamento=fechamento)
        
        assert conciliador.conciliar() is True
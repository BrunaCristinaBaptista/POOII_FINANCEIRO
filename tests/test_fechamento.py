from datetime import date
from decimal import Decimal
import pytest
from financeiro.categoria import Categoria
from financeiro.conta import Conta
from financeiro.lancamento import Lancamento
from financeiro.fechamento import Fechamento
from financeiro.extrato import Extrato  # <- Novo import necessário

class TestFechamento:

    def test_cria_fechamento_vazio_com_sucesso(self) -> None:
        fechamento = Fechamento(mes=8, ano=2026, saldo_inicial=500.00, lancamentos=[])

        assert fechamento.mes == 8
        assert fechamento.ano == 2026
        assert fechamento.saldo_inicial == Decimal("500.00")
        assert len(fechamento.lancamentos) == 0
        assert fechamento.calcular_total_receitas() == Decimal("0.00")
        assert fechamento.calcular_total_despesas() == Decimal("0.00")
        assert fechamento.calcular_resultado_periodo() == Decimal("0.00")
        assert fechamento.calcular_saldo_final() == Decimal("500.00")

    def test_calcula_fechamento_com_receitas_e_despesas(self) -> None:
        cat = Categoria("Geral")
        conta = Conta(nome="Nubank", saldo=1000.00)
        salario = Lancamento("Salário", date(2026, 8, 5), 3000.00, cat, conta, "pix", "receita")
        aluguel = Lancamento("Aluguel", date(2026, 8, 10), 1200.00, cat, conta, "debito", "despesa")
        fechamento = Fechamento(
            mes=8, 
            ano=2026, 
            saldo_inicial=1000.00, 
            lancamentos=[salario, aluguel]
        )

        assert fechamento.calcular_total_receitas() == Decimal("3000.00")
        assert fechamento.calcular_total_despesas() == Decimal("1200.00")
        assert fechamento.calcular_resultado_periodo() == Decimal("1800.00")  
        assert fechamento.calcular_saldo_final() == Decimal("2800.00")       

    def test_mes_ou_ano_invalido_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            Fechamento(mes=13, ano=2026)

        with pytest.raises(ValueError):
            Fechamento(mes=8, ano=1999)

    def test_saldo_inicial_negativo_lanca_erro(self) -> None:
        with pytest.raises(ValueError, match="O saldo inicial não pode ser negativo."):
            Fechamento(mes=8, ano=2026, saldo_inicial=-100.00)

    def test_gerar_extrato_com_sucesso(self) -> None:
        conta = Conta(nome="Bradesco", saldo=1000.00)
        cat = Categoria("Renda")
        
        fechamento = Fechamento(mes=8, ano=2026, saldo_inicial=1000.00, lancamentos=[])
        
        lanc = Lancamento("Projeto", date(2026, 8, 20), 500.00, cat, conta, "pix", "receita")
        fechamento.lancamentos.append(lanc)
        
        extrato = fechamento.gerar_extrato(contas=[conta])
        
        assert isinstance(extrato, Extrato)
        assert extrato.mes == 8
        assert extrato.saldo_final() == Decimal("500.00")

    def test_gerar_extrato_falha_ao_detectar_furo_de_caixa(self) -> None:
        conta = Conta(nome="Bradesco", saldo=1000.00)
        cat = Categoria("Renda")
        
        fechamento = Fechamento(mes=8, ano=2026, saldo_inicial=1000.00, lancamentos=[])
        
        lanc = Lancamento("Projeto", date(2026, 8, 20), 500.00, cat, conta, "pix", "receita")
        fechamento.lancamentos.append(lanc)
        
        conta.retirar_saldo(100.00)
        
        with pytest.raises(ValueError, match="Falha na conciliação!"):
            fechamento.gerar_extrato(contas=[conta])
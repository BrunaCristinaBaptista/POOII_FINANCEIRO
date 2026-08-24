# tests/test_extrato.py
from datetime import date
from decimal import Decimal
import pytest
from financeiro.categoria import Categoria
from financeiro.conta import Conta
from financeiro.lancamento import Lancamento
from financeiro.fechamento import Fechamento
from financeiro.extrato import Extrato

class TestExtrato:

    def test_gera_extrato_com_sucesso(self) -> None:
        """Garante que o extrato consolida corretamente os dados dos fechamentos do período."""
        cat = Categoria("Geral")
        # Criamos a conta já simulando o saldo final após as operações (1000 inicial + 3000 - 1000)
        conta = Conta(nome="Conta Corrente", saldo=3000.00) 

        receita = Lancamento("Salário", date(2026, 8, 5), 3000.00, cat, conta, "pix", "receita")
        despesa = Lancamento("Aluguel", date(2026, 8, 10), 1000.00, cat, conta, "debito", "despesa")

        fechamento = Fechamento(mes=8, ano=2026, saldo_inicial=1000.00, lancamentos=[receita, despesa])
        
        # O Extrato é criado apenas com mês, ano e a lista de fechamentos. Simples e direto.
        extrato = Extrato(mes=8, ano=2026, fechamentos=[fechamento])

        assert extrato.total_lancamentos() == 2
        assert extrato.total_creditos() == Decimal("3000.00")
        assert extrato.total_debitos() == Decimal("1000.00")
        assert extrato.saldo_final() == Decimal("2000.00")  # 3000 (Créditos) - 1000 (Débitos)

    def test_mes_ou_ano_invalido_lanca_erro(self) -> None:
        """Assegura que meses fora de 1-12 ou anos inválidos disparam ValueError no extrato."""
        fechamento = Fechamento(mes=8, ano=2026, lancamentos=[])

        with pytest.raises(ValueError):
            Extrato(mes=0, ano=2026, fechamentos=[fechamento])

        with pytest.raises(ValueError):
            Extrato(mes=8, ano=1995, fechamentos=[fechamento])
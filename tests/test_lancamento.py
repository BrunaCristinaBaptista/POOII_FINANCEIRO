from datetime import date
from decimal import Decimal
import pytest
from financeiro.categoria import Categoria
from financeiro.conta import Conta
from financeiro.lancamento import Lancamento


class TestLancamento:

    def setup_method(self) -> None:
        self.cat = Categoria("Alimentação")
        self.conta_padrao = Conta(nome="Nubank", saldo=1000.0, limite_credito=500.0)

    def test_cria_lancamento_receita_adiciona_saldo(self) -> None:
        l = Lancamento(
            descricao="Salário",
            data=date(2026, 8, 20),
            valor=2500.00,
            categoria=self.cat,
            conta=self.conta_padrao,
            forma_pagamento="pix",
            natureza_lancamento="receita"
        )
        assert l.valor == Decimal("2500.00")
        assert self.conta_padrao.saldo == Decimal("3500.00") 

    def test_cria_lancamento_despesa_avista_retira_saldo(self) -> None:
        l = Lancamento(
            descricao="Supermercado",
            data=date(2026, 8, 20),
            valor=150.50,
            categoria=self.cat,
            conta=self.conta_padrao,
            forma_pagamento="debito",
            natureza_lancamento="despesa"
        )
        assert l.valor == Decimal("-150.50")
        assert self.conta_padrao.saldo == Decimal("849.50")  
        
    def test_cria_lancamento_despesa_credito_valida_limite(self) -> None:
        l = Lancamento(
            descricao="Compra Parcelada",
            data=date(2026, 8, 20),
            valor=300.00,
            categoria=self.cat,
            conta=self.conta_padrao,
            forma_pagamento="credito",
            natureza_lancamento="despesa"
        )
        assert l.valor == Decimal("-300.00")
        assert self.conta_padrao.saldo == Decimal("1000.00")  

    def test_despesa_credito_acima_do_limite_lanca_erro(self) -> None:
        with pytest.raises(ValueError, match="Limite de crédito insuficiente."):
            Lancamento(
                descricao="Compra Cara",
                data=date(2026, 8, 20),
                valor=600.00,  # Limite é 500
                categoria=self.cat,
                conta=self.conta_padrao,
                forma_pagamento="credito",
                natureza_lancamento="despesa"
            )

    def test_despesa_avista_sem_saldo_lanca_erro(self) -> None:
        conta_pobre = Conta(nome="Carteira Vazia", saldo=50.00)
        with pytest.raises(ValueError):
            Lancamento(
                descricao="Tênis Caro",
                data=date(2026, 8, 23),
                valor=100.00,
                categoria=self.cat,
                conta=conta_pobre,
                forma_pagamento="dinheiro",
                natureza_lancamento="despesa"
            )
        assert conta_pobre.saldo == Decimal("50.00")  

    def test_forma_pagamento_invalida_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            Lancamento("Teste", date(2026, 8, 20), 50.0, self.cat, self.conta_padrao, "cartao_invalido", "despesa")

    def test_natureza_lancamento_invalida_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            Lancamento("Teste", date(2026, 8, 20), 50.0, self.cat, self.conta_padrao, "debito", "investimento")

    def test_valor_zero_ou_negativo_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            Lancamento("Teste", date(2026, 8, 20), 0.0, self.cat, self.conta_padrao, "pix", "receita")
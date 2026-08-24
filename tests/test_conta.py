from decimal import Decimal
import pytest
from financeiro.conta import Conta


class TestConta:

    def test_cria_conta_bancaria_completa(self) -> None:
        conta = Conta(
            nome="Conta Nubank",
            saldo=1250.50,
            limite_credito=3000.00,  # Ajustado de valor_credito para limite_credito
            nome_banco="Nu Pagamentos",
            numero_banco="260",
            agencia="0001",
            numero_conta="123456-7"
        )
        assert conta.nome == "Conta Nubank"
        assert conta.saldo == Decimal("1250.50")
        assert conta.limite_credito == Decimal("3000.00")
        assert conta.nome_banco == "Nu Pagamentos"
        assert conta.numero_banco == "260"
        assert conta.agencia == "0001"
        assert conta.numero_conta == "123456-7"

    def test_cria_conta_simples_carteira(self) -> None:
        carteira = Conta(
            nome="Carteira",
            saldo=75.00
        )
        assert carteira.nome == "Carteira"
        assert carteira.saldo == Decimal("75.00")
        assert carteira.limite_credito == Decimal("0.0")
        assert carteira.nome_banco == "Não se aplica"
        assert carteira.numero_banco == "-"
        assert carteira.agencia == "-"
        assert carteira.numero_conta == "-"

    def test_consultar_total_disponivel(self) -> None:
        conta = Conta(
            nome="Conta Corrente",
            saldo=500.0,
            limite_credito=1000.0
        )
        assert conta.consultar_total_disponivel() == Decimal("1500.0")

    def test_adicionar_e_retirar_saldo(self) -> None:
        conta = Conta(nome="Teste", saldo=100.00)
        conta.adicionar_saldo(50.00)
        assert conta.consultar_saldo() == Decimal("150.00")

        conta.retirar_saldo(30.00)
        assert conta.consultar_saldo() == Decimal("120.00")

    def test_retirar_saldo_insuficiente_lanca_erro(self) -> None:
        conta = Conta(nome="Teste", saldo=50.00)
        with pytest.raises(ValueError):
            conta.retirar_saldo(100.00)
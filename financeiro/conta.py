from decimal import Decimal


class Conta:

    def __init__(
        self,
        nome: str,
        saldo: float | Decimal = 0.0,
        limite_credito: float | Decimal = 0.0,
        nome_banco: str | None = None,
        numero_banco: str | None = None,
        agencia: str | None = None,
        numero_conta: str | None = None
    ) -> None:

        if not nome.strip():
            raise ValueError("O nome da conta não pode ser vazio.")

        if Decimal(str(saldo)) < 0:
            raise ValueError("O saldo não pode ser negativo.")

        if Decimal(str(limite_credito)) < 0:
            raise ValueError("O limite de crédito não pode ser negativo.")

        self.nome = nome.strip()
        self.saldo = Decimal(str(saldo))
        self.limite_credito = Decimal(str(limite_credito))

        self.nome_banco = (
            nome_banco.strip()
            if nome_banco
            else "Não se aplica"
        )

        self.numero_banco = (
            numero_banco.strip()
            if numero_banco
            else "-"
        )

        self.agencia = (
            agencia.strip()
            if agencia
            else "-"
        )

        self.numero_conta = (
            numero_conta.strip()
            if numero_conta
            else "-"
        )

    def consultar_saldo(self) -> Decimal:
        return self.saldo

    def consultar_limite_credito(self) -> Decimal:
        return self.limite_credito

    def adicionar_saldo(self, valor: float | Decimal) -> None:

        valor = Decimal(str(valor))

        if valor <= 0:
            raise ValueError(
                "O valor para adicionar deve ser maior que zero."
            )

        self.saldo += valor

    def retirar_saldo(self, valor: float | Decimal) -> None:

        valor = Decimal(str(valor))

        if valor <= 0:
            raise ValueError(
                "O valor para retirar deve ser maior que zero."
            )

        if valor > self.saldo:
            raise ValueError(
                "Saldo insuficiente."
            )

        self.saldo -= valor

    def consultar_total_disponivel(self) -> Decimal:
        return self.saldo + self.limite_credito
from datetime import date
from decimal import Decimal
from financeiro.categoria import Categoria
from financeiro.conta import Conta

class Lancamento:

    FORMAS_PAGAMENTO = {
        "credito",
        "debito",
        "pix",
        "dinheiro"
    }

    NATUREZAS = {
        "receita",
        "despesa"
    }

    def __init__(
        self,
        descricao: str,
        data: date,
        valor: float | Decimal,
        categoria: Categoria,
        conta: Conta,
        forma_pagamento: str,
        natureza_lancamento: str
    ) -> None:

        valor = Decimal(str(valor))

        if valor <= 0:
            raise ValueError(
                "O valor do lançamento deve ser maior que zero."
            )

        forma_pagamento = forma_pagamento.strip().lower()

        if forma_pagamento not in self.FORMAS_PAGAMENTO:
            raise ValueError(
                f"Forma de pagamento inválida. "
                f"Escolha entre: {self.FORMAS_PAGAMENTO}"
            )

        natureza_lancamento = (
            natureza_lancamento.strip().lower()
        )

        if natureza_lancamento not in self.NATUREZAS:
            raise ValueError(
                f"Natureza inválida. "
                f"Escolha entre: {self.NATUREZAS}"
            )

        self.descricao = descricao
        self.data = data
        self.categoria = categoria
        self.conta = conta
        self.forma_pagamento = forma_pagamento
        self.natureza_lancamento = natureza_lancamento

        if natureza_lancamento == "receita":
            self.valor = valor
            conta.adicionar_saldo(valor)

        else:
            self.valor = -valor
            if forma_pagamento != "credito":
                conta.retirar_saldo(valor)
            else:
                if valor > conta.limite_credito:

                    raise ValueError(
                        "Limite de crédito insuficiente."
                    )
    def eh_receita(self) -> bool:
        return self.valor > 0

    def eh_despesa(self) -> bool:
        return self.valor < 0
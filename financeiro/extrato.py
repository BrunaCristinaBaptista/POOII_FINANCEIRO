# financeiro/extrato.py
from decimal import Decimal
from typing import List
from financeiro.fechamento import Fechamento

class Extrato:
    """
    Consolida todos os fechamentos de um período em um relatório financeiro final.
    Sua existência no sistema garante que a conciliação do período já foi aprovada.
    """
    def __init__(
        self, 
        mes: int, 
        ano: int, 
        fechamentos: List[Fechamento] | None = None
    ) -> None:
        if not (1 <= mes <= 12):
            raise ValueError("O mês deve estar entre 1 e 12.")
        if ano < 2000:
            raise ValueError("Ano inválido.")

        self._mes = mes
        self._ano = ano
        self._fechamentos = fechamentos if fechamentos is not None else []

    @property
    def mes(self) -> int:
        return self._mes

    @property
    def ano(self) -> int:
        return self._ano

    @property
    def fechamentos(self) -> List[Fechamento]:
        return self._fechamentos

    def total_lancamentos(self) -> int:
        """Retorna a quantidade total de lançamentos somados em todos os fechamentos do período."""
        return sum(len(f.lancamentos) for f in self._fechamentos)

    def total_creditos(self) -> Decimal:
        """Retorna o somatório total de créditos (receitas) do período."""
        return sum((f.calcular_total_receitas() for f in self._fechamentos), Decimal("0.00"))

    def total_debitos(self) -> Decimal:
        """Retorna o somatório total de débitos (despesas) do período."""
        return sum((f.calcular_total_despesas() for f in self._fechamentos), Decimal("0.00"))

    def saldo_final(self) -> Decimal:
        """Calcula o resultado líquido final do extrato (Total de Créditos - Total de Débitos)."""
        return self.total_creditos() - self.total_debitos()
from __future__ import annotations
from decimal import Decimal
from typing import List, TYPE_CHECKING
from financeiro.lancamento import Lancamento
from financeiro.conta import Conta

if TYPE_CHECKING:
    from financeiro.extrato import Extrato

class Fechamento:
    def __init__(
        self,
        mes: int,
        ano: int,
        saldo_inicial: float | Decimal = 0.0,
        lancamentos: List[Lancamento] | None = None
    ) -> None:

        if not (1 <= mes <= 12):
            raise ValueError("O mês deve estar entre 1 e 12.")
        if ano < 2000:
            raise ValueError("Ano inválido.")

        self._mes = mes
        self._ano = ano
        self._saldo_inicial = Decimal(str(saldo_inicial))
        self._lancamentos = lancamentos if lancamentos is not None else []

        if self._saldo_inicial < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")

    @property
    def mes(self) -> int:
        return self._mes

    @property
    def ano(self) -> int:
        return self._ano

    @property
    def saldo_inicial(self) -> Decimal:
        return self._saldo_inicial

    @property
    def lancamentos(self) -> List[Lancamento]:
        return self._lancamentos

    def calcular_total_receitas(self) -> Decimal:
        total = Decimal("0.00")
        for lancamento in self._lancamentos:
            if lancamento.eh_receita():
                total += lancamento.valor
        return total

    def calcular_total_despesas(self) -> Decimal:
        total = Decimal("0.00")
        for lancamento in self._lancamentos:
            if lancamento.eh_despesa():
                total += abs(lancamento.valor)
        return total

    def calcular_resultado_periodo(self) -> Decimal:
        return self.calcular_total_receitas() - self.calcular_total_despesas()

    def calcular_saldo_final(self) -> Decimal:
        return self._saldo_inicial + self.calcular_resultado_periodo()

    def gerar_extrato(self, contas: List['Conta']) -> 'Extrato':
        from financeiro.conciliacao import Conciliacao
        from financeiro.extrato import Extrato
        
        conciliador = Conciliacao(contas=contas, fechamento=self)
        conciliador.conciliar()

        return Extrato(
            mes=self.mes,
            ano=self.ano,
            fechamentos=[self]
        )
from decimal import Decimal
from typing import List
from financeiro.conta import Conta
from financeiro.fechamento import Fechamento

class Conciliacao:

    def __init__(self, contas: List[Conta], fechamento: Fechamento) -> None:
        self._contas = contas if contas is not None else []
        self._fechamento = fechamento

    @property
    def contas(self) -> List[Conta]:
        return self._contas

    @property
    def fechamento(self) -> Fechamento:
        return self._fechamento

    def conciliar(self) -> bool:
        saldo_real_contas = sum(conta.consultar_saldo() for conta in self._contas)
        
        saldo_calculado = self._fechamento.calcular_saldo_final()

        if saldo_real_contas != saldo_calculado:
            raise ValueError(
                f"Falha na conciliação! Saldo real (R${saldo_real_contas}) "
                f"difere do calculado no fechamento (R${saldo_calculado})."
            )
        
        return True
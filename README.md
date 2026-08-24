# Projeto Financeiro - Entrega 24 de Agosto de 2026

- Primeiros passos
    
    ```bash
    mkdir -p financeiro tests
    ```
    
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    
    ```bash
    pip install pytest
    ```
    
    ```bash
    pip freeze > requirements.txt
    ```
    
- Criação **`financeiro/__init__.py`**
    
    ```python
    
    ```
    
- Criação **`financeiro/categoria.py`**
    
    Toda categoria de movimentação financeira (seja receita ou despesa) precisa ter um nome descritivo (ex: "Alimentação", "Salário") para organizar os lançamentos de forma clara.
    
    ```python
    class Categoria:
    
        def __init__(self, nome: str) -> None:
            self.nome = nome
    ```
    
- Criação **`tests/__init__.py`**
    
    ```python
    
    ```
    
- Criação **`tests/test_categoria.py`**
    
    **`test_cria_categoria_com_nome`**: Garante que, ao instanciar a classe passando um nome, o objeto armazena corretamente esse valor no atributo `nome`, garantindo a correta inicialização da entidade.
    
    ```python
    from financeiro.categoria import Categoria
    
    class TestCategoria:
    
        def test_cria_categoria_com_nome(self) -> None:
            cat = Categoria("Alimentação")
            assert cat.nome == "Alimentação"
    ```
    
- Criação **`financeiro/conta.py`**
    - **Flexibilidade:** Permite cadastrar contas bancárias completas ou carteiras simples em espécie. Campos bancários não informados recebem valores padrão automáticos (`Não se aplica` e ).
    - **Precisão Financeira:** Utiliza a classe `Decimal` para todos os valores monetários, evitando erros de arredondamento de ponto flutuante.
    - **Validações Fail-Fast (Prevenção de Erros):**
        - O nome da conta não pode ser vazio.
        - O saldo inicial e o limite de crédito não podem ser negativos.
        - Valores para adicionar ou retirar saldo devem ser estritamente maiores que zero.
        - **Bloqueio de Saque:** Operações de retirada bloqueiam a transação com `ValueError` caso o valor desejado seja superior ao saldo disponível.
    - **Consultas e Operações:**
        - `consultar_saldo()` e `consultar_limite_credito()`: Retornam os valores atuais.
        - `adicionar_saldo()` e `retirar_saldo()`: Atualizam dinamicamente o saldo da conta.
        - `consultar_total_disponivel()`: Retorna a soma do saldo atual com o limite de crédito.
    
    ```python
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
    ```
    
- Criação  **`/tests/test_conta.py`**
    - **`test_cria_conta_bancaria_completa`**: Valida se todos os dados fornecidos são salvos corretamente e se os valores financeiros são convertidos para `Decimal`.
    - **`test_cria_conta_simples_carteira`**: Verifica se, ao omitir dados bancários, o sistema preenche os vazios com os valores padrão de segurança.
    - **`test_consultar_total_disponivel`**: Confere se o sistema soma corretamente o saldo real com o limite de crédito.
    - **`test_adicionar_e_retirar_saldo`**: Testa a matemática das operações de depósito e saque, garantindo a atualização do saldo.
    - **`test_retirar_saldo_insuficiente_lanca_erro`**: Garante a regra de segurança que impede a conta de ficar com saldo negativo em transações de débito.
    
    ```python
    from decimal import Decimal
    import pytest
    from financeiro.conta import Conta
    
    class TestConta:
    
        def test_cria_conta_bancaria_completa(self) -> None:
            conta = Conta(
                nome="Conta Nubank",
                saldo=1250.50,
                limite_credito=3000.00,
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
    ```
    
- Criação **`/financeiro/lancamento.py`**
    - **Restrições Estritas:** A forma de pagamento só aceita `credito`, `debito`, `pix` ou `dinheiro`. A natureza só aceita `receita` ou `despesa`.
    - **Integração Automática com a Conta:**
        - **Receitas:** O valor é positivo e injetado automaticamente no saldo da conta.
        - **Despesas à vista:** O valor é negativo e retirado automaticamente do saldo da conta (dispara erro se não houver saldo).
        - **Despesas no crédito:** O valor é negativo, o saldo da conta não é alterado, mas o sistema valida se a compra cabe no limite de crédito da conta.
    
    ```python
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
    ```
    
- Criação **`/tests/test_lancamento.py`**
    - **`test_cria_lancamento_receita_adiciona_saldo`**: Prova que uma receita engorda o saldo da conta vinculada automaticamente.
    - **`test_cria_lancamento_despesa_avista_retira_saldo`**: Prova que um gasto no débito/pix/dinheiro reduz o saldo da conta no mesmo instante.
    - **`test_cria_lancamento_despesa_credito_valida_limite`**: Garante que o cartão de crédito não mexe no saldo à vista, mas registra a despesa.
    - **`test_despesa_credito_acima_do_limite_lanca_erro`**: Verifica se o sistema barra compras de crédito que estouram o limite.
    - **`test_despesa_avista_sem_saldo_lanca_erro`**: Garante o bloqueio de compras à vista para as quais não há dinheiro suficiente.
    - **`test_forma_pagamento_invalida_lanca_erro` / `test_natureza_lancamento_invalida_lanca_erro`**: Evitam que o sistema seja poluído com dados incorretos (ex: escrever "cartão" em vez de "credito").
    - **`test_valor_zero_ou_negativo_lanca_erro`**: Impede transações de R$ 0,00 ou negativas, mantendo a coerência contábil.
    
    ```python
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
    ```
    
- Criação **`/financeiro/fechamento.py`**
    - **Guardião do Período:** Consolida todas as movimentações de um mês/ano específico. Valida se o mês é real (1 a 12).
    - **Contabilidade:** É capaz de calcular separadamente o total de receitas, o total de despesas (tratadas em valor absoluto) e o resultado líquido daquele mês.
    - **Emissão Segura:** É a **única** classe responsável por emitir um `Extrato`. O extrato só é liberado se, internamente, o Fechamento invocar a `Conciliacao` e ela aprovar as contas.
    
    ```python
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
    ```
    
- Criação  **`/tests/test_fechamento.py`**
    - **`test_cria_fechamento_vazio_com_sucesso` / `test_calcula_fechamento_com_receitas_e_despesas`**: Garantem que a matemática interna do fechamento (somas e subtrações) está 100% precisa.
    - **`test_mes_ou_ano_invalido_lanca_erro` / `test_saldo_inicial_negativo_lanca_erro`**: Impedem a criação de fechamentos com dados temporais ou financeiros impossíveis.
    - **`test_gerar_extrato_com_sucesso`**: Garante a integração arquitetural: se a conta estiver certa, o método instanciará e retornará um objeto `Extrato`.
    - **`test_gerar_extrato_falha_ao_detectar_furo_de_caixa`**: Garante que o extrato seja sumariamente bloqueado se houver divergência entre o sistema e as contas (graças à injeção da Conciliação).
    
    ```python
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
    ```
    
- Criação **`/financeiro/conciliacao.py`**
    - **Auditoria de Caixa:** Funciona como o "leão de chácara" do sistema. Ela não altera dados, apenas cruza informações para descobrir fraudes ou esquecimentos.
    - **Verificação Cruzada:** Pega o dinheiro real que está na(s) Conta(s) e compara com a projeção matemática feita pelo Fechamento (Saldo Inicial + Receitas - Despesas). Se faltar ou sobrar 1 centavo, ela dispara um erro e barra qualquer operação seguinte.
    
    ```python
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
    ```
    
- Criação **`/tests/test_conciliacao.py`**
    - **`test_conciliacao_com_saldo_inicial_e_movimentacao` (Caminho Feliz)**: Verifica se a auditoria aprova quando as movimentações do sistema batem perfeitamente com o saldo da conta.
    - **`test_conciliacao_furo_de_caixa_lanca_erro`**: Simula um cenário onde um dinheiro sai da conta real (ex: taxa do banco) mas o usuário esquece de lançar no sistema. O teste garante que o erro será detectado e disparado.
    - **`test_conciliacao_com_multiplas_contas`**: Testa a habilidade do conciliador de somar o dinheiro espalhado em várias contas (ex: Corrente e Poupança) e cruzar com os lançamentos gerais.
    
    ```python
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
    ```
    
- Criação**`/financeiro/extrato.py`**
    - **Relatório Final Imutável:** É um documento de consolidação gerencial de um ou mais fechamentos.
    - **Garantia de Autenticidade:** Como a regra de negócio obriga o Extrato a nascer somente a partir de um Fechamento conciliado, **a própria existência de um objeto Extrato em memória é a prova cabal de que as contas daquele período estão auditadas e corretas.** Não há status "pendente".
    
    ```python
    from decimal import Decimal
    from typing import List
    from financeiro.fechamento import Fechamento
    
    class Extrato:
    
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
            return sum(len(f.lancamentos) for f in self._fechamentos)
    
        def total_creditos(self) -> Decimal:
            return sum((f.calcular_total_receitas() for f in self._fechamentos), Decimal("0.00"))
    
        def total_debitos(self) -> Decimal:
            return sum((f.calcular_total_despesas() for f in self._fechamentos), Decimal("0.00"))
    
        def saldo_final(self) -> Decimal:
            return self.total_creditos() - self.total_debitos()
    ```
    
- Criação **`/tests/test_extrato.py`**
    - **`test_gera_extrato_com_sucesso`**: Verifica se o extrato consegue ler os fechamentos que lhe foram passados e apurar os totais de créditos, débitos, e o saldo líquido final do relatório.
    - **`test_mes_ou_ano_invalido_lanca_erro`**: Evita a emissão de relatórios com cabeçalhos de data inconsistentes.
    
    ```python
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
            cat = Categoria("Geral")
            conta = Conta(nome="Conta Corrente", saldo=3000.00) 
            receita = Lancamento("Salário", date(2026, 8, 5), 3000.00, cat, conta, "pix", "receita")
            despesa = Lancamento("Aluguel", date(2026, 8, 10), 1000.00, cat, conta, "debito", "despesa")
            fechamento = Fechamento(mes=8, ano=2026, saldo_inicial=1000.00, lancamentos=[receita, despesa])
            extrato = Extrato(mes=8, ano=2026, fechamentos=[fechamento])
    
            assert extrato.total_lancamentos() == 2
            assert extrato.total_creditos() == Decimal("3000.00")
            assert extrato.total_debitos() == Decimal("1000.00")
            assert extrato.saldo_final() == Decimal("2000.00")  
    
        def test_mes_ou_ano_invalido_lanca_erro(self) -> None:
            fechamento = Fechamento(mes=8, ano=2026, lancamentos=[])
            with pytest.raises(ValueError):
                Extrato(mes=0, ano=2026, fechamentos=[fechamento])
            with pytest.raises(ValueError):
                Extrato(mes=8, ano=1995, fechamentos=[fechamento])
    ```
    

### 1. No Fechamento, os lançamentos originais foram copiados ou referenciados? Por quê?

**Eles foram referenciados.**

Por causa do conceito de Agregação na Orientação a Objetos. O `Fechamento` não é o "dono" absoluto do `Lançamento` (o lançamento existe por si só e tem vida própria). Se copiássemos os objetos, estaríamos duplicando dados na memória à toa e perdendo a sincronia. Referenciar garante que o `Fechamento` está sempre olhando para a verdade absoluta do sistema.

### 2. Conciliacao virou uma classe própria ou um método de Fechamento? Por quê?

A `Conciliacao` virou uma classe própria.

Se colocássemos a `Conciliação` dentro dele, o `Fechamento` teria que assumir o papel de Auditor, precisando ir lá na classe `Conta`, olhar saldos bancários e cruzar dados. Isso deixaria o `Fechamento` "inchado" e com muitas responsabilidades. Criar a `Conciliacao` como uma classe própria (uma Entidade Associativa) cria um especialista no sistema: a única função dela na vida é atuar como uma balança que pega as `Contas` de um lado, o `Fechamento` do outro, e verifica se os dois pesos são idênticos.

### 3. O que acontece quando não há lançamentos no período, ou quando a conciliação não bate?

Quando NÃO HÁ lançamentos no período: 

O `Fechamento` é inicializado com uma lista vazia (`[]`). Ele processa tudo normalmente, calculando R$ 0,00 de receitas e despesas. Se o saldo real das contas continuar sendo exatamente igual ao `saldo_inicial` (já que nada movimentou), a `Conciliacao` aprova e o `Extrato` é gerado normalmente, mostrando que o mês ficou no "zero a zero".

Quando a conciliação NÃO BATE: 

Aplica-se o padrão Fail-Fast (falha rápida). A classe `Conciliacao` dispara imediatamente uma exceção (`ValueError:` Falha na conciliação!). Como o método `gerar_extrato()` do `Fechamento` chama a `Conciliação` logo na primeira linha, esse erro interrompe a execução do código na mesma hora. O resultado: o objeto `Extrato` nunca chega a ser instanciado e o sistema bloqueia a emissão de relatórios furados.
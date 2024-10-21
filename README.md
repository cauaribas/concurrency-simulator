# Simulação de transações concorrentes com a detecção e resolução de Deadlocks

Este projeto implementa uma simulação de transações concorrentes utilizando threads em Python, onde várias threads competem por dois recursos compartilhados (X e Y). O programa simula situações de deadlock e utiliza uma técnica baseada em timestamp e wait-die para evitar ou resolver esses deadlocks.

## Requisitos

- Python 3.x

## Como executar o código

1. Abra o terminal na pasta do projeto
2. Execute o programa com o seguinte comando:

```
python app.py
```

## Funcionalidade do programa

1. O programa cria 5 threads, cada uma simulando uma transação concorrente.
2. Cada thread tenta acessar dois recursos compartilhados: X e Y, com uso de bloqueios binários (`LOCK`)
3. As threads executam operações com tempos de espera aleatórios, simulando cenários reais de concorrência.
4. O programa:
   - Detecta situações de deadlock utilizando uma técnica de timestamp.
   - Resolve o deadlock ao finalizar a thread que iniciou mais tarde, aplicando a lógica de `wait-die`.
5. Mensagens são exibidas no terminal para acompanhar:
   - Quando uma thread é inicializada.
   - Quando uma thread é finalizada.
   - Quando uma thread obtém um recurso.
   - Quando uma thread libera um recurso.
   - Quando uma thread entra em deadlock e é finalizada.

## Estrutura do código

- `run():` Função principal de cada thread, que tentam realizar uma transação.
- `check_deadlock():` Verifica e resolve situações de deadlock com base em timestamps.
- `transaction():` Define a lógica para acessar os recursos X e Y.
- `main()`: Função principal que cria e inicia as threads, aguardando sua finalização.

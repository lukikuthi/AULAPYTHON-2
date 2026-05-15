# Simulador de Semáforo — Documentação

## Visão Geral

Simulador de semáforo com ciclo automático (Vermelho 30s → Verde 25s → Amarelo 4s), interface visual em tempo real e botão de reinício.

## Arquitetura

```
app.py              Backend Flask (estado + API)
templates/index.html Frontend (visual + polling)
```

## Backend (`app.py`)

- **Estado global** — dicionário `estado_atual` com índice, nome, cor, tempo restante e duração total, protegido por `threading.Lock`.
- **Thread daemon** (`ciclo_semaforo`) — decrementa o contador a cada 1 segundo e avança para o próximo estado quando o tempo chega a zero.
- **Rotas:**
  - `GET /` — serve a página HTML.
  - `GET /status` — retorna JSON com o estado atual do semáforo.
  - `POST /reset` — reinicia o ciclo para o estado Vermelho.

## Frontend (`templates/index.html`)

- **Polling** — a cada 500ms, `fetch('/status')` atualiza a interface.
- **Lâmpadas** — 3 divs circulares com classes CSS dinâmicas (`vermelho-ativo`, `amarelo-ativo`, `verde-ativo`) que ativam gradientes, glows e animações de pulso.
- **Contador** — exibe o tempo restante em segundos, colorido conforme o estado ativo.
- **Barra de progresso** — preenchimento proporcional ao tempo restante.
- **Botão Reiniciar** — envia `POST /reset` e atualiza a interface imediatamente.

## Ciclo de Funcionamento

1. Thread decrementa `tempo_restante` a cada segundo.
2. Quando `tempo_restante <= 0`, avança para o próximo estado no array `ESTADOS` (circular).
3. Frontend consulta `/status` a cada 500ms e reflete o estado nas lâmpadas, contador e barra.
4. O botão de reset volta o índice para 0 (Vermelho) e reinicia o contador.

# Análise de Ações

Aplicação web para acompanhar ações e estimar valor intrínseco com métodos fundamentalistas, sem score ou algoritmo proprietário.

## O que está incluído

- Dashboard com preço, valor intrínseco, margem de segurança e indicadores.
- DCF em fluxo de caixa livre para a firma (premissas editáveis).
- DDM de Gordon para companhias com política de dividendos estável.
- Comparação por P/L, P/VP, EV/EBITDA, EV/EBIT e PEG.
- Página de detalhe com gráfico preço x valores intrínsecos e simulador.
- API em FastAPI, camada de serviços separada e arquivo local de cotações (substituível por PostgreSQL).
- Atualização diária dos preços via `yfinance`, acionável localmente ou pelo GitHub Actions.

## Início rápido

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra http://127.0.0.1:8000. Os dados iniciais são didáticos; antes de usar a aplicação para decisões, importe demonstrações financeiras confiáveis e revise as premissas.

## Atualização de preços

```bash
python -m app.jobs.update_prices
```

No GitHub, o workflow em `.github/workflows/daily-prices.yml` executa nos dias úteis e grava as alterações no repositório. Para produção, substitua o arquivo local por PostgreSQL e use uma fonte de dados licenciada para preços e fundamentos.

## Estrutura

- `app/services/valuation.py`: regras transparentes de DCF, DDM e múltiplos.
- `app/services/market_data.py`: adaptador para fonte de preços.
- `app/data/repository.py`: persistência, isolada do restante da aplicação.
- `app/templates` e `app/static`: interface web.

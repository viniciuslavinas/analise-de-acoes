from app.services.market_data import refresh_prices

if __name__ == "__main__":
    updated = refresh_prices()
    print(f"Cotações atualizadas: {', '.join(updated) or 'nenhuma'}")

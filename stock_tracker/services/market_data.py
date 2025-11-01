import httpx
import logging 
import asyncio
from datetime import datetime
from stock_tracker.setting import settings 


# We use the key from setting 

ALPHA_VANTAGE_API_KEY = settings.ALPHA_VANTAGE_API_KEY
BASE_URL = "https://www.alphavantage.co/query"

async def fetch_alpha_vantage_price(symbol: str, retries=3, timeout=10) -> dict:
    """
    Llama a la API de Alpha Vantage con lógica robusta de reintento.
    """
    if not ALPHA_VANTAGE_API_KEY:
        raise RuntimeError("ALPHA_VANTAGE_API_KEY no está configurada.")
    
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol.upper(),
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    for attempt in range(retries):
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                resp = await client.get(BASE_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                # Parsing de la respuesta
                if "Global Quote" not in data or not data["Global Quote"]:
                    raise ValueError(f"Símbolo no encontrado o datos incompletos para {symbol}")
                    
                quote = data["Global Quote"]
                price = float(quote["05. price"])
                date_str = quote["07. latest trading day"]
                
                # Convertir fecha a objeto datetime para facilitar el futuro guardado en DB
                timestamp_dt = datetime.strptime(date_str, '%Y-%m-%d')
                
                return {
                    "symbol": symbol.upper(),
                    "price": price,
                    "timestamp": timestamp_dt.isoformat() + "Z", # Retornamos ISO 8601 string
                    "provider": "alpha_vantage",
                }
            except Exception as e:
                logging.warning(f"Error en intento {attempt+1} para {symbol}: {e}")
                
        await asyncio.sleep(2 ** attempt)
    
    raise Exception(f"Fallo al obtener datos de Alpha Vantage para {symbol}.")

# Crea un archivo __init__.py vacío en la carpeta services para que Python la reconozca
# touch services/__init__.py


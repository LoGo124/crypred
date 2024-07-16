import os

# Obtener las variables de entorno
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# Validar que las variables de entorno se hayan cargado correctamente
if not API_KEY or not SECRET_KEY:
    raise ValueError("Las variables de entorno API_KEY y SECRET_KEY no están configuradas")

ALPACA_CONFIG = {
    # Put your own Alpaca key here:
    "API_KEY": API_KEY,
    # Put your own Alpaca secret here:
    "API_SECRET": SECRET_KEY,
    # If you want to go live, you must change this
    "ENDPOINT": "https://paper-api.alpaca.markets",
    "is_paper": True
}
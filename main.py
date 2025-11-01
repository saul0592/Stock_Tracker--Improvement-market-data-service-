# main.py (En la carpeta raíz, solo para iniciar Uvicorn)

from dotenv import load_dotenv
load_dotenv() # Carga el .env

# Importa el objeto 'app' desde el módulo 'main' que está en el paquete 'stock_tracker'
from stock_tracker.main import app 

if __name__ == "__main__":
    import uvicorn
    # Le dice a Uvicorn: "Ejecuta el objeto 'app' que importamos"
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
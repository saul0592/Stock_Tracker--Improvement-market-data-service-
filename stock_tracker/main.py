from fastapi import FastAPI, HTTPException, Request, Form
from stock_tracker.services.market_data import fetch_alpha_vantage_price # Importa la función del servicio
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

#start new_project 

app = FastAPI(title="Simple stock API")

"Jinga2 will directly head to the folder 'templates'"
templates = Jinja2Templates(directory ="stock_tracker/templates")


#-- ENDPOINT 1 FOR SEARCH: GET IT WILL SHOW THE FORM
@app.get("/search", response_class=HTMLResponse)
async def get_search_form(request: Request):
    "Shows the form to seach for the stock"
    return templates.TemplateResponse("search.html", {"request": request})


#-- ENDPOINT 2 FOR POST: PROCESS THE SEARCH 

@app.post("/search", response_class=HTMLResponse)
async def post_stock_search(request:Request, symbol: str = Form(...)):
    "The symbol of the form and then it will search for it in Alpha Vantage without using the database"

    try:
        #call the funcitoto to obtain the service of the data
        # Llama a la función del servicio para obtener los datos
        price_data = await fetch_alpha_vantage_price(symbol)
        
        # Retorna el resultado
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "symbol": price_data["symbol"],
                "price":price_data["price"],
                "provider": price_data["provider"]
            }
        )

    except HTTPException as e:
        # Re-lanza errores HTTP específicos
        return templates.templateResponse(
            "result.hmtl",
            {
                "request" : request,
                "error": f" fail in the service or stock don't found it"
            }

        )
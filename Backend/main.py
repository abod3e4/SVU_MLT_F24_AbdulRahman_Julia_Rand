from fastapi import FastAPI
from api.endpoints import router
from fastapi.staticfiles import StaticFiles
from eda_charts import generate_charts
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Loan Approval API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/eda-charts")
def get_charts():
    chart_urls = generate_charts()
    return {"charts": chart_urls}


app.include_router(router)

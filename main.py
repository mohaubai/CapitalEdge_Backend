from fastapi import FastAPI
import uvicorn
from routers import analytics, branches,customers, fraud, transfers

app = FastAPI()

app.include_router(analytics.router)
app.include_router(branches.router)
app.include_router(customers.router)
app.include_router(fraud.router)
app.include_router(transfers.router)

if __name__ =='__main__':
    uvicorn.run(app)
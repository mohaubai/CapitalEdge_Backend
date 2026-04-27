from fastapi import FastAPI
import uvicorn
from routers import analytics, branches,customers, fraud

app = FastAPI()

app.include_router(analytics.router)
app.include_router(branches.router)
app.include_router(customers.router)
app.include_router(fraud.router)

if __name__ =='__main__':
    uvicorn.run(app)
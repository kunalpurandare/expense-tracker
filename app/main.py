from fastapi import FastAPI
from app.admin import admin
from app.database.database import engine, Base
from app.routes import users, transactions

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

# Routers
app.include_router(users.router, tags=['Users'])
app.include_router(transactions.router, tags=['Transactions'])
app.include_router(admin.router, tags=['Admin'])

@app.get("/")
def root():
    return {"message": "Welcome to the Expense Tracker API"}

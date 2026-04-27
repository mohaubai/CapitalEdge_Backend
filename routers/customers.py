from schemas.responses import CustomerSummary
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from database import get_db
from sqlalchemy.orm import Session
from schemas.responses import CustomerSummary
from typing import List

router = APIRouter()

@router.get("/customers/{customer_id}/summary", response_model=List[CustomerSummary])
def get_get_customer_summary(customer_id:int, db: Session = Depends(get_db)):
    query = text("""
        WITH customer_account_data AS (
            SELECT customers.customer_id, name, city, COUNT(account_id) as account_count, SUM(balance) AS account_balance
            FROM customers
            INNER JOIN accounts ON customers.customer_id = accounts.customer_id
            WHERE customers.customer_id = :customer_id
            GROUP BY customers.customer_id, name, city
        ),
        customer_transaction AS (
            SELECT name, SUM(amount) AS total_transactions, customer_account_data.customer_id
            FROM customer_account_data
            INNER JOIN accounts ON customer_account_data.customer_id = accounts.customer_id
            INNER JOIN transactions ON accounts.account_id = transactions.account_id
            GROUP BY name, customer_account_data.customer_id
        )
        SELECT customer_account_data.name, city, account_count, account_balance, total_transactions
        FROM customer_account_data
        INNER JOIN customer_transaction ON customer_account_data.customer_id = customer_transaction.customer_id
    """)
    result = db.execute(query, {'customer_id': customer_id})
    rows = result.all()
    if len(rows) == 0:
        raise HTTPException(status_code=404, detail='Details not found')
    return [row._mapping for row in rows]
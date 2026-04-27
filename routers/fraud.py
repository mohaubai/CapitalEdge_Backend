from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from schemas.responses import FraudTransaction

router = APIRouter()

@router.get("/fraud", response_model=List[FraudTransaction])
def get_fraud_data(db: Session = Depends(get_db)):
    result = db.execute(text("""
        WITH customer_avg AS(
            SELECT 
                account_id, 
                AVG(amount) as avg_amount
            FROM transactions
            GROUP BY account_id
        )
        SELECT 
            transactions.account_id,
            amount,
            avg_amount,
            CASE
                WHEN amount > avg_amount * 1.5 THEN 'suspicious'
                ELSE 'normal'
            END AS flag
        FROM customer_avg
        INNER JOIN transactions ON customer_avg.account_id = transactions.account_id
    """))
    rows = result.all()
    return [row._mapping for row in rows]
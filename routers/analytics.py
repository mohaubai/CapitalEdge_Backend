from fastapi import APIRouter, Depends
from schemas.responses import MonthlySummary
from database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter()

@router.get('/analytics')
def get_monthly_summary_data(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT
            EXTRACT(YEAR FROM created_at) AS year,
            EXTRACT(MONTH FROM created_at) AS month,
            COUNT(account_id),
            SUM(amount::NUMERIC),
            ROUND(AVG(amount::NUMERIC), 2),
            MAX(amount::NUMERIC)
        FROM transactions
        GROUP BY year, month
        """)
    )
    rows = result.all()
    return {
        "data": [row._mapping for row in rows]
    }
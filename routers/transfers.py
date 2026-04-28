from fastapi import APIRouter, Depends, HTTPException
from schemas.responses import TransfersAmount
from database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/transfers")
def transfer_money(data: TransfersAmount, db: Session = Depends(get_db)):
    idempotency_key = data.idempotency_key
    idempotency_check = text("""
        SELECT idempotency_key FROM transactions
        WHERE idempotency_key = :idempotency_key
    """)
    result = db.execute(idempotency_check, {'idempotency_key': idempotency_key})
    rows = result.first()
    if rows is not None:
        return {
            "message": "Duplicate request",
            "data": rows._mapping
        }
    try:
        from_account_id = data.from_account_id
        to_account_id = data.to_account_id
        amount = data.amount
        db.execute(text("""
            INSERT INTO transactions (account_id, amount, idempotency_key)
            VALUES (:from_account_id, :amount, :idempotency_key)
        """), {'from_account_id': from_account_id, 'amount': amount, 'idempotency_key': idempotency_key})
        db.execute(text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE account_id = :from_account_id
        """), {'from_account_id': from_account_id, 'amount': amount})
        db.execute(text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE account_id = :to_account_id
        """), {'to_account_id': to_account_id, 'amount': amount})
        db.commit()
        return {"message": "Transfer Completed"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter()

@router.get('/branches')
def get_all_branches(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT * FROM branches
    """))
    rows = result.all()
    print(rows[0][0])
    return {
        'data':[row._mapping for row in rows]
    }

@router.get('/branches/{branch_id}')
def get_one_branch(branch_id: int, db: Session = Depends(get_db)):
    query = (text("""
        SELECT * FROM branches WHERE branch_id = :branch_id
    """))
    result = db.execute(query, {'branch_id': branch_id})
    rows = result.first()
    if rows is None:
        raise HTTPException(status_code=404, detail="Branch not found!")
    return {
        'data': rows._mapping
    }
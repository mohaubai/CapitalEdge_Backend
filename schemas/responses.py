from pydantic import BaseModel

class MonthlySummary(BaseModel):
    year: int
    month: int
    transaction_count: int
    total_volume: float
    average_amount: float
    highest_transaction: float

class FraudTransaction(BaseModel):
    account_id: int
    amount: float
    avg_amount: float
    flag: str

class CustomerSummary(BaseModel):
    name: str
    city: str
    account_count: int
    account_balance: float
    total_transactions: float

class TransfersAmount(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float
    idempotency_key: str
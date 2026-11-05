import json
from pathlib import Path
from langchain.tools import tool
from datetime import datetime, timezone

TOOLS_DIR = Path(__file__).resolve().parent

POLICY_PATH = TOOLS_DIR / "refund_policy.md"

TRANSACTIONS_PATH = TOOLS_DIR.parent / "data" / "transactions.json"

@tool
def get_refund_policy() -> str:
    
    """
    Fetches the platform refund policy that includes all the conditions and requirements for a refund processing.
    """

    print("get_refund_policy called")
    with open(POLICY_PATH, "r" ) as f:
        refund_policy = f.read()

        return refund_policy

@tool
def get_transaction_details(transaction_id: str) -> str:
    """Fetches the status, date and prior refund state for a given transaction ID."""

    print("get_transaction_details called")
    with open(TRANSACTIONS_PATH, "r") as file:
        transactions = json.load(file)

    details = transactions.get(transaction_id, {"error": "Transaction details not found."})

    return json.dumps(details)


@tool
def calculate_elapsed_time(transaction_time: str) -> str:
    """
    Calculate the exact calender days elapsed between transaction time and today.
    """

    print("calculate_elapsed_time called")
    now = datetime.now(timezone.utc)
    txn_date = datetime.fromisoformat(transaction_time.replace("Z", "+00:00"))
    elapsed_days = (now - txn_date).days    

    return json.dumps({
        "current_time": now.isoformat(),
        "transaction_time": txn_date.isoformat(),
        "elapsed_days": elapsed_days,
        "within_refund_period": elapsed_days <= 30
        })

@tool
def process_refund(transaction_id:str, reason:str) -> str:
    """
    Process the refund request for a given transaction ID once refund policy is satisfied.
    """
    print("process_refund called")
    with open(TRANSACTIONS_PATH, "r") as file:
        transactions = json.load(file)

    if transaction_id not in transactions:
        return json.dumps({"success": False,"error": f"Transaction {transaction_id} not found."})

    transactions[transaction_id]["refund_status"] = "Processed"

    with open(TRANSACTIONS_PATH, "w") as file:
        json.dump(transactions, file, indent=2)

    return json.dumps({
        "success": True,
        "amount_refunded": transactions[transaction_id].get("amount"),
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "status": "Processed",
        "message": "Refund initiated successfully to the source payment method."       
    })

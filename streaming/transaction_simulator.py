# ==========================================
# File: streaming/transaction_simulator.py
# Purpose: Generate realistic SA bank transactions and send to Fabric Eventstream
# ==========================================

import os
import uuid
import random
import json
import time
from datetime import datetime, timezone
from azure.eventhub import EventHubProducerClient, EventData

# ===== CONNECTION STRING =====
# Set FABRIC_CONNECTION_STR in your environment or in a .env file (never commit the real key!)
# Example .env entry:
#   FABRIC_CONNECTION_STR=Endpoint=sb://....servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on environment variable being set

CONNECTION_STR = os.environ.get("FABRIC_CONNECTION_STR", "PASTE_YOUR_CONNECTION_STRING_HERE")

# Real South African Bank Branch/Sort Codes
SA_BANK_CODES = {
    "ABSA": "632005",
    "FNB": "250655",
    "NEDBANK": "198765",
    "STANDARD_BANK": "051001",
    "CAPITEC": "470010",
    "INVESTEC": "580105"
}

TRANSACTION_TYPES = ["EFT", "CASH_DEPOSIT", "CARD_PAYMENT", "INSTANT_PAY"]

# High risk companies from your Gold layer (will get larger amounts to trigger alerts)
HIGH_RISK_COMPANIES = [
    "2023/421702/08",  # AFRICAN TECHNOLOGIES 424 (PTY) LTD
    "2015/554508/21"   # ABC TECHNOLOGIES 570 (PTY) LTD
]

# Normal companies for baseline transactions
NORMAL_COMPANIES = [
    "2018/320346/21",  # SUMMIT CONSULTING 359 (PTY) LTD
    "2022/446840/08",  # CONTINENTAL CONSULTING 481 (PTY) LTD
    "2023/176079/21",  # PREMIUM SOLUTIONS 448 (PTY) LTD
    "2023/691707/08",  # PREMIUM SERVICES 774 (PTY) LTD
    "2021/716218/08"   # UNITED GROUP 673 (PTY) LTD
]

def generate_transaction():
    """Generates a single realistic SA bank transaction"""
    
    # 30% chance to pick a HIGH risk company to trigger alerts during demo
    if random.random() < 0.3:
        company_reg = random.choice(HIGH_RISK_COMPANIES)
        # Higher chance of large amounts for high-risk companies (above FICA R100k threshold)
        amount_zar = round(random.uniform(5000, 150000), 2) 
    else:
        company_reg = random.choice(NORMAL_COMPANIES)
        # Normal transaction amounts
        amount_zar = round(random.uniform(50, 25000), 2)

    bank_name = random.choice(list(SA_BANK_CODES.keys()))
    
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "company_registration_number": company_reg,
        "amount_zar": amount_zar,
        "bank_code": SA_BANK_CODES[bank_name],
        "bank_name": bank_name,
        "transaction_type": random.choice(TRANSACTION_TYPES),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    return transaction

def send_to_fabric(transaction):
    """Sends a transaction to Fabric Eventstream"""
    try:
        # Create producer client
        producer = EventHubProducerClient.from_connection_string(
            conn_str=CONNECTION_STR
        )
        
        # Create event data
        event_data = EventData(json.dumps(transaction))
        
        # Send the event
        with producer:
            producer.send_event(event_data)
        
        # Print success message
        risk_flag = "🚨 HIGH RISK" if transaction["company_registration_number"] in HIGH_RISK_COMPANIES else "✅ Normal"
        print(f"{risk_flag}: {transaction['company_registration_number']} | R{transaction['amount_zar']:,.2f} | {transaction['bank_name']}")
        
    except Exception as e:
        print(f"❌ Error sending to Fabric: {e}")

if __name__ == "__main__":
    print("🚀 Starting SA Transaction Simulator (Fabric Eventstream Edition)...")
    print("=" * 60)
    
    # Verify connection string is set
    if CONNECTION_STR == "PASTE_YOUR_CONNECTION_STRING_HERE":
        print("❌ ERROR: You need to paste your Fabric connection string!")
        print("   Go to: Eventstream > Transaction_Simulator_Source > SAS Key Authentication")
        print("   Copy the 'Connection string-primary key' and paste it in the script.")
        exit(1)
    
    print("✅ Connection string configured")
    print("📡 Sending transactions to Fabric Eventstream...")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            txn = generate_transaction()
            send_to_fabric(txn)
            time.sleep(2)  # One transaction every 2 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Simulator stopped.")
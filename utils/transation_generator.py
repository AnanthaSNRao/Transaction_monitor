import pandas as pd
import random
from datetime import datetime, timedelta

def generate_fraudulent_transactions(user_ids, merchant_names, num_fraudulent):
    
    missspelled_merchant_names = [
        "Amaz0n Prime", "Walm@rt", "Apple.com", "Nike@sports.com", "$tarbuccks",
        "Net_filx", "-"
    ]

    fraudulent_transactions = []
    for _ in range(num_fraudulent):
        rule = random.randint(1, 5) 
        user_id = random.choice(user_ids)
        if rule == 1:  # High-value transaction
            transaction = {
                "user_id": user_id,
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d %H:%M:%S"),
                "merchant_name": random.choice(merchant_names),
                "amount": round(random.uniform(5000.0, 15000.0), 2), 
            }
        elif rule == 2:  # Multiple transactions in a very short amount of time
            timestamp = datetime.now() - timedelta(days=random.randint(0, 5))
            for _ in range(random.randint(3, 7)): 
                transaction = {
                    "user_id": user_id,
                    "timestamp": (timestamp + timedelta(minutes=random.randint(1, 15))).strftime("%Y-%m-%d %H:%M:%S"),
                    "merchant_name": random.choice(merchant_names),
                    "amount": round(random.uniform(10.0, 500.0), 2),
                }
                fraudulent_transactions.append(transaction)
        elif rule == 3:  # Multiple transactions at the same merchant in span of few days
            merchant_name = random.choice(merchant_names)
            for _ in range(random.randint(6, 10)):
                transaction = {
                    "user_id": user_id,
                    "timestamp": (datetime.now() - timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d %H:%M:%S"),
                    "merchant_name": merchant_name,
                    "amount": round(random.uniform(10.0, 500.0), 2),
                }
                fraudulent_transactions.append(transaction)
        elif rule == 4:  # Same amount of spent in short duration 4 or transactions with same price with 1-2 hrs
            price = round(random.uniform(20.0, 1000.0), 2)
            for _ in range(random.randrange(4,8)):
                transaction = {
                    "user_id": user_id,
                    "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 2))).strftime("%Y-%m-%d %H:%M:%S"),
                    "merchant_name": random.choice(merchant_names),
                    "amount": price,
                }
                fraudulent_transactions.append(transaction)
            
        elif rule == 5:  # Mis-spelled name for merchants
            transaction = {
                "user_id": user_id,
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d %H:%M:%S"),
                "merchant_name": random.choice(missspelled_merchant_names),
                "amount": round(random.uniform(10.0, 500.0), 2),
            }
        fraudulent_transactions.append(transaction)
    return fraudulent_transactions

def generate_legitimatetransaction_csv(user_ids, merchant_names, num_transactions):
    # Generate legitimate transactions
    legitimate_transactions = {
        "user_id": [random.choice(user_ids) for _ in range(num_transactions)],
        "timestamp": [
            (datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59)))
            .strftime("%Y-%m-%d %H:%M:%S")
            for _ in range(num_transactions)
        ],
        "merchant_name": [random.choice(merchant_names) for _ in range(num_transactions)],
        "amount": [round(random.uniform(5.0, 1000.0), 2) for _ in range(num_transactions)],
    }

    return legitimate_transactions


def generate_transaction_csv_with_fraudulent_data(file_path, num_transactions=500, num_fraudulent=50):
    user_ids = [f"user_{i}" for i in range(1, 11)]
    merchant_names = [
        "Amazon", "Walmart", "Apple Store", "Nike", "Starbucks",
        "Target", "Best Buy", "Uber", "Airbnb", "Netflix", "Disney", "Hulu", "Esty", "Tarder Joe"  ]
    # Generate legitimate transactions
    legitimate_transactions = generate_legitimatetransaction_csv(user_ids, merchant_names, num_transactions - num_fraudulent)

    # Generate fraudulent transactions
    fraudulent_transactions = generate_fraudulent_transactions(user_ids, merchant_names, num_fraudulent)

    # Combine legitimate and fraudulent transactions
    all_transactions = pd.DataFrame(legitimate_transactions).to_dict('records') + fraudulent_transactions

    # Shuffle the transactions to mix legitimate and fraudulent
    random.shuffle(all_transactions)

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(all_transactions)
    df.to_csv(file_path, index=False)

# Generate the CSV
generate_transaction_csv_with_fraudulent_data("transaction_list_with_fraud.csv", num_transactions=500, num_fraudulent=50)


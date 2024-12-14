from utils.transation_generator import generate_transaction_csv_with_fraudulent_data
from transactionMonitor.fraud_detector import analyze_transactions

def main():
    # Run analysis
    analyze_transactions("transaction_list_with_fraud.csv")

if __name__ == "__main__":
    main()
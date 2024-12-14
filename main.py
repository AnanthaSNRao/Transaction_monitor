from utils.transation_generator import generate_transaction_csv_with_fraudulent_data
from transactionMonitor.fraud_detector import analyze_transactions

def main():
    # Generate the CSV
    generate_transaction_csv_with_fraudulent_data("../transaction_list_with_fraud.csv", num_transactions=500, num_fraudulent=50)

    # Run analysis
    analyze_transactions("../transaction_list_with_fraud.csv")

if __name__ == "main":
    main()
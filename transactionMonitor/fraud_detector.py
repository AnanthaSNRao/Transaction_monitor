import re
import pandas as pd
from datetime import datetime, timedelta

# Function to detect high-value transactions
def detect_high_value_transactions(df, threshold=5000):
    # Identify transactions above the threshold
    high_value_transactions = df[df['amount'] > threshold]
    
    # Identify users with first transactions greater than 1000
    first_transactions = df.sort_values('timestamp').groupby('user_id').first()
    first_high_transactions = first_transactions[first_transactions['amount'] > 1000]
    
    # Combine both conditions
    flagged_transactions = pd.concat([high_value_transactions, df[df['user_id'].isin(first_high_transactions.index)]])

    # Add Z-score based outlier detection
    zscore_flagged = detect_outliers_using_zscore_per_user(df)
    
    # Combine all flagged transactions
    combined_flagged = pd.concat([flagged_transactions, zscore_flagged]).drop_duplicates()

    return combined_flagged

# Function to detect outliers using Z-score per user
def detect_outliers_using_zscore_per_user(df, threshold=3):
    df['zscore'] = df.groupby('user_id')['amount'].filter(lambda x: len(x) > 1).transform(lambda x: (x - x.mean()) / x.std())
    
    # Flag transactions with Z-score above the threshold
    flagged_transactions = df[(df['zscore'] > threshold)]
    
    # Include single transactions above $5000
    single_transaction_flagged = df.groupby('user_id')['amount'].filter(lambda x: len(x) == 1 and x.iloc[0] > 5000)
    flagged_transactions = pd.concat([flagged_transactions, df[df['user_id'].isin(single_transaction_flagged.index)]])
    
    return flagged_transactions


# Function to detect multiple transactions in a short time span
def detect_multiple_transactions_short_time(df, time_window_minutes=5, min_transactions=4):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    flagged_transactions = []

    for user_id, group in df.groupby('user_id'):
        group = group.sort_values('timestamp')
        rolling_count = group['timestamp'].diff().dt.total_seconds().fillna(float('inf')) / 60
        consecutive_transactions = rolling_count <= time_window_minutes
        flagged = group[consecutive_transactions].iloc[:min_transactions]

        if len(flagged) >= min_transactions:
            flagged_transactions.append(flagged)

    return pd.concat(flagged_transactions) if flagged_transactions else pd.DataFrame()

# Function to detect multiple transactions at the same merchant
def detect_multiple_transactions_same_merchant(df, min_transactions=7, time_window_days=2):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    flagged_transactions = []

    for (user_id, merchant_name), group in df.groupby(['user_id', 'merchant_name']):
        group = group.sort_values('timestamp')
        rolling_count = group['timestamp'].diff().dt.total_seconds().fillna(float('inf')) / (60 * 60 * 24)
        consecutive_transactions = rolling_count <= time_window_days
        flagged = group[consecutive_transactions]

        if len(flagged) >= min_transactions:
            flagged_transactions.append(flagged)

    return pd.concat(flagged_transactions) if flagged_transactions else pd.DataFrame()

# Function to detect same amounts spent in a short time span
def detect_same_amount_short_time(df, time_window_minutes=30):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    flagged_transactions = []

    for user_id, group in df.groupby('user_id'):
        group = group.sort_values('timestamp')
        for amount, sub_group in group.groupby('amount'):
            rolling_count = sub_group['timestamp'].diff().dt.total_seconds().fillna(float('inf')) / 60
            consecutive_transactions = rolling_count <= time_window_minutes
            flagged = sub_group[consecutive_transactions]

            if len(flagged) > 3:
                flagged_transactions.append(flagged)

    return pd.concat(flagged_transactions) if flagged_transactions else pd.DataFrame()

# Function to detect transactions with misspelled merchant names
def detect_misspelled_merchant_names(df):
    pattern = re.compile(r"[^a-zA-Z ]+")
    return df[df['merchant_name'].str.contains(pattern)]

# Function to detect transactions adding up to $15,000 within 24 hours
def detect_transactions_totaling_threshold(df, threshold=15000, time_window_hours=24):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    flagged_transactions = []

    for user_id, group in df.groupby('user_id'):
        group = group.sort_values('timestamp')
        for i in range(len(group)):
            start_time = group.iloc[i]['timestamp']
            window = group[(group['timestamp'] >= start_time) & (group['timestamp'] <= start_time + timedelta(hours=time_window_hours))]
            if window['amount'].sum() >= threshold:
                flagged_transactions.append(window)
    return flagged_transactions


def analyze_transactions(file_path):

    df = pd.read_csv(file_path)

    # Detect anomalies
    high_value = detect_high_value_transactions(df)
    short_time_multiple = detect_multiple_transactions_short_time(df)
    same_merchant_multiple = detect_multiple_transactions_same_merchant(df)
    same_amount_short_time = detect_same_amount_short_time(df)
    misspelled_merchants = detect_misspelled_merchant_names(df)
    transactions_totaling_threshold = detect_transactions_totaling_threshold(df)

    # Write results to a text file
    with open("../anomaly_detection_summary.txt", "w") as file:
        file.write("High-Value Transactions:\n")
        for user_id, group in high_value.groupby('user_id'):
            file.write(f"User {user_id}: {len(group)} transactions flagged\n")
            file.write("\n")

        file.write("\nMultiple Transactions in Short Time:\n")
        for user_id, group in short_time_multiple.groupby('user_id'):
            file.write(f"User {user_id}: {len(group)} transactions flagged\n")
            file.write("\n")

        file.write("\nMultiple Transactions at Same Merchant:\n")
        for user_id, group in same_merchant_multiple.groupby('user_id'):
            file.write(f"User {user_id}: {len(group)} transactions flagged\n")
            file.write("\n")

        file.write("\nSame Amount in Short Time:\n")
        for user_id, group in same_amount_short_time.groupby('user_id'):
            file.write(f"User {user_id}: {len(group)} transactions flagged\n")
            file.write("\n")

        file.write("\nMisspelled Merchant Names:\n")
        for user_id, group in misspelled_merchants.groupby('user_id'):
            file.write(f"User {user_id}: {len(group)} transactions flagged\n")
            file.write("\n")

        file.write("\nTransactions adding up to $10,000 within 24 hours:\n")
        if transactions_totaling_threshold:
            for data in transactions_totaling_threshold:
                for user_id, group in data.groupby('user_id'):
                    file.write(f"User {user_id}: {len(group)} transactions flagged\n")
                    file.write("\n")
        else:
            file.write("No transactions flagged for this rule.\n")


    with open("../detailed_anomaly_detection.log", "a+") as log:
        log.write("High-Value Transactions:\n")
        log.write(high_value.to_string())
        log.write("\n---------------------------------------------------------------------------------------\n")
        log.write("\nMultiple Transactions in Short Time:\n") 
        log.write(short_time_multiple.to_string())
        log.write("\n---------------------------------------------------------------------------------------\n")
        log.write("\nMultiple Transactions at Same Merchant:\n")  
        log.write(same_merchant_multiple.to_string())
        log.write("\n---------------------------------------------------------------------------------------\n")
        log.write("\nSame Amount in Short Time:\n")  
        log.write(same_amount_short_time.to_string())
        log.write("\n---------------------------------------------------------------------------------------\n")
        log.write("\nMisspelled Merchant Names:\n")  
        log.write(misspelled_merchants.to_string())
        log.write("\n---------------------------------------------------------------------------------------\n")
        log.write("\nTransactions adding up to $15,000 within 24 hours:\n")  
        for t in transactions_totaling_threshold:
            log.write(t.to_string())
            log.write("\n---------------------------------------------------------------------------------------\n")



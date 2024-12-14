# Transaction Monitor

**Problem statment**

Build a transaction monitoring subsystem 
Input to the subsystem will be transaction list csv file (max 10k rows) with following fields - user ID, timestamp, merchant name, amount 
Propose 5 fraud related transaction monitoring rules + a short explanation on why 
Implement the subsystem and flag suspicious transactions as the output

**Rules considerd to detect fraudlent transactions**

- Rule 1: to detect high-value transactions. This is to flag any transactions which abnormally high amount of transactions. Cases considered:
    - transactions above the 5000.
    - users with first transactions greater than 1000.
    - Z-score-based outlier detection. A statistical method is used to find out abnormal values in a series of values present.

- Rule 2: to detect multiple transactions in a short time span. Identifying the users with more than 3 transactions in 5 mins.

- Rule 3: to detect multiple transactions at the same merchant. Identifying the users with more than 7 transactions in the span of 2 days with the same merchant. 
    - This rule will help in detecting any malicious merchant with users' stored credit card or wallet data misusing user data.

- Rule 4: to detect the same amounts spent in a short time span. This is to identify users with the same amount spent in more than 3 transactions within 30 minutes.

- Rule 5: to detect transactions with misspelled merchant names. Helps to detect malicious/phishing websites using user details.

- Rule 6: detect transactions adding up to $15,000 within 24 hours. Helps to flag a user’s activity with more than 15,000 spending within a span of 24 hrs.


**Note: All the above constant values are assumptions made for the sake of the problem statement.**
- Also, all the constants directly used in the function should be used from a constants file or config file.


# Project Structure

- |- .vevn # for virtual python environment
- |- transactionMonitor 
    - |-fraud_detector.py # contains all the core logic for flagging transactions
- |- utils
    - |- transcation_generator.py # generates csv file needed.
- |- main.py
- |- requirements.txt # conatins all the py libraries
- |- makefile

# Running the project
Just execute the following command
- make run

# Files Generated
- transaction_list_with_fraud.csv is a test file generated.
- anomaly_detection_summary.txt will provide a brief overview.
- detailed_anomaly_detection.log will provide a detailed view of each transaction that failed according to each rule mentioned above.

# Minor improvements
- Visual representation of fraud detection for each rule.
- Unit testing
- Have precedence of Rules: And remove duplicate flagged transactions based on precedence
- Have error/flag codes for each rule.

# Future Considerations
-  Location: obtained from the time of transaction with timezone or as separate information that can be used to detect fraudulent transactions.
- Streaming Data: By using stream processing tools like Apache filing along with low latency, look up the databases.
- Parallel Processing: can use the sharding technique to group a cluster of users and store & process them separately.
- Using sophisticated statistical methods to tune the constants presented above: 
    - Like using Hypothesis Testing to see if the test parameters.
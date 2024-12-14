# Transaction Monitor

Problem statment

Build a transaction monitoring subsystem 
Input to the subsystem will be transaction list csv file (max 10k rows) with following fields - user ID, timestamp, merchant name, amount 
Propose 5 fraud related transaction monitoring rules + a short explanation on why 
Implement the subsystem and flag suspicious transactions as the output

Rules considerd to detect fraudlent transactions

- Rule 1: to detect high-value transactions. This to flag any transctions which abnormaly high amount of transaction. Cases considered:
    - transactions above the 5000.
    - users with first transactions greater than 1000.
    - Z-score based outlier detection. A statistical method used to find out abnomal values in a series of values present.

- Rule 2: to detect multiple transactions in a short time span. Indentifing the users with more than 3 transactions in 5 mins.

- Rule 3: to detect multiple transactions at the same merchant. Indentifing the users with more than 7 transactions in span of 2 days with same marchant. 
    - This rule will helps in detecting any malious merchant with users' stored credit card or wallet data misusing the user data.

- Rule 4: to detect same amounts spent in a short time span. This is to identify users with same amount spent in more than 3 transcations with in 30 minutes.

- Rule 5: to detect transactions with misspelled merchant names. Helps to detect malious/pishing websites using user details.

- Rule 6: detect transactions adding up to $15,000 within 24 hours. Helps to flag a users activity with more 15,000 spending with span of 24 hrs.


**Note: All the above contants values are assumtions made for the sake of problem statment.**


# Project Structure

- |- .vevn # for vitural python evnironment
- |- transactionMonitor 
    - |-fraud_detector.py # contains all the core logic to flagging transactions
- |- utils
    - |- transcation_generator.py # generates csv file needed.
- |- main.py
- |- requirements.txt # conatins all the py libraries
- |- makefile

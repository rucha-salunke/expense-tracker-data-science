import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Categories and realistic behavior
CATEGORIES = {
    "Food": ["Groceries", "Dining"],
    "Transport": ["Fuel", "Cab"],
    "Bills": ["Electricity", "Internet"],
    "Shopping": ["Clothes", "Electronics"],
    "Entertainment": ["Movies", "Subscriptions"],
    "Rent": ["House Rent"]
}

PAYMENT_MODES = ["Cash", "UPI", "Credit Card", "Debit Card"]
PERSONS = ["Aman", "Riya", "Rahul", "Sneha"]

def generate_data(days=180):
    data = []
    start_date = datetime.today() - timedelta(days=days)

    for i in range(days):
        date = start_date + timedelta(days=i)

        # 1–4 transactions per day
        for _ in range(np.random.randint(1, 5)):
            category = random.choice(list(CATEGORIES.keys()))
            sub_category = random.choice(CATEGORIES[category])

            # realistic spending ranges
            if category == "Rent":
                amount = np.random.randint(8000, 20000)
            elif category == "Food":
                amount = np.random.randint(100, 800)
            else:
                amount = np.random.randint(200, 5000)

            data.append([
                date,
                random.choice(PERSONS),
                category,
                sub_category,
                amount,
                random.choice(PAYMENT_MODES)
            ])

    df = pd.DataFrame(data, columns=[
        "date", "person", "category", "sub_category",
        "amount", "payment_mode"
    ])

    df.to_csv("data/expenses.csv", index=False)
    print("✅ Dataset created!")

if __name__ == "__main__":
    generate_data()
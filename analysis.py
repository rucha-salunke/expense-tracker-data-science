import pandas as pd

# ---------------- LOAD ---------------- #

def load_data(path="data/expenses.csv"):
    df = pd.read_csv(path)
    return df


# ---------------- PREPROCESS ---------------- #

def preprocess_data(df):
    df['date'] = pd.to_datetime(df['date'])

    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.day_name()

    df['is_weekend'] = df['weekday'].isin(['Saturday', 'Sunday'])

    return df


# ---------------- KPI ---------------- #

def compute_kpis(df):
    total_spend = df['amount'].sum()
    transactions = len(df)
    avg_transaction = df['amount'].mean()

    daily = df.groupby('date')['amount'].sum()
    avg_daily = daily.mean()

    top_category = df.groupby('category')['amount'].sum().idxmax()

    return total_spend, transactions, avg_transaction, avg_daily, top_category


# ---------------- AGGREGATIONS ---------------- #

def monthly_spending(df):
    return df.groupby(['month', 'month_num'])['amount'].sum().reset_index().sort_values('month_num')


def payment_distribution(df):
    return df.groupby('payment_mode')['amount'].sum().reset_index()


def person_spending(df):
    return df.groupby('person')['amount'].sum().reset_index().sort_values(by='amount', ascending=False)


def heatmap_data(df):
    pivot = df.pivot_table(
        values='amount',
        index='category',
        columns='month',
        aggfunc='sum'
    )
    return pivot.fillna(0)


def rolling_spending(df):
    daily = df.groupby('date')['amount'].sum().reset_index()
    daily['rolling_avg'] = daily['amount'].rolling(7).mean()
    return daily


# ---------------- BUSINESS LOGIC ---------------- #

def overspending_detection(df, budget=30000):
    monthly = df.groupby(['month', 'month_num'])['amount'].sum().reset_index()
    monthly = monthly.sort_values('month_num')
    monthly['overspend'] = monthly['amount'] > budget
    return monthly


def savings_rate(df, income=100000):
    monthly = df.groupby(['month', 'month_num'])['amount'].sum().reset_index()
    monthly = monthly.sort_values('month_num')

    monthly['savings'] = income - monthly['amount']
    monthly['savings_rate'] = (monthly['savings'] / income) * 100

    return monthly


def top_transactions(df, n=10):
    return df.sort_values(by='amount', ascending=False).head(n)


# ---------------- INSIGHTS ---------------- #

def generate_insights(df):
    total = df['amount'].sum()
    top_cat = df.groupby('category')['amount'].sum().idxmax()

    monthly = df.groupby('month')['amount'].sum()

    peak_month = monthly.idxmax()
    low_month = monthly.idxmin()

    weekend = df[df['is_weekend']]['amount'].mean()
    weekday = df[~df['is_weekend']]['amount'].mean()

    return [
        f"Total Spend: ₹{total:.0f}",
        f"Top Category: {top_cat}",
        f"Peak Month: {peak_month}",
        f"Lowest Month: {low_month}",
        f"Weekend Avg: ₹{weekend:.0f} vs Weekday Avg: ₹{weekday:.0f}"
    ]
    
    # ---------------- EXTRA (FOR MAIN.PY) ---------------- #

def category_analysis(df):
    return df.groupby('category')['amount'].sum().sort_values(ascending=False)


def monthly_trends(df):
    return df.groupby(['month', 'month_num'])['amount'].sum().reset_index().sort_values('month_num')
import matplotlib.pyplot as plt
import seaborn as sns

from src.analysis import *

# Load data
df = load_data()

# KPIs
print("\n📊 KPIs")
kpis = compute_kpis(df)
for k, v in kpis.items():
    print(f"{k}: {v}")

# ---------------- CATEGORY CHART ---------------- #
plt.figure()
cat = category_analysis(df)
cat.plot(kind='bar', title="Category Spending")
plt.ylabel("Amount")
plt.show()

# ---------------- MONTHLY TREND ---------------- #
plt.figure()
monthly = monthly_trends(df)
sns.lineplot(data=monthly, x='month', y='amount')
plt.title("Monthly Spending Trend")
plt.xticks(rotation=45)
plt.show()

# ---------------- HEATMAP ---------------- #
plt.figure()
pivot = df.pivot_table(values='amount', index='category', columns='month', aggfunc='sum')
sns.heatmap(pivot, cmap='coolwarm')
plt.title("Category vs Month Heatmap")
plt.show()

# ---------------- INSIGHTS ---------------- #
print("\n🧠 Insights")
for i in generate_insights(df):
    print("-", i)
    
    
    
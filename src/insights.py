def generate_insights(df):

    insights = []

    # Best category
    best_cat = df.groupby("Category")["Profit"].sum().idxmax()
    insights.append(f"🏆 Most profitable category: {best_cat}")

    # Loss category
    loss_cat = df.groupby("Category")["Profit"].sum().idxmin()
    insights.append(f"⚠️ Loss generating category: {loss_cat}")

    # High discount risk
    risky = df[df["Discount"] > 0.3]["Profit"].mean()

    if risky < 0:
        insights.append("🚨 Discounts above 30% usually cause losses")

    return insights
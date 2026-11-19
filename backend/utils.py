import pandas as pd


def safe_div(a, b, default=0.0):
    try:
        return float(a / b) if float(b) != 0.0 else float(default)
    except Exception:
        return float(default)


def profit_recommendation(pred_profit: float) -> str:
    if pred_profit > 500:
        return "✅ Highly Profitable — Increase Marketing"
    elif pred_profit > 0:
        return "👍 Profitable — Maintain Strategy"
    elif pred_profit > -500:
        return "⚠️ Low Profit — Reduce Discount"
    else:
        return "❌ Loss — Stop Selling / Review Pricing"


def health_score_from_margin(profit_margin: float) -> int:
    """
    Convert profit margin to 0..100.
    -20% => 0
      0% => 50
     20% => 100
    """
    m = max(-0.2, min(0.2, float(profit_margin)))
    score = int(round((m + 0.2) / 0.4 * 100))
    return max(0, min(100, score))


def scenario_health_score(base_score: int, scenario_pred_profit: float) -> int:
    """
    Dynamic score: adjusts the base score based on scenario predicted profit.
    """
    if scenario_pred_profit > 1000:
        adj = +18
    elif scenario_pred_profit > 500:
        adj = +12
    elif scenario_pred_profit > 0:
        adj = +6
    elif scenario_pred_profit > -500:
        adj = -6
    else:
        adj = -12

    return max(0, min(100, int(base_score) + adj))


def generate_insights(df):
    insights = []
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    margin = safe_div(total_profit, total_sales, 0.0)

    cat_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    reg_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)

    best_cat = str(cat_profit.index[0]) if len(cat_profit) else "N/A"
    worst_cat = str(cat_profit.index[-1]) if len(cat_profit) else "N/A"
    best_reg = str(reg_profit.index[0]) if len(reg_profit) else "N/A"
    worst_reg = str(reg_profit.index[-1]) if len(reg_profit) else "N/A"

    loss_orders = int((df["Profit"] < 0).sum())

    insights.append(f"📌 Profit margin: **{margin*100:.2f}%** (Profit / Sales).")
    insights.append(f"🏆 Best category (profit): **{best_cat}**.")
    insights.append(f"⚠️ Worst category (profit): **{worst_cat}**.")
    insights.append(f"🌍 Best region (profit): **{best_reg}**.")
    insights.append(f"🚩 Worst region (profit): **{worst_reg}**.")
    insights.append(f"🔻 Loss-making orders: **{loss_orders}**. Focus on discounts + low-margin products.")

    return insights


def _filter(df, category="All", region="All"):
    if category and category != "All":
        df = df[df["Category"] == category]
    if region and region != "All":
        df = df[df["Region"] == region]
    return df


def build_dashboard(df_all, category="All", region="All"):
    """
    Everything the Overview dashboard needs, in ONE response.
    Region and Category charts ignore their own filter, so the chart
    still shows the comparison (same idea as the old Sales page).
    """
    df_all = df_all.copy()
    df_all["Order Date"] = pd.to_datetime(df_all["Order Date"], format="mixed", errors="coerce")

    df = _filter(df_all, category, region)

    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    margin = safe_div(total_profit, total_sales, 0.0)

    kpis = {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "profit_margin": margin,
        "orders": int(df["Order ID"].nunique()),
        "quantity": int(df["Quantity"].sum()),
        "avg_discount": float(df["Discount"].mean()) if len(df) else 0.0,
        "health_score": health_score_from_margin(margin),
    }

    def group(frame, col, top=None):
        g = (
            frame.groupby(col)[["Sales", "Profit"]]
            .sum()
            .sort_values("Sales", ascending=False)
        )
        if top:
            g = g.head(top)
        return [
            {"name": str(i), "sales": round(float(r["Sales"]), 2), "profit": round(float(r["Profit"]), 2)}
            for i, r in g.iterrows()
        ]

    by_region = group(_filter(df_all, category, "All"), "Region")
    by_category = group(_filter(df_all, "All", region), "Category")
    by_segment = group(df, "Segment")
    by_subcategory = group(df, "Sub-Category", top=10)
    by_state = group(df, "State")

    # Sales per quarter, one line per region
    quarters = pd.period_range(df_all["Order Date"].min(), df_all["Order Date"].max(), freq="Q")
    d = df.dropna(subset=["Order Date"]).copy()
    d["Q"] = d["Order Date"].dt.to_period("Q")
    pivot = d.pivot_table(index="Q", columns="Region", values="Sales", aggfunc="sum", fill_value=0)
    pivot = pivot.reindex(quarters, fill_value=0)

    trend = {
        "labels": [f"{q.year} Q{q.quarter}" for q in quarters],
        "series": [
            {"region": str(col), "values": [round(float(v), 2) for v in pivot[col].tolist()]}
            for col in pivot.columns
        ],
    }

    return {
        "kpis": kpis,
        "by_region": by_region,
        "by_category": by_category,
        "by_segment": by_segment,
        "by_subcategory": by_subcategory,
        "by_state": by_state,
        "trend": trend,
    }

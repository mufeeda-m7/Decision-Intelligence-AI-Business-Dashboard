# ==============================
# PROFIT RECOMMENDATION
# ==============================

def profit_recommendation(profit):

    if profit > 500:
        return "✅ Highly Profitable — Increase Marketing"
    elif profit > 0:
        return "👍 Profitable — Maintain Strategy"
    elif profit > -500:
        return "⚠️ Low Profit — Reduce Discount"
    else:
        return "❌ Loss — Review Pricing Strategy"


# ==============================
# STATIC BUSINESS HEALTH (DATASET)
# ==============================

def business_health_score(df):

    profit_ratio = df["Profit"].sum() / df["Sales"].sum()

    score = max(0, min(100, int((profit_ratio + 0.2) * 250)))

    return score


# ==============================
# DYNAMIC AI HEALTH SCORE ⭐
# ==============================

def dynamic_health_score(predicted_profit):

    if predicted_profit > 500:
        return 90
    elif predicted_profit > 0:
        return 70
    elif predicted_profit > -500:
        return 50
    else:
        return 30
    
    def dynamic_health_score(predicted_profit):
    # profit is predicted profit for a scenario (total)
      if predicted_profit > 500:
        return 90
      elif predicted_profit > 0:
        return 70
      elif predicted_profit > -500:
        return 50
      else:
        return 30


def scenario_health_score(total_pred_profit, total_sales):
    """
    A more stable scenario score using margin % (better than only profit)
    """
    if total_sales <= 0:
        return 0

    margin = total_pred_profit / total_sales  # profit margin
    # Convert margin into 0-100 score (tweakable)
    score = int((margin + 0.2) * 250)  # same logic style you used
    score = max(0, min(100, score))
    return score
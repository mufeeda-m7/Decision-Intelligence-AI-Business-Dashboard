from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import os
import pickle
from typing import List

from backend.utils import (
    safe_div,
    profit_recommendation,
    health_score_from_margin,
    scenario_health_score,
    generate_insights,
    build_dashboard,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "superstore.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "profit_model.pkl")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = FastAPI(title="Decision Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_data():
    return pd.read_csv(DATA_PATH, encoding="latin1")


def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def apply_filters(df: pd.DataFrame, category: str, region: str):
    if category and category != "All":
        df = df[df["Category"] == category]
    if region and region != "All":
        df = df[df["Region"] == region]
    return df


def product_baseline(df: pd.DataFrame, product_name: str):
    """
    Realistic baseline:
    Use MEDIAN Sales & Quantity from history for that product.
    """
    sub = df[df["Product Name"] == product_name]
    if sub.empty:
        return None
    base_sales = float(sub["Sales"].median())
    base_qty = int(sub["Quantity"].median())
    return base_sales, base_qty


# ------------------ Schemas ------------------

class Filters(BaseModel):
    category: str = "All"
    region: str = "All"


class SingleSimRequest(BaseModel):
    product: str
    discount: float = Field(ge=0.0, le=1.0)
    category: str = "All"
    region: str = "All"


class ScenarioItem(BaseModel):
    product: str
    discount: float = Field(ge=0.0, le=1.0)


class ScenarioRequest(BaseModel):
    items: List[ScenarioItem]
    category: str = "All"
    region: str = "All"


# ------------------ API ------------------

@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/filters")
def filters(_: dict = None):
    df = load_data()
    cats = ["All"] + sorted(df["Category"].dropna().unique().tolist())
    regs = ["All"] + sorted(df["Region"].dropna().unique().tolist())
    return {"categories": cats, "regions": regs}


@app.post("/api/products")
def products(filters: Filters):
    df = load_data()
    df = apply_filters(df, filters.category, filters.region)
    prods = sorted(df["Product Name"].dropna().unique().tolist())
    return {"products": prods}


@app.post("/api/metrics")
def metrics(filters: Filters):
    df = load_data()
    df = apply_filters(df, filters.category, filters.region)

    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    orders = int(df.shape[0])
    margin = safe_div(total_profit, total_sales, 0.0)

    base_score = health_score_from_margin(margin)

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "orders": orders,
        "profit_margin": margin,
        "overall_health_score": base_score
    }


@app.post("/api/dashboard")
def dashboard(filters: Filters):
    df = load_data()
    return build_dashboard(df, filters.category, filters.region)


@app.post("/api/sales_by_category")
def sales_by_category(filters: Filters):
    df = load_data()
    df = apply_filters(df, "All", filters.region)  # region filter only
    data = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .to_dict(orient="records")
    )
    return {"data": data}


@app.post("/api/profit_by_region")
def profit_by_region(filters: Filters):
    df = load_data()
    df = apply_filters(df, filters.category, "All")  # category filter only
    data = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .to_dict(orient="records")
    )
    return {"data": data}


@app.post("/api/loss_products")
def loss_products(filters: Filters):
    df = load_data()
    df = apply_filters(df, filters.category, filters.region)

    loss_df = df[df["Profit"] < 0].sort_values("Profit").head(15)
    cols = ["Product Name", "Category", "Region", "Sales", "Profit", "Discount", "Quantity"]
    return {"data": loss_df[cols].to_dict(orient="records")}


@app.post("/api/insights")
def insights(filters: Filters):
    df = load_data()
    df = apply_filters(df, filters.category, filters.region)
    return {"insights": generate_insights(df)}


@app.post("/api/simulate_single")
def simulate_single(req: SingleSimRequest):
    df = load_data()
    df_filtered = apply_filters(df, req.category, req.region)

    # overall health from filtered dataset
    total_sales = float(df_filtered["Sales"].sum())
    total_profit = float(df_filtered["Profit"].sum())
    margin = safe_div(total_profit, total_sales, 0.0)
    overall_score = health_score_from_margin(margin)

    baseline = product_baseline(df_filtered, req.product) or product_baseline(df, req.product)
    if baseline is None:
        return {"error": "Product not found in dataset"}

    base_sales, base_qty = baseline

    model = load_model()
    pred_profit = float(model.predict([[base_sales, base_qty, req.discount]])[0])

    reco = profit_recommendation(pred_profit)
    scenario_score = scenario_health_score(overall_score, pred_profit)

    return {
        "baseline_sales": base_sales,
        "baseline_quantity": base_qty,
        "predicted_profit": pred_profit,
        "recommendation": reco,
        "overall_health_score": overall_score,
        "scenario_health_score": scenario_score
    }


@app.post("/api/simulate_scenario")
def simulate_scenario(req: ScenarioRequest):
    df = load_data()
    df_filtered = apply_filters(df, req.category, req.region)

    # overall health from filtered dataset
    total_sales = float(df_filtered["Sales"].sum())
    total_profit = float(df_filtered["Profit"].sum())
    margin = safe_div(total_profit, total_sales, 0.0)
    overall_score = health_score_from_margin(margin)

    model = load_model()

    results = []
    scenario_total_pred_profit = 0.0
    scenario_total_sales = 0.0

    for item in req.items:
        baseline = product_baseline(df_filtered, item.product) or product_baseline(df, item.product)
        if baseline is None:
            continue

        base_sales, base_qty = baseline
        pred_profit = float(model.predict([[base_sales, base_qty, item.discount]])[0])

        scenario_total_pred_profit += pred_profit
        scenario_total_sales += base_sales

        results.append({
            "product": item.product,
            "baseline_sales": round(base_sales, 2),
            "baseline_quantity": int(base_qty),
            "discount": float(item.discount),
            "predicted_profit": round(pred_profit, 2),
            "recommendation": profit_recommendation(pred_profit)
        })

    scenario_score = scenario_health_score(overall_score, scenario_total_pred_profit)

    return {
        "items": results,
        "scenario_total_sales": round(scenario_total_sales, 2),
        "scenario_total_pred_profit": round(scenario_total_pred_profit, 2),
        "overall_health_score": overall_score,
        "scenario_health_score": scenario_score
    }


# ✅ mount frontend last (so /api routes work)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
// Works when the page is served by FastAPI (same address),
// and also when you open the HTML file directly.
const API_BASE = location.protocol.startsWith("http") ? "" : "http://127.0.0.1:8000";

const PALETTE = ["#1e3a8a", "#2563eb", "#38bdf8", "#14b8a6", "#8b5cf6", "#f59e0b"];
const charts = {};

/* ---------------- helpers ---------------- */
const PAGES = [
  ["overview", "index.html", "Overview"],
  ["sales", "sales.html", "Sales Analytics"],
  ["losses", "losses.html", "Loss Products"],
  ["simulator", "simulator.html", "Profit Simulator"],
  ["insights", "insights.html", "Insights"],
];

function esc(text) {
  const d = document.createElement("div");
  d.textContent = String(text);
  return d.innerHTML;
}

function money(n) {
  const sign = n < 0 ? "-" : "";
  const a = Math.abs(n);
  if (a >= 1e6) return `${sign}$${(a / 1e6).toFixed(2)}M`;
  if (a >= 1e3) return `${sign}$${(a / 1e3).toFixed(0)}K`;
  return `${sign}$${a.toFixed(2)}`;
}

function getFilters() {
  return {
    category: localStorage.getItem("category") || "All",
    region: localStorage.getItem("region") || "All",
  };
}

async function post(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function makeChart(id, config) {
  if (charts[id]) charts[id].destroy();
  const ctx = document.getElementById(id);
  if (!ctx) return;
  charts[id] = new Chart(ctx, config);
}

/* ---------------- header + filter bar (shared by all pages) ---------------- */
async function renderShell() {
  const page = document.body.dataset.page;
  const links = PAGES.map(
    ([key, href, label]) =>
      `<a href="${href}" class="${key === page ? "active" : ""}">${label}</a>`
  ).join("");

  document.getElementById("shell").innerHTML = `
    <header class="topbar">
      <div class="brand">
        <div class="logo">DI</div>
        <div><h1>Decision Intelligence</h1><p>AI Business Dashboard</p></div>
      </div>
      <nav class="nav">${links}</nav>
      <span id="statusBadge" class="status ok">● Online</span>
    </header>
    <div class="filterbar">
      <div><label for="categoryFilter">Category</label><select id="categoryFilter"></select></div>
      <div><label for="regionFilter">Region</label><select id="regionFilter"></select></div>
      <button class="btn ghost" id="resetBtn">Reset</button>
    </div>`;

  const data = await post("/api/filters", {});
  const fill = (id, items, saved) => {
    const el = document.getElementById(id);
    el.innerHTML = items.map((v) => `<option value="${esc(v)}">${esc(v)}</option>`).join("");
    el.value = saved;
  };
  const f = getFilters();
  fill("categoryFilter", data.categories, f.category);
  fill("regionFilter", data.regions, f.region);

  const save = () => {
    localStorage.setItem("category", document.getElementById("categoryFilter").value);
    localStorage.setItem("region", document.getElementById("regionFilter").value);
    location.reload();
  };
  document.getElementById("categoryFilter").addEventListener("change", save);
  document.getElementById("regionFilter").addEventListener("change", save);
  document.getElementById("resetBtn").addEventListener("click", () => {
    localStorage.setItem("category", "All");
    localStorage.setItem("region", "All");
    location.reload();
  });
}

/* ---------------- Overview dashboard ---------------- */
const STATE_ABBR = {
  "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
  "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
  "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
  "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
  "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
  "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
  "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
  "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
  "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
  "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
  "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
};

// [row, column] of each state in the tile map
const TILE_POS = {
  AK: [0, 0], ME: [0, 10],
  VT: [1, 9], NH: [1, 10],
  WA: [2, 0], ID: [2, 1], MT: [2, 2], ND: [2, 3], MN: [2, 4], IL: [2, 5], WI: [2, 6],
  MI: [2, 7], NY: [2, 8], RI: [2, 9], MA: [2, 10],
  OR: [3, 0], NV: [3, 1], WY: [3, 2], SD: [3, 3], IA: [3, 4], IN: [3, 5], OH: [3, 6],
  PA: [3, 7], NJ: [3, 8], CT: [3, 9],
  CA: [4, 0], UT: [4, 1], CO: [4, 2], NE: [4, 3], MO: [4, 4], KY: [4, 5], WV: [4, 6],
  VA: [4, 7], MD: [4, 8], DE: [4, 9],
  AZ: [5, 1], NM: [5, 2], KS: [5, 3], AR: [5, 4], TN: [5, 5], NC: [5, 6], SC: [5, 7], DC: [5, 8],
  OK: [6, 3], LA: [6, 4], MS: [6, 5], AL: [6, 6], GA: [6, 7],
  HI: [7, 0], TX: [7, 3], FL: [7, 8],
};

function mixColor(t) {
  // light blue -> dark blue
  const a = [219, 234, 254], b = [30, 58, 138];
  const c = a.map((v, i) => Math.round(v + (b[i] - v) * t));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}

function drawTileMap(byState) {
  const sales = {};
  byState.forEach((s) => { sales[STATE_ABBR[s.name]] = s.sales; });
  const max = Math.max(...Object.values(sales), 1);

  const rows = 8, cols = 11;
  const grid = Array.from({ length: rows }, () => Array(cols).fill(null));
  Object.entries(TILE_POS).forEach(([abbr, [r, c]]) => { grid[r][c] = abbr; });

  let html = "";
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const abbr = grid[r][c];
      if (!abbr) { html += `<div></div>`; continue; }
      const v = sales[abbr];
      if (v === undefined) {
        html += `<div class="tile" title="${abbr}: no sales">${abbr}</div>`;
      } else {
        const t = Math.sqrt(v / max); // sqrt so small states are still visible
        html += `<div class="tile has ${t < 0.45 ? "light" : ""}" style="background:${mixColor(t)}" title="${abbr}: ${money(v)}">${abbr}</div>`;
      }
    }
  }
  document.getElementById("tileMap").innerHTML = html;
}

async function loadOverview() {
  const d = await post("/api/dashboard", getFilters());
  const k = d.kpis;

  setText("kSales", money(k.total_sales));
  setText("kProfit", money(k.total_profit));
  setText("kMargin", `${(k.profit_margin * 100).toFixed(1)}%`);
  setText("kOrders", k.orders.toLocaleString());
  setText("kDiscount", `${(k.avg_discount * 100).toFixed(1)}%`);
  setText("kHealth", `${k.health_score}/100`);
  document.getElementById("healthFill").style.width = `${k.health_score}%`;
  if (k.total_profit < 0) document.getElementById("kProfit").classList.add("neg");

  const tipMoney = { callbacks: { label: (c) => ` ${c.label}: ${money(c.parsed.y ?? c.parsed.x ?? c.parsed)}` } };

  makeChart("regionChart", {
    type: "pie",
    data: {
      labels: d.by_region.map((r) => r.name),
      datasets: [{ data: d.by_region.map((r) => r.sales), backgroundColor: PALETTE, borderWidth: 2, borderColor: "#fff" }],
    },
    options: { maintainAspectRatio: false, plugins: { legend: { position: "bottom" }, tooltip: tipMoney } },
  });

  makeChart("categoryChart", {
    type: "bar",
    data: {
      labels: d.by_category.map((r) => r.name),
      datasets: [{ data: d.by_category.map((r) => r.sales), backgroundColor: ["#2563eb", "#38bdf8", "#14b8a6"], borderRadius: 8 }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: tipMoney },
      scales: { y: { ticks: { callback: (v) => money(v) } } },
    },
  });

  makeChart("segmentChart", {
    type: "doughnut",
    data: {
      labels: d.by_segment.map((r) => r.name),
      datasets: [{ data: d.by_segment.map((r) => r.sales), backgroundColor: ["#2563eb", "#1e3a8a", "#38bdf8"], borderWidth: 2, borderColor: "#fff" }],
    },
    options: { maintainAspectRatio: false, cutout: "58%", plugins: { legend: { position: "bottom" }, tooltip: tipMoney } },
  });

  makeChart("subChart", {
    type: "bar",
    data: {
      labels: d.by_subcategory.map((r) => r.name),
      datasets: [{ data: d.by_subcategory.map((r) => r.sales), backgroundColor: "#38bdf8", borderRadius: 6 }],
    },
    options: {
      indexAxis: "y",
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: tipMoney },
      scales: { x: { ticks: { callback: (v) => money(v) } } },
    },
  });

  drawTileMap(d.by_state);

  const fills = ["rgba(30,58,138,.55)", "rgba(37,99,235,.55)", "rgba(56,189,248,.55)", "rgba(20,184,166,.55)"];
  makeChart("trendChart", {
    type: "line",
    data: {
      labels: d.trend.labels,
      datasets: d.trend.series.map((s, i) => ({
        label: s.region,
        data: s.values,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 1.5,
        borderColor: PALETTE[i % PALETTE.length],
        backgroundColor: fills[i % fills.length],
      })),
    },
    options: {
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: { legend: { position: "bottom" } },
      scales: { y: { stacked: true, ticks: { callback: (v) => money(v) } }, x: { ticks: { maxTicksLimit: 8 } } },
    },
  });
}

/* ---------------- Sales Analytics page ---------------- */
async function loadSalesPage() {
  const d = await post("/api/dashboard", getFilters());
  const make = (id, rows) =>
    makeChart(id, {
      type: "bar",
      data: {
        labels: rows.map((r) => r.name),
        datasets: [
          { label: "Sales", data: rows.map((r) => r.sales), backgroundColor: "#2563eb", borderRadius: 6 },
          { label: "Profit", data: rows.map((r) => r.profit), backgroundColor: "#14b8a6", borderRadius: 6 },
        ],
      },
      options: {
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom" } },
        scales: { y: { ticks: { callback: (v) => money(v) } } },
      },
    });
  make("catChart", d.by_category);
  make("regChart", d.by_region);
}

/* ---------------- Loss products ---------------- */
async function loadLossProducts() {
  const d = await post("/api/loss_products", getFilters());
  document.getElementById("lossTableBody").innerHTML = d.data
    .map(
      (r) => `<tr>
        <td>${esc(r["Product Name"])}</td>
        <td>${esc(r.Category)}</td>
        <td>${esc(r.Region)}</td>
        <td>$${r.Sales.toFixed(2)}</td>
        <td class="neg">-$${Math.abs(r.Profit).toFixed(2)}</td>
        <td>${Math.round(r.Discount * 100)}%</td>
      </tr>`
    )
    .join("");
}

/* ---------------- Insights ---------------- */
async function loadInsights() {
  const d = await post("/api/insights", getFilters());
  // the API sends **bold** markers; turn them into real bold text
  document.getElementById("insightsList").innerHTML = d.insights
    .map((t) => `<li>${esc(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")}</li>`)
    .join("");
}

/* ---------------- Simulator ---------------- */
async function loadProductOptions() {
  const d = await post("/api/products", getFilters());
  document.getElementById("productSelect").innerHTML = d.products
    .map((p) => `<option value="${esc(p)}">${esc(p)}</option>`)
    .join("");
}

async function runSingleSimulation() {
  const product = document.getElementById("productSelect").value;
  const discount = parseFloat(document.getElementById("discountInput").value);
  const d = await post("/api/simulate_single", { product, discount, ...getFilters() });

  if (d.error) {
    setText("recommendation", d.error);
    return;
  }

  const big = document.getElementById("predictedProfit");
  big.textContent = money(d.predicted_profit);
  big.className = `big-number ${d.predicted_profit >= 0 ? "pos" : "neg"}`;

  setText("baselineSales", `$${d.baseline_sales.toFixed(2)}`);
  setText("baselineQuantity", d.baseline_quantity);
  setText("scenarioHealth", `${d.scenario_health_score}/100`);
  document.getElementById("scenarioFill").style.width = `${d.scenario_health_score}%`;
  setText("recommendation", d.recommendation);
}

/* ---------------- start ---------------- */
async function initPage() {
  try {
    await renderShell();
    const page = document.body.dataset.page;

    if (page === "overview") await loadOverview();
    if (page === "sales") await loadSalesPage();
    if (page === "losses") await loadLossProducts();
    if (page === "insights") await loadInsights();
    if (page === "simulator") {
      await loadProductOptions();
      const slider = document.getElementById("discountInput");
      slider.addEventListener("input", () => {
        setText("discountValue", `${Math.round(slider.value * 100)}%`);
      });
    }
  } catch (err) {
    console.error(err);
    const badge = document.getElementById("statusBadge");
    if (badge) {
      badge.textContent = "● Error - is the backend running?";
      badge.className = "status err";
    }
  }
}

window.addEventListener("load", initPage);

import streamlit as st
import pandas as pd
import plotly.express as px
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MetroPulse | Urban Mobility Intelligence",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATA
# ============================================================

DATA_DIR = "dashboard/data"


@st.cache_data
def load_data(file_name):
    return pd.read_csv(os.path.join(DATA_DIR, file_name))


executive = load_data("mart_executive_summary.csv")
daily = load_data("mart_daily_demand.csv")
hourly = load_data("mart_hourly_demand.csv")
zones = load_data("mart_zone_performance.csv")
payments = load_data("mart_payment_analysis.csv")
weather = load_data("mart_weather_demand.csv")
transit = load_data("mart_transit_demand.csv")

kpi = executive.iloc[0]

daily["trip_date"] = pd.to_datetime(daily["trip_date"])
# ============================================================
# DATE FILTER
# ============================================================

st.sidebar.markdown("### 📅 Date Filter")

min_date = daily["trip_date"].min().date()
max_date = daily["trip_date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range

    daily_filtered = daily[
        (daily["trip_date"].dt.date >= start_date) &
        (daily["trip_date"].dt.date <= end_date)
    ]
else:
    daily_filtered = daily
    # ============================================================
# BOROUGH FILTER
# ============================================================

st.sidebar.markdown("### 🏙️ Borough Filter")

# Check which borough column actually exists
if "borough" in zones.columns:
    borough_column = "borough"
elif "pickup_borough" in zones.columns:
    borough_column = "pickup_borough"
else:
    borough_column = None

if borough_column is not None:

    borough_options = ["All Boroughs"] + sorted(
        zones[borough_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_borough = st.sidebar.selectbox(
        "Select borough",
        borough_options
    )

    if selected_borough == "All Boroughs":
        zones_filtered = zones
    else:
        zones_filtered = zones[
            zones[borough_column].astype(str) == selected_borough
        ]

else:

    selected_borough = "All Boroughs"
    zones_filtered = zones

    st.sidebar.warning(
        "Borough data is not available in the zone dataset."
    )


# ============================================================
# CLASSIC DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #0b1120;
    }

    .main {
        background: #0b1120;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* ---------- ALL HEADINGS ---------- */

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    p, span, label, div {
        color: inherit;
    }

    .stMarkdown p {
        color: #d1d5db;
    }

    /* ---------- HERO ---------- */

    .hero {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    }

    .hero-title {
        color: #ffffff !important;
        font-size: 42px;
        font-weight: 750;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        color: #9ca3af !important;
        font-size: 16px;
        margin-top: 3px;
    }

    /* ---------- SECTION HEADINGS ---------- */

    .section-header {
        color: #ffffff !important;
        font-size: 25px;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 4px;
        letter-spacing: -0.3px;
    }

    .section-description {
        color: #9ca3af !important;
        font-size: 14px;
        margin-bottom: 14px;
    }

    /* ---------- KPI CARDS ---------- */

    div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #111827,
        #172033
    );
    border: 1px solid #263244;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    transition: all 0.2s ease;
}

    div[data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-size: 13px;
    }

    div[data-testid="stMetricValue"] {
    color: #22D3EE !important;
    font-size: 28px;
    font-weight: 750;
}

    /* ---------- CHART CONTAINERS ---------- */

    div[data-testid="stPlotlyChart"] {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 14px;
        padding: 8px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    }

    /* ---------- INSIGHT CARDS ---------- */

    .insight-card {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 14px;
        padding: 18px;
        min-height: 105px;
    }

    .insight-title {
        color: #ffffff !important;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .insight-text {
        color: #9ca3af !important;
        font-size: 14px;
        line-height: 1.5;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #080d18;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #d1d5db !important;
    }

    /* ---------- INFO BOX ---------- */

    div[data-testid="stAlert"] {
        background: #111827;
        border: 1px solid #263244;
    }

    /* ---------- DIVIDER ---------- */

    hr {
        border-color: #263244 !important;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #6b7280 !important;
        font-size: 12px;
        padding-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "<h2 style='color:#ffffff;'>🚕 MetroPulse</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#9ca3af;'>Urban Mobility Intelligence</p>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        "<h4 style='color:#ffffff;'>Analysis Period</h4>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background:#111827;
            border:1px solid #263244;
            border-radius:10px;
            padding:12px;
            color:#d1d5db;
        ">
        <b style="color:white;">01 Apr 2024</b><br>
        to<br>
        <b style="color:white;">30 Jun 2024</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<h4 style='color:#ffffff;'>Data Sources</h4>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="color:#d1d5db;">🚕 NYC TLC Taxi</p>
        <p style="color:#d1d5db;">🌦 Historical Weather</p>
        <p style="color:#d1d5db;">🚇 MTA Subway</p>
        <p style="color:#d1d5db;">📍 NYC Taxi Zones</p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        "<p style='color:#6b7280;font-size:12px;'>MetroPulse analytical platform<br>Python • DuckDB • SQL • Streamlit</p>",
        unsafe_allow_html=True
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🚕 MetroPulse</div>
        <div class="hero-subtitle">
            NYC Urban Mobility Intelligence
        </div>
        <div class="hero-subtitle">
            Demand • Revenue • Zones • Weather • Transit
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.markdown(
    "<div class='section-header'>Executive Overview</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='section-description'>Key mobility indicators across the three-month analysis period.</div>",
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Trips",
    f"{int(kpi['total_trips']):,}"
)

c2.metric(
    "Charged Amount",
    f"${kpi['total_revenue']/1_000_000:.2f}M"
)

c3.metric(
    "Avg Amount / Trip",
    f"${kpi['avg_amount_per_trip']:.2f}"
)

c4.metric(
    "Median Duration",
    f"{kpi['median_trip_duration_minutes']:.0f} min"
)


st.markdown("<br>", unsafe_allow_html=True)


c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "Passengers",
    f"{int(kpi['total_passengers']):,}"
)

c6.metric(
    "Peak-Hour Share",
    f"{kpi['peak_hour_share_pct']:.2f}%"
)

c7.metric(
    "Airport Share",
    f"{kpi['airport_trip_share_pct']:.2f}%"
)

c8.metric(
    "Rainy-Hour Share",
    f"{kpi['rainy_trip_share_pct']:.2f}%"
)


# ============================================================
# KEY FINDINGS
# ============================================================

st.markdown(
    "<div class='section-header'>Key Findings</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='section-description'>Observed patterns from the analytical dataset.</div>",
    unsafe_allow_html=True
)

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">Peak Demand</div>
            <div class="insight-text">
            25.62% of recorded taxi trips occurred between
            17:00 and 20:00.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with i2:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">Weather Pattern</div>
            <div class="insight-text">
            17.94% of recorded trips occurred during
            hours with measurable precipitation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with i3:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">Transit Relationship</div>
            <div class="insight-text">
            Taxi trips and subway ridership showed a
            Pearson correlation of 0.6748.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DEMAND
# ============================================================

st.markdown(
    "<div class='section-header'>Demand Intelligence</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='section-description'>How taxi demand changes across dates and hours.</div>",
    unsafe_allow_html=True
)


fig_daily = px.line(
    daily_filtered,
    x="trip_date",
    y="total_trips",
    labels={
        "trip_date": "Date",
        "total_trips": "Trips"
    }
)
fig_daily.update_traces(
    line=dict(
        color="#205962",
        width=3
    )
)

fig_daily.update_layout(
    height=420,
    paper_bgcolor="#222A3B",
    plot_bgcolor="#111827",
    font=dict(color="#d1d5db"),
    xaxis=dict(
        gridcolor="#263244"
    ),
    yaxis=dict(
        gridcolor="#263244"
    ),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig_daily,
    use_container_width=True
)

# ============================================================
# FILTERED HOURLY DEMAND
# ============================================================

hourly["trip_date"] = pd.to_datetime(hourly["trip_date"])

if len(date_range) == 2:

    hourly_filtered = hourly[
        (hourly["trip_date"].dt.date >= start_date) &
        (hourly["trip_date"].dt.date <= end_date)
    ]

else:

    hourly_filtered = hourly


hourly_summary = (
    hourly_filtered
    .groupby("pickup_hour", as_index=False)
    .agg(
        total_trips=("total_trips", "sum")
    )
)


fig_hourly = px.bar(
    hourly_summary,
    x="pickup_hour",
    y="total_trips",
    labels={
        "pickup_hour": "Hour of Day",
        "total_trips": "Trips"
    }
)
fig_hourly.update_traces(
    marker_color="#25B7D8"
)

fig_hourly.update_layout(
    height=420,
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="#d1d5db"),
    xaxis=dict(gridcolor="#263244"),
    yaxis=dict(gridcolor="#263244"),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig_hourly,
    use_container_width=True
)
# ============================================================
# MONTHLY DEMAND
# ============================================================

monthly_summary = (
    daily_filtered
    .assign(
        month=daily_filtered["trip_date"].dt.strftime("%b %Y")
    )
    .groupby("month", as_index=False)
    .agg(
        total_trips=("total_trips", "sum")
    )
)

month_order = ["Apr 2024", "May 2024", "Jun 2024"]

monthly_summary["month"] = pd.Categorical(
    monthly_summary["month"],
    categories=month_order,
    ordered=True
)

monthly_summary = monthly_summary.sort_values("month")

st.markdown(
    "<div class='section-description'>Monthly taxi demand across the selected period.</div>",
    unsafe_allow_html=True
)

fig_monthly = px.bar(
    monthly_summary,
    x="month",
    y="total_trips",
    labels={
        "month": "Month",
        "total_trips": "Trips"
    }
)

fig_monthly.update_traces(
    marker_color="#C3C7EE"
)

fig_monthly.update_layout(
    height=420,
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="#d1d5db"),
    xaxis=dict(
        gridcolor="#263244"
    ),
    yaxis=dict(
        gridcolor="#263244"
    ),
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# ============================================================
# ZONES
# ============================================================

st.markdown(
    "<div class='section-header'>Zone Performance</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='section-description'>Highest-volume pickup zones during the analysis period.</div>",
    unsafe_allow_html=True
)


top_zones = (
    zones_filtered
    .sort_values("total_trips", ascending=False)
    .head(15)
    .sort_values("total_trips")
)


fig_zones = px.bar(
    top_zones,
    x="total_trips",
    y="zone",
    orientation="h",
    labels={
        "total_trips": "Trips",
        "zone": "Pickup Zone"
    }
)
fig_zones.update_traces(
    marker_color="#448E97"
)

fig_zones.update_layout(
    height=560,
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="#d1d5db"),
    xaxis=dict(gridcolor="#263244"),
    yaxis=dict(gridcolor="#263244"),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig_zones,
    use_container_width=True
)


# ============================================================
# WEATHER + PAYMENT
# ============================================================

st.markdown(
    "<div class='section-header'>External Factors</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='section-description'>Weather and payment behavior across recorded trips.</div>",
    unsafe_allow_html=True
)


w1, w2 = st.columns(2)


with w1:

    fig_weather = px.bar(
        weather,
        x="precipitation_category",
        y="total_trips",
        labels={
            "precipitation_category": "Precipitation",
            "total_trips": "Trips"
        }
    )

    fig_weather.update_layout(
        height=430,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#d1d5db"),
        xaxis=dict(gridcolor="#726A2D"),
        yaxis=dict(gridcolor="#263244"),
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_weather,
        use_container_width=True
    )


with w2:

    fig_payment = px.bar(
        payments,
        x="payment_type",
        y="total_trips",
        labels={
            "payment_type": "Payment Type",
            "total_trips": "Trips"
        }
    )

    fig_payment.update_layout(
    height=430,
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="#d1d5db"),
    xaxis=dict(
        gridcolor="#263244"
    ),
    yaxis=dict(
        gridcolor="#263244"
    ),
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )
)

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )


# ============================================================
# TRANSIT
# ============================================================

st.markdown(
    "<div class='section-header'>Taxi & Subway Relationship</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='section-description'>Hourly relationship between taxi demand and subway ridership.</div>",
    unsafe_allow_html=True
)


transit_plot = transit.dropna(
    subset=["subway_ridership"]
)


fig_transit = px.scatter(
    transit_plot,
    x="subway_ridership",
    y="taxi_trips",
    opacity=0.45,
    labels={
        "subway_ridership": "Subway Ridership",
        "taxi_trips": "Taxi Trips"
    }
)

fig_transit.update_layout(
    height=500,
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="#d1d5db"),
    xaxis=dict(gridcolor="#263244"),
    yaxis=dict(gridcolor="#263244"),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig_transit,
    use_container_width=True
)


st.markdown(
    """
    <div class="insight-card">
        <div class="insight-title">Observed relationship</div>
        <div class="insight-text">
        Pearson correlation = <b style="color:white;">0.6748</b>
        across 2,184 hourly observations.
        Correlation describes association and does not establish causation.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# METHODOLOGY
# ============================================================

st.markdown(
    "<div class='section-header'>Methodology & Data Quality</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="insight-card">

    <div class="insight-title">Data pipeline</div>

    <div class="insight-text">

    Raw sources → Staging → Intermediate transformations → Analytical marts

    <br><br>

    <b style="color:white;">Analysis period:</b>
    April 1, 2024 – June 30, 2024

    <br><br>

    <b style="color:white;">Sources:</b>
    NYC TLC taxi data, NYC taxi zones, historical weather and MTA subway ridership.

    <br><br>

    <b style="color:white;">Quality controls:</b>
    Timestamp validation, financial-value checks, zone uniqueness,
    weather matching and fact-table reconciliation.

    <br><br>

    <b style="color:white;">Interpretation:</b>
    Results are observational and should not be interpreted as causal effects.

    </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        MetroPulse • NYC Urban Mobility Intelligence • 2024 Q2<br>
        Built with Python • SQL • DuckDB • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
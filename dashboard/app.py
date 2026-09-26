import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

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
dropoff = load_data("mart_dropoff_performance.csv")
payments = load_data("mart_payment_analysis.csv")
rate_analysis = load_data("mart_rate_analysis.csv")
airport_analysis = load_data("mart_airport_analysis.csv")
weather = load_data("mart_weather_demand.csv")
transit = load_data("mart_transit_demand.csv")
quality = load_data("mart_quality.csv")

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
# HOUR FILTER
# ============================================================

st.sidebar.markdown("### 🕐 Hour Filter")

hour_options = ["All Hours"] + list(range(24))

selected_hour = st.sidebar.selectbox(
    "Select pickup hour",
    hour_options
)

if selected_hour == "All Hours":
    hourly_filtered = hourly
else:
    hourly_filtered = hourly[
        hourly["pickup_hour"] == selected_hour
    ]
    # ============================================================
# BOROUGH FILTER
# ============================================================


# ============================================================
# BOROUGH + PICKUP ZONE FILTERS
# ============================================================

st.sidebar.markdown("### 🏙️ Location Filters")

# ---------------- BOROUGH FILTER ----------------

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

        zones_filtered = zones.copy()

    else:

        zones_filtered = zones[
            zones[borough_column].astype(str) == selected_borough
        ].copy()

else:

    selected_borough = "All Boroughs"
    zones_filtered = zones.copy()

    st.sidebar.warning(
        "Borough data is not available in the zone dataset."
    )


# ---------------- PICKUP ZONE FILTER ----------------

zone_options = sorted(
    zones_filtered["zone"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_zones = st.sidebar.multiselect(
    "Select pickup zone",
    zone_options,
    placeholder="Search or select zones"
)

if selected_zones:

    zones_filtered = zones_filtered[
        zones_filtered["zone"].isin(selected_zones)
    ].copy()

# ---------------- PAYMENT TYPE FILTER ----------------

st.sidebar.markdown("### 💳 Payment Filter")

payment_options = ["All Payment Types"] + sorted(
    payments["payment_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_payment = st.sidebar.selectbox(
    "Select payment type",
    payment_options
)

# ---------------- WEATHER FILTER ----------------

st.sidebar.markdown("### 🌧️ Weather Filter")

weather_options = ["All Weather Conditions"] + sorted(
    weather["precipitation_category"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_weather = st.sidebar.selectbox(
    "Select weather condition",
    weather_options
)

st.sidebar.markdown("### 📍 Drop-off Filters")

dropoff_borough_options = ["All Drop-off Boroughs"] + sorted(
    dropoff["dropoff_borough"].dropna().astype(str).unique().tolist()
)

selected_dropoff_borough = st.sidebar.selectbox(
    "Select drop-off borough",
    dropoff_borough_options
)

dropoff_zone_options = sorted(
    dropoff["dropoff_zone"].dropna().astype(str).unique().tolist()
)

selected_dropoff_zones = st.sidebar.multiselect(
    "Select drop-off zone",
    dropoff_zone_options,
    placeholder="Search or select drop-off zones"
)


st.sidebar.markdown("### 🚕 Rate Type Filter")

rate_options = ["All Rate Types"] + sorted(
    rate_analysis["rate_code_id"].dropna().astype(str).unique().tolist()
)

selected_rate = st.sidebar.selectbox(
    "Select rate type",
    rate_options
)


st.sidebar.markdown("### ✈️ Airport Trip Filter")

airport_options = ["All Airport Status"] + sorted(
    airport_analysis["airport_flag"].dropna().astype(str).unique().tolist()
)

selected_airport = st.sidebar.selectbox(
    "Select airport status",
    airport_options
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

/* ---------- METRIC LABELS ---------- */

div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] *,
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] span,
div[data-testid="stMetricLabel"] label {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricLabel"] {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

/* ---------- METRIC VALUES ---------- */

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
st.caption(
    f"Last dashboard refresh: {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
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
    f"{int(kpi['total_trips']):,}",
    help="Total number of valid taxi trips included in the analytical dataset after data-quality filtering."
)

c2.metric(
    "Charged Amount",
    f"${kpi['total_revenue']/1_000_000:.2f}M",
    help="Total charged amount recorded across valid taxi trips."
)

c3.metric(
    "Avg Amount / Trip",
    f"${kpi['avg_amount_per_trip']:.2f}",
    help="Average charged amount per valid taxi trip."
)

c4.metric(
    "Median Duration",
    f"{kpi['median_trip_duration_minutes']:.0f} min",
    help="Median taxi trip duration in minutes. Median is used because trip duration can be highly skewed."
)

st.markdown("<br>", unsafe_allow_html=True)


c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "Passengers",
    f"{int(kpi['total_passengers']):,}",
    help="Total recorded passenger count across valid taxi trips."
)

c6.metric(
    "Peak-Hour Share",
    f"{kpi['peak_hour_share_pct']:.2f}%",
    help="Percentage of taxi trips occurring during the defined peak period of 17:00–20:00."
)

c7.metric(
    "Airport Share",
    f"{kpi['airport_trip_share_pct']:.2f}%",
    help="Percentage of taxi trips classified as airport-related trips."
)

c8.metric(
    "Rainy-Hour Share",
    f"{kpi['rainy_trip_share_pct']:.2f}%",
    help="Percentage of recorded taxi trips occurring during hours classified as having measurable precipitation."
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

# Apply date filter first
if len(date_range) == 2:

    hourly_filtered = hourly[
        (hourly["trip_date"].dt.date >= start_date) &
        (hourly["trip_date"].dt.date <= end_date)
    ]

else:

    hourly_filtered = hourly


# Apply hour filter
if selected_hour != "All Hours":

    hourly_filtered = hourly_filtered[
        hourly_filtered["pickup_hour"] == selected_hour
    ]


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
# DROP-OFF ZONE PERFORMANCE
# ============================================================

st.markdown(
    "<div class='section-description'>Drop-off zone activity based on the selected destination filters.</div>",
    unsafe_allow_html=True
)

dropoff_filtered = dropoff.copy()

if selected_dropoff_borough != "All Drop-off Boroughs":
    dropoff_filtered = dropoff_filtered[
        dropoff_filtered["dropoff_borough"].astype(str)
        == selected_dropoff_borough
    ]

if selected_dropoff_zones:
    dropoff_filtered = dropoff_filtered[
        dropoff_filtered["dropoff_zone"].isin(selected_dropoff_zones)
    ]

if dropoff_filtered.empty:

    st.info(
        "No drop-off-zone data matches the selected filters. "
        "Try selecting a different borough or zone."
    )

else:

    top_dropoff = (
        dropoff_filtered
        .sort_values("total_trips", ascending=False)
        .head(15)
        .sort_values("total_trips")
    )

    fig_dropoff = px.bar(
        top_dropoff,
        x="total_trips",
        y="dropoff_zone",
        orientation="h",
        labels={
            "total_trips": "Trips",
            "dropoff_zone": "Drop-off Zone"
        }
    )

    fig_dropoff.update_traces(
        marker_color="#6FA8DC"
    )

    fig_dropoff.update_layout(
        height=560,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#d1d5db"),
        xaxis=dict(gridcolor="#263244"),
        yaxis=dict(gridcolor="#263244"),
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_dropoff,
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

    if selected_weather == "All Weather Conditions":

        weather_filtered = weather.copy()

    else:

        weather_filtered = weather[
            weather["precipitation_category"].astype(str)
            == selected_weather
        ].copy()

    fig_weather = px.bar(
        weather_filtered,
        x="precipitation_category",
        y="total_trips",
        labels={
            "precipitation_category": "Weather",
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

    if selected_payment == "All Payment Types":

        payments_filtered = payments.copy()

    else:

        payments_filtered = payments[
            payments["payment_type"].astype(str) == selected_payment
        ].copy()

    fig_payment = px.bar(
        payments_filtered,
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
# RATE TYPE + AIRPORT ANALYSIS
# ============================================================

st.markdown(
    "<div class='section-header'>Rate Type & Airport Analysis</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='section-description'>Trip activity by taxi rate type and airport classification.</div>",
    unsafe_allow_html=True
)

r1, r2 = st.columns(2)


# ------------------------------------------------------------
# RATE TYPE
# ------------------------------------------------------------

with r1:

    rate_filtered = rate_analysis.copy()

    if selected_rate != "All Rate Types":
        rate_filtered = rate_filtered[
            rate_filtered["rate_code_id"].astype(str)
            == selected_rate
        ]

    if rate_filtered.empty:

        st.info(
            "No rate-type data matches the selected filter."
        )

    else:

        fig_rate = px.bar(
            rate_filtered,
            x="rate_code_id",
            y="total_trips",
            labels={
                "rate_code_id": "Rate Type",
                "total_trips": "Trips"
            }
        )

        fig_rate.update_traces(
            marker_color="#7C83FD"
        )

        fig_rate.update_layout(
            height=430,
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#d1d5db"),
            xaxis=dict(gridcolor="#263244"),
            yaxis=dict(gridcolor="#263244"),
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig_rate,
            use_container_width=True
        )


# ------------------------------------------------------------
# AIRPORT
# ------------------------------------------------------------

with r2:

    airport_filtered = airport_analysis.copy()

    if selected_airport != "All Airport Status":
        airport_filtered = airport_filtered[
            airport_filtered["airport_flag"].astype(str)
            == selected_airport
        ]

    if airport_filtered.empty:

        st.info(
            "No airport-trip data matches the selected filter."
        )

    else:

        fig_airport = px.bar(
            airport_filtered,
            x="airport_flag",
            y="total_trips",
            labels={
                "airport_flag": "Airport Status",
                "total_trips": "Trips"
            }
        )

        fig_airport.update_traces(
            marker_color="#F4A261"
        )

        fig_airport.update_layout(
            height=430,
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#d1d5db"),
            xaxis=dict(gridcolor="#263244"),
            yaxis=dict(gridcolor="#263244"),
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig_airport,
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

# ============================================================
# DATA QUALITY & ANOMALIES
# ============================================================

st.markdown(
    "<div class='section-header'>Data Quality & Anomaly Status</div>",
    unsafe_allow_html=True
)

quality = load_data("mart_quality.csv")

q = quality.iloc[0]

# Quality KPI cards
q1, q2, q3, q4 = st.columns(4)

with q1:
    st.metric(
        "Raw Taxi Rows",
        f"{int(q['raw_taxi_rows']):,}",
        help="Total taxi records ingested from the raw TLC trip files."
    )

with q2:
    st.metric(
        "Fact Taxi Rows",
        f"{int(q['fact_taxi_rows']):,}",
        help="Final cleaned taxi trip records available in the analytical fact table."
    )

with q3:
    st.metric(
        "Reconciliation Difference",
        f"{int(q['clean_fact_difference']):,}",
        help="Difference between cleaned taxi rows and final fact-table rows. Zero indicates reconciliation."
    )

with q4:
    st.metric(
        "Missing Weather",
        f"{int(q['missing_weather_rows']):,}",
        help="Taxi records without a matching hourly weather observation."
    )


st.markdown("<br>", unsafe_allow_html=True)

# Validation results
st.markdown(
    "<div class='insight-card'>"
    "<div class='insight-title'>Validation checks</div>"
    "<div class='insight-text'>",
    unsafe_allow_html=True
)

checks = [
    ("Clean vs fact reconciliation", int(q["clean_fact_difference"]) == 0),
    ("Invalid timestamp rows", int(q["invalid_timestamp_rows"]) == 0),
    ("Negative distance rows", int(q["negative_distance_rows"]) == 0),
    ("Negative fare rows", int(q["negative_fare_rows"]) == 0),
    ("Negative total amount rows", int(q["negative_total_amount_rows"]) == 0),
    ("Missing weather rows", int(q["missing_weather_rows"]) == 0),
]

for check_name, passed in checks:
    if passed:
        st.success(f"PASS — {check_name}")
    else:
        st.warning(f"CHECK — {check_name}")

st.markdown(
    "</div></div>",
    unsafe_allow_html=True
)


# Zone completeness
st.markdown(
    "<div class='insight-card'>"
    "<div class='insight-title'>Zone completeness</div>"
    "<div class='insight-text'>",
    unsafe_allow_html=True
)

pickup_missing = int(q["missing_pickup_zone_rows"])
dropoff_missing = int(q["missing_dropoff_zone_rows"])

st.write(
    f"Missing pickup-zone mappings: **{pickup_missing:,}**"
)

st.write(
    f"Missing drop-off-zone mappings: **{dropoff_missing:,}**"
)

st.caption(
    "These records are retained in the analytical pipeline. "
    "Missing zone mappings can affect zone-level analysis but do not remove the underlying taxi trip."
)

st.markdown(
    "</div></div>",
    unsafe_allow_html=True
)


# Methodology
st.markdown(
    "<div class='section-header'>Methodology</div>",
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
    Timestamp validation, financial-value checks, zone mapping,
    weather matching and fact-table reconciliation.

    <br><br>

    <b style="color:white;">Interpretation:</b>
    Results are observational and should not be interpreted as causal effects.

    </div>
    </div>
    """,
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
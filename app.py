import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Nassau Candy | Shipping Route Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    '''
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    section[data-testid="stSidebar"] { border-right: 1px solid rgba(120,130,150,0.18); }
    .dashboard-title {
    font-size: 2.15rem;
    font-weight: 750;
    line-height: 1.25;
    letter-spacing: -0.03em;
    padding-top: 0.35rem;
    margin-bottom: 0.25rem;
}
    .dashboard-subtitle { font-size: 1rem; color: #7f8a9a; margin-bottom: 0.25rem; }
    .dashboard-description { color: #9aa4b2; font-size: 0.92rem; line-height: 1.55; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(37,99,235,0.12), rgba(15,23,42,0.30));
        border: 1px solid rgba(96,165,250,0.18);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        min-height: 118px;
    }
    div[data-testid="stMetricLabel"] { font-size: 0.82rem; }
    div[data-testid="stMetricValue"] { font-weight: 750; }
    .section-note { color: #8b96a7; font-size: 0.9rem; margin-top: -0.35rem; margin-bottom: 0.9rem; }
    </style>
    ''',
    unsafe_allow_html=True
)

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard_data.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    return df

data = load_data()

st.sidebar.markdown("## Dashboard Filters")
st.sidebar.caption("Use the filters below to explore shipping performance.")

min_date = data["Order Date"].min().date()
max_date = data["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])
    filtered_data = data[
        (data["Order Date"] >= start_date) &
        (data["Order Date"] <= end_date)
    ].copy()
else:
    filtered_data = data.copy()

regions = sorted(filtered_data["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
filtered_data = filtered_data[filtered_data["Region"].isin(selected_regions)].copy()

states = sorted(filtered_data["State/Province"].dropna().unique())
selected_states = st.sidebar.multiselect("State / Province", states, default=states)
filtered_data = filtered_data[filtered_data["State/Province"].isin(selected_states)].copy()

ship_modes = sorted(filtered_data["Ship Mode"].dropna().unique())
selected_ship_modes = st.sidebar.multiselect("Ship Mode", ship_modes, default=ship_modes)
filtered_data = filtered_data[filtered_data["Ship Mode"].isin(selected_ship_modes)].copy()

lead_time_threshold = st.sidebar.slider(
    "Lead-Time Threshold (days)",
    min_value=int(data["Shipping Lead Time"].min()),
    max_value=int(data["Shipping Lead Time"].max()),
    value=1274
)

filtered_data["Dashboard Delay"] = (
    filtered_data["Shipping Lead Time"] > lead_time_threshold
)

st.markdown(
    '''
    <div>
        <div class="dashboard-title">📦 Nassau Candy Distributor</div>
        <div class="dashboard-subtitle">Factory-to-Customer Shipping Route Efficiency</div>
        <div class="dashboard-description">
            Interactive logistics dashboard for analyzing shipping lead time,
            route performance, geographic patterns, delay frequency, and
            shipping-mode performance.
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

overview_tab, geography_tab, ship_mode_tab, drilldown_tab = st.tabs(
    ["📊 Overview", "🗺️ Geography", "🚚 Ship Modes", "🔎 Route Drill-Down"]
)

with overview_tab:
    st.markdown("## Performance Overview")
    st.markdown(
        '<div class="section-note">High-level shipping performance for the currently selected filters.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)
    total_shipments = len(filtered_data)

    if total_shipments > 0:
        avg_lead_time = filtered_data["Shipping Lead Time"].mean()
        delayed_count = int(filtered_data["Dashboard Delay"].sum())
        delay_rate = filtered_data["Dashboard Delay"].mean() * 100
    else:
        avg_lead_time = delayed_count = delay_rate = 0

    with col1:
        st.metric("Total Shipments", f"{total_shipments:,}")
    with col2:
        st.metric("Average Lead Time", f"{avg_lead_time:,.1f} days")
    with col3:
        st.metric("Delayed Shipments", f"{delayed_count:,}")
    with col4:
        st.metric("Delay Frequency", f"{delay_rate:.2f}%")

    st.markdown("---")

    if len(filtered_data) > 0:
        st.markdown("### Route Efficiency Overview")
        st.markdown(
            '<div class="section-note">Route performance combines shipment volume, average lead time, delay frequency, and a normalized efficiency score.</div>',
            unsafe_allow_html=True
        )

        route_summary = (
            filtered_data.groupby("Route")
            .agg(
                Shipment_Volume=("Order ID", "count"),
                Average_Lead_Time=("Shipping Lead Time", "mean"),
                Delay_Frequency=("Dashboard Delay", "mean")
            )
            .reset_index()
        )
        route_summary["Delay_Frequency"] *= 100

        if len(route_summary) > 1:
            max_lead = route_summary["Average_Lead_Time"].max()
            min_lead = route_summary["Average_Lead_Time"].min()
            if max_lead != min_lead:
                route_summary["Efficiency_Score"] = (
                    (max_lead - route_summary["Average_Lead_Time"]) /
                    (max_lead - min_lead)
                ) * 100
            else:
                route_summary["Efficiency_Score"] = 100
        else:
            route_summary["Efficiency_Score"] = 100

        route_summary["Average_Lead_Time"] = route_summary["Average_Lead_Time"].round(2)
        route_summary["Delay_Frequency"] = route_summary["Delay_Frequency"].round(2)
        route_summary["Efficiency_Score"] = route_summary["Efficiency_Score"].round(2)

        left_col, right_col = st.columns(2)

        with left_col:
            st.markdown("#### Highest Route Efficiency Scores")
            leaderboard = route_summary.sort_values("Efficiency_Score", ascending=False).head(10).copy()
            fig_efficiency = px.bar(
                leaderboard.sort_values("Efficiency_Score"),
                x="Efficiency_Score",
                y="Route",
                orientation="h",
                labels={"Efficiency_Score": "Efficiency Score", "Route": ""},
                hover_data=["Shipment_Volume", "Average_Lead_Time", "Delay_Frequency"]
            )
            fig_efficiency.update_layout(height=430, margin=dict(l=10, r=10, t=15, b=10), showlegend=False)
            st.plotly_chart(fig_efficiency, width="stretch")

        with right_col:
            st.markdown("#### Highest-Volume Routes")
            volume_routes = route_summary.sort_values("Shipment_Volume", ascending=False).head(10).copy()
            fig_volume = px.bar(
                volume_routes.sort_values("Shipment_Volume"),
                x="Shipment_Volume",
                y="Route",
                orientation="h",
                labels={"Shipment_Volume": "Shipments", "Route": ""},
                hover_data=["Average_Lead_Time", "Delay_Frequency", "Efficiency_Score"]
            )
            fig_volume.update_layout(height=430, margin=dict(l=10, r=10, t=15, b=10), showlegend=False)
            st.plotly_chart(fig_volume, width="stretch")

        st.markdown("#### Route Leaderboard")
        st.dataframe(
            leaderboard[["Route", "Shipment_Volume", "Average_Lead_Time", "Delay_Frequency", "Efficiency_Score"]],
            width="stretch",
            hide_index=True
        )

        st.markdown("---")
        st.markdown("### Filtered Shipment Records")
        st.dataframe(
            filtered_data[
                ["Order ID", "Order Date", "Ship Date", "Ship Mode",
                 "State/Province", "Region", "Factory", "Route", "Shipping Lead Time"]
            ],
            width="stretch",
            hide_index=True
        )
    else:
        st.info("No shipment records match the selected filters.")

with geography_tab:
    st.markdown("## Geographic Shipping Performance")
    st.markdown(
        '<div class="section-note">Explore state-level shipping performance across the United States.</div>',
        unsafe_allow_html=True
    )

    state_abbreviations = {
        "Alabama":"AL","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO",
        "Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","DC":"DC",
        "Florida":"FL","Georgia":"GA","Idaho":"ID","Illinois":"IL","Indiana":"IN",
        "Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME",
        "Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN",
        "Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE",
        "Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM",
        "New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH",
        "Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI",
        "South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX",
        "Utah":"UT","Vermont":"VT","Virginia":"VA","Washington":"WA",
        "West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"
    }

    us_data = filtered_data[filtered_data["Country/Region"] == "United States"].copy()

    if len(us_data) > 0:
        state_map_data = (
            us_data.groupby("State/Province")
            .agg(
                Shipment_Volume=("Order ID", "count"),
                Average_Lead_Time=("Shipping Lead Time", "mean"),
                Delay_Frequency=("Dashboard Delay", "mean")
            )
            .reset_index()
        )
        state_map_data["Delay_Frequency"] *= 100
        state_map_data["State_Code"] = state_map_data["State/Province"].map(state_abbreviations)
        state_map_data = state_map_data.dropna(subset=["State_Code"])
        state_map_data["Average_Lead_Time"] = state_map_data["Average_Lead_Time"].round(2)
        state_map_data["Delay_Frequency"] = state_map_data["Delay_Frequency"].round(2)

        map_metric = st.selectbox("Map Metric", ["Average Lead Time", "Delay Frequency"])

        if map_metric == "Average Lead Time":
            color_column = "Average_Lead_Time"
            map_title = "Average Shipping Lead Time by U.S. State"
        else:
            color_column = "Delay_Frequency"
            map_title = "Delay Frequency by U.S. State"

        fig_map = px.choropleth(
            state_map_data,
            locations="State_Code",
            locationmode="USA-states",
            color=color_column,
            scope="usa",
            hover_name="State/Province",
            hover_data={
                "State_Code": False,
                "Shipment_Volume": True,
                "Average_Lead_Time": True,
                "Delay_Frequency": True
            },
            labels={
                "Shipment_Volume":"Shipments",
                "Average_Lead_Time":"Avg Lead Time (days)",
                "Delay_Frequency":"Delay Frequency (%)"
            },
            color_continuous_scale="Blues",
            title=map_title
        )
        fig_map.update_layout(height=570, margin=dict(l=0, r=0, t=55, b=0))
        st.plotly_chart(fig_map, width="stretch")

        st.markdown("### Geographic Bottlenecks")
        bottleneck_data = (
            state_map_data[state_map_data["Shipment_Volume"] >= 10]
            .sort_values(["Average_Lead_Time", "Shipment_Volume"], ascending=[False, False])
            .head(10)
        )
        st.dataframe(
            bottleneck_data[
                ["State/Province", "Shipment_Volume", "Average_Lead_Time", "Delay_Frequency"]
            ],
            width="stretch",
            hide_index=True
        )
    else:
        st.info("No U.S. shipment records match the selected filters.")

with ship_mode_tab:
    st.markdown("## Ship Mode Comparison")
    st.markdown(
        '<div class="section-note">Compare shipping modes using volume, lead time, delay frequency, and average cost.</div>',
        unsafe_allow_html=True
    )

    if len(filtered_data) > 0:
        ship_mode_summary = (
            filtered_data.groupby("Ship Mode")
            .agg(
                Shipment_Volume=("Order ID", "count"),
                Average_Lead_Time=("Shipping Lead Time", "mean"),
                Delay_Frequency=("Dashboard Delay", "mean"),
                Average_Cost=("Cost", "mean")
            )
            .reset_index()
        )
        ship_mode_summary["Delay_Frequency"] *= 100
        ship_mode_summary["Average_Lead_Time"] = ship_mode_summary["Average_Lead_Time"].round(2)
        ship_mode_summary["Delay_Frequency"] = ship_mode_summary["Delay_Frequency"].round(2)
        ship_mode_summary["Average_Cost"] = ship_mode_summary["Average_Cost"].round(2)

        st.markdown("### Shipping Mode Performance")
        st.dataframe(ship_mode_summary, width="stretch", hide_index=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Average Lead Time")
            fig_lead = px.bar(
                ship_mode_summary,
                x="Ship Mode",
                y="Average_Lead_Time",
                labels={"Ship Mode":"", "Average_Lead_Time":"Days"}
            )
            fig_lead.update_layout(height=390, margin=dict(l=10, r=10, t=15, b=10), showlegend=False)
            st.plotly_chart(fig_lead, width="stretch")

        with col2:
            st.markdown("#### Delay Frequency")
            fig_delay = px.bar(
                ship_mode_summary,
                x="Ship Mode",
                y="Delay_Frequency",
                labels={"Ship Mode":"", "Delay_Frequency":"Delay Frequency (%)"}
            )
            fig_delay.update_layout(height=390, margin=dict(l=10, r=10, t=15, b=10), showlegend=False)
            st.plotly_chart(fig_delay, width="stretch")

        st.markdown("#### Average Cost")
        fig_cost = px.bar(
            ship_mode_summary,
            x="Ship Mode",
            y="Average_Cost",
            labels={"Ship Mode":"", "Average_Cost":"Average Cost"}
        )
        fig_cost.update_layout(height=350, margin=dict(l=10, r=10, t=15, b=10), showlegend=False)
        st.plotly_chart(fig_cost, width="stretch")
    else:
        st.info("No shipment records match the selected filters.")

with drilldown_tab:
    st.markdown("## Route Drill-Down")
    st.markdown(
        '<div class="section-note">Select a factory-to-customer route to inspect route KPIs, shipping modes, and order-level shipment details.</div>',
        unsafe_allow_html=True
    )

    available_routes = sorted(filtered_data["Route"].dropna().unique())

    if len(available_routes) > 0:
        selected_route = st.selectbox("Select a Factory-to-Customer Route", available_routes)
        route_data = filtered_data[filtered_data["Route"] == selected_route].copy()

        route_col1, route_col2, route_col3, route_col4 = st.columns(4)

        with route_col1:
            st.metric("Shipments", f"{len(route_data):,}")
        with route_col2:
            st.metric("Average Lead Time", f'{route_data["Shipping Lead Time"].mean():,.1f} days')
        with route_col3:
            st.metric("Delay Frequency", f'{route_data["Dashboard Delay"].mean() * 100:.2f}%')
        with route_col4:
            st.metric("Average Cost", f'{route_data["Cost"].mean():,.2f}')

        st.markdown("---")
        st.markdown("### Route Information")
        route_info = route_data[["Factory", "State/Province", "Region"]].drop_duplicates()
        st.dataframe(route_info, width="stretch", hide_index=True)

        st.markdown("### Ship Mode Distribution")
        route_mode_summary = (
            route_data.groupby("Ship Mode")
            .agg(
                Shipments=("Order ID", "count"),
                Average_Lead_Time=("Shipping Lead Time", "mean"),
                Delay_Frequency=("Dashboard Delay", "mean")
            )
            .reset_index()
        )
        route_mode_summary["Delay_Frequency"] *= 100
        route_mode_summary["Average_Lead_Time"] = route_mode_summary["Average_Lead_Time"].round(2)
        route_mode_summary["Delay_Frequency"] = route_mode_summary["Delay_Frequency"].round(2)
        st.dataframe(route_mode_summary, width="stretch", hide_index=True)

        st.markdown("### Order-Level Shipment Timeline")
        timeline_data = route_data[
            ["Order ID", "Order Date", "Ship Date", "Ship Mode",
             "State/Province", "Shipping Lead Time", "Dashboard Delay"]
        ].sort_values("Order Date")
        st.dataframe(timeline_data, width="stretch", hide_index=True)
    else:
        st.info("No routes are available for the currently selected filters.")

st.markdown("---")
st.caption(
    "Nassau Candy Distributor | Factory-to-Customer Shipping Route Efficiency Analysis | Data Analytics Internship Project"
)

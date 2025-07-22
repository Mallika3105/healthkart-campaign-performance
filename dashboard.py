# healthkart_dashboard.py

import streamlit as st
import pandas as pd

# Load datasets
@st.cache_data
def load_data():
    influencers = pd.read_csv('influencers_data.csv')
    posts = pd.read_csv('posts_data.csv')
    tracking = pd.read_csv('tracking_data.csv')
    payouts = pd.read_csv('payouts_data.csv')
    return influencers, posts, tracking, payouts

influencers, posts, tracking, payouts = load_data()

st.title("📊 HealthKart Influencer Campaign Dashboard")

# Sidebar filters
st.sidebar.header("🔎 Filter Data")

# Platform Filter
platform_filter = st.sidebar.multiselect(
    "Select Platform(s):", influencers["platform"].unique(), default=influencers["platform"].unique()
)

# Influencer Type (Category)
category_filter = st.sidebar.multiselect(
    "Select Influencer Type(s):", influencers["category"].unique(), default=influencers["category"].unique()
)

# Campaign (Brand)
campaign_filter = st.sidebar.multiselect(
    "Select Campaign(s):", tracking["campaign"].unique(), default=tracking["campaign"].unique()
)

# Product
product_filter = st.sidebar.multiselect(
    "Select Product(s):", tracking["product"].unique(), default=tracking["product"].unique()
)

# Influencer Name
influencer_filter = st.sidebar.multiselect(
    "Select Influencer(s):", influencers["name"].unique(), default=influencers["name"].unique()
)

# Apply filters
filtered_influencers = influencers[
    (influencers["platform"].isin(platform_filter)) &
    (influencers["category"].isin(category_filter)) &
    (influencers["name"].isin(influencer_filter))
]

filtered_tracking = tracking[
    (tracking["campaign"].isin(campaign_filter)) &
    (tracking["product"].isin(product_filter)) &
    (tracking["influencer_id"].isin(filtered_influencers["ID"]))
]

filtered_posts = posts[posts["influencer_id"].isin(filtered_influencers["ID"])]
filtered_payouts = payouts[payouts["influencer_id"].isin(filtered_influencers["ID"])]

# Display overview
st.subheader("📌 Influencer Overview")
st.dataframe(filtered_influencers)

st.subheader("📝 Posts Data")
st.dataframe(filtered_posts)

st.subheader("📦 Tracking Data")
st.dataframe(filtered_tracking)

st.subheader("💰 Payout Details")
st.dataframe(filtered_payouts)
st.subheader("📈 ROI and Incremental ROAS")

try:
    if not filtered_tracking.empty and not filtered_payouts.empty:
        tracking_agg = filtered_tracking.groupby('influencer_id').agg({
            'orders': 'sum',
            'revenue': 'sum'
        }).reset_index()

        payouts_data = filtered_payouts[['influencer_id', 'total_payout']]

        merged = pd.merge(tracking_agg, payouts_data, on='influencer_id', how='inner')

        merged['ROI'] = merged['revenue'] / merged['total_payout']

        # Assume a baseline order value of ₹300
        baseline_order_value = 300
        merged['incremental_revenue'] = merged['revenue'] - (merged['orders'] * baseline_order_value)
        merged['Incremental_ROAS'] = merged['incremental_revenue'] / merged['total_payout']

        # Add influencer names
        merged = pd.merge(merged, influencers[['ID', 'name']], left_on='influencer_id', right_on='ID', how='left')

        st.dataframe(merged[['name', 'orders', 'revenue', 'total_payout', 'ROI', 'Incremental_ROAS']].round(2))

    else:
        st.warning("⚠️ No data available for ROI/ROAS calculations based on current filters.")

except Exception as e:
    st.error(f"Error calculating ROI: {e}")
import plotly.express as px

st.subheader("📊 Visualizing ROI and Incremental ROAS")

# Bar chart: ROI
fig_roi = px.bar(
    merged.sort_values("ROI", ascending=False),
    x="name",
    y="ROI",
    title="Return on Investment (ROI) by Influencer",
    color="ROI",
    color_continuous_scale="viridis"
)
st.plotly_chart(fig_roi, use_container_width=True)

# Bar chart: Incremental ROAS
fig_roas = px.bar(
    merged.sort_values("Incremental_ROAS", ascending=False),
    x="name",
    y="Incremental_ROAS",
    title="Incremental ROAS by Influencer",
    color="Incremental_ROAS",
    color_continuous_scale="plasma"
)
st.plotly_chart(fig_roas, use_container_width=True)
st.subheader("🏆 Top Influencer Leaderboard")

# Radio button to select ranking criteria
ranking_metric = st.radio("Rank influencers by:", ["ROI", "Incremental_ROAS"], index=0, horizontal=True)

# Sort by selected metric
leaderboard = merged.sort_values(ranking_metric, ascending=False).reset_index(drop=True)
leaderboard.index += 1  # Start index from 1 for ranking

# Select columns to display
leaderboard_display = leaderboard[['name', 'orders', 'revenue', 'total_payout', 'ROI', 'Incremental_ROAS']].round(2)
leaderboard_display.rename(columns={
    'name': 'Influencer',
    'orders': 'Orders',
    'revenue': 'Revenue',
    'total_payout': 'Payout',
    'ROI': 'ROI',
    'Incremental_ROAS': 'Inc. ROAS'
}, inplace=True)

st.dataframe(leaderboard_display.style.highlight_max(axis=0, color='lightgreen'), use_container_width=True)

# Download button for leaderboard
st.download_button(
    label="📥 Download Leaderboard as CSV",
    data=leaderboard_display.to_csv(index=False),
    file_name="top_influencer_leaderboard.csv",
    mime="text/csv"
)

st.subheader("🧠 Key Performance Insights")

try:
    if not merged.empty:
        # Best ROI influencer
        best_roi = merged.loc[merged['ROI'].idxmax()]
        best_roas = merged.loc[merged['Incremental_ROAS'].idxmax()]

        # Most orders
        most_orders = merged.loc[merged['orders'].idxmax()]

        # Most revenue
        most_revenue = merged.loc[merged['revenue'].idxmax()]

        st.markdown(f"""
        - 🏅 **{best_roi['name']}** delivered the **highest ROI** of **{best_roi['ROI']:.2f}** on the **{influencers[influencers['ID'] == best_roi['influencer_id']]['platform'].values[0]}** platform.
        - 💡 **{best_roas['name']}** had the **best Incremental ROAS** of **{best_roas['Incremental_ROAS']:.2f}**, indicating high campaign impact.
        - 📦 **{most_orders['name']}** drove the **most orders** with **{int(most_orders['orders'])} total orders**.
        - 💰 **{most_revenue['name']}** generated the **highest revenue** of ₹**{most_revenue['revenue']:.2f}**.
        """)

    else:
        st.info("Not enough data to generate insights. Try changing the filters.")

except Exception as e:
    st.error(f"Error generating insights: {e}")

st.subheader("📉 Loss-Making Influencer Alerts")

try:
    # Filter influencers with ROI < 1 or Incremental ROAS < 0
    losses = merged[(merged['ROI'] < 1) | (merged['Incremental_ROAS'] < 0)]

    if not losses.empty:
        st.warning(f"🚨 {len(losses)} influencer(s) are incurring losses.")

        # Display loss-makers
        losses_display = losses[['name', 'revenue', 'total_payout', 'ROI', 'Incremental_ROAS']].round(2)
        losses_display.rename(columns={
            'name': 'Influencer',
            'revenue': 'Revenue',
            'total_payout': 'Payout',
            'ROI': 'ROI',
            'Incremental_ROAS': 'Inc. ROAS'
        }, inplace=True)

        st.dataframe(losses_display.style.applymap(
            lambda val: 'background-color: salmon' if isinstance(val, (int, float)) and val < 1 else ''
        , subset=['ROI', 'Inc. ROAS']), use_container_width=True)
    else:
        st.success("✅ All influencer campaigns are currently profitable based on ROI and Incremental ROAS.")
except Exception as e:
    st.error(f"Error detecting loss-makers: {e}")

st.markdown("### 🔍 Common Underperformance Patterns")

try:
    # Merge full influencer data with losses
    full_loss_data = pd.merge(losses, influencers, left_on='influencer_id', right_on='ID', how='left')
    loss_tracking = pd.merge(losses, tracking, on='influencer_id')

    # Platform-level insights
    top_platforms = full_loss_data['platform'].value_counts()
    top_platforms = top_platforms[top_platforms >= 2]  # show only if >= 2 losses

    # Category-level insights
    top_categories = full_loss_data['category'].value_counts()
    top_categories = top_categories[top_categories >= 2]

    # Product-level insights
    top_products = loss_tracking['product'].value_counts()
    top_products = top_products[top_products >= 2]

    if not top_platforms.empty:
        st.markdown("#### 📱 Platforms Frequently Associated with Losses")
        for platform, count in top_platforms.items():
            st.markdown(f"- **{platform}** had **{count}** loss-making influencers")

    if not top_categories.empty:
        st.markdown("#### 👥 Influencer Types with Consistent Underperformance")
        for category, count in top_categories.items():
            st.markdown(f"- **{category}** category influencers underperformed in **{count}** campaigns")

    if not top_products.empty:
        st.markdown("#### 📦 Products Driving Repeated Losses")
        for product, count in top_products.items():
            st.markdown(f"- **{product}** was linked to **{count}** low-ROI campaigns")

    if top_platforms.empty and top_categories.empty and top_products.empty:
        st.success("No recurring loss patterns detected. Losses are likely isolated.")

except Exception as e:
    st.error(f"Error detecting common patterns: {e}")

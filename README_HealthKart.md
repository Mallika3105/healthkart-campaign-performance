
# 📊 HealthKart Influencer Campaign Dashboard

A Streamlit-based dashboard built to analyze the ROI and Incremental ROAS of influencer campaigns for HealthKart. This tool tracks performance metrics, visualizes outcomes, and identifies underperforming influencers and patterns.

---

## 🧾 Objective

To build an interactive tool that simulates influencer marketing data and helps in:

- Tracking influencer and post performance
- Calculating ROI and Incremental ROAS
- Identifying low-performing campaigns and influencers
- Analyzing underperformance patterns by platform, category, and product

---

## 📁 Dataset Structure (Simulated)

1. **influencers_data.csv**
   - `ID`, `name`, `category`, `gender`, `follower_count`, `platform`

2. **posts_data.csv**
   - `influencer_id`, `platform`, `date`, `URL`, `caption`, `reach`, `likes`, `comments`

3. **tracking_data.csv**
   - `source`, `campaign`, `influencer_id`, `user_id`, `product`, `date`, `orders`, `revenue`

4. **payouts_data.csv**
   - `influencer_id`, `basis` (post/order), `rate`, `orders`, `total_payout`

---

## ⚙️ How to Run

1. Install requirements:
   ```bash
   pip install streamlit pandas plotly
   ```

2. Place the following files in the same folder:
   - `dashboard.py`
   - `influencers_data.csv`
   - `posts_data.csv`
   - `tracking_data.csv`
   - `payouts_data.csv`

3. Launch the dashboard:
   ```bash
   streamlit run dashboard.py
   ```

---

## ✨ Features

✅ ROI and Incremental ROAS Calculation  
✅ Performance Tracking for Posts, Influencers, and Campaigns  
✅ Filters for Platform, Product, Campaign, Category, and Influencer  
✅ ROI & ROAS Visualizations (Bar Charts)  
✅ Leaderboard of Top Influencers (with download option)  
✅ Loss-making Influencer Alerts  
✅ Detection of Recurring Underperformance Patterns

---

## 📌 Assumptions

- All datasets are simulated locally for the assignment
- ROI = Revenue / Total Payout
- Incremental ROAS uses a fixed baseline average order value of ₹300
- Data is read from CSV files rather than uploaded dynamically

---

## 📄 Output Files

- `dashboard.py` – Streamlit dashboard app
- `README.md` – This documentation file
- `.csv` files – Input datasets

---

## 🙋 Author

Developed by **Mallika Bhojak** as part of the HealthKart Data Analyst Internship Assignment.  
This project combines applied economics, data science, and visualization to extract actionable insights from simulated influencer marketing data.

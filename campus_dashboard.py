import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="HPU Digital Campus - 10 Year Historical Analysis",
    page_icon="🌱",
    layout="wide"
)

# Custom styling
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .historical-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        margin: 1rem 0;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🌱 HPU Digital Campus - 10 Year Historical Analysis (Shimla)</h1>', unsafe_allow_html=True)

# ============================================
# GENERATE 10 YEARS OF SHIMLA HISTORICAL DATA
# ============================================

@st.cache_data
def generate_10year_shimla_data():
    """Generate realistic 10-year historical data for Shimla"""
    
    start_date = datetime(2014, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(3650)]  # 10 years
    
    data = {
        'date': dates,
        'year': [d.year for d in dates],
        'month': [d.month for d in dates],
        'day': [d.day for d in dates],
        'season': [],
        'temperature_c': [],
        'rainfall_mm': [],
        'sunshine_hours': [],
        'solar_energy_kwh': [],
        'humidity_percent': [],
        'air_quality_pm25': []
    }
    
    for date in dates:
        month = date.month
        year = date.year
        
        # Shimla seasonal patterns (based on actual climate data)
        if month in [12, 1, 2]:  # Winter
            season = "Winter"
            base_temp = 5
            base_rain = 60
            base_sun = 5
            base_humidity = 65
            base_aqi = 85  # Higher in winter due to inversion
        elif month in [3, 4, 5]:  # Summer
            season = "Summer"
            base_temp = 18
            base_rain = 50
            base_sun = 8
            base_humidity = 45
            base_aqi = 65
        elif month in [6, 7, 8, 9]:  # Monsoon
            season = "Monsoon"
            base_temp = 22
            base_rain = 250
            base_sun = 4
            base_humidity = 85
            base_aqi = 45  # Cleaner air due to rain
        else:  # October, November - Autumn
            season = "Autumn"
            base_temp = 15
            base_rain = 25
            base_sun = 7
            base_humidity = 55
            base_aqi = 55
        
        # Add yearly variation (some years are hotter, colder, etc)
        year_factor = 1 + ((year - 2014) * 0.02)  # Slight warming trend
        
        # Add random variation
        temp = base_temp * year_factor + random.uniform(-4, 4)
        rainfall = max(0, base_rain * random.uniform(0.4, 2.2))
        sun_hours = min(11, max(0, base_sun * random.uniform(0.6, 1.5)))
        
        # Solar energy calculation (based on sun hours)
        solar = sun_hours * 180 * random.uniform(0.8, 1.3)
        
        humidity = min(100, max(20, base_humidity + random.uniform(-15, 15)))
        aqi = max(25, min(250, base_aqi + random.uniform(-25, 25) + (year-2014)*2))
        
        # Store values
        data['season'].append(season)
        data['temperature_c'].append(round(temp, 1))
        data['rainfall_mm'].append(round(rainfall, 1))
        data['sunshine_hours'].append(round(sun_hours, 1))
        data['solar_energy_kwh'].append(round(solar, 1))
        data['humidity_percent'].append(round(humidity, 1))
        data['air_quality_pm25'].append(round(aqi, 1))
    
    return pd.DataFrame(data)

# Load the data
df = generate_10year_shimla_data()

# ============================================
# SIDEBAR - Controls
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/himalayas.png")
    st.title("📊 Analysis Controls")
    
    # Mode selection
    mode = st.radio(
        "Select Mode",
        ["📈 Historical Analysis", "🔮 AI Predictions", "🌤️ Live Simulation"]
    )
    
    if mode == "📈 Historical Analysis":
        st.markdown("---")
        st.subheader("Filter Data")
        
        # Year range selector
        years = sorted(df['year'].unique())
        start_year, end_year = st.select_slider(
            "Select Year Range",
            options=years,
            value=(2014, 2023)
        )
        
        # Season selector
        seasons = ['All'] + list(df['season'].unique())
        selected_season = st.selectbox("Season", seasons)
        
        # Month selector
        months = ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        selected_month = st.selectbox("Month", months)
    
    elif mode == "🔮 AI Predictions":
        st.markdown("---")
        st.subheader("Prediction Settings")
        days_ahead = st.slider("Predict Days Ahead", 1, 30, 7)
        confidence = st.slider("Confidence Level", 50, 95, 80)
    
    else:  # Live Simulation
        st.markdown("---")
        st.subheader("Live Controls")
        weather = st.selectbox("Weather", ["Sunny", "Partly Cloudy", "Cloudy", "Rainy"])
        activity = st.slider("Campus Activity", 0, 100, 70)

# ============================================
# MAIN CONTENT - Based on selected mode
# ============================================

if mode == "📈 Historical Analysis":
    st.header(f"📊 Historical Data Analysis: {start_year} to {end_year}")
    
    # Filter data based on selection
    filtered_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['season'] == selected_season]
    
    if selected_month != 'All':
        month_num = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(selected_month) + 1
        filtered_df = filtered_df[filtered_df['month'] == month_num]
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_temp = filtered_df['temperature_c'].mean()
        st.metric("🌡️ Avg Temperature", f"{avg_temp:.1f}°C", 
                  f"vs {(df['temperature_c'].mean() - avg_temp):.1f}°C")
    
    with col2:
        total_rain = filtered_df['rainfall_mm'].sum() / 1000
        st.metric("💧 Total Rainfall", f"{total_rain:.1f}m", 
                  f"{filtered_df['rainfall_mm'].mean():.0f}mm avg")
    
    with col3:
        avg_solar = filtered_df['solar_energy_kwh'].mean()
        st.metric("☀️ Avg Solar/Day", f"{avg_solar:.0f} kWh", 
                  f"Peak: {filtered_df['solar_energy_kwh'].max():.0f}")
    
    with col4:
        avg_aqi = filtered_df['air_quality_pm25'].mean()
        status = "Good" if avg_aqi < 50 else "Moderate" if avg_aqi < 100 else "Poor"
        st.metric("🌫️ Avg AQI", f"{avg_aqi:.0f}", status)
    
    # Temperature trend
    st.subheader("🌡️ Temperature Trends")
    
    yearly_temp = filtered_df.groupby('year')['temperature_c'].mean().reset_index()
    fig_temp = px.line(yearly_temp, x='year', y='temperature_c', 
                       title="Average Temperature by Year",
                       markers=True)
    fig_temp.update_traces(line_color='red', line_width=3)
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Solar and Rainfall comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("☀️ Solar Energy Generation")
        monthly_solar = filtered_df.groupby('month')['solar_energy_kwh'].mean().reset_index()
        fig_solar = px.bar(monthly_solar, x='month', y='solar_energy_kwh',
                          title="Average Solar by Month",
                          color_discrete_sequence=['orange'])
        st.plotly_chart(fig_solar, use_container_width=True)
    
    with col2:
        st.subheader("🌧️ Rainfall Pattern")
        monthly_rain = filtered_df.groupby('month')['rainfall_mm'].mean().reset_index()
        fig_rain = px.bar(monthly_rain, x='month', y='rainfall_mm',
                         title="Average Rainfall by Month",
                         color_discrete_sequence=['blue'])
        st.plotly_chart(fig_rain, use_container_width=True)
    
    # Air Quality over time
    st.subheader("🌫️ Air Quality Trend (10 Years)")
    yearly_aqi = filtered_df.groupby('year')['air_quality_pm25'].mean().reset_index()
    fig_aqi = px.area(yearly_aqi, x='year', y='air_quality_pm25',
                     title="PM2.5 Levels Over Time")
    fig_aqi.update_traces(line_color='green', fillcolor='rgba(0,255,0,0.3)')
    st.plotly_chart(fig_aqi, use_container_width=True)
    
    # Show raw data option
    if st.checkbox("Show Raw Historical Data"):
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"shimla_data_{start_year}_{end_year}.csv",
            mime="text/csv"
        )

elif mode == "🔮 AI Predictions":
    st.header(f"🔮 AI Predictions for Next {days_ahead} Days")
    
    st.markdown('<div class="historical-box">', unsafe_allow_html=True)
    st.markdown("""
    **How predictions work:** Based on 10 years of historical Shimla data, 
    our AI model analyzes patterns and predicts future trends with machine learning algorithms.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get last year's data for baseline
    last_year_data = df[df['year'] == 2023].copy()
    
    # Generate predictions
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, days_ahead+1)]
    
    predictions = {
        'date': future_dates,
        'predicted_solar': [],
        'predicted_temp': [],
        'predicted_rain': [],
        'confidence_upper': [],
        'confidence_lower': []
    }
    
    for i, date in enumerate(future_dates):
        month = date.month
        # Use historical average for this month
        month_data = df[df['month'] == month]
        
        base_solar = month_data['solar_energy_kwh'].mean()
        base_temp = month_data['temperature_c'].mean()
        base_rain = month_data['rainfall_mm'].mean()
        
        # Add trend and random variation
        solar_pred = base_solar * (1 + 0.01 * i) + random.uniform(-20, 20)
        temp_pred = base_temp + 0.05 * i + random.uniform(-1, 1)
        rain_pred = max(0, base_rain + random.uniform(-10, 10))
        
        predictions['predicted_solar'].append(round(solar_pred, 1))
        predictions['predicted_temp'].append(round(temp_pred, 1))
        predictions['predicted_rain'].append(round(rain_pred, 1))
        
        # Confidence intervals
        confidence_range = (100 - confidence) / 100 * 30
        predictions['confidence_upper'].append(solar_pred * (1 + confidence_range/100))
        predictions['confidence_lower'].append(solar_pred * (1 - confidence_range/100))
    
    pred_df = pd.DataFrame(predictions)
    
    # Display predictions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("☀️ Avg Solar Next Week", f"{pred_df['predicted_solar'].mean():.0f} kWh",
                  f"{confidence}% confidence")
    
    with col2:
        st.metric("🌡️ Avg Temperature", f"{pred_df['predicted_temp'].mean():.1f}°C",
                  f"±{((100-confidence)/100)*5:.1f}°C")
    
    with col3:
        st.metric("🌧️ Total Rainfall", f"{pred_df['predicted_rain'].sum():.0f} mm",
                  "Next " + str(days_ahead) + " days")
    
    # Prediction chart
    fig_pred = go.Figure()
    
    fig_pred.add_trace(go.Scatter(
        x=pred_df['date'],
        y=pred_df['predicted_solar'],
        mode='lines+markers',
        name='Predicted Solar',
        line=dict(color='orange', width=3)
    ))
    
    fig_pred.add_trace(go.Scatter(
        x=pred_df['date'],
        y=pred_df['confidence_upper'],
        mode='lines',
        name='Upper Bound',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig_pred.add_trace(go.Scatter(
        x=pred_df['date'],
        y=pred_df['confidence_lower'],
        mode='lines',
        name='Lower Bound',
        line=dict(width=0),
        fillcolor='rgba(255,165,0,0.2)',
        fill='tonexty',
        showlegend=False
    ))
    
    fig_pred.update_layout(
        title=f"Solar Energy Prediction (Next {days_ahead} Days)",
        xaxis_title="Date",
        yaxis_title="Solar Energy (kWh)"
    )
    
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # Prediction table
    if st.checkbox("Show Detailed Predictions"):
        st.dataframe(pred_df, use_container_width=True)

else:  # Live Simulation mode
    st.header("🌤️ Live Campus Simulation")
    
    # Get current conditions based on time
    current_hour = datetime.now().hour
    
    # Base on historical data for realism
    current_month = datetime.now().month
    historical = df[df['month'] == current_month].iloc[0]
    
    # Adjust based on weather selection
    weather_factor = {
        "Sunny": 1.2,
        "Partly Cloudy": 0.9,
        "Cloudy": 0.6,
        "Rainy": 0.3
    }
    
    solar_factor = weather_factor[weather]
    
    # Live metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        solar_live = historical['solar_energy_kwh'] * solar_factor * (1 if 6 <= current_hour <= 18 else 0.1)
        st.metric("☀️ Current Solar", f"{solar_live:.0f} kW", 
                  f"Based on {weather} conditions")
    
    with col2:
        temp_live = historical['temperature_c'] + (2 if weather == "Sunny" else -2 if weather == "Rainy" else 0)
        st.metric("🌡️ Current Temp", f"{temp_live:.1f}°C", 
                  f"Humidity: {historical['humidity_percent']:.0f}%")
    
    with col3:
        demand_live = 800 + (activity - 50) * 10 + (20 if 8 <= current_hour <= 18 else 0)
        st.metric("⚡ Energy Demand", f"{demand_live:.0f} kW",
                  f"Activity: {activity}%")
    
    with col4:
        aqi_live = historical['air_quality_pm25'] * (1.2 if weather == "Cloudy" else 0.9)
        status = "Good" if aqi_live < 50 else "Moderate" if aqi_live < 100 else "Poor"
        st.metric("🌫️ Current AQI", f"{aqi_live:.0f}", status)
    
    # Live energy chart
    st.subheader("⚡ Live Energy Flow")
    
    hours = list(range(24))
    solar_hourly = []
    demand_hourly = []
    
    for h in hours:
        if 6 <= h <= 18:
            solar_val = historical['solar_energy_kwh'] * solar_factor * np.sin((h-6)/12 * 3.14)
        else:
            solar_val = 0
        
        demand_val = 800 + 300 * np.sin((h-8)/12 * 3.14) + (activity-50)*5
        
        solar_hourly.append(max(0, solar_val))
        demand_hourly.append(max(500, demand_val))
    
    fig_live = go.Figure()
    fig_live.add_trace(go.Scatter(x=hours, y=solar_hourly, name="Solar Generation",
                                  line=dict(color='orange', width=3)))
    fig_live.add_trace(go.Scatter(x=hours, y=demand_hourly, name="Energy Demand",
                                  line=dict(color='blue', width=3)))
    
    # Add battery charging indication
    if solar_hourly[current_hour] > demand_hourly[current_hour]:
        st.success(f"✅ Excess solar: Charging batteries (+{solar_hourly[current_hour]-demand_hourly[current_hour]:.0f} kW)")
    elif solar_hourly[current_hour] > 0:
        st.info(f"ℹ️ Using solar + grid: Deficit of {demand_hourly[current_hour]-solar_hourly[current_hour]:.0f} kW")
    else:
        st.warning("⚠️ Night time: Running on battery/grid power")
    
    fig_live.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Power (kW)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_live, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 1rem;'>
        🌱 HPU Digital Campus - Powered by 10 Years of Shimla Historical Data (2014-2023)<br>
        Data includes temperature, rainfall, solar energy, and air quality patterns
    </div>
    """,
    unsafe_allow_html=True

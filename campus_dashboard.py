import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# ============================================
# GOOGLE SHEETS CONFIG
# ============================================
SHEET_ID = "1R5EJ-ukTg5KbEfc6Lt7cVYXyPsGRmGatwWWTNKmu2Y4"
SHEET_NAME = "Sheet1"

GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=10)
def load_sensor_data():
    try:
        df = pd.read_csv(GSHEET_URL)
        return df
    except Exception as e:
        return None

# Page config
st.set_page_config(
    page_title="HPU Digital Campus - Smart Control Center",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    .alert-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-left-color: #ffc107;
        color: #856404;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-left-color: #dc3545;
        color: #721c24;
    }
    .alert-success {
        background-color: #d4edda;
        border-left-color: #28a745;
        color: #155724;
    }
    .section-header {
        color: #2E7D32;
        font-size: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2E7D32;
        padding-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SIMULATION DATA GENERATION
# ============================================
# ============================================
# SENSOR DATA SIMULATION FUNCTIONS
# ============================================

def simulate_sensor_data(date, hour):
    """Generate realistic sensor data for all 5 systems"""
    
    # Solar Energy Sensor (W/m²)
    if 6 <= hour <= 18:
        solar_irradiance = 800 * np.sin((hour-6)/12 * np.pi) * random.uniform(0.8, 1.2)
        solar_power = solar_irradiance * 0.2 * random.uniform(0.9, 1.1)
    else:
        solar_irradiance = 0
        solar_power = 0
    
    # Air Quality Sensors
    base_aqi = 45 + 30 * np.sin((date.month-1)/11 * np.pi)
    pm25 = base_aqi * random.uniform(0.7, 1.3)
    pm10 = pm25 * 1.5 * random.uniform(0.8, 1.2)
    co2 = 400 + 200 * random.uniform(0.5, 1.5)
    
    # Water Sensors
    water_flow = random.uniform(50, 200)
    tank_level = random.uniform(40, 95)
    water_tds = random.uniform(50, 150)
    water_ph = random.uniform(6.5, 8.5)
    
    # Waste Sensors
    bin_levels = {
        'Academic Block': random.uniform(20, 95),
        'Hostel A': random.uniform(30, 98),
        'Hostel B': random.uniform(30, 98),
        'Hostel C': random.uniform(30, 98),
        'Cafeteria': random.uniform(40, 99),
        'Support Complex': random.uniform(25, 90)
    }
    
    # Thermal Sensors
    outdoor_temp = 5 + 15 * np.sin((date.month-1)/11 * np.pi) + random.uniform(-3, 3)
    indoor_temp = outdoor_temp + 10 * random.uniform(0.8, 1.2)
    humidity = 40 + 30 * random.uniform(0.5, 1.5)
    
    return {
        'timestamp': f"{date.date()} {hour}:00",
        'solar': {
            'irradiance_w_m2': round(solar_irradiance, 1),
            'power_kw': round(solar_power, 1),
        },
        'air_quality': {
            'pm25': round(pm25, 1),
            'pm10': round(pm10, 1),
            'co2': round(co2, 1),
            'aqi_category': 'Good' if pm25 < 50 else 'Moderate' if pm25 < 100 else 'Poor'
        },
        'water': {
            'flow_rate_lpm': round(water_flow, 1),
            'tank_level_pct': round(tank_level, 1),
            'tds_ppm': round(water_tds, 1),
            'ph': round(water_ph, 1)
        },
        'waste': {
            'bins': {k: round(v, 1) for k, v in bin_levels.items()},
            'total_fullness': round(sum(bin_levels.values())/len(bin_levels), 1)
        },
        'thermal': {
            'outdoor_temp_c': round(outdoor_temp, 1),
            'indoor_temp_c': round(indoor_temp, 1),
            'humidity_pct': round(humidity, 1),
            'temp_delta': round(indoor_temp - outdoor_temp, 1)
        }
    }

# ============================================
# DAILY HISTORICAL DATA GENERATOR
# ============================================

@st.cache_data
def generate_daily_historical_data():
    """Generate 10 years of daily data (3650 days)"""
    
    start_date = datetime(2016, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(3650)]
    
    daily_data = []
    
    for date in dates:
        month = date.month
        year = date.year
        
        # Solar
        if 3 <= month <= 5:
            solar = random.uniform(800, 1200)
        elif 6 <= month <= 9:
            solar = random.uniform(300, 600)
        elif 10 <= month <= 11:
            solar = random.uniform(500, 800)
        else:
            solar = random.uniform(400, 700)
        solar *= (1 + (year-2016) * 0.01)
        
        # Air Quality
        if month in [12, 1, 2]:
            aqi_base = 80
        elif month in [6, 7, 8, 9]:
            aqi_base = 40
        else:
            aqi_base = 55
        pm25 = aqi_base * random.uniform(0.7, 1.3)
        pm10 = pm25 * 1.6
        
        # Water & Waste
        water_consumption = 3500 * 150 * random.uniform(0.8, 1.2)
        waste = 3500 * 0.4 * random.uniform(0.9, 1.1)
        
        # Temperature
        if month in [12, 1, 2]:
            temp = random.uniform(2, 8)
        elif month in [3, 4, 5]:
            temp = random.uniform(12, 20)
        elif month in [6, 7, 8, 9]:
            temp = random.uniform(18, 24)
        else:
            temp = random.uniform(8, 15)
        
        daily_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'year': year,
            'month': month,
            'day': date.day,
            'solar_kwh': round(solar, 1),
            'pm25': round(pm25, 1),
            'pm10': round(pm10, 1),
            'water_consumption_l': round(water_consumption, 0),
            'waste_kg': round(waste, 1),
            'temperature_c': round(temp, 1),
            'heating_demand': round(random.uniform(500, 2000), 1)
        })
    
    return pd.DataFrame(daily_data)
@st.cache_data
def generate_campus_data():
    """Generate realistic campus data for all blocks"""
    
    # Building data from our earlier discussion
    buildings = {
        "Academic Block": {
            "area": 13500, "floors": 4, "students": 2650,
            "base_energy": 5500, "peak_factor": 1.3
        },
        "Hostel Block A": {
            "area": 1800, "floors": 3, "students": 400,
            "base_energy": 1800, "peak_factor": 1.4
        },
        "Hostel Block B": {
            "area": 1800, "floors": 3, "students": 400,
            "base_energy": 1800, "peak_factor": 1.4
        },
        "Hostel Block C": {
            "area": 1800, "floors": 3, "students": 400,
            "base_energy": 1800, "peak_factor": 1.4
        },
        "Support Complex": {
            "area": 4075, "floors": 3, "students": 700,
            "base_energy": 2500, "peak_factor": 1.5
        },
        "Dining Hall": {
            "area": 600, "floors": 1, "students": 400,
            "base_energy": 800, "peak_factor": 1.8
        }
    }
    
    # Generate hourly data for a typical day
    hours = list(range(24))
    hourly_data = []
    
    solar_capacity = 2500  # kW
    current_hour = datetime.now().hour
    
    for hour in hours:
        hour_data = {"hour": hour}
        
        # Solar generation (6 AM to 6 PM)
        if 6 <= hour <= 18:
            solar_factor = np.sin((hour-6)/12 * np.pi)
            hour_data["solar_kw"] = solar_capacity * solar_factor * random.uniform(0.9, 1.1)
        else:
            hour_data["solar_kw"] = 0
        
        # Total energy demand
        total_demand = 0
        for building, data in buildings.items():
            # Base demand with time variation
            if 8 <= hour <= 18:  # Daytime
                demand = data["base_energy"] * 0.8
            elif 18 <= hour <= 23:  # Evening peak
                demand = data["base_energy"] * data["peak_factor"]
            else:  # Night
                demand = data["base_energy"] * 0.3
            
            # Add random variation
            demand *= random.uniform(0.85, 1.15)
            hour_data[f"{building}_kw"] = demand
            total_demand += demand
        
        hour_data["total_demand_kw"] = total_demand
        hour_data["grid_import_kw"] = max(0, total_demand - hour_data["solar_kw"])
        hour_data["battery_soc"] = 50 + 30 * np.sin((hour-6)/12 * np.pi) if hour <= 18 else max(20, 80 - (hour-18)*10)
        
        hourly_data.append(hour_data)
    
    df_hourly = pd.DataFrame(hourly_data)
    
    # Generate 10-year monthly data
    start_date = datetime(2016, 1, 1)
    dates = [start_date + timedelta(days=30*i) for i in range(120)]  # 10 years
    
    monthly_data = []
    for i, date in enumerate(dates):
        month = date.month
        year = date.year
        
        # Seasonal patterns for Shimla
        if month in [12, 1, 2]:  # Winter
            temp = random.uniform(2, 8)
            solar = random.uniform(3000, 4500)
            rain = random.uniform(40, 80)
        elif month in [3, 4, 5]:  # Summer
            temp = random.uniform(15, 22)
            solar = random.uniform(6000, 8000)
            rain = random.uniform(30, 60)
        elif month in [6, 7, 8, 9]:  # Monsoon
            temp = random.uniform(18, 25)
            solar = random.uniform(2500, 4000)
            rain = random.uniform(150, 300)
        else:  # Autumn
            temp = random.uniform(12, 18)
            solar = random.uniform(4500, 6000)
            rain = random.uniform(20, 40)
        
        monthly_data.append({
            "date": date,
            "month": month,
            "year": year,
            "temperature": round(temp + (year-2016)*0.2, 1),
            "solar_kwh": round(solar * random.uniform(0.9, 1.1), 0),
            "rainfall_mm": round(rain * random.uniform(0.7, 1.3), 1),
            "energy_demand_kwh": round(random.uniform(14000, 18000), 0),
            "aqi": round(random.uniform(40, 120), 0)
        })
    
    df_monthly = pd.DataFrame(monthly_data)
    
    return buildings, df_hourly, df_monthly

# Load data
buildings, df_hourly, df_monthly = generate_campus_data()
current_hour = datetime.now().hour
current_data = df_hourly[df_hourly['hour'] == current_hour].iloc[0]

# ============================================
# SIDEBAR - Navigation
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/himalayas.png")
    st.markdown("## 🏛️ HPU Control Center")
    
    # Navigation
    page = st.radio(
        "Navigate to:",
        ["🏠 Dashboard", 
         "📊 Simulation Results", 
         "🏢 Digital Twin", 
         "🔁 Scenario Analysis", 
         "💰 Cost & Sustainability",
         "📈 Analytics",
         "⚙️ System Architecture",
         "🔴 Live Sensors",
         "📅 10-Year Daily Data",
         "📊 What-If Scenario"]
    )
    
    st.markdown("---")
    st.markdown(f"**Current Time:** {datetime.now().strftime('%H:%M')}")
    st.markdown(f"**Date:** {datetime.now().strftime('%d %b %Y')}")
    st.progress(0.7, "System Health: 70%")  
    
    st.markdown("---")
    st.subheader("🔴 SENSOR STATUS")
    
    # Sensor status indicators
    sensor_status = {
        "Solar Sensors": "✅ Online" if random.random() > 0.1 else "⚠️ Offline",
        "AQI Sensors": "✅ Online" if random.random() > 0.1 else "⚠️ Offline",
        "Water Sensors": "✅ Online" if random.random() > 0.1 else "⚠️ Offline",
        "Waste Sensors": "✅ Online" if random.random() > 0.1 else "⚠️ Offline",
        "Thermal Sensors": "✅ Online" if random.random() > 0.1 else "⚠️ Offline"
    }
    
    for sensor, status in sensor_status.items():
        st.text(f"{sensor}: {status}")
    
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# ============================================
# PAGE 1: DASHBOARD
# ============================================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-title">🏛️ HPU Smart Campus Dashboard</p>', unsafe_allow_html=True)
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⚡ Total Demand", f"{current_data['total_demand_kw']:.0f} kW", 
                  f"{((current_data['total_demand_kw']/15000)-1)*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("☀️ Solar Gen", f"{current_data['solar_kw']:.0f} kW", 
                  f"{((current_data['solar_kw']/2500)-1)*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🔋 Grid Import", f"{current_data['grid_import_kw']:.0f} kW", 
                  f"{current_data['battery_soc']:.0f}% battery")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        sustainability_score = 65 + random.randint(-5, 5)
        st.metric("🌱 Sustainability", f"{sustainability_score}%", 
                  "Good" if sustainability_score > 60 else "Fair")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Energy chart
    st.markdown('<p class="section-header">⚡ Energy Flow (24 Hours)</p>', unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_hourly['hour'], 
        y=df_hourly['solar_kw'],
        name="Solar Generation",
        fill='tozeroy',
        line=dict(color='orange', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=df_hourly['hour'], 
        y=df_hourly['total_demand_kw'],
        name="Total Demand",
        line=dict(color='red', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=df_hourly['hour'], 
        y=df_hourly['grid_import_kw'],
        name="Grid Import",
        line=dict(color='blue', width=3, dash='dot')
    ))
    fig.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    # Alerts panel
    st.markdown('<p class="section-header">⚠️ Live Alerts</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if current_data['total_demand_kw'] > 15000:
            st.markdown('<div class="alert-box alert-danger">🚨 CRITICAL: Energy demand exceeding 15,000 kW!</div>', unsafe_allow_html=True)
        elif current_data['total_demand_kw'] > 13000:
            st.markdown('<div class="alert-box alert-warning">⚠️ WARNING: High energy usage detected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box alert-success">✅ Energy usage normal</div>', unsafe_allow_html=True)
    
    with col2:
        if current_data['solar_kw'] < 500 and 6 <= current_hour <= 18:
            st.markdown('<div class="alert-box alert-warning">⚠️ Low solar output - possible weather issue</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box alert-success">☀️ Solar generation normal</div>', unsafe_allow_html=True)
    
    if current_hour in [18, 19, 20, 21] and current_data['total_demand_kw'] > 14000:
        st.markdown('<div class="alert-box alert-warning">⚠️ Peak hours - consider load shedding</div>', unsafe_allow_html=True)

# ============================================
# PAGE 2: SIMULATION RESULTS
# ============================================
elif page == "📊 Simulation Results":
    st.markdown('<p class="main-title">📊 EnergyPlus Simulation Results</p>', unsafe_allow_html=True)
    
    # Scenario selector
    scenario = st.selectbox(
        "Select Comparison Scenario",
        ["☀️ Solar Integration", "🧱 Insulation Upgrade", "🪟 Window Upgrade", "💡 Lighting Upgrade", "❄️ HVAC Upgrade"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Before")
        if scenario == "☀️ Solar Integration":
            st.metric("Annual Energy", "6,500 MWh")
            st.metric("Grid Import", "6,500 MWh")
            st.metric("Energy Cost", "₹39 Lakhs")
            st.metric("CO₂ Emissions", "5,330 tons")
        elif scenario == "🧱 Insulation Upgrade":
            st.metric("Annual Energy", "6,500 MWh")
            st.metric("Heating Load", "2,800 MWh")
            st.metric("Cooling Load", "1,200 MWh")
        elif scenario == "🪟 Window Upgrade":
            st.metric("Annual Energy", "6,500 MWh")
            st.metric("Heat Loss", "1,500 MWh")
        elif scenario == "💡 Lighting Upgrade":
            st.metric("Lighting Energy", "1,200 MWh")
            st.metric("Total Energy", "6,500 MWh")
        else:  # HVAC
            st.metric("Annual Energy", "6,500 MWh")
            st.metric("HVAC Energy", "3,200 MWh")
            st.metric("COP", "2.5")
    
    with col2:
        st.subheader("After")
        if scenario == "☀️ Solar Integration":
            st.metric("Annual Energy", "6,500 MWh")
            st.metric("Grid Import", "3,900 MWh", delta="-40%")
            st.metric("Energy Cost", "₹23.4 Lakhs", delta="-40%")
            st.metric("CO₂ Emissions", "3,198 tons", delta="-40%")
        elif scenario == "🧱 Insulation Upgrade":
            st.metric("Annual Energy", "5,525 MWh", delta="-15%")
            st.metric("Heating Load", "2,100 MWh", delta="-25%")
            st.metric("Cooling Load", "1,020 MWh", delta="-15%")
        elif scenario == "🪟 Window Upgrade":
            st.metric("Annual Energy", "5,850 MWh", delta="-10%")
            st.metric("Heat Loss", "1,275 MWh", delta="-15%")
        elif scenario == "💡 Lighting Upgrade":
            st.metric("Lighting Energy", "1,020 MWh", delta="-15%")
            st.metric("Total Energy", "6,275 MWh", delta="-3.5%")
        else:  # HVAC
            st.metric("Annual Energy", "5,200 MWh", delta="-20%")
            st.metric("HVAC Energy", "2,240 MWh", delta="-30%")
            st.metric("COP", "4.0", delta="+60%")
    
    # Monthly breakdown
    st.markdown('<p class="section-header">📅 Monthly Energy Breakdown</p>', unsafe_allow_html=True)
    
    fig = px.bar(
        df_monthly.groupby('month')['energy_demand_kwh'].mean().reset_index(),
        x='month', y='energy_demand_kwh',
        labels={'month': 'Month', 'energy_demand_kwh': 'Energy (kWh)'},
        color_discrete_sequence=['#2E7D32']
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 3: DIGITAL TWIN
# ============================================
elif page == "🏢 Digital Twin":
    st.markdown('<p class="main-title">🏢 Digital Twin - Academic Block</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Zone")
        floor = st.selectbox("Floor", ["Ground Floor", "First Floor", "Second Floor", "Third Floor"])
        
        if floor == "Ground Floor":
            zone = st.selectbox("Zone", ["Main Lobby", "Admin Offices", "Auditorium", "Seminar Hall 1", "Server Room"])
        elif floor == "First Floor":
            zone = st.selectbox("Zone", ["Lecture Hall 1", "Lecture Hall 2", "Classroom 1", "Faculty Lounge"])
        elif floor == "Second Floor":
            zone = st.selectbox("Zone", ["Reading Area", "Digital Section", "Group Study Room 1", "Book Stacks"])
        else:
            zone = st.selectbox("Zone", ["Computer Lab 1", "Engineering Lab", "Science Lab", "Research Area"])
        
        st.markdown("---")
        st.subheader("Zone Data")
        
        # Generate zone-specific data
        zone_data = {
            "Main Lobby": {"energy": 45, "temp": 22, "occ": 30, "light": 85},
            "Admin Offices": {"energy": 120, "temp": 23, "occ": 85, "light": 90},
            "Auditorium": {"energy": 80, "temp": 21, "occ": 0, "light": 10},
            "Lecture Hall 1": {"energy": 95, "temp": 24, "occ": 75, "light": 95},
            "Reading Area": {"energy": 60, "temp": 22, "occ": 40, "light": 100},
        }.get(zone, {"energy": 70, "temp": 22, "occ": 50, "light": 80})
        
        st.metric("⚡ Energy", f"{zone_data['energy']} kWh/h")
        st.metric("🌡️ Temperature", f"{zone_data['temp']}°C")
        st.metric("👥 Occupancy", f"{zone_data['occ']}%")
        st.metric("💡 Lighting", f"{zone_data['light']}%")
        
        if zone_data['energy'] > 100:
            st.warning("⚠️ High energy usage")
        if zone_data['temp'] > 26:
            st.warning("🌡️ Overheating")
    
    with col2:
        st.subheader(f"{floor} Plan")
        
        # Create a simple floor plan representation
        if floor == "Ground Floor":
            st.image("https://via.placeholder.com/600x400/2E7D32/FFFFFF?text=Ground+Floor+Plan", use_container_width=True)
            st.caption("1: Main Lobby | 2: Admin Offices | 3: Auditorium | 4: Seminar Halls | 5: Server Room")
        elif floor == "First Floor":
            st.image("https://via.placeholder.com/600x400/1B5E20/FFFFFF?text=First+Floor+Plan", use_container_width=True)
            st.caption("1-5: Lecture Halls | 6-15: Classrooms | 16: Faculty Lounge")
        else:
            st.image("https://via.placeholder.com/600x400/0D47A1/FFFFFF?text=Floor+Plan", use_container_width=True)

# ============================================
# PAGE 4: SCENARIO ANALYSIS
# ============================================
elif page == "🔁 Scenario Analysis":
    st.markdown('<p class="main-title">🔁 What-If Scenario Analysis</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Adjust Parameters")
        
        insulation = st.select_slider("🧱 Insulation", options=["Poor", "Standard", "High"], value="Standard")
        windows = st.select_slider("🪟 Windows", options=["Single", "Double", "Triple"], value="Double")
        solar_area = st.slider("☀️ Solar Panel Area (m²)", 0, 5000, 2000, step=100)
        occupancy = st.slider("👥 Occupancy Level", 0, 100, 70, step=5)
        hvac_cop = st.slider("❄️ HVAC Efficiency (COP)", 2.0, 5.0, 3.5, step=0.1)
        lighting = st.radio("💡 Lighting", ["Conventional", "LED"], horizontal=True)
        
        analyze = st.button("🔮 Analyze Scenario", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("Results")
        
        if analyze or "last_analysis" in st.session_state:
            # Base energy: 15,000 kWh/day for campus
            base_energy = 15000
            
            # Apply factors
            insulation_factors = {"Poor": 1.0, "Standard": 0.9, "High": 0.75}
            window_factors = {"Single": 1.0, "Double": 0.85, "Triple": 0.75}
            lighting_factor = 0.85 if lighting == "LED" else 1.0
            
            energy = base_energy
            energy *= insulation_factors[insulation]
            energy *= window_factors[windows]
            energy *= lighting_factor
            energy *= (0.8 + 0.4 * occupancy/100)
            energy *= (3.5 / hvac_cop)
            
            # Solar offset: 150 kWh/year per m²
            solar_offset = solar_area * 150 / 365
            energy = max(5000, energy - solar_offset)
            
            # Calculate savings
            savings = (base_energy - energy) * 365 * 6 / 100000  # Lakhs per year at ₹6/kWh
            co2_saved = (base_energy - energy) * 365 * 0.8 / 1000  # tons CO2
            
            st.metric("⚡ Daily Energy", f"{energy:.0f} kWh", 
                      f"{((energy/base_energy)-1)*100:.1f}%")
            st.metric("💰 Annual Savings", f"₹{savings:.1f} Lakhs")
            st.metric("🌲 CO₂ Reduction", f"{co2_saved:.0f} tons/year")
            st.metric("💡 Efficiency Gain", f"{((base_energy-energy)/base_energy*100):.1f}%")
            
            # Payback calculation
            if solar_area > 0:
                solar_cost = solar_area * 45000 / 0.3  # ₹45000/kW with 30% subsidy
                payback = solar_cost / (savings * 100000)
                st.metric("⏱️ Solar Payback", f"{payback:.1f} years")
            
            st.session_state.last_analysis = True
        else:
            st.info("👆 Adjust parameters and click 'Analyze Scenario'")

# ============================================
# PAGE 5: COST & SUSTAINABILITY
# ============================================
elif page == "💰 Cost & Sustainability":
    st.markdown('<p class="main-title">💰 Cost Analysis & Environmental Impact</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Energy Costs")
        annual_energy = 6500000  # kWh
        tariff = 6.0  # ₹/kWh
        annual_cost = annual_energy * tariff / 100000  # Lakhs
        
        st.metric("Annual Consumption", f"{annual_energy/1e6:.1f} GWh")
        st.metric("Electricity Tariff", f"₹{tariff}/kWh")
        st.metric("Annual Energy Cost", f"₹{annual_cost:.1f} Lakhs")
        
        with st.expander("Cost Breakdown"):
            st.write("• Academic: ₹18.5 Lakhs")
            st.write("• Hostels: ₹12.2 Lakhs")
            st.write("• Support: ₹8.3 Lakhs")
    
    with col2:
        st.subheader("Solar Investment")
        solar_capacity = 2500  # kW
        solar_cost_per_kw = 45000  # ₹
        subsidy = 0.30
        annual_solar = solar_capacity * 1500  # kWh/year
        
        total_cost = solar_capacity * solar_cost_per_kw * (1 - subsidy) / 100000  # Lakhs
        annual_savings = annual_solar * tariff / 100000  # Lakhs
        payback = total_cost / annual_savings
        
        st.metric("Solar Capacity", f"{solar_capacity} kW")
        st.metric("Total Investment", f"₹{total_cost:.1f} Lakhs")
        st.metric("Annual Savings", f"₹{annual_savings:.1f} Lakhs")
        st.metric("Payback Period", f"{payback:.1f} years")
        
        with st.expander("Subsidy Details"):
            st.write("• MNRE Subsidy: 30%")
            st.write("• State Subsidy: Additional 10% available")
    
    with col3:
        st.subheader("Environmental Impact")
        
        grid_emission = 0.82  # kg CO2/kWh
        annual_solar = solar_capacity * 1500
        co2_saved = annual_solar * grid_emission / 1000  # tons
        trees_equivalent = co2_saved * 50  # 1 tree absorbs ~20kg CO2/year
        
        st.metric("CO₂ Reduction", f"{co2_saved:.0f} tons/year")
        st.metric("Equivalent Trees", f"{trees_equivalent:.0f}")
        st.metric("Cars Removed", f"{co2_saved/4.6:.0f}")
        
        # Progress bar for sustainability goal
        st.progress(0.45, "HPU Sustainability Goal: 45%")
        st.caption("Target: 100% renewable by 2035")

# ============================================
# PAGE 6: ANALYTICS
# ============================================
elif page == "📈 Analytics":
    st.markdown('<p class="main-title">📈 Advanced Analytics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Load Factor
        avg_demand = df_hourly['total_demand_kw'].mean()
        peak_demand = df_hourly['total_demand_kw'].max()
        load_factor = avg_demand / peak_demand
        
        st.metric("📊 Load Factor", f"{load_factor:.2f}", 
                  "Good" if load_factor > 0.7 else "Poor")
        
        # Energy Intensity
        total_area = sum(b["area"] for b in buildings.values())
        eui = (avg_demand * 24 * 365) / total_area
        st.metric("🏢 Energy Intensity", f"{eui:.1f} kWh/m²/year",
                  "vs 120 target")
        
        # Renewable Penetration
        total_solar = df_hourly['solar_kw'].sum()
        total_demand = df_hourly['total_demand_kw'].sum()
        ren_pct = (total_solar / total_demand) * 100
        st.metric("🌱 Renewable %", f"{ren_pct:.1f}%",
                  f"+{ren_pct-15:.1f}% vs target")
    
    with col2:
        # Peak Hours
        peak_hour = df_hourly.loc[df_hourly['total_demand_kw'].idxmax(), 'hour']
        st.metric("⏰ Peak Hour", f"{int(peak_hour)}:00", "Evening peak")
        
        # Top Consumers
        st.subheader("Top 3 Energy Consumers")
        consumers = {
            "Academic Block": 5500,
            "Hostel Complex": 5400,
            "Support Complex": 2500
        }
        for name, value in sorted(consumers.items(), key=lambda x: x[1], reverse=True):
            st.write(f"⚠️ {name}: {value} kWh/day")
    
    # Monthly trends
    st.markdown('<p class="section-header">📅 10-Year Monthly Trends</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Temperature", "Solar", "AQI"])
    
    with tab1:
        fig = px.line(df_monthly, x='date', y='temperature', title="Temperature Trend (2016-2026)")
        fig.update_traces(line_color='red')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.line(df_monthly, x='date', y='solar_kwh', title="Solar Generation")
        fig.update_traces(line_color='orange')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = px.line(df_monthly, x='date', y='aqi', title="Air Quality Index")
        fig.update_traces(line_color='green')
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE 7: SYSTEM ARCHITECTURE
# ============================================
elif page == "⚙️ System Architecture":
    st.markdown('<p class="main-title">⚙️ System Architecture & Data Flow</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Data Pipeline")
        
        # Create architecture diagram using simple text
        diagram = """
        ┌─────────┐     ┌──────────┐     ┌───────────┐     ┌────────────┐
        │SketchUp │────▶│OpenStudio│────▶│EnergyPlus │────▶│Streamlit   │
        │3D Model │     │Simulation│     │Calculations│    │Dashboard   │
        └─────────┘     └──────────┘     └───────────┘     └────────────┘
                                                                  │
                                                          ┌───────┴───────┐
                                                          │   Web App     │
                                                          │   Live URL    │
                                                          └───────────────┘
        """
        st.text(diagram)
        
        st.markdown("---")
        st.subheader("Tools Used")
        
        tools = {
            "SketchUp": "3D modeling of campus buildings (Academic, Hostel, Support)",
            "OpenStudio": "Building energy modeling and simulation",
            "EnergyPlus": "Detailed energy calculations and load analysis",
            "Python": "Data processing and backend logic",
            "Streamlit": "Interactive web dashboard and visualization",
            "GitHub": "Version control and cloud deployment"
        }
        
        for tool, desc in tools.items():
            st.markdown(f"**{tool}:** {desc}")
    
    with col2:
        st.subheader("Data Sources")
        data_sources = """
        ✅ **Historical Data (2016-2026)**
        • Temperature
        • Solar radiation
        • Rainfall
        • Air quality
        
        ✅ **Building Specifications**
        • Floor plans
        • Material properties
        • Occupancy schedules
        
        ✅ **Utility Data**
        • Electricity tariffs
        • Water costs
        • Subsidy rates
        """
        st.markdown(data_sources)
        
        st.metric("Data Points", "120,000+", "10 years")
        st.metric("Buildings Modeled", "6", "13,500 m² total")

# ============================================
# PAGE 8: LIVE SENSORS
# ============================================
elif page == "🔴 Live Sensors":
    st.markdown('<p class="main-title">🔴 Live Sensor Data (Google Sheets)</p>', unsafe_allow_html=True)
    
    df = load_sensor_data()
    
    if df is not None and not df.empty:
        # Latest reading
        last = df.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌡️ Temperature", f"{last['Temperature (°C)']} °C")
        col2.metric("💧 Humidity", f"{last['Humidity (%)']} %")
        col3.metric("📏 Distance", f"{last['Distance (cm)']} cm")
        col4.metric("🧪 Gas Level", f"{last['Gas Level']}")
        
        # Historical chart
        st.subheader("📊 Historical Data")
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        st.line_chart(df.set_index('Timestamp')[['Temperature (°C)', 'Humidity (%)']])
        
        # Alerts
        st.subheader("🚨 Alerts")
        alerts = []
        
        temp = float(last['Temperature (°C)'])
        if temp > 30:
            alerts.append("⚠️ **High Temperature** > 30°C")
        if temp < 10:
            alerts.append("⚠️ **Low Temperature** < 10°C")
        
        hum = float(last['Humidity (%)'])
        if hum > 80:
            alerts.append("⚠️ **High Humidity** > 80%")
        if hum < 30:
            alerts.append("⚠️ **Low Humidity** < 30%")
        
        dist = float(last['Distance (cm)'])
        if dist < 10:
            alerts.append("⚠️ **Tank/Bin Full** (Distance < 10cm)")
        if dist > 200:
            alerts.append("⚠️ **Tank/Bin Empty** (Distance > 200cm)")
        
        gas = float(last['Gas Level'])
        if gas > 2000:
            alerts.append("⚠️ **High Gas Level** > 2000")
        
        if alerts:
            for alert in alerts:
                st.error(alert)
        else:
            st.success("✅ All parameters are within normal range.")
        
        if st.checkbox("Show Raw Data"):
            st.dataframe(df.tail(20))
    else:
        st.warning("No data available. Make sure the Python script is running.")
# ============================================
# PAGE 9: 10-YEAR DAILY DATA
# ============================================
elif page == "📅 10-Year Daily Data":
    st.markdown('<p class="main-title">📅 10-Year Daily Historical Data (2016-2026)</p>', unsafe_allow_html=True)
    
    # Load daily data
    daily_df = generate_daily_historical_data()
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2016, 1, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2026, 12, 31))
    
    # Filter data
    mask = (pd.to_datetime(daily_df['date']) >= pd.to_datetime(start_date)) & \
           (pd.to_datetime(daily_df['date']) <= pd.to_datetime(end_date))
    filtered_df = daily_df[mask]
    
    # Parameter selector
    param = st.selectbox(
        "Select Parameter",
        ["Solar Energy (kWh)", "PM2.5", "PM10", "Water Consumption (L)", 
         "Waste Generation (kg)", "Temperature (°C)", "Heating Demand"]
    )
    
    # Map parameter
    param_map = {
        "Solar Energy (kWh)": "solar_kwh",
        "PM2.5": "pm25",
        "PM10": "pm10",
        "Water Consumption (L)": "water_consumption_l",
        "Waste Generation (kg)": "waste_kg",
        "Temperature (°C)": "temperature_c",
        "Heating Demand": "heating_demand"
    }
    
    # Display chart
    st.subheader(f"Daily {param} from {start_date} to {end_date}")
    
    fig = px.line(
        filtered_df, 
        x='date', 
        y=param_map[param],
        title=f"{param} - Daily Values",
        labels={'date': 'Date', param_map[param]: param}
    )
    fig.update_traces(line_color='#2E7D32')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average", f"{filtered_df[param_map[param]].mean():.1f}")
    with col2:
        st.metric("Maximum", f"{filtered_df[param_map[param]].max():.1f}")
    with col3:
        st.metric("Minimum", f"{filtered_df[param_map[param]].min():.1f}")
    
    # Show raw data
    if st.checkbox("Show Raw Daily Data"):
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"hpu_daily_data_{start_date}_{end_date}.csv",
            mime="text/csv"
        )

# ============================================
# WHAT-IF SCENARIO PAGE
# ============================================
elif page == "📊 What-If Scenario":
    st.markdown('<p class="main-title">📊 What-If Scenario Engine</p>', unsafe_allow_html=True)
    
    st.markdown("Adjust the parameters below to see how they affect campus energy consumption.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Adjust Parameters")
        
        insulation = st.select_slider(
            "🧱 Insulation Level",
            options=["Poor", "Standard", "Good", "Excellent"],
            value="Standard"
        )
        
        window_type = st.select_slider(
            "🪟 Window Type",
            options=["Single", "Double", "Triple"],
            value="Double"
        )
        
        solar_area = st.slider(
            "☀️ Solar Panel Area (m²)",
            0, 10000, 2000, step=100
        )
        
        occupancy = st.slider(
            "👥 Occupancy Level (%)",
            0, 100, 70, step=5
        )
        
        hvac_efficiency = st.slider(
            "❄️ HVAC Efficiency (COP)",
            2.0, 5.0, 3.5, step=0.1
        )
        
        lighting = st.radio(
            "💡 Lighting Type",
            ["Conventional", "LED"],
            horizontal=True
        )
        
        analyze = st.button("🔮 Run Scenario", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("📊 Results")
        
        if analyze:
            # Base energy: 15,000 kWh/day
            base_energy = 15000
            
            # Insulation factors
            insulation_factors = {
                "Poor": 1.0,
                "Standard": 0.90,
                "Good": 0.80,
                "Excellent": 0.70
            }
            
            # Window factors
            window_factors = {
                "Single": 1.0,
                "Double": 0.85,
                "Triple": 0.75
            }
            
            # Lighting factor
            lighting_factor = 0.85 if lighting == "LED" else 1.0
            
            # Calculate energy
            energy = base_energy
            energy *= insulation_factors[insulation]
            energy *= window_factors[window_type]
            energy *= lighting_factor
            energy *= (0.8 + 0.4 * occupancy / 100)
            energy *= (3.5 / hvac_efficiency)
            
            # Solar offset: 150 kWh/year per m²
            solar_offset = solar_area * 150 / 365
            energy = max(5000, energy - solar_offset)
            
            # Calculate savings
            savings = (base_energy - energy) * 365 * 6 / 100000
            co2_saved = (base_energy - energy) * 365 * 0.8 / 1000
            
            # Display results
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("⚡ Daily Energy", f"{energy:.0f} kWh", f"{((energy/base_energy)-1)*100:.1f}%")
                st.metric("💰 Annual Savings", f"₹{savings:.1f} Lakhs")
            with col_b:
                st.metric("🌲 CO₂ Reduction", f"{co2_saved:.0f} tons/year")
                st.metric("💡 Efficiency Gain", f"{((base_energy-energy)/base_energy*100):.1f}%")
            
            # Chart comparison
            st.subheader("📊 Energy Comparison")
            
            comparison_data = pd.DataFrame({
                'Scenario': ['Current', 'Optimized'],
                'Energy (kWh/day)': [base_energy, energy]
            })
            
            st.bar_chart(comparison_data.set_index('Scenario'))
            
            if solar_area > 0:
                solar_cost = solar_area * 45000 * 0.7 / 100000
                if savings > 0:
                    payback = solar_cost / savings
                    st.metric("⏱️ Solar Payback", f"{payback:.1f} years")
                else:
                    st.info("Solar payback: No savings to calculate")
            else:
                st.info("Add solar panels to see payback calculation")
        else:
            st.info("👆 Adjust parameters and click 'Run Scenario'")
# ============================================
# IF NO PAGE MATCHES (should never happen)
# ============================================
else:
    st.error("Page not found")

# Footer for all pages
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 0.5rem; font-size: 0.8rem;'>
        🌱 HPU Digital Campus v2.0 | Smart Control Center | Data: 2016-2026
    </div>
    """,
    unsafe_allow_html=True
)

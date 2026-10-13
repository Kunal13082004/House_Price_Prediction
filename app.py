
import streamlit as st
from real_market_data import get_nhb_data


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Kunal.AI | House Price Intelligence",
    page_icon="🏡",
    layout="wide"
)


# =====================================================
# NHB CITY MAPPING
# =====================================================

NHB_CITY_IDS = {
    "Mumbai": 1,
    "Pune": 2,
    "Hyderabad": 18,
    "Bengaluru": 23,
    "Chennai": 26,
    "Kolkata": 27,
    "Ahmedabad": 28,
    "Jaipur": 38,
    "Delhi": 113,
    "Noida": 112,
    "Gurugram": 82,
    "Ludhiana": 68,
    "Chandigarh": 37,
}


# =====================================================
# CUSTOM DESIGN
# =====================================================

st.html("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 10%, #172554, transparent 30%),
        radial-gradient(circle at 90% 10%, #164e63, transparent 30%),
        linear-gradient(135deg, #07111f, #0b1220, #111827);
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 30px;
}

.hero {
    padding: 40px;
    border-radius: 28px;
    margin-bottom: 25px;
    background: linear-gradient(
        135deg,
        rgba(30,41,59,0.95),
        rgba(15,23,42,0.85)
    );
    border: 1px solid rgba(148,163,184,0.2);
    box-shadow: 0 25px 80px rgba(0,0,0,0.35);
}

.badge {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 30px;
    color: #86efac;
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(134,239,172,0.25);
    font-size: 12px;
    font-weight: 700;
}

.title {
    font-size: 52px;
    font-weight: 800;
    margin-top: 15px;
    color: #f8fafc;
}

.description {
    color: #cbd5e1;
    font-size: 17px;
    line-height: 1.7;
    max-width: 800px;
    margin-top: 10px;
}

.signature {
    color: #93c5fd;
    font-weight: 700;
    margin-top: 15px;
}

.result {
    padding: 32px;
    border-radius: 25px;
    margin: 25px 0;
    background: linear-gradient(
        135deg,
        rgba(16,185,129,0.22),
        rgba(14,116,144,0.12)
    );
    border: 1px solid rgba(52,211,153,0.30);
}

.result-label {
    color: #86efac;
    font-size: 14px;
    font-weight: 700;
}

.result-price {
    font-size: 44px;
    font-weight: 800;
    margin: 8px 0;
    color: white;
}

.result-info {
    color: #cbd5e1;
    font-size: 13px;
}

.info {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(148,163,184,0.15);
    border-radius: 20px;
    padding: 22px;
    line-height: 1.8;
}

div[data-testid="stMetric"] {
    background: rgba(15,23,42,0.65);
    border: 1px solid rgba(148,163,184,0.15);
    padding: 15px;
    border-radius: 15px;
}

.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    padding: 35px 0 15px;
}
</style>
""")


# =====================================================
# HERO SECTION - HTML DISPLAY FIXED
# =====================================================

st.html("""
<div class="hero">
    <div class="badge">
        ● NHB RESIDEX BENCHMARK ESTIMATOR
    </div>

    <div class="title">
        🏡 Kunal.AI
    </div>

    <div class="description">
        Explore supported Indian cities and estimate property
        values using available NHB RESIDEX housing benchmarks.
    </div>

    <div class="signature">
        Built &amp; designed by Kunal
    </div>
</div>
""")


# =====================================================
# PROPERTY PRICE ESTIMATOR
# =====================================================

st.header("🏠 Property Price Estimator")

st.caption(
    "Select a supported city and enter the property area "
    "to calculate an NHB benchmark-based estimate."
)

left, right = st.columns(2)

with left:
    selected_city = st.selectbox(
        "📍 Select City",
        sorted(NHB_CITY_IDS.keys())
    )

with right:
    area = st.number_input(
        "📐 Property Area (sq ft)",
        min_value=100,
        max_value=20000,
        value=1800,
        step=50
    )


# =====================================================
# FETCH NHB DATA
# =====================================================

if st.button(
    "🚀 Calculate Property Value",
    use_container_width=True,
    type="primary"
):

    city_id = NHB_CITY_IDS[selected_city]

    with st.spinner(
        f"Fetching NHB RESIDEX benchmark for {selected_city}..."
    ):
        try:
            result = get_nhb_data(
                city_id=city_id,
                lookup="HFC",
                price_method_id=2
            )
        except Exception as error:
            result = {
                "success": False,
                "message": str(error)
            }

    if result.get("success"):

        rows = result.get("data", [])

        if isinstance(rows, list) and rows:

            latest = rows[-1]

            try:
                price_sqm = float(
                    latest["WTAVG_COMPOSITE_sqm"]
                )

                if price_sqm <= 0:
                    raise ValueError("Invalid benchmark price.")

                # Rupees per square metre to square foot
                price_per_sqft = price_sqm * 0.092903
                estimated_value = price_per_sqft * area

                st.session_state["nhb_price"] = price_per_sqft
                st.session_state["estimated_value"] = estimated_value
                st.session_state["nhb_quarter"] = latest.get(
                    "QTR_YEAR", "N/A"
                )
                st.session_state["nhb_index"] = float(
                    latest.get("HFC_INDEX", 0) or 0
                )
                st.session_state["nhb_records"] = int(
                    latest.get("USABLE_RECORD_COUNT", 0) or 0
                )
                st.session_state["selected_city"] = selected_city
                st.session_state["selected_area"] = area

            except (KeyError, TypeError, ValueError) as error:
                st.error(
                    "NHB returned data, but a usable price "
                    f"could not be calculated: {error}"
                )

        else:
            st.error(
                f"No usable NHB benchmark records were returned "
                f"for {selected_city}."
            )

    else:
        st.error(
            "Unable to fetch NHB data: "
            + str(result.get("message", "Unknown error"))
        )


# =====================================================
# RESULTS
# =====================================================

if "estimated_value" in st.session_state:

    estimated_value = st.session_state["estimated_value"]
    nhb_price = st.session_state["nhb_price"]
    result_city = st.session_state["selected_city"]
    result_area = st.session_state["selected_area"]
    quarter = st.session_state["nhb_quarter"]

    st.html(f"""
    <div class="result">
        <div class="result-label">
            🏦 NHB MARKET BENCHMARK ESTIMATE
        </div>

        <div class="result-price">
            ₹{estimated_value:,.0f}
        </div>

        <div class="result-info">
            Location: {result_city}
            &nbsp; • &nbsp;
            Area: {result_area:,.0f} sq ft
            &nbsp; • &nbsp;
            NHB Quarter: {quarter}
        </div>
    </div>
    """)

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "NHB Benchmark",
        f"₹{nhb_price:,.0f} / sq ft"
    )

    m2.metric(
        "NHB HPI",
        f'{st.session_state["nhb_index"]:.2f}'
    )

    m3.metric(
        "Usable Records",
        f'{st.session_state["nhb_records"]:,}'
    )

    st.info(
        "This is an NHB RESIDEX benchmark-based estimate, "
        "not an exact transaction price or formal valuation."
    )


# =====================================================
# EMI CALCULATOR
# =====================================================

st.divider()
st.header("💳 Smart EMI Calculator")

st.caption(
    "Calculate an approximate home-loan EMI using your property price."
)

x, y = st.columns(2)

with x:
    default_price = int(
        st.session_state.get("estimated_value", 5000000)
    )

    property_price = st.number_input(
        "🏠 Property Price (₹)",
        min_value=100000,
        max_value=1000000000,
        value=max(100000, min(default_price, 1000000000)),
        step=100000
    )

    down_percent = st.slider(
        "💰 Down Payment (%)",
        min_value=0,
        max_value=80,
        value=20
    )

with y:
    interest = st.number_input(
        "📈 Annual Interest Rate (%)",
        min_value=0.0,
        max_value=25.0,
        value=8.5,
        step=0.1
    )

    years = st.slider(
        "📅 Loan Tenure (years)",
        min_value=1,
        max_value=30,
        value=20
    )


# =====================================================
# EMI CALCULATION
# =====================================================

down_payment = property_price * down_percent / 100
loan = property_price - down_payment
months = years * 12
monthly_rate = interest / 1200

if monthly_rate == 0:
    emi = loan / months
else:
    emi = (
        loan
        * monthly_rate
        * (1 + monthly_rate) ** months
        / ((1 + monthly_rate) ** months - 1)
    )

total_payment = emi * months
total_interest = total_payment - loan

e1, e2, e3, e4 = st.columns(4)

e1.metric("Monthly EMI", f"₹{emi:,.0f}")
e2.metric("Loan Amount", f"₹{loan:,.0f}")
e3.metric("Total Interest", f"₹{total_interest:,.0f}")
e4.metric("Total Payment", f"₹{total_payment:,.0f}")


# =====================================================
# ABOUT
# =====================================================

st.divider()
st.header("ℹ️ About Kunal.AI")

u, v = st.columns(2)

with u:
    st.html("""
    <div class="info">
        <b>Data Source</b><br>
        National Housing Bank (NHB) RESIDEX<br><br>

        <b>Calculation</b><br>
        NHB benchmark price per sq ft × property area
    </div>
    """)

with v:
    st.html("""
    <div class="info">
        <b>Project Features</b><br><br>
        • Supported city selection<br>
        • NHB benchmark lookup<br>
        • Property value estimation<br>
        • Home-loan EMI calculator<br>
        • Built and designed by Kunal
    </div>
    """)


# =====================================================
# FOOTER
# =====================================================

st.html("""
<div class="footer">
    Kunal.AI • NHB House Price Intelligence
</div>
""")

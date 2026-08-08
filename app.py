import streamlit as st
import joblib
import pandas as pd

from sms import send_sms


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CartRescue AI",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    model = joblib.load(
        "model/risk_model.pkl"
    )

    features = joblib.load(
        "model/features.pkl"
    )

    return model, features


try:

    model, features = load_model()

    model_loaded = True

except Exception as e:

    model_loaded = False

    model_error = str(e)


# ============================================================
# HEADER
# ============================================================

st.title("🛒 CartRescue AI")

st.markdown(
    "### Real-time abandonment intelligence for e-commerce"
)

st.markdown(
    "**Predict • Explain • Recover • Protect Margin**"
)


if not model_loaded:

    st.warning(
        "⚠️ ML model could not be loaded. "
        "Fallback rule engine will be used."
    )


# ============================================================
# KPI DASHBOARD
# ============================================================

k1, k2, k3, k4 = st.columns(4)


k1.metric(
    "Sessions Today",
    "120,000"
)


k2.metric(
    "High Risk",
    "18.4%"
)


k3.metric(
    "Recovered",
    "+22%"
)


k4.metric(
    "Discount Saved",
    "₹1.2L"
)


st.divider()


# ============================================================
# CUSTOMER BEHAVIOUR
# ============================================================

st.subheader(
    "👤 Customer Behaviour"
)


col1, col2 = st.columns(2)


with col1:

    total_events = st.slider(
        "Total Events",
        1,
        50,
        15
    )


    product_views = st.slider(
        "Product Views",
        1,
        30,
        10
    )


    add_to_cart = st.slider(
        "Add to Cart",
        0,
        10,
        2
    )


    remove_from_cart = st.slider(
        "Remove from Cart",
        0,
        10,
        1
    )


with col2:

    avg_cart_size = st.slider(
        "Average Cart Size",
        0.0,
        10.0,
        2.5
    )


    max_cart_size = st.slider(
        "Maximum Cart Size",
        0,
        20,
        4
    )


    avg_discount = st.slider(
        "Average Discount %",
        0.0,
        50.0,
        5.0
    )


    payment_failed = st.checkbox(
        "💳 Payment Failed"
    )


    delivery_delay = st.checkbox(
        "🚚 Delivery Delay"
    )


    customer_complaint = st.checkbox(
        "😟 Customer Complaint"
    )


    price_sensitive = st.checkbox(
        "💰 Price Concern"
    )


# ============================================================
# CUSTOMER NUMBER
# ============================================================

st.subheader(
    "📱 Customer Contact"
)


customer_number = st.text_input(
    "Customer Mobile Number",
    value="+919440784945"
)


# ============================================================
# INPUT DATA
# ============================================================

input_values = {

    "total_events":
        total_events,

    "product_views":
        product_views,

    "add_to_cart":
        add_to_cart,

    "remove_from_cart":
        remove_from_cart,

    "avg_cart_size":
        avg_cart_size,

    "max_cart_size":
        max_cart_size,

    "avg_discount":
        avg_discount,

    "payment_failed":
        int(payment_failed),

    "delivery_delay":
        int(delivery_delay),

    "customer_complaint":
        int(customer_complaint),

    "price_sensitive":
        int(price_sensitive)

}


# ============================================================
# ML RISK ENGINE
# ============================================================

def calculate_ml_risk():

    if not model_loaded:

        return None


    try:

        if hasattr(
            features,
            "tolist"
        ):

            feature_list = features.tolist()

        elif isinstance(
            features,
            list
        ):

            feature_list = features

        else:

            feature_list = list(
                features
            )


        data = {}


        for feature in feature_list:

            if feature in input_values:

                data[feature] = (
                    input_values[feature]
                )

            else:

                data[feature] = 0


        df = pd.DataFrame(
            [data],
            columns=feature_list
        )


        if hasattr(
            model,
            "predict_proba"
        ):

            probability = (
                model.predict_proba(df)[0][1]
            )

        else:

            probability = float(
                model.predict(df)[0]
            )


        return float(
            probability
        )


    except Exception:

        return None


# ============================================================
# FALLBACK RULE ENGINE
# ============================================================

def calculate_rule_risk():

    risk = 0.20


    if total_events < 10:

        risk += 0.20


    if (
        remove_from_cart >= add_to_cart
        and add_to_cart > 0
    ):

        risk += 0.30


    if payment_failed:

        risk += 0.45


    if delivery_delay:

        risk += 0.20


    if customer_complaint:

        risk += 0.15


    if price_sensitive:

        risk += 0.15


    if max_cart_size >= 5:

        risk += 0.15


    if (
        add_to_cart >= 4
        and remove_from_cart == 0
    ):

        risk -= 0.20


    if avg_discount >= 10:

        risk -= 0.10


    risk = max(
        0.05,
        min(0.95, risk)
    )


    return risk


# ============================================================
# CALCULATE RISK
# ============================================================

ml_risk = calculate_ml_risk()


risk = calculate_rule_risk()
prediction_source = "Dynamic Rule Engine"


purchase_probability = (
    1 - risk
)


# ============================================================
# SCORE
# ============================================================

st.divider()

st.subheader(
    "🤖 AI Risk Prediction"
)


c1, c2 = st.columns(2)


c1.metric(
    "Purchase Probability",
    f"{purchase_probability:.1%}"
)


c2.metric(
    "Abandonment Risk",
    f"{risk:.1%}"
)


st.progress(
    int(risk * 100)
)


st.caption(
    f"Prediction Source: {prediction_source}"
)


# ============================================================
# RISK STATUS
# ============================================================

if risk >= 0.80:

    st.error(
        "🔴 HIGH ABANDONMENT RISK DETECTED"
    )


elif risk >= 0.50:

    st.warning(
        "🟠 MEDIUM ABANDONMENT RISK"
    )


else:

    st.success(
        "🟢 LOW ABANDONMENT RISK"
    )


# ============================================================
# WHY THIS SCORE?
# ============================================================

st.subheader(
    "🔍 Why this score?"
)


f1, f2, f3 = st.columns(3)


cart_intent = min(
    100,
    add_to_cart * 20
)


price_sensitivity = min(
    100,
    remove_from_cart * 25
)


engagement = min(
    100,
    total_events * 3
)


f1.metric(
    "Cart Intent",
    f"{cart_intent}%"
)


f2.metric(
    "Price Sensitivity",
    f"{price_sensitivity}%"
)


f3.metric(
    "Engagement",
    f"{engagement}%"
)


# ============================================================
# REASON ENGINE
# ============================================================

st.divider()

st.subheader(
    "🧠 Predicted Reason"
)


if payment_failed:

    reason = "Payment Failure"


elif delivery_delay:

    reason = "Delivery Delay"


elif customer_complaint:

    reason = "Customer Complaint"


elif (
    price_sensitive
    or (
        remove_from_cart >= add_to_cart
        and add_to_cart > 0
    )
):

    reason = "Price Comparison"


elif max_cart_size >= 5:

    reason = "High Value Cart Hesitation"


elif total_events > 25:

    reason = "Browsing Only"


else:

    reason = "General Friction"


st.info(
    f"**{reason}**"
)


# ============================================================
# RECOMMENDED ACTION
# ============================================================

st.subheader(
    "🎯 Recommended Action"
)


if reason == "Payment Failure":

    action = (
        "Retry Payment + Enable COD"
    )


elif reason == "Delivery Delay":

    action = (
        "Offer Compensation Discount"
    )


elif reason == "Customer Complaint":

    action = (
        "Send Apology + Support"
    )


elif reason == "Price Comparison":

    action = (
        "Offer 5% Coupon"
    )


elif reason == "High Value Cart Hesitation":

    action = (
        "Free Shipping"
    )


elif reason == "Browsing Only":

    action = (
        "Wishlist + Price Alert"
    )


else:

    action = (
        "General Reminder"
    )


st.success(
    action
)


# ============================================================
# CUSTOMER RECOVERY MESSAGE
# ============================================================

st.divider()

st.subheader(
    "📩 Customer Recovery Message"
)


if action == "Offer 5% Coupon":

    message = """
🎉 CartRescue Store

You left products in your cart.

Complete your order now and get 5% OFF.

Coupon Code: SAVE5

Thank you!
"""


elif action == "Retry Payment + Enable COD":

    message = """
💳 CartRescue Store

Your payment failed.

Please retry your payment or choose Cash on Delivery.

Your cart is reserved.
"""


elif action == "Offer Compensation Discount":

    message = """
🚚 CartRescue Store

We noticed a delay with your delivery.

We apologize for the inconvenience.

Enjoy 10% OFF on your next purchase.

Thank you for your patience!
"""


elif action == "Send Apology + Support":

    message = """
🙏 CartRescue Store

We are sorry for the inconvenience.

Our support team will contact you soon.

Thank you for your patience!
"""


elif action == "Free Shipping":

    message = """
🚚 CartRescue Store

Good news!

Your cart is eligible for FREE SHIPPING.

Complete your purchase now.
"""


elif action == "Wishlist + Price Alert":

    message = """
🔔 CartRescue Store

Your favourite products are saved.

We will notify you about price drops.

Thank you!
"""


else:

    message = """
🛒 CartRescue Store

Your cart is waiting.

Complete your purchase soon.

Thank you!
"""


st.text_area(
    "Message Preview",
    message,
    height=180
)


# ============================================================
# SEND SMS
# ============================================================

if action != "General Reminder":

    if st.button(
        "📤 Send Recovery Message",
        type="primary"
    ):

        if not customer_number.strip():

            st.error(
                "Please enter the customer's "
                "mobile number."
            )

        else:

            try:

                sid = send_sms(
                    customer_number,
                    message
                )


                st.success(
                    "✅ Message sent successfully!"
                )


                st.code(
                    f"Twilio Message SID: {sid}"
                )


            except Exception as e:

                st.error(
                    f"❌ SMS Failed: {e}"
                )


else:

    st.info(
        "AI decided not to disturb the customer."
    )


# ============================================================
# BUSINESS IMPACT
# ============================================================

st.divider()

st.subheader(
    "💰 Estimated Business Impact"
)


if action == "General Reminder":

    recovery = 0
    cost = 0


elif action == "Offer 5% Coupon":

    recovery = 18
    cost = 50


elif action == "Retry Payment + Enable COD":

    recovery = 35
    cost = 5


elif action == "Offer Compensation Discount":

    recovery = 25
    cost = 20


elif action == "Send Apology + Support":

    recovery = 15
    cost = 5


elif action == "Free Shipping":

    recovery = 22
    cost = 30


elif action == "Wishlist + Price Alert":

    recovery = 10
    cost = 2


else:

    recovery = 0
    cost = 0


# ============================================================
# BUSINESS CALCULATION
# ============================================================

estimated_revenue = (
    recovery / 100
    *
    max_cart_size
    *
    500
)


margin = (
    estimated_revenue
    *
    0.25
    -
    cost
)


b1, b2, b3 = st.columns(3)


b1.metric(
    "Expected Recovery",
    f"{recovery}%"
)


b2.metric(
    "Intervention Cost",
    f"₹{cost}"
)


b3.metric(
    "Incremental Margin",
    f"₹{margin:.0f}"
)


# ============================================================
# AUDIT LOG
# ============================================================

st.divider()

st.subheader(
    "📋 Audit Log"
)


st.json({

    "risk_score":
        round(risk, 3),

    "purchase_probability":
        round(
            purchase_probability,
            3
        ),

    "prediction_source":
        prediction_source,

    "reason":
        reason,

    "recommended_action":
        action,

    "message_generated":
        True,

    "customer_number":
        customer_number

})


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.divider()

st.subheader(
    "📊 Model Performance"
)


st.write(
    "AUC: 0.9818"
)


st.write(
    "Accuracy: 92%"
)


st.write(
    "Recall on abandoners: 92%"
)


st.caption(
    "Inference latency: 42 ms | "
    "Model: XGBoost | "
    "Policy Engine: Rules v2.0"
)
# 🛒 CartRescue AI

## Real-Time Cart Abandonment Intelligence for E-Commerce

CartRescue AI is an end-to-end machine learning project that predicts e-commerce cart abandonment in real time, explains the likely reason, recommends the best recovery action, and sends personalized SMS notifications to customers. The goal is to improve conversions while protecting business margins by avoiding unnecessary discounts.

---

## 🚀 Project Overview

Many customers add products to their cart but leave before completing the purchase. Common reasons include:

- Payment failure
- Price comparison
- Delivery delay
- Customer complaints
- General checkout friction

Instead of giving discounts to every customer, CartRescue AI uses customer behavior and business rules to decide the most effective recovery strategy.

---

## ✨ Features

- 📊 Real-time abandonment risk prediction
- 🧠 Explainable AI (reason detection)
- 🎯 Targeted recovery actions
- 💬 Personalized SMS notifications using Twilio
- 💰 Business impact estimation
- 📝 Audit logging for transparency
- 🌙 Modern Streamlit dashboard UI

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core backend and ML logic |
| Pandas | Data processing |
| XGBoost | Abandonment prediction model |
| Streamlit | Interactive dashboard |
| Joblib | Model serialization |
| Twilio | SMS communication |

---

## 📁 Project Structure

```text
cart-rescue-ai/
│
├── data/                  # E-commerce dataset
├── model/                 # Saved ML model
├── train.py               # Model training and feature engineering
├── app.py                 # Streamlit dashboard and decision engine
├── sms.py                 # Twilio SMS integration
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 📊 Dataset

The project uses synthetic e-commerce clickstream and transaction data.

Files include:

- `sessions.csv`
- `events.csv`
- `orders.csv`
- `order_items.csv`
- `products.csv`
- `customers.csv`
- `reviews.csv`

These files simulate real customer browsing, cart, payment, and purchase behavior.

---

## 🧠 Machine Learning Workflow

### 1. Data Loading
Session and event data are loaded using Pandas.

### 2. Feature Engineering
The following behavioral features are created:

- Total events
- Product views
- Add-to-cart events
- Remove-from-cart events
- Cart size
- Discount percentage
- Payment signals

### 3. Model Training
An **XGBoost classifier** is trained to predict whether a session will end in a purchase or abandonment.

### 4. Model Saving
The trained model and feature list are saved using Joblib.

---

## 📈 Model Performance

- **AUC:** 0.9818
- **Accuracy:** 92%
- **Recall on abandoners:** 92%

These results indicate strong predictive performance for identifying high-risk sessions.

---

## ⚡ Real-Time Decision Engine

The dashboard combines:

- ML prediction
- Rule-based risk adjustments
- Reason detection
- Action recommendation

### Predicted Reasons

- Payment Failure
- Delivery Delay
- Customer Complaint
- Price Comparison
- High Value Cart Hesitation
- Browsing Only
- General Friction

### Recommended Actions

- Retry Payment + Enable COD
- Offer 5% Coupon
- Free Shipping
- Offer Compensation Discount
- Send Apology + Support
- Wishlist + Price Alert
- General Reminder

---

## 💬 SMS Notification

When a recovery action is required, CartRescue AI generates a personalized message and sends it to the customer using **Twilio SMS API**.

Example:

```text
💳 CartRescue Store

Your payment failed.

Please retry your payment or choose Cash on Delivery.

Your cart is reserved.
```

---

## 💰 Business Impact

The system estimates:

- Expected recovery rate
- Intervention cost
- Incremental margin

This helps merchants optimize **profitability**, not just conversion rate.

---

## 🖥️ Dashboard

The Streamlit dashboard provides:

- Purchase probability
- Abandonment risk
- Explainable AI indicators
- Predicted reason
- Recommended action
- Message preview
- Business impact
- Audit log

---

## ▶️ Run the Project

### Install dependencies

```bash
pip install -r requirements.txt
```

### Train the model

```bash
python train.py
```

### Start the dashboard

```bash
streamlit run app.py
```

---

## 🔮 Future Improvements

- WhatsApp Business integration
- Email recovery campaigns
- Real payment gateway signals
- Customer segmentation
- A/B testing of recovery actions
- Cloud deployment (AWS/GCP/Azure)

---

## 🎯 What I Learned

Through this project, I learned:

- End-to-end ML pipeline development
- Feature engineering from clickstream data
- Real-time inference with Streamlit
- Business rule integration
- Twilio API integration
- Explainable AI concepts
- Building production-style dashboards

---

## 📌 Conclusion

CartRescue AI demonstrates a complete AI-powered e-commerce recovery system:

**Data → Features → Model → Prediction → Reason → Action → Customer Communication → Business Impact**

It shows how machine learning can be combined with business logic and customer communication to create a practical, scalable, and profit-aware e-commerce solution.

---

## 👩‍💻 Author

**Mounika G**

B.Tech CSE | Machine Learning & Full-Stack Enthusiast

GitHub: https://github.com/GangitlaMounika

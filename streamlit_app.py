import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attrition Predictor", layout="centered")
st.markdown("""
    <style>
        body { background-color: #ffdce0; }
        .main { background-color: #ffdce0; font-family: 'Poppins', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Employee Attrition Predictor")
st.markdown("#### Enter employee details to estimate performance & attrition risk.")

# Input fields
age = st.number_input("📅 Age", min_value=18, max_value=65)
distance = st.number_input("🏠 Distance From Home", min_value=0)
education = st.selectbox("🎓 Education", [1, 2, 3, 4, 5], format_func=lambda x: f"{x} - {'Below College' if x==1 else 'College' if x==2 else 'Bachelor' if x==3 else 'Master' if x==4 else 'Doctor'}")
job_satisfaction = st.selectbox("😊 Job Satisfaction", [1, 2, 3, 4], format_func=lambda x: f"{x} - {'Low' if x==1 else 'Medium' if x==2 else 'High' if x==3 else 'Very High'}")
income = st.number_input("💰 Monthly Income", min_value=1000)
years = st.number_input("🏢 Years At Company", min_value=0)
tasks_last_month = st.number_input("✅ Tasks Completed Last Month", min_value=0)

# Predict
if st.button("🔍 PREDICT"):
    with st.spinner("Predicting..."):
        try:
            res = requests.post("http://127.0.0.1:8000/predict", json={
                "Age": age,
                "DistanceFromHome": distance,
                "Education": education,
                "JobSatisfaction": job_satisfaction,
                "MonthlyIncome": income,
                "YearsAtCompany": years,
                "TasksCompletedLastMonth": tasks_last_month
            })

            if res.status_code == 200:
                result = res.json()
                st.success("✅ Prediction Complete")
                st.markdown(f"### 📊 Predicted Tasks Next Month: `{result['Predicted Tasks Next Month']}`")
                st.markdown(f"### 🔍 Attrition Prediction: `{result['Attrition Prediction']}`")

                # Chart
                fig, ax = plt.subplots()
                ax.bar(["Last Month", "Predicted"], [tasks_last_month, result['Predicted Tasks Next Month']], color=["#ffb6c1", "#8a2be2"])
                ax.set_title("📈 Task Performance", fontsize=14)
                ax.set_ylabel("Tasks Completed")
                st.pyplot(fig)
            else:
                st.error(f"❌ Server Error: {res.text}")
        except Exception as e:
            st.error(f"🚨 Error: {e}")

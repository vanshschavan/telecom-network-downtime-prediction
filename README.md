# 📡 5G/4G Cell Site Downtime & Fault Prediction Suite

An end-to-end Machine Learning and Business Intelligence solution designed to predict telecommunication RAN cell tower outages, monitor network KPIs, and prioritize field engineer maintenance workflows before critical failures occur.

---

## 🛠️ Tech Stack & Tools

* **Programming Language:** Python 3.10+
* **Data Processing & ML:** Pandas, NumPy, Scikit-Learn
* **Containerization:** Docker
* **CI/CD Automation:** GitHub Actions
* **Visualization & Analytics:** Power BI Desktop (DAX, Conditional Formatting, Interactive Visuals)

---

## 🏗️ Project Architecture & Workflow

1. **Synthetic Telemetry Generation (`generate_data.py`):**
   * Generates realistic 5G/4G RAN telemetry metrics including hardware temperature ($^\circ\text{C}$), signal-to-noise ratio (SNR), packet loss rate, power fluctuation index, and ambient temperature across multi-region site IDs.
2. **Predictive Modeling & Scoring (`train_model.py`):**
   * Trains a Machine Learning Classifier to detect failure risk.
   * Assigns continuous risk scores and categorizes towers into dynamic operational tiers (`High Risk`, `Warning`, `Stable`).
   * Exports processed risk evaluations into an Excel dataset for downstream analytics.
3. **Automated MLOps Pipeline (`.github/workflows/telecom_pipeline.yml`):**
   * GitHub Actions workflow that automatically executes data generation and model retraining upon code commits.
4. **Interactive Executive Dashboard (`Power BI`):**
   * Features high-level network health KPIs, failure risk distribution donut charts, and a real-time maintenance triage heatmap for network field operations.

---

## 🚀 Quickstart: Running Locally

### 1. Environment Setup
```bash
# Clone the repository
git clone [https://github.com/vanshschavan/telecom-network-downtime-prediction.git](https://github.com/vanshschavan/telecom-network-downtime-prediction.git)
cd telecom-network-downtime-prediction

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows
# source venv/bin/activate    # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
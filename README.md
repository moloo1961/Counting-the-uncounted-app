# Counting the Uncounted: GBV Kenya Analysis

An interactive Streamlit web application that visualizes and analyzes data related to Gender-Based Violence (GBV) in Kenya. This project aims to bring visibility to patterns, reporting rates, and physical data trends across different counties.

🚀 *[View Live Web Application](https://counting-the-uncounted.streamlit.app/)*

## 📊 Project Overview
Data regarding GBV is often siloed or underreported. "Counting the Uncounted" processes complex socioeconomic metrics to calculate visibility and reporting scores across Kenyan counties. This allows researchers, policy makers, and citizens to uncover data gaps and trends easily.

## ✨ Key Features
- *Interactive Map & Visualizations:* Dynamic rendering of GBV indicators using Matplotlib.
- *County-by-County Analysis:* Sift through localized reporting statistics (e.g., KDHS physical violence scores and police reporting statistics).
- *Data Integrity:* Fast-loading data cached securely to optimize performance.

## 📁 Repository Structure
bash
Counting-the-Uncounted/
├── Outputs/
│   └── visibility_scores.json    # Processed JSON dataset
├── requirements.txt              # Application dependencies
├── streamlit_app.py              # Main Streamlit application entrypoint
└── README.md                     # Documentation


## 🛠️ Installation & Local Setup

If you want to run this application locally on your machine, follow these steps:

1. *Clone the repository:*
   bash
   git clone https://github.com
   cd Counting-the-uncounted-app
   

2. *Install requirements:*
   bash
   pip install -r requirements.txt
   

3. *Run the Streamlit server:*
   bash
   streamlit run streamlit_app.py
   

## 🧰 Tech Stack
- *Language:* Python 3.11
- *Framework:* Streamlit
- *Data Visualization:* Matplotlib
- *Data Format:* JSON

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
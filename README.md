# FinMentor – Financial Health and Risk Assessment System
FinMentor is a data-driven web application developed to analyze personal financial data and provide insights into financial health, risk levels, and decision-making. The system applies machine learning techniques to move beyond traditional rule-based financial tools and enable more reliable and data-driven analysis.

## Overview
The application processes user inputs such as income, expenses, savings, and EMI obligations. These inputs are subjected to data preprocessing steps including data cleaning, feature engineering, encoding, and standardization to ensure consistency and accuracy.
FinMentor employs a hybrid ensemble machine learning approach by integrating Support Vector Machine (SVM), Conditional Random Field (CRF), and Hidden Markov Model (HMM). The predictions from these models are combined using a voting-based mechanism to improve robustness and overall prediction reliability.

## Key Features
- Financial health score generation and persona classification (Stable, Moderate, Stressed)  
- EMI-based risk assessment and loan affordability analysis  
- Scenario-based “What-If” simulation for financial decision-making  
- Ensemble-based prediction to enhance model reliability  
- Interactive dashboard for structured visualization of financial insights  

## Machine Learning Approach
Models Used:
- Support Vector Machine (SVM)  
- Conditional Random Field (CRF)  
- Hidden Markov Model (HMM)  

Ensemble Strategy:
- Voting-based approach with priority-based decision handling  
- Improves prediction consistency and reduces individual model limitations  

Evaluation Metrics:
- Accuracy  
- Precision  
- Recall  
- F1-Score  

## Tech Stack
- Python  
- Django  
- SQLite  
- Scikit-learn  
- hmmlearn  
- sklearn-crfsuite  
- Pandas  
- NumPy  

## Project Structure
FinMentor/
│── fintechsnap/          # Main Django application  
│── data/                 # Dataset (sample data)  
│── ml_models/            # Trained models  
│── requirements.txt  
│── README.md  

## Setup Instructions
1. Clone the repository:
git clone https://github.com/riya-24jagtap/FinMentor.git
cd FinMentor
2. Install dependencies:
pip install -r requirements.txt
3. Run the application:
python manage.py runserver

4. Open the application in your browser:
Live Demo: https://finmentor-gnx0.onrender.com/

## Dataset
The dataset includes financial attributes such as income, expenses, savings, and EMI obligations, along with derived indicators such as savings rate and EMI ratio. A sample dataset is provided for demonstration purposes.

## Results
The Support Vector Machine (SVM) achieved the highest individual model performance. The ensemble approach further improved overall robustness and consistency of predictions across financial persona categories.

## Future Scope
- Integration with real-time financial data sources  
- Incorporation of explainable AI techniques for interpretability  
- Deployment on scalable cloud infrastructure  
- Expansion of dataset for improved generalization  

## Author
Riya Jagtap  
Final Year Computer Science Student

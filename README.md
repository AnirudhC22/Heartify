
# Heartify: Heart Disease Prediction with Explainable AI

Heartify is an advanced heart disease prediction web application built with Flask. It integrates Explainable AI (XAI) using SHAP (SHapley Additive exPlanations) to provide transparent, interpretable insights into model predictions. The application helps users understand their heart health by offering accurate predictions along with detailed explanations of the contributing factors.

## 🚀 Features
- **Heart Disease Prediction**: Predicts the likelihood of heart disease based on user input.
- **Explainable AI (XAI)**: Utilizes SHAP to explain model predictions.
- **Dynamic SHAP Charts**: Includes summary plots, dependence plots, bar plots, waterfall plots, and force plots.
- **Navigation for SHAP Charts**: Easy navigation between SHAP explanation charts with "Next" and "Previous" buttons.
- **PDF Report Generation**: Generates a comprehensive PDF report containing:
  - Prediction results  
  - SHAP charts  
  - AI explanations  
  - Heart health tips
- **Dark Theme UI**: Modern, user-friendly interface designed with Tailwind CSS.

## ⚙️ Installation Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/Heartify.git
   cd Heartify
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   flask run
   ```

5. **Access the App:**
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## 🌱 Scope for Further Development
- **Mobile App Integration:** Develop a mobile version for Android and iOS.
- **Advanced Predictive Models:** Incorporate deep learning models for enhanced accuracy.
- **Real-Time Health Monitoring:** Integrate with wearable devices for real-time data.
- **Multilingual Support:** Add language options to reach a wider audience.
- **User Authentication:** Implement secure login and data storage for personalized reports.
- **Health Recommendations:** Provide AI-driven personalized health and lifestyle recommendations.
- **API Development:** Create RESTful APIs for integration with other healthcare platforms.

---

💡 **Contributions are welcome!**  
Feel free to fork the repository and submit pull requests.

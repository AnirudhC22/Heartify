import tensorflow as tf
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import joblib

# Load the saved model and data
loaded_model = tf.keras.models.load_model('my_model.keras')
x_train, x_test = joblib.load('notebook_data.pkl')

# Initialize SHAP Explainer
background = x_train.sample(100, random_state=42).values
explainer = shap.DeepExplainer(loaded_model, background)
shap_values = explainer.shap_values(x_test.values)
feature_names = x_test.columns.tolist()

app = Flask(__name__)

# Function to save SHAP plots
def save_shap_plot(plot_func, *args, **kwargs):
    plt.figure()
    plot_func(*args, **kwargs)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

# Generate SHAP plots
base_value = explainer.expected_value[1]
if hasattr(base_value, 'numpy'):
    base_value = base_value.numpy()

shap_charts = [
    save_shap_plot(shap.summary_plot, shap_values[:, :, 0], x_test, feature_names=feature_names, show=False),
    save_shap_plot(shap.summary_plot, shap_values[:, :, 1], x_test, feature_names=feature_names, show=False),
    save_shap_plot(shap.dependence_plot, 'Cholesterol', shap_values[:, :, 1], x_test, feature_names=feature_names, show=False),
    save_shap_plot(shap.summary_plot, shap_values[:, :, 1], x_test, plot_type="bar", feature_names=feature_names, show=False),
    save_shap_plot(
        shap.waterfall_plot,
        shap.Explanation(
            values=shap_values[0, :, 1],
            base_values=base_value,
            data=x_test.iloc[0],
            feature_names=feature_names
        ),
        show=False
    ),
    save_shap_plot(
        shap.force_plot,
        base_value,
        shap_values[0, :, 1],
        x_test.iloc[0],
        feature_names=feature_names,
        show=False
    )
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            features = [
                int(request.form.get('age')),
                int(request.form.get('sex')),
                int(request.form.get('cp')),
                int(request.form.get('trestbps')),
                int(request.form.get('chol')),
                int(request.form.get('fbs')),
                int(request.form.get('restecg')),
                int(request.form.get('thalach')),
                int(request.form.get('exang')),
                float(request.form.get('oldpeak')),
                int(request.form.get('slope')),
                int(request.form.get('ca')),
                int(request.form.get('thal')),
                int(request.form.get('Sex_M')),
                int(request.form.get('Sex_F')),
                int(request.form.get('ChestPainType_TA')),
                int(request.form.get('ChestPainType_ATA')),
                int(request.form.get('ChestPainType_NAP')),
                int(request.form.get('ChestPainType_ASY')),
                int(request.form.get('ExerciseAngina_Y'))
            ]

            input_data = np.array([features], dtype=np.float32)
            prediction = loaded_model.predict(input_data)[0][0]
            result = "heart disease" if prediction >= 0.5 else "no heart disease"

            return render_template('result.html', result=result)
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('form.html')

@app.route('/xai_intro')
def xai_intro():
    return render_template('xai_intro.html')

@app.route('/xai')
def xai():
    chart_id = int(request.args.get('chart_id', 0))
    chart = shap_charts[chart_id]
    ai_explanation = f"This SHAP chart {chart_id + 1} explains the model's decision-making process."

    return render_template(
        'xai.html',
        chart=chart,
        ai_explanation=ai_explanation,
        prev_chart=max(0, chart_id - 1),
        next_chart=min(len(shap_charts) - 1, chart_id + 1),
        chart_id=chart_id
    )

if __name__ == '__main__':
    app.run(debug=True)

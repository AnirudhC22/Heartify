import tensorflow as tf
from flask import Flask, request, render_template, send_file
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import joblib
import os
from dotenv import load_dotenv
from google import genai
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Load environment variables
load_dotenv()

# Load OpenAI API key
api_key = os.getenv("heartify")

# Load the saved model and data
loaded_model = tf.keras.models.load_model('my_model.keras')
x_train, x_test = joblib.load('notebook_data.pkl')

# Initialize SHAP Explainer
background = x_train.sample(100, random_state=42).values
explainer = shap.DeepExplainer(loaded_model, background)
shap_values = explainer.shap_values(x_test.values)
feature_names = x_test.columns.tolist()

# Initialize Flask app
app = Flask(__name__)

# Function to save SHAP plots
def save_shap_plot(plot_func, *args, **kwargs):
    buf = BytesIO()
    plt.figure()
    plot_func(*args, **kwargs)
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded}"

# Function to generate AI explanations
def generate_ai_explanation(chart_type):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"Explain the insights provided by a {chart_type} in heart disease prediction."],
        config=genai.types.GenerateContentConfig(
            max_output_tokens=400,
            temperature=0.1
        )
    )
    return response.text

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
]

# Generate SHAP force plot as HTML
force_plot_html = shap.force_plot(
    base_value,
    shap_values[0, :, 1],
    x_test.iloc[0],
    feature_names=feature_names,
    matplotlib=False
)
force_plot_html_str = f"<head>{shap.getjs()}</head><body>{force_plot_html.html()}</body>"
shap_charts.append(force_plot_html_str)

# Chart types
chart_types = ["summary plot", "summary plot", "dependence plot", "bar plot", "waterfall plot", "force plot"]

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
            prediction = loaded_model.predict(input_data)[0][1]
            result = "heart disease" if prediction >= 0.5 else "no heart disease"

            return render_template('result.html', result=result, features=features)
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
    ai_explanation = generate_ai_explanation(chart_types[chart_id])

    return render_template(
        'xai.html',
        chart=chart,
        ai_explanation=ai_explanation,
        prev_chart=max(0, chart_id - 1),
        next_chart=min(len(shap_charts) - 1, chart_id + 1),
        chart_id=chart_id,
        max_chart=len(shap_charts) - 1
    )


from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64


@app.route('/generate_report')
def generate_report():
    try:
        health_tips = [
            "Maintain a healthy, balanced diet rich in fruits and vegetables.",
            "Exercise regularly, aiming for at least 30 minutes a day.",
            "Avoid smoking and limit alcohol consumption.",
            "Keep your cholesterol and blood pressure under control.",
            "Maintain a healthy weight.",
            "Manage stress through relaxation techniques and hobbies.",
            "Get enough quality sleep every night.",
            "Stay hydrated by drinking plenty of water.",
            "Limit your intake of processed and high-sugar foods.",
            "Have regular health check-ups to monitor heart health."
        ]

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 50  # Add margin for better layout
        text_width = width * 0.75  # Limit text to 75% of the page width

        for idx, (chart, explanation) in enumerate(zip(shap_charts, chart_types)):
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(margin, height - margin, f"Chart {idx + 1}: {explanation.capitalize()}")

            # Add image below heading
            image_height = 200  # Fixed image height
            if isinstance(chart, str) and chart.startswith("data:image/png;base64,"):
                img_data = base64.b64decode(chart.split(",")[1])
                img_buffer = BytesIO(img_data)
                image = ImageReader(img_buffer)
                pdf.drawImage(image, margin, height - margin - image_height - 20, width=width - 2*margin, height=image_height, preserveAspectRatio=True)

            # Add explanation below the image
            ai_explanation = generate_ai_explanation(explanation)
            pdf.setFont("Helvetica", 12)
            text_obj = pdf.beginText(margin, height - margin - image_height - 50)
            text_obj.setLeading(15)

            for line in ai_explanation.split('. '):
                # Wrap text to fit within 75% of the page width
                wrapped_lines = [line[i:i+80] for i in range(0, len(line), 80)]
                for wrapped_line in wrapped_lines:
                    text_obj.textLine(wrapped_line.strip())

            pdf.drawText(text_obj)
            pdf.showPage()  # Move to the next page

        # 10 Steps for Better Heart Health
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(margin, height - margin, "10 Steps for Better Heart Health")
        pdf.setFont("Helvetica", 12)
        text_obj = pdf.beginText(margin, height - margin - 30)
        text_obj.setLeading(15)
        for i, tip in enumerate(health_tips, start=1):
            # Wrap tips within 75% of the page width
            wrapped_tips = [tip[j:j+80] for j in range(0, len(tip), 80)]
            for wrapped_tip in wrapped_tips:
                text_obj.textLine(f"{i}. {wrapped_tip}" if wrapped_tip == wrapped_tips[0] else wrapped_tip)
        pdf.drawText(text_obj)

        pdf.save()
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, download_name="heartify_report.pdf", mimetype='application/pdf')

    except Exception as e:
        return f"An error occurred while generating the report: {e}"


@app.route('/report_done')
def report_done():
    return render_template('report_done.html')


if __name__ == '__main__':
    app.run(debug=True)


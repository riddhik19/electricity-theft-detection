from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import pandas as pd
import numpy as np
import joblib
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'theft_detection_secret_key_2024'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Model and data paths
MODEL_PATH = 'theft_model.pkl'

# Load model at startup
model = None
model_features = ['mean', 'std', 'max', 'min', 'zero_days', 'cv', 'range']

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully!")
except Exception as e:
    print(f"Warning: Could not load model - {e}")
    print("Please ensure theft_model.pkl exists in the application directory")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_theft(data_dict):
    """Make prediction using the loaded model"""
    if model is None:
        return None, None, "Model not loaded"
    
    try:
        # Create DataFrame with feature values
        features = []
        for feature in model_features:
            if feature in data_dict:
                features.append(float(data_dict[feature]))
            else:
                return None, None, f"Missing required feature: {feature}"
        
        # Make prediction
        X = np.array(features).reshape(1, -1)
        probs = model.predict_proba(X)[0]
        prediction = 1 if probs[1] > 0.25 else 0  # Lower threshold
        probability = probs
        
        return int(prediction), probability, None
    except Exception as e:
        return None, None, str(e)


@app.route('/')
def index():
    return render_template('index.html', features=model_features)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Read the file
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            
            # Store in session (convert to dict for JSON serialization)
            session_data = {
                'filename': filename,
                'columns': df.columns.tolist(),
                'row_count': len(df),
                'data': df.head(100).to_dict('records')  # Limit to 100 rows for display
            }
            
            # Make predictions for all rows
            predictions = []
            for idx, row in df.iterrows():
                row_data = {}
                for col in df.columns:
                    row_data[col] = row[col]
                
                # Check if row has required features
                has_features = all(f in row_data for f in model_features)
                if has_features:
                    probs = model.predict_proba(np.array([row_data[f] for f in model_features]).reshape(1, -1))[0]
                    pred = 1 if probs[1] > 0.25 else 0
                    row_data['prediction'] = 'Suspicious' if pred == 1 else 'Normal'
                    row_data['confidence'] = f"{max(probs) * 100:.1f}%"

                else:
                    row_data['prediction'] = 'Missing Features'
                    row_data['confidence'] = 'N/A'
                
                predictions.append(row_data)
            
            session_data['predictions'] = predictions[:100]  # Store first 100 for display
            session_data['total_rows'] = len(df)
            
            flash(f'File uploaded successfully! {len(df)} rows found.', 'success')
            return render_template('index.html', 
                                  uploaded=True, 
                                  data=session_data,
                                  features=model_features)
                                  
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload CSV or Excel file.', 'error')
        return redirect(url_for('index'))


@app.route('/predict_row', methods=['POST'])
def predict_row():
    data = request.get_json()
    row_index = data.get('row_index')
    row_data = data.get('row_data')
    
    if not row_data:
        return jsonify({'error': 'No data provided'}), 400
    
    prediction, probability, error = predict_theft(row_data)
    
    if error:
        return jsonify({'error': error}), 400
    
    result = {
        'prediction': 'Suspicious' if prediction == 1 else 'Normal',
        'confidence': f"{max(probability) * 100:.1f}%",
        'suspicious_probability': f"{probability[1] * 100:.1f}%",
        'normal_probability': f"{probability[0] * 100:.1f}%"
    }
    
    return jsonify(result)


@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Handle manual data entry predictions"""
    try:
        # Get form data
        form_data = {}
        for feature in model_features:
            value = request.form.get(feature)
            if value is None or value == '':
                flash(f'Please enter value for {feature}', 'error')
                return redirect(url_for('index'))
            try:
                form_data[feature] = float(value)
            except ValueError:
                flash(f'Invalid value for {feature}. Please enter a number.', 'error')
                return redirect(url_for('index'))
        
        # Make prediction
        prediction, probability, error = predict_theft(form_data)
        
        if error:
            flash(f'Prediction error: {error}', 'error')
            return redirect(url_for('index'))
        
        result = {
            'prediction': 'Suspicious' if prediction == 1 else 'Normal',
            'confidence': f"{max(probability) * 100:.1f}%",
            'suspicious_probability': f"{probability[1] * 100:.1f}%",
            'normal_probability': f"{probability[0] * 100:.1f}%"
        }
        
        return render_template('index.html', 
                              manual_result=result, 
                              manual_input=form_data,
                              features=model_features)
                              
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/clear')
def clear_data():
    """Clear uploaded data"""
    # Clean up uploaded files
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        except:
            pass
    
    flash('Data cleared successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("=" * 60)
    print("Electricity Theft Detection Web Application")
    print("=" * 60)
    print(f"Model loaded: {model is not None}")
    print(f"Model features: {model_features}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)


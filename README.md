# Electricity Theft Detection Web Application

A Flask-based web application for detecting electricity theft using machine learning.

## Features

- **Upload Dataset**: Upload CSV or Excel files with energy consumption data
- **Row-wise Prediction**: Select and predict individual rows from uploaded data
- **Manual Data Entry**: Enter feature values manually to check for theft
- **Prediction Confidence**: Display probability scores for each prediction
- **Visual Highlighting**: Suspicious rows are highlighted in the data table

## Requirements

- Python 3.8+
- Flask 3.0+
- pandas 2.2+
- numpy 2.2+
- lightgbm 4.6+
- scikit-learn 1.8+
- joblib 1.5+
- openpyxl 3.1+

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure model file exists**:
   - The application requires `theft_model.pkl` file
   - Run the notebook first to generate this file, or copy your trained model here

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser**:
   Navigate to `http://localhost:5000`

## Model Features

The model expects the following features:

| Feature | Description |
|---------|-------------|
| mean | Average daily energy consumption |
| std | Standard deviation of energy consumption |
| max | Maximum daily energy consumption |
| min | Minimum daily energy consumption |
| zero_days | Number of days with zero consumption |
| cv | Coefficient of variation (std/mean) |
| range | Range of energy consumption (max-min) |

## Usage

### Option 1: Upload Dataset
1. Click on the upload area
2. Select a CSV or Excel file containing energy data
3. The table will display with predictions for each row
4. Suspicious rows are highlighted in red

### Option 2: Manual Entry
1. Scroll to the Manual Data Entry section
2. Enter values for all 7 features
3. Click "Check for Theft" button
4. View the prediction result with confidence scores

## Project Structure

```
Theft_Detection/
├── app.py                  # Flask application
├── templates/
│   └── index.html         # Frontend HTML template
├── theft_model.pkl        # Trained ML model
├── daily_dataset.csv      # Sample data
├── requirements.txt       # Python dependencies
└── README.md            # This file
```

## Sample Data Format

Your CSV/Excel file should have columns matching the model features:
- mean, std, max, min, zero_days, cv, range

Example:
```csv
mean,std,max,min,zero_days,cv,range
15.5,4.2,25.3,3.1,0,0.27,22.2
12.8,3.9,21.5,2.8,1,0.30,18.7
```

## Running on Different Port

To run on a different port:
```bash
python app.py --port 8080
```

## Model Performance

The trained model achieves:
- **Accuracy**: ~99%
- **Precision**: 99% (normal), 100% (theft)
- **Recall**: 100% (normal), 94% (theft)
- **F1-Score**: 99% (normal), 97% (theft)

## License

MIT License


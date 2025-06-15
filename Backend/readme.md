# Loan Approval API

A FastAPI-based web application for loan approval prediction and data analysis.

## Project Structure

├── api/ # API endpoints
├── data/ # Data files
├── model/ # ML models
├── services/ # Business logic
├── static/ # Static files
├── main.py # Main application
└── eda_charts.py # Data visualization

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

2. Install required packages:

```bash
pip install fastapi uvicorn pandas numpy matplotlib seaborn scikit-learn
```

## Running the Application

1. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

2. Access the API:

- API Documentation: http://localhost:8000/docs
- EDA Charts: http://localhost:8000/eda-charts

## API Endpoints

- `/eda-charts`: Get data visualization charts
- Additional endpoints available through the API router

## Features

- Loan approval prediction
- Data visualization
- RESTful API endpoints
- Interactive API documentation

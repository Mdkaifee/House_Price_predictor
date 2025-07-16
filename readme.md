# House Price Predictor

## Overview
Predict house prices using linear regression based on features like area, location, BHK, etc.

## Structure

- **data/**: CSV datasets.
- **src/**: All core source code.
- **tests/**: Test scripts.
- **main.py**: Main entry point.

## Setup

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python tests/test_pipeline.py
python main.py

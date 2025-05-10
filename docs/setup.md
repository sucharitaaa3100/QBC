# Setup Instructions for QBC - Quiz Based Challenge

This document provides step-by-step instructions to set up and run the Flask-based qbc application locally.

## Prerequisites

- Python 3.8+
- `pip` (Python package installer)
- Git

## 1. Clone the Repository

```bash
git clone https://github.com/Shahid6174/QBC.git
cd your-ml-flask-app
```

## 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## 3. Install rest of the dependencies using poetry

```bash
pip install poetry
poetry install --no-root
```
## 4. Update .env variables

```bash
cp .env.example .env
```

Replace environment variables with your own

## Run the Application

```bash
flask run
```
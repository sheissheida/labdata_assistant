# LabData Assistant 🔬📊

A small web app I built for working with laboratory data.

The idea is pretty simple: instead of opening a CSV in Excel, manually cleaning it, calculating a bunch of statistics, making plots, and then doing the same thing again for the next experiment, I wanted to put the whole workflow in one place.

I originally started this as a way to get better at Python and data analysis, but it gradually turned into a proper little data analysis tool.

## What it does

The basic workflow is:

```text
Upload
  ↓
Inspect
  ↓
Clean
  ↓
Analyze
  ↓
Visualize
  ↓
Regression
  ↓
Compare Models
  ↓
Analyze Residuals
  ↓
Export
```

You upload a CSV file and the app tries to give you a useful overview of the dataset before you start doing anything with it.

It can show things like:

* Number of rows and columns
* Column names and data types
* Missing values
* Duplicate rows
* Numerical and categorical columns

Then you can move on to cleaning and analysis.

## Features

### Dataset Inspection

The app automatically inspects the uploaded dataset and generates a summary of its structure.

It checks:

* Dataset dimensions
* Column names
* Data types
* Missing values
* Duplicate rows
* Numerical and categorical data

The raw dataset is kept separate from the working dataset, so cleaning operations don't directly modify the original data.

### Data Cleaning

The cleaning workflow currently includes:

* Duplicate row detection and removal
* Missing value detection
* Missing value handling
* Cleaning history
* Reset to raw data
* Download cleaned data

Every cleaning operation produces a small report with information such as rows before/after the operation and how many values or rows were affected.

### Descriptive Statistics

For numerical columns, the app can calculate:

* Mean
* Median
* Standard deviation
* Minimum
* Maximum
* Confidence intervals

There is also a separate categorical analysis section for things like value counts and categorical distributions.

### Visualization

The app can generate different plots depending on the type of data being analyzed.

Some of the current visualizations include:

* Scatter plots
* Line plots
* Histograms
* Box plots
* Bar charts
* Pie charts
* Correlation heatmaps

There is also a plot builder where the user can select the variables they want to visualize.

### Correlation Analysis

The correlation section generates a correlation matrix and heatmap for numerical variables.

This makes it easier to quickly see which variables have stronger positive or negative relationships before fitting a model.

### Regression

The regression section currently supports:

**Linear Regression**

* Slope
* Intercept
* Equation
* R²
* RMSE
* MAE
* Fitted curve
* Basic interpretation

**Polynomial Regression**

* Degree selection
* Polynomial coefficients
* Generated equation
* R²
* RMSE
* MAE
* Fitted curve

Polynomial regression currently supports degrees up to 3.

### Model Comparison

Different models can be compared using the same dataset and X/Y variables.

Currently the comparison includes:

* Linear Regression
* Polynomial Regression (Degree 2)
* Polynomial Regression (Degree 3)

The results are shown together using:

* R²
* RMSE
* MAE

The goal here isn't to blindly pick a model based on one number, but to make the differences between the models easier to inspect.

### Residual Analysis

Residual analysis is used to look at the errors produced by the regression model.

The app can work with:

* Predicted values
* Residuals
* Residual statistics
* Residual plots

This is useful for checking whether the model is leaving behind obvious patterns that a simple regression might not be capturing.

### Export

The final results can be exported so the analysis doesn't stay inside the web app.

The project is being built toward generating:

* Cleaned datasets
* Excel analysis files
* PDF experiment reports

## Tech Stack

### Python

The main language used for basically everything in the project.

### Data Analysis

* Pandas
* NumPy
* SciPy

### Visualization

* Plotly
* Matplotlib

### Web App

* Reflex

I wanted to keep the frontend in Python instead of building a separate React application for this project.

### Database

* SQLite
* SQLAlchemy

The database is used to keep track of datasets and cleaning operations.

## Project Structure

```text
labdata_assistant/
│
├── core/
│   ├── data_loader.py
│   ├── inspector.py
│   ├── cleaning.py
│   ├── regression.py
│   └── ...
│
├── db/
│   ├── database.py
│   └── crud.py
│
├── assets/
│   └── screenshots/
│
├── uploads/
│
├── state.py
├── labdata_assistant.py
├── requirements.txt
└── README.md
```

I tried to keep the data-processing logic separate from the Reflex UI as much as possible. For example, loading a dataset, inspecting it, cleaning it, and running regression calculations are handled in the `core` layer rather than being written directly inside the UI components.

## Screenshots

### Dataset Inspection

![Dataset Inspection](assets/screenshots/01_upload.png)

### Data Cleaning

![Data Cleaning](assets/screenshots/02_cleaning.png)

### Polynomial Regression

![Polynomial Regression](assets/screenshots/03_regression.png)

### Export

![Export](assets/screenshots/04_export.png)

## Running Locally

Clone the repository:

```bash
git clone https://github.com/sheissheida/labdata-assistant.git
cd labdata-assistant
```

Create a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Initialize Reflex:

```bash
reflex init
```

Run the app:

```bash
reflex run
```

Then open:

```text
http://localhost:3000
```

## Demo Data

There is a sample dataset in the repository that can be used to test the application.

The dataset is based on a simple batch reactor kinetics experiment and contains some intentional issues such as missing values and duplicate rows.

## Why I Built This

I'm a Chemical Engineering student, so a lot of the datasets I work with are experimental data.

I also wanted to get better at Python, Pandas, NumPy, statistics, data visualization, and building actual applications instead of just writing small scripts and solving isolated problems.

So I decided to build something around a workflow I actually understand:

```text
experimental data
      ↓
cleaning
      ↓
statistics
      ↓
plots
      ↓
modeling
      ↓
interpretation
```

This project is still evolving, and I'm using it as a way to learn by actually building the different parts instead of trying to design the whole thing perfectly beforehand.

## Current Status

The main data pipeline is working, including dataset inspection, cleaning, statistics, visualization, correlation analysis, regression, model comparison, and the beginning of report generation.

More features and better analysis tools will probably be added as I keep working on it.

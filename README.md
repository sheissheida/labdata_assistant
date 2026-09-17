# LabData Assistant 🧪📊

Let's be real: raw lab data is usually a mess. Before we can even think about feeding datasets into COMSOL, MATLAB, or Aspen HYSYS for serious simulations, that data needs to be prepped and polished. 

**LabData Assistant** is a streamlined data-cleaning and analysis workflow built specifically for engineering and biomedical datasets. It takes you from a chaotic CSV to a clean, mathematically sound dataset without the headache.

## 🚀 What It Does
- **Data Inspection:** Get a quick overview of your dataset's structure.
- **Scrubbing:** Automatically handle missing values and kick out duplicates.
- **Outlier Treatment:** Smart outlier detection (using IQR) with three standard engineering strategies: *Nullify, Cap, or Drop*.
- **Descriptive Statistics (New!):** Instant math (Mean, Std Dev, Min, Max, Median) generated exclusively on your cleaned numerical columns.

## 🛠️ Tech Stack
- **Python** (The backbone)
- **Pandas & NumPy** (For heavy data crunching)
- **Reflex** (For a clean, reactive UI without touching frontend frameworks)

## 💡 Why I Built This
As someone deep into chemical engineering and computational work, I got tired of manually cleaning datasets before running thermal ablation or pharmacokinetic models. I needed a reliable, traceable pipeline. This tool acts as my automated bridge between raw lab results and the simulation environment. 

## 🏃‍♀️ How to Run It Locally
Make sure you have your virtual environment set up, then run:
```bash
pip install -r requirements.txt
reflex run

(Stay tuned! More analytical features like correlation matrices and regression models are in the pipeline.)
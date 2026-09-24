import pandas as pd
from core.regression import calculate_polynomial_regression

df = pd.DataFrame({
    "X": [1, 2, 3, 4, 5, 6],
    "Y": [10, 19, 32, 49, 70, 95] 
})

print("Testing Polynomial Regression (Degree 2)...")
result = calculate_polynomial_regression(df, x_col="X", y_col="Y", degree=2)

if result:
    print("✅ Success!\n")
    print(f"Degree: {result['degree']}")
    
    rounded_coeffs = [round(c, 2) for c in result['coefficients']]
    print(f"Coefficients: {rounded_coeffs}")
    
    print(f"R² Score: {result['r2']:.4f}")
    print(f"RMSE:     {result['rmse']:.4f}")
else:
    print("❌ Error processing data")
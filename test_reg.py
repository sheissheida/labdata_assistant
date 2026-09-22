import pandas as pd
from core.regression import calculate_linear_regression

# داده‌های تستی با یک رابطه‌ی خطیِ واضح (y ≈ 2x + 10) و یک ردیفِ دارای NaN
df = pd.DataFrame({
    "Temperature": [10, 20, 30, 40, 50, 60],
    "Yield": [31, 48, 72, 89, 112, None], 
    "Status": ["A", "B", "A", "C", "B", "A"]
})

result = calculate_linear_regression(df, x_col="Temperature", y_col="Yield")

if result:
    print("✅ Regression Analysis Successful:\n")
    print(f"Equation: Y = {result['slope']:.2f}X + {result['intercept']:.2f}")
    print(f"R² Score: {result['r2']:.4f}")
    print(f"RMSE:     {result['rmse']:.4f}")
    print(f"MAE:      {result['mae']:.4f}")
else:
    print("❌ خطای پردازش داده‌ها")
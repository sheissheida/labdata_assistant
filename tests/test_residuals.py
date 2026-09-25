import pandas as pd
from core.residuals import calculate_residuals

# داده‌های مصنوعی با یک خطای سیستماتیک کوچک (Y ≈ 2X + نویز)
df = pd.DataFrame({
    "X": [1, 2, 3, 4, 5],
    "Y": [2.1, 3.9, 6.2, 8.1, 9.8] 
})

print("Testing Residual Engine (Linear Model)...")
result = calculate_residuals(df, x_col="X", y_col="Y", model_type="linear")

if result:
    print("✅ Engine Successful!\n")
    
    stats = result["statistics"]
    print("--- Residual Statistics ---")
    print(f"Mean Residual: {stats['mean_residual']:.6f} (Should be close to 0)")
    print(f"Std Residual:  {stats['std_residual']:.4f}")
    print(f"Min / Max:     {stats['min_residual']:.4f} / {stats['max_residual']:.4f}\n")
    
    data = result["data"]
    print("--- Data Points (First 3) ---")
    print(f"X values:   {data['x'][:3]}")
    print(f"Actual:     {data['actual'][:3]}")
    print(f"Predicted:  {[round(p, 4) for p in data['predicted'][:3]]}")
    print(f"Residuals:  {[round(r, 4) for r in data['residual'][:3]]}")
else:
    print("❌ Error processing data")
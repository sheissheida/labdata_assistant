import pandas as pd
from core.analysis import calculate_correlation_matrix

# ۱. تعریف داده‌های تستی
df = pd.DataFrame({
    "Temperature": [100, 110, 120, 130, 140],
    "Pressure": [2, 3, 4, 5, 6],
    "Yield": [50, 55, 61, 68, 75],
    "Sample": ["A", "B", "C", "D", "E"],
})

# ۲. اجرای موتور تحلیل
corr_matrix = calculate_correlation_matrix(df)

# ۳. بررسی نتایج
if corr_matrix is not None:
    print("✅ محاسبه موفقیت‌آمیز ماتریس همبستگی:\n")
    print(corr_matrix)
else:
    print("❌ خطای منطقی: ستون‌های عددی کافی وجود نداشت.")
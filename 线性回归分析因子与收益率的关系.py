from sklearn.linear_model import LinearRegression
import pandas as pd

# 假设df是包含因子和收益率的数据
X = df[['PE', 'PB', '动量']]  # 因子
y = df['收益率']  # 目标变量

model = LinearRegression()
model.fit(X, y)
print("因子权重：", model.coef_)
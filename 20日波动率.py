import akshare as ak
import pandas as pd
import numpy as np

# 获取沪深300成分股数据
def fetch_hs300_components():
    # 使用 AKShare 获取沪深300成分股
    df = ak.index_stock_cons(symbol="000300")  # 000300 是沪深300指数的代码
    return df

# 获取单只股票的历史数据
def fetch_stock_data(stock_code):
    # 使用 AKShare 获取股票历史数据
    df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date="20220101", end_date="20231231", adjust="qfq")
    return df

# 计算20日波动率
def calculate_20d_volatility(df):
    # 计算对数收益率
    df['log_return'] = np.log(df['收盘'] / df['收盘'].shift(1))
    # 计算20日波动率（标准差）
    df['20d_volatility'] = df['log_return'].rolling(window=20).std() * np.sqrt(252)  # 年化波动率
    return df

# 主函数
def main():
    # 获取沪深300成分股
    hs300_components = fetch_hs300_components()
    print("沪深300成分股数量:", len(hs300_components))

    # 创建一个空的 DataFrame 用于存储结果
    volatility_results = pd.DataFrame(columns=['股票代码', '股票名称', '20日波动率'])

    # 遍历每只成分股，计算20日波动率
    for index, row in hs300_components.iterrows():
        stock_code = row['品种代码']
        stock_name = row['品种名称']
        print(f"正在处理: {stock_name} ({stock_code})")

        try:
            # 获取股票历史数据
            stock_data = fetch_stock_data(stock_code)
            if stock_data.empty:
                print(f"未找到数据: {stock_name} ({stock_code})")
                continue

            # 计算20日波动率
            stock_data = calculate_20d_volatility(stock_data)
            latest_volatility = stock_data['20d_volatility'].iloc[-1]  # 获取最新的20日波动率

            # 将结果保存到 DataFrame
            new_row = pd.DataFrame({
                '股票代码': [stock_code],
                '股票名称': [stock_name],
                '20日波动率': [latest_volatility]
            })
            volatility_results = pd.concat([volatility_results, new_row], ignore_index=True)
        except Exception as e:
            print(f"处理 {stock_name} ({stock_code}) 时出错: {e}")

    # 保存结果到 CSV 文件
    volatility_results.to_csv('hs300_20d_volatility.csv', index=False)
    print("20日波动率计算完成，结果已保存到 hs300_20d_volatility.csv")

# 运行主函数
if __name__ == '__main__':
    main()
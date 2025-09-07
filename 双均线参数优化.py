import backtrader as bt
import pandas as pd
import numpy as np

# 创建双均线策略类
class SmaCross(bt.Strategy):
    params = (
        ('short_period', 5),   # 短期均线周期
        ('long_period', 20),   # 长期均线周期
    )

    def __init__(self):
        # 计算短期均线和长期均线
        self.sma_short = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.long_period)

    def next(self):
        # 如果短期均线上穿长期均线，买入
        if not self.position and self.sma_short > self.sma_long:
            self.buy()
        # 如果短期均线下穿长期均线，卖出
        elif self.position and self.sma_short < self.sma_long:
            self.sell()

# 参数优化函数
def optimize_strategy(data, short_periods, long_periods):
    # 创建一个空的 DataFrame 用于存储结果
    results = pd.DataFrame(columns=['短期均线', '长期均线', '夏普比率', '最大回撤'])

    # 遍历不同的均线组合
    for short in short_periods:
        for long in long_periods:
            if short >= long:
                continue  # 短期均线必须小于长期均线

            # 创建 Cerebro 引擎
            cerebro = bt.Cerebro()

            # 添加策略
            cerebro.addstrategy(SmaCross, short_period=short, long_period=long)

            # 加载数据
            data_feed = bt.feeds.PandasData(dataname=data)
            cerebro.adddata(data_feed)

            # 设置初始资金
            cerebro.broker.set_cash(100000.0)

            # 设置手续费
            cerebro.broker.setcommission(commission=0.001)

            # 添加分析器
            cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
            cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

            # 运行回测
            print(f"测试参数: 短期={short}, 长期={long}")
            result = cerebro.run()[0]
            sharpe_ratio = result.analyzers.sharpe.get_analysis()['sharperatio']
            max_drawdown = result.analyzers.drawdown.get_analysis()['max']['drawdown']

            # 将结果保存到 DataFrame
            new_row = pd.DataFrame({
                '短期均线': [short],
                '长期均线': [long],
                '夏普比率': [sharpe_ratio],
                '最大回撤': [max_drawdown]
            })
            results = pd.concat([results, new_row], ignore_index=True)

    # 保存结果到 CSV 文件
    results.to_csv('sma_optimization_results.csv', index=False)
    print("参数优化完成，结果已保存到 sma_optimization_results.csv")

# 主函数
def main():
    # 加载数据（假设已经有一个 CSV 文件）
    data = pd.read_csv('000300.SH.csv', parse_dates=['date'], index_col='date')

    # 定义参数范围
    short_periods = range(5, 21, 5)  # 短期均线周期：5, 10, 15, 20
    long_periods = range(20, 61, 10)  # 长期均线周期：20, 30, 40, 50, 60

    # 运行参数优化
    optimize_strategy(data, short_periods, long_periods)

# 运行主函数
if __name__ == '__main__':
    main()
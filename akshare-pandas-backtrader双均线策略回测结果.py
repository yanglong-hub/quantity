import akshare as ak
import pandas as pd
import backtrader as bt
import os

# 获取沪深 300 指数数据
def fetch_data():
    # 使用 AKShare 获取沪深 300 指数数据
    df = ak.stock_zh_index_daily(symbol="sh000300")  # sh000300 是沪深 300 指数的代码

    # 将日期列转换为 DatetimeIndex
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # 按日期排序
    df.sort_index(inplace=True)

    # 重命名列以符合 Backtrader 的要求
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)

    # 保存为 CSV 文件（保存到桌面）
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop_path, '000300.SH.csv')
    df.to_csv(file_path)
    print(f'数据已保存到: {file_path}')
    return file_path

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

# 主函数
def run_backtest(file_path):
    # 创建 Cerebro 引擎
    cerebro = bt.Cerebro()

    # 添加策略
    cerebro.addstrategy(SmaCross)

    # 加载数据（使用 GenericCSVData）
    data = bt.feeds.GenericCSVData(
        dataname=file_path,
        fromdate=pd.to_datetime('2015-01-01'),
        todate=pd.to_datetime('2020-12-31'),
        dtformat='%Y-%m-%d',  # 日期格式
        timeframe=bt.TimeFrame.Days,
        compression=1,
        openinterest=-1,  # 不需要持仓量列
        headers=True,  # CSV 文件包含表头
        reverse=False  # 数据顺序是正序
    )
    cerebro.adddata(data)

    # 设置初始资金
    cerebro.broker.set_cash(100000.0)

    # 设置手续费
    cerebro.broker.setcommission(commission=0.001)

    # 添加分析器
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    # 运行回测
    print('初始资金: %.2f' % cerebro.broker.getvalue())
    results = cerebro.run()
    print('最终资金: %.2f' % cerebro.broker.getvalue())

    # 输出分析结果
    strat = results[0]
    sharpe_ratio = strat.analyzers.sharpe.get_analysis()['sharperatio']
    max_drawdown = strat.analyzers.drawdown.get_analysis()['max']['drawdown']
    print('夏普比率: %.2f' % sharpe_ratio)
    print('最大回撤: %.2f%%' % max_drawdown)

    # 绘制回测结果
    cerebro.plot()

# 获取数据并运行回测
if __name__ == '__main__':
    file_path = fetch_data()  # 获取数据并保存为 CSV 文件
    run_backtest(file_path)  # 运行回测
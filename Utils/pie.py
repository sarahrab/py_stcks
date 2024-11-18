from typing import List

import matplotlib.pyplot as plt
import numpy as np
from numpy.core.multiarray import ndarray

from stocks import Stock, Stocks


class Pie:

    @classmethod
    def show_stock_pie(cls, stocks: Stocks):
        values = []
        vals = 0
        for s in stocks.stocks:
            total = s.price * s.count
            val = int(total / stocks.get_stocks_value() * 100)
            if vals + val > 100:
                val = 100 - vals
            vals += val
            values.append(val)

        if  vals < 100:
            values[len(values) - 1] += 100 - vals

        y = np.array(values)
        #y = np.array([10, 20, 30, 40])
        plt.pie(y)
        plt.show()
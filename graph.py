import unittest
from collections import OrderedDict
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib.ticker import NullFormatter




class Draw():

    @staticmethod
    def plot_rainfall(nlist):
        # Creating data to plot
        dates, rainfalls = [], []
        for record in nlist:
            dates.append(record['DATE'])
            rainfalls.append(record['Rainfall sum'])

        # Creating plot
        fig, ax = plt.subplots()
        ax.plot(dates, rainfalls)

        ax.set(xlabel='month', ylabel='day rainfall (mm)',
               title='simple graph')
        ax.grid()

        # Set month as x label
        ax.xaxis.set_major_locator(MonthLocator(bymonthday=1))
        ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))

        ax.xaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_minor_formatter(DateFormatter('%B'))

        # Set center of month
        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')

        # Saving image
        # fig.savefig("test.png")

        # Show plot
        plt.show()

class DrawTests(unittest.TestCase):

    def setUp(self):
        self.nlist = [OrderedDict([(u'DATE', datetime.date(2016, 4, 12)), (u'Rainfall sum', 1.0)]),
                      OrderedDict([(u'DATE', datetime.date(2016, 4, 13)), (u'Rainfall sum', 3.0)]),
                      OrderedDict([(u'DATE', datetime.date(2016, 4, 14)), (u'Rainfall sum', 8.1)]),
                      OrderedDict([(u'DATE', datetime.date(2016, 4, 15)), (u'Rainfall sum', 10.0)]),
                      OrderedDict([(u'DATE', datetime.date(2016, 4, 16)), (u'Rainfall sum', 5.1)])]

    def test_sample_out(self):
        Draw.plot_rainfall(self.nlist)

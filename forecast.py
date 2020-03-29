import pandas
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

"""
Based on https://towardsdatascience.com/covid-19-infection-in-italy-mathematical-models-and-predictions-7784b4d7dd8d
"""

def plot(attribute_alias, attribute, data, plot_file):
    data_time = [t//1000 for t,_ in data]
    day = 60*60*24
    data_time_forecast = data_time + list(range(data_time[-1], data_time[-1]+day*30, day))
    # print(data_time)
    filling = [None]*(len(data_time_forecast)-len(data_time))

    df = pandas.DataFrame({
        attribute: [v for _,v in data] + filling,
    })

    df.index = [datetime.fromtimestamp(t) for t in data_time_forecast]

    # print(df)

    # ax = df.plot(kind='line', y=attribute, color='red')
    # ax.legend([attribute_alias]);
    
    def linear(x, a, b):
        return a * x + b

    def logistic_model(x,a,b,c):
        return c/(1+np.exp(-(x-b)/a))

    def inverse_logistic_model(y,a,b,c):
        return -np.log((c/y)-1)*a + b

    x = np.array([(t-data_time[0])//day for t in data_time])
    y = np.array([v for _,v in data])

    #print(x)
    #print(y)

    popt, pcov = curve_fit(logistic_model, xdata=x, ydata=y, p0=[3.54,68.00,15968.38])

    errors = [np.sqrt(pcov[i][i]) for i in [0,1,2]]

    a, b, c = popt

    day_max = inverse_logistic_model(popt[2]-1, a, b, c)

    report = [
        str(datetime.fromtimestamp(data_time[-1])),
        "Infection speed: {} +/- {}".format(popt[0], errors[0]),
        "Day of maximum infections: {} +/- {}".format(datetime.fromtimestamp((popt[1]*day)+data_time[0]), errors[1]),
        "Total number of infected people: {} +/- {}".format(popt[2], errors[2]),
        "Infection end: {}".format(datetime.fromtimestamp((day_max*day)+data_time[0]))
    ]

    print("\n".join(report))
    #print(popt)
    # print(errors)
    # print(day_max)

    yy = np.array([logistic_model((t-data_time[0])//day, a, b, c) for t in data_time_forecast])
    #print(yy)

    df['logistic'] = yy 
    ax = df.plot(kind='line', style=['bo-', 'r-'], figsize=[15,10])

    ax.yaxis.grid()
    ax.text(0.05, -0.25, "\n".join(report), transform=ax.transAxes, fontsize=14, verticalalignment='bottom') 

    plt.savefig(plot_file)


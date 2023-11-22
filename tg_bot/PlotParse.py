import matplotlib.pyplot as plt
import random #для теста

def PlotParse(dates, values, chat_id, username, month): #len(dates) == len(values) !!!
    #plt.plot(dates, values, 'ro', dates, values, 'r--') #dots and punktir
    plt.bar(dates, values)
    plt.axis((0.5, 31.5, 0, 5.5))
    plt.ylabel('emotions')
    plt.title(f"{username}'s mood in {month}")
    plt.xlabel(f'date, {month}')
    #plt.show()
    plt.savefig(f'userplots/{chat_id}_plot.png')


#тестовые значения
#dates = [1, 2, 3, 4, 5]
#values = [4, 3, 5, 2, 5]
dates = range(31)
values = [random.randint(1, 5) for i in range(31)]
PlotParse(dates, values, 'vanya', 'Vanya', 'January')
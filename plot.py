import matplotlib.pyplot as plt


def PlotParse(dates, values, chat_id, username, when):  # len(dates) == len(values)
    # plt.plot(dates, values, 'ro', dates, values, 'r--') #dots and punktir
    print("Plot parser:", dates, values)

    # добавим фиктивный столбик в начало
    dates = ['---'] + dates
    values = [0] + values

    plt.clf()
    plt.figure(figsize=(8, 7))
    plt.bar(dates, values)
    plt.axis((0.5, len(dates) + 1.5, 0, 5.5))
    plt.ylabel("mood")
    plt.title(f"{username}'s mood {when}")
    plt.xlabel(f"dates")
    plt.xticks(rotation=90)
    # plt.show()
    plt.savefig(f"userplots/{chat_id}_plot.png")

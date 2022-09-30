def avg_rate(rates):
    rate_on = 0.0
    rating = 0
    ra = []
    for i in rates:
        ra.append(i.rate)
        rating += 1
    for no_rate in ra:
        rate_on += no_rate
    average_rate = rate_on / rating
    return round(average_rate, 2)
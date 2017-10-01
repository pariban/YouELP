import csv
import plotly.offline as py
import plotly.graph_objs as go

with open('indian.tsv') as fd:
    reader = csv.reader(fd, delimiter='\t')
    x=[]
    y=[]
    for row in reader:
        x.append(row[0])
        y.append(float(row[1]))

    sum_y = sum(y)
    for i, val in enumerate(y):
        y[i] /= sum_y

    data = [go.Bar( x=x, y=y)] 
    py.plot(data, filename='basic-bar')
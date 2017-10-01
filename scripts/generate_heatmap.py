import csv
import sys
# import plotly.plotly as py
import plotly.offline as py
import plotly.graph_objs as go


def main(filename):
    """ plots heatmap """
    with open(filename) as fd:
        category_names = set()
        reader = csv.reader(fd, delimiter='\t')
        category_sums = {}
        for row in reader:
            category_names.add(row[0])
            category_names.add(row[1])
            if row[0] not in category_sums:
                category_sums[row[0]] = 0
            category_sums[row[0]] += float(row[2])
        category_to_index = {}
        for i, cat in enumerate(category_names):
            category_to_index[cat] = i
        fd.seek(0)
        results = [[0 for i in range(len(category_names))]
                   for i in range(len(category_names))]
        reader = csv.reader(fd, delimiter='\t')
        for row in reader:
            i = category_to_index[row[0]]
            j = category_to_index[row[1]]
            results[i][j] = float(row[2]) / category_sums[row[0]]
        data = [go.Heatmap(z=results, x=list(
            category_names), y=list(category_names))]

        py.plot(data, filename='basic-heatmap')


if __name__ == "__main__":
    main(sys.argv[1])

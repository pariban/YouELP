"""
run as:

truncate.py < resources/correlation_full.tsv > resources/correlation.tsv
"""
import csv
import sys

blacklisted_categories = set([
    'Restaurants'
])

def emit_rows(rows, count, writer):
    i = 0
    for row in sorted(rows, key=lambda x: float(x[2]), reverse=True):
        writer.writerow(row)
        i += 1
        if i >= count:
            return


def is_blacklisted(source, target):
    if source == target:
        return True
    global blacklisted_categories
    if target in blacklisted_categories:
        return True
    return False


def main():
    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t')
    source = None
    max_entries = 1
    rows = []
    for row in reader:
        if row[0] != source:
            if len(rows) > 0:
                emit_rows(rows, max_entries, writer)
            rows = []
            source = row[0]
            count = 0
        if is_blacklisted(row[0], row[1]):
            continue
        rows.append(row)


if __name__ == "__main__":
    main()

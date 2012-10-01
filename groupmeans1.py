import sys
import pandas as pd

data = pd.read_csv(sys.argv[1])
numbers = data.dtypes[data.dtypes == float].index
groups  = data.dtypes[data.dtypes != float].index

pd.set_printoptions(max_columns=100, max_rows=5000)

for group in groups:
    ave = data.groupby(group).mean()
    ave['#'] = data[group].value_counts()
    for number in numbers:
        print '\n%s by %s' % (number, group)
        ave = ave[ave[number].notnull() & (ave['#'] > 10)]
        print ave.sort(number, ascending=False)

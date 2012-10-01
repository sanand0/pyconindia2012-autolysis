import sys
from scipy.stats.mstats import f_oneway
import pandas as pd

data = pd.read_csv(sys.argv[1])
numbers = data.dtypes[data.dtypes == float].index
groups  = data.dtypes[data.dtypes != float].index

pd.set_printoptions(max_columns=100)

for group in groups:
    grouped = data.groupby(group)
    ave = grouped.mean()
    ave['#'] = data[group].value_counts()
    for number in numbers:
        F, prob = f_oneway(*grouped[number].values)
        ave = ave[ave[number].notnull() & (ave['#'] > 10)]
        if len(ave):
            print '\n%s by %s: %0.3f' % (number, group, prob)
            print ave.sort(number, ascending=False).head(10)

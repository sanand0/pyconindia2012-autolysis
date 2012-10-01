import sys
from scipy.stats.mstats import f_oneway
import pandas as pd

data = pd.read_csv(sys.argv[1])
numbers = data.dtypes[data.dtypes == float].index
groups  = data.dtypes[data.dtypes != float].index

pd.set_printoptions(max_columns=100)

results = []
for group in groups:
    grouped = data.groupby(group)
    ave = grouped.mean()
    ave['#'] = data[group].value_counts()
    for number in numbers:
        F, prob = f_oneway(*grouped[number].values)
        improvement = ave[number].max() / data[number].mean() - 1
        if prob < .05:
            ave = ave[ave[number].notnull() & (ave['#'] > 10)]
            results.append([group, number, improvement, prob,
                ave.sort(number, ascending=False)])

for group, number, improvement, prob, ave in sorted(results, key=lambda v: v[2], reverse=True):
    print '\n%s by %s: %0.1f%% (%0.3f)' % (number, group, 100 * improvement, prob)
    # print '-' * 80
    # print ave.head(10)
    # if len(ave) > 20:
    #     print ave.tail(10)

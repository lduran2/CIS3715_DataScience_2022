r'''
 Canonical : https://github.com/lduran2/CIS3715_DataScience_2022/blob/main/final/sample_dataset.py
 Samples a set of X, y from examples of dataset files.
 By        : Leomar Durán <https://github.com/lduran2>
 When      : 2022-04-06t19:43Q
 For       : CIS 3715/Principles of Data Science
 Version   : 1.0.0

 CHANGELOG :
    v1.0.0 - 2022-04-07t07:34Q
        gets the options for sampling
 '''

import sys                          # gets command line arguments
from getopt import getopt           # to handle command line options
import csv                          # for list read
import random                       # for sampling
import pandas as pd                 # for dataframe
from pathlib import Path            # for handling paths

# constants
K_EXAMPLES = 20000                  # default to sampling 20,000
OPTIONS = r'n:'                     # short commandline option names
LONG_OPTIONS = [ r'nsamples=' ]     # long commandline option names
SEED = 42                           # seed for sampling

# apply the seed
random.seed(SEED)

# get the options from commandline
option_to_values, argv = getopt(sys.argv[1:], OPTIONS, LONG_OPTIONS)

# loop through options (key, value) pair
for kopt, opt_value in option_to_values:
    # store if K_EXAMPLES key
    if (kopt in (r'-n', r'--nsamples')):
        K_EXAMPLES = int(opt_value)
    # end if (kopt in (r'-n', r'--nsamples'))
# next kopt

# loop through filenames in argv
for filename in argv:
    # open the corresponding file
    with open(filename) as csvfile:
        # read each row as a list
        csvin = csv.reader(csvfile)
        # loop through the rows
        for irow, row in enumerate(csvin):
            pass
        # next row
        # rewind the file
        csvfile.seek(0)

        # store the dimensionality of the file
        (N_EXAMPLES, N_FEATURES) = (irow, len(row))
        # create the sample indices
        i_samples_unsorted = random.sample(range(N_EXAMPLES), K_EXAMPLES)
        i_samples = sorted(i_samples_unsorted)[::-1]

        matrix_builder = []
        # loop through the rows
        for irow, row in enumerate(csvin):
            # break if no more samples
            if (not(i_samples)):
                break
            # end if (not(i_samples))
            # if row is not sampled
            if (irow != i_samples[-1]):
                continue
            # end if (row != i_samples[-1])
            # add this row
            matrix_builder.append(row)
            # pop the sample found
            i_samples.pop()
        # next row

        # create the dataframe
        df = pd.DataFrame(matrix_builder)
        print(df.shape)
        # write to csv file
        df.to_csv(Path('dataset/sampled.csv'))
    # end with csvfile
# next filename

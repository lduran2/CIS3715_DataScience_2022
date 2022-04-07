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

# to handle command line options
import sys
from getopt import getopt

# constants
N_SAMPLES = 20000                   # default to sampling 20,000
OPTIONS = r'n:'                     # short commandline option names
LONG_OPTIONS = [ r'nsamples=' ]     # long commandline option names

# get the options from commandline
option_to_values, argv = getopt(sys.argv[1:], OPTIONS, LONG_OPTIONS)

# loop through options (key, value) pair
for kopt, opt_value in option_to_values:
    # store if N_SAMPLES key
    if (kopt in (r'-n', r'--nsamples')):
        N_SAMPLES = opt_value
    # end if (kopt in (r'-n', r'--nsamples'))
# next kopt

print(N_SAMPLES)

# loop through file names in argv
for filename in argv:
    print(filename)
# next filename

print(r'Done.')

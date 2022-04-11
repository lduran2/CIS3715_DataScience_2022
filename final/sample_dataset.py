r'''
 Canonical : https://github.com/lduran2/CIS3715_DataScience_2022/blob/main/final/sample_dataset.py
 Samples a set of X, y from examples of dataset files.
 By        : Leomar Durán <https://github.com/lduran2>
 For       : CIS 3715/Principles of Data Science

 CHANGELOG :
    v1.3.0 - 2022-04-10t21:35Q
        modularized sample_dataset

    v1.2.0 - 2022-04-10t17:22Q
        sampling is done

    v1.1.0 - 2022-04-10t14:56Q
        counting row of each file

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

def main(K_EXAMPLES=K_EXAMPLES):
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
        with open(filename) as csvfile:
            # sample the csvfile
            df = sampleCsvFile(csvfile, K_EXAMPLES)
            # write to csv file
            df.to_csv(Path(r'dataset/sampled.csv'))
        # end with csvfile
    # next filename
# end def main()

def sampleCsvFile(infile, K_EXAMPLES):
    r'''
     Samples K_EXAMPLES from infile into a dataframe.
     @param infile : file = source file
     @param K_EXAMPLES : int = # indices to sample
     @return dataframe of K-sampled examples.
     '''
    # read each row as a list
    csvin = csv.reader(infile)
    # get the dimensionality
    (N_EXAMPLES, N_FEATURES) =  shape_2d(csvin)
    # rewind the file
    infile.seek(0)
    # sample the indiced
    i_samples = sampleIndexStack(N_EXAMPLES, K_EXAMPLES)
    # copy csv file and convert to a dataframe
    df = pd.DataFrame(idxdCpy([], csvin, i_samples))
    # return the dataframe
    return df
# end def sample

def shape_2d(list2d):
    r'''
     Finds the shape of bidimensional list-like of a dataframe.
     @param list2d : listlike<listlike> = to traverse
     @return (N_EXAMPLES, N_FEATURES) = # of examples, # features of
        the dataframe
     '''
    # loop through the rows
    for irow, row in enumerate(list2d):
        pass
    # next row
    # store the dimensionality of the file
    (N_EXAMPLES, N_FEATURES) = (irow, len(row))
    # return the dimensionality
    return (N_EXAMPLES, N_FEATURES)
# end def shape_2d(list2d)

def sampleIndexStack(N, K):
    r'''
     Creates a stack of the K sampled indices [0..N[.
     @param N : int = # elements in original iterable
     @param K : int = # indices to sample
     @return stack of sampled indices.
     '''
    # indices to be sampled
    iis = range(N)
    # sample them
    i_samples = random.sample(iis, K)
    # sort them
    i_sorted = sorted(i_samples)
    # reverse them for a stack
    istack = i_sorted[::-1]
    # return the stack
    return istack
# end def sampleIndexStack(N, K)

def idxdCpy(dest, src, istack):
    r'''
     Copies elements whose index matches those from istack in order
     from src in dest.
     @param dest : list<T> = destination list
     @param src : iterable = source iterable
     @param istack : list<int> = the index stack
     @return the list copy, dest.
     '''
    for idx, el in enumerate(src):
        # return if no more samples
        if (not(istack)):
            return dest
        # end if (not(istack))
        consumeIdxd(dest.append, idx, el, istack)
    # next el
    return dest
# end def idxdCpy(dest, src, istack)

def consumeIdxd(consume, idx, el, istack):
    r'''
     Calls the consume callback on the given element if its index is
     next in the index stack.

     This function is destructive on i_samples.
     @param consume : function<? super T> = to consume elements
     @param idx : int = index of current element
     @param el : T = element to consume
     @param istack : list<int> = the index stack
     '''
    # consume only if element is next indexed
    if (idx != istack[-1]):
        return
    # end if (idx != istack[-1])
    # add this element
    consume(el)
    # pop the sample found
    istack.pop()
# end def consumeIdxd(consume, idx, el, istack)

if __name__ == "__main__":
    main()

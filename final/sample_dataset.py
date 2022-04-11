r'''
 Canonical : https://github.com/lduran2/CIS3715_DataScience_2022/blob/main/final/sample_dataset.py
 Samples a set of X, y from examples of dataset files.
 By        : Leomar Durán <https://github.com/lduran2>
 For       : CIS 3715/Principles of Data Science

 CHANGELOG :
    v1.2.3 - 2022-04-10t23:45Q
        stacks->iterators, implemented associated (X,y)

    v1.2.2 - 2022-04-10t22:16Q
        fixed df index written, IDed feat/tgt files

    v1.2.1 - 2022-04-10t21:35Q
        modularized `sample_dataset.py`

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
from cqs_iter import CqsIter        # for iterator

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

    # report number of samples
    print(r"===sampling to {} examples===".format(K_EXAMPLES))

    # loop through filenames in argv
    for X_inname in argv:
        # set up file names
        # input X, y
        X_inpath = Path(X_inname)
        y_inpath = X_inpath.parent / r''.join([r'y', X_inpath.name[1:]])
        # output X, y
        samp_label = [r'_samp', str(K_EXAMPLES), X_inpath.suffix]
        X_outpath = X_inpath.parent / r''.join([X_inpath.stem, *samp_label])
        y_outpath = X_inpath.parent / r''.join([y_inpath.stem, *samp_label])
        # report reading/writing
        print(r'===reading from===')
        print(X_inpath)
        print(y_inpath)
        print(r'===writing to===')
        print(X_outpath)
        print(y_outpath)
        # perform conversion
        with open(X_inpath) as X_csvfile, open(y_inpath) as y_csvfile:
            # sample the csvfiles
            # y_csvfile 1st because it will be used to find
            #   dimensionality and is smaller
            dfs = sampleCsvFile([y_csvfile, X_csvfile], K_EXAMPLES)
            # write to each csv file
            for (df, outpath) in zip(dfs, [y_outpath, X_outpath]):
                df.to_csv(outpath, index=False)
            # next (df, outpath)
        # end with X_csvfile, y_csvfile
        print()
    # next filename
# end def main()

def sampleCsvFile(infiles, K_EXAMPLES):
    r'''
     Samples K_EXAMPLES from infile into a dataframe.
     @param infiles : file = source files in CSV format
     @param K_EXAMPLES : int = # indices to sample
     @return list of dataframes of K-sampled examples from infiles.
     '''
    # create readers for rows as lists
    csvins = [ csv.reader(infile) for infile in infiles ]
    # get the dimensionality (from 1st file)
    (N_EXAMPLES, _) =  shape_2d(csvins[0])
    # rewind the file
    infiles[0].seek(0)
    # report number of examples
    print(r"===sampling {} examples".format(N_EXAMPLES))
    # sample the indices
    i_samples = sampleIndexes(N_EXAMPLES, K_EXAMPLES)
    # list of output dataframes
    dfs = []
    # for each csv input file
    for csvin in csvins:
        # iterator on samples
        iit = CqsIter(iter(i_samples))
        # copy csv file, convert to dataframe
        dfs.append(pd.DataFrame(idxdCpy([], csvin, iit)))
    # next csvin
    # return the dataframe
    return dfs
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

def sampleIndexes(N, K):
    r'''
     Creates a list of the K sampled indices [0..N[.
     @param N : int = # elements in original iterable
     @param K : int = # indices to sample
     @return list of sampled indices.
     '''
    # indices to be sampled
    iis = range(N)
    # sample them
    i_samples = random.sample(iis, K)
    # sort them
    i_sorted = sorted(i_samples)
    # return sorted indexes
    return i_sorted
# end def sampleIndexes(N, K)

def idxdCpy(dest, src, iit):
    r'''
     Copies elements whose index matches those from the index iterator
     in order from src in dest.
     @param dest : list<T> = destination list
     @param src : iterable = source iterable
     @param iit : CqsIter<int> = the index iterator
     @return the list copy, dest.
     '''
    for idx, el in enumerate(src):
        # return if no more samples
        if (not(iit.isValid())):
            return dest
        # end if (not(iit))
        consumeIdxd(dest.append, idx, el, iit)
    # next el
    return dest
# end def idxdCpy(dest, src, iit)

def consumeIdxd(consume, idx, el, iit):
    r'''
     Calls the consume callback on the given element if its index is
     next in the index iterator.
     @param consume : function<? super T> = to consume elements
     @param idx : int = index of current element
     @param el : T = element to consume
     @param iit : CqsIter<int> = the index iterator
     '''
    # consume only if element is next indexed
    if (idx != iit.get()):
        return
    # end if (idx != iit.get())
    # add this element
    consume(el)
    # pop the sample found
    iit.next()
# end def consumeIdxd(consume, idx, el, iit)

if __name__ == "__main__":
    main()

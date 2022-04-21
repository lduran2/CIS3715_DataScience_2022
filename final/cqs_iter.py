r'''
 Canonical : https://github.com/lduran2/CIS3715_DataScience_2022/blob/main/final/cqs_iter.py
 A command-query separated version of iterator.
 By        : Leomar Durán <https://github.com/lduran2>
 For       : CIS 3715/Principles of Data Science

 @see https://wiki.kluv.in/a/CommandQuerySeparation (wiki.c2.com)

 CHANGELOG :
    v1.0.1 - 2022-04-11t00:41Q
        `isValid`->`__bool__`, implemented `__iter__`

    v1.0.1 - 2022-04-10t23:26Q
        handling no more elements in iterator

    v1.0.0 - 2022-04-10t22:59Q
        initial implementation
 '''

class CqsIter:
    # Represents no more elements in an iterator.
    __default = object()

    def __init__(self, it):
        r'''
         Adapts the iterator `it`.
         @param it : iter = the backing iterator
         '''
        self._it = it
        CqsIter.__next(self)
    # end def __init__(self, it)

    def next(self):
        r'''
         Moves the iterator to the next element.
         '''
        CqsIter.__next(self)
    # def next(self)

    def __bool__(self):
        r'''
         Returns true if the iterator is valid, i.e., if there is a current element.
         @return true if the iterator is valid; false otherwise.
         '''
        return (self._curr is not CqsIter.__default)
    # def isValid(self)

    def get(self, default=__default):
        r'''
         Returns the current element whereto the iterator points.
         @param default : object = to return when no more elements
         @return the current element whereto the iterator points.
         '''
        # if no more elements
        if (self._curr is CqsIter.__default):
            # and no default, then raise exception
            if (default is CqsIter.__default):
                raise StopIteration
            else:
                # otherwise, return the given default
                return default
            # end if (default is CqsIter.__default) ||
        return self._curr
    # end def get(self, default=CqsIter.__default)

    def __iter__(self):
        r'''
         Returns the backing iterator.
         @return the backing iterator.
         '''
        return self._it

    def __next(self):
        r'''
         Private function implements #next.
         @see #next
         '''
        self._curr = next(self._it, CqsIter.__default)
    # end def __next(self)

# end class CqsIter
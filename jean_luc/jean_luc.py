from collections import defaultdict
from itertools import chain
import numpy as np


def _reverse_index(mapping, index, item):
    for element in set(item):
        mapping[element].append(index)
    return mapping


class JeanLuc:
    def __init__(self):
        self.mapping = defaultdict(list)
        self.items = {}

    def add_item(self, index, item):
        """add_item

        Parameters
        ----------
        index : 
            Hashable index.
        item :
            Iterable of hashable objects.
        """
        if index in self.items:
            raise ValueError(f'index {index} already exists')
        else:
            self.items[index] = item
            self.mapping = _reverse_index(self.mapping, index, item)

    def by_id(self, index, cmin=0.0, cmax=1.0, jaccard=True, jmin=0.0, 
            jmax=1.0, ignore=None):
        '''by_id
        '''
        item = self.items[index]
        return by_item(item, cmin, cmax, jaccard, jmin, jmax, ignore)

    def by_item(self, item, cmin=0.0, cmax=1.0, jaccard=True, jmin=0.0, 
            jmax=1.0, ignore=None, index=None):
        '''by_item
        '''
        item_size = len(item)
        match_ids, counts = self._matches(item)
        containments = counts / item_size
        
        mask = self._mask(cmin, cmax, match_ids, containments, counts, ignore)

        if mask is not None:
            match_ids = match_ids[mask]
            counts = counts[mask]
            containments = containments[mask]

        if jaccard:
            jaccards = self._pyccard(match_ids, counts, item_size)
            mask = (jaccards >= jmin) & (jaccards <= jmax)
            containments = containments[mask]
            jaccards = jaccards[mask]
            for m, c, j in zip(match_ids, containments, jaccards):
                result = (m, c, j)
                if index is not None:
                    result =  (index,) + result
                yield result
        else:
            for m, c in zip(match_ids, containments):
                result = (m, c)
                if index is not None:
                    result =  (index,) + result
                yield result
    
    def pairwise(self, compare=None, cmin=0.0, cmax=1.0, jaccard=True, 
            jmin=0.0, jmax=1.0, self_loops=False):
        """pairwise

        Parameters
        ---------- 
        compare : iter (optional)
            An alternative sequence of sets to perform pairwise calculations.
            If None, then pairwise calculations are carried out between the 
            elements of class attribute, `items`. Defaults to None.
        cmin : int or float
        cmax : int or float
        jaccard : bool
        jmin : float
        jmax : float
        self_loops : bool

        Returns
        -------
        """

        p = self._generate_pairwise(compare, cmin, cmax, jaccard,
                jmin, jmax, self_loops)

        for result in chain(*p):
            yield result

    def _generate_pairwise(self, compare=None, cmin=0.0, cmax=1.0, jaccard=True, 
            jmin=0.0, jmax=1.0, self_loops=False):
        """_generate_pairwise
        """
        if compare is None:
            compare = self.items

        for index, item in compare.items():
            if not self_loops:
                ignore = index
            else:
                ignore = None
            yield self.by_item(item, cmin, cmax, jaccard, jmin, jmax, ignore, index)
    
    def _pyccard(self, match_ids, counts, item_size):
        """_pyccard
        """
        match_sizes = np.array([len(self.items[m]) for m in match_ids])
        union = item_size + match_sizes - counts
        jaccards = counts / union
        return jaccards

    def _matches(self, item):
        """_matches
        """
        candidates = chain(*[self.mapping[e] for e in item])
        match_ids, counts = np.unique(list(candidates), return_counts=True)
        return match_ids, counts

    def _mask(self, cmin, cmax, match_ids, containments=None, counts=None, ignore=None):
        if type(cmin) == float:
            min_mask = containments >= cmin
        elif type(cmin) == int:
            min_mask = counts >= cmin

        if type(cmax) == float:
            max_mask = containments <= cmax
        elif type(cmax) == int:
            max_mask = counts <= cmax

        if ignore is not None:
            self_mask = match_ids != ignore
        else:
            self_mask = True

        mask = min_mask & max_mask & self_mask

        if all(mask) == True:
            return None
        else:
            return mask


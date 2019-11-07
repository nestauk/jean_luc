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

    def pairwise(self, compare=None, cmin=0.0, cmax=1.0, jaccard=False, 
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
        if compare is None:
            compare = self.items
            
        for index, item in compare.items():
            item_size = len(item)
            candidates = chain(*[self.mapping[e] for e in item])

            match_ids, counts = np.unique(list(candidates), return_counts=True)
            
            if not self_loops:
                self_mask = match_ids != index
                match_ids = match_ids[self_mask]
                counts = counts[self_mask]

            containments = counts / item_size
            
            if type(cmin) == float:
                min_mask = containments >= cmin
            elif type(cmin) == int:
                min_mask = counts >= cmin

            if type(cmax) == float:
                max_mask = containments <= cmax
            elif type(cmax) == int:
                max_mask = counts <= cmax

            mask = min_mask & max_mask
            match_ids = match_ids[mask]
            counts = counts[mask]
            containments = containments[mask]

            if jaccard:
                match_sizes = np.array([len(self.items[m]) for m in match_ids])
                union = item_size + match_sizes - counts
                jaccards = counts / union
                mask = (jaccards >= jmin) & (jaccards <= jmax)
                containments = containments[mask]
                jaccards = jaccards[mask]

                for m, c, j in zip(match_ids, containments, jaccards):
                    yield(index, m, c, j)
            else:
                for m, c in zip(match_ids, containments):
                    yield (index, m, c)


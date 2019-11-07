Jean-Luc
========

Calculates Jaccard similarity at  warp speed, using the method devised by
Jean-Luc Pyccard himself.


## Usage

```python
from jean_luc import JeanLuc
import numpy as np

x = [set(np.random.randint(0, 500, np.random.randint(1, 11))) for _ in range(1000)]

j = JeanLuc()

for item in x:
    j.add_item(item)

p = j.pairwise()

print(next(p))
(0, 1, 0.75, 0.6)
```

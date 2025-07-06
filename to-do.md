1. Use bit masking to hash processed states in `PowersetConstruction.toDFA`
```python
newStatesInv = dict()
def to_bitmask(s: set[int]) -> int:
  bitmask = 0
  for val in s:
    bitmask |= (1<<val)
  return bitmask
# new states
newStatesInv[to_bitmask(state)] = id

# check if processed
bitmask = to_bitmask(state)
if bitmask in newStatesInv:
  id = newStatesInv[bitmask]

```
constraint: `S ⊂ [0, 63]`
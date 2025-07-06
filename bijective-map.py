# from typing import Dict, TypeVar, Generic

# A = TypeVar('A')
# B = TypeVar('B')

# class BijectiveMap(Generic[A, B]):
#     def __init__(self):
#         self._data: Dict[A, B] = {}

#     def add(self, x: A, y: B) -> None:
#         self._data[x] = y
#         self._data[y] = x

#     def get(self, key: T) -> T:
#         return self._data[key]

# # Example:
# bm = BijectiveMap()
# bm.add(1, "a")
# print(bm.get(1))  # Output: "a"
# print(bm.get("a"))  # Output: 1
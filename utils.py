from typing import TypeVar, Generic

T = TypeVar('T')
class Queue(Generic[T]):
  def __init__(self) -> None:
    super().__init__()
from typing import TypeVar, Generic, Callable
from queue import Queue

T = TypeVar("T")

class Stack(Generic[T]):
  data: list[T] = []
  
  def isEmpty(self) -> bool:
    return len(self.data) == 0
  
  def pop(self) -> T:
    return self.data.pop()
  
  def peek(self) -> T | None:
    if not self.isEmpty():
      return self.data[-1]
    return None
  
  def push(self, val: T):
    self.data.append(val)

# +---+----------------------------------------------------------+
# |   |             ERE Precedence (from high to low)            |
# +---+----------------------------------------------------------+
# | 1 | Collation-related bracket symbols | [==] [::] [..]       |
# | 2 | Escaped characters                | \<special character> |
# | 3 | Bracket expression                | []                   |
# | 4 | Grouping                          | ()                   |
# | 5 | Single-character-ERE duplication  | * + ? {m,n}          |
# | 6 | Concatenation                     |                      |
# | 7 | Anchoring                         | ^ $                  |
# | 8 | Alternation                       | |                    |
# +---+-----------------------------------+----------------------+

unaryOperators: set[str] = {"*", "?", "+"}  # operator[i] = 5
operations: dict[str, int] = {
  "(": 4,
  ")": 10,
  "*": 5,
  "+": 5,
  "?": 5,
  ".": 6,
  "|": 8
}

def standardizeRegex(string: str) -> str:
  """
  Standardizes a regex string by adding implicit concatenation operators.
  This function ensures that concatenation is explicitly represented in the regex.
  """
  standardized = ""
  for i in range(len(string)):
    currentChar = string[i]
    
    # handle implicit concatenation
    if i > 0 and (string[i-1] not in operations or operations[string[i-1]] == 5 or string[i-1] == ")") and (currentChar not in operations or currentChar == "("):
      standardized += "."
      
    standardized += currentChar
    
  return standardized
    

def infixToPostfix(string: str) -> str:
  stack: Stack[str] = Stack()
  postfix: str = ""
  for i in range(len(string)):
    currentChar: str = string[i]
    if currentChar == " ":
      continue  # skip spaces
      
    if currentChar in operations:
      if currentChar == ")":
        while True:
          top = stack.peek()
          if top is None:
            raise ValueError("Invalid input regex")
          if top == "(":
            stack.pop()
            break
          postfix += stack.pop()
        top = stack.peek()
      elif operations[currentChar] == 5:
        postfix += currentChar
      else:
        stack.push(currentChar)
    else:
      postfix += currentChar
      top = stack.peek()
      if top and top != "(":
        if i >= len(string) - 1 or (string[i + 1] in operations and operations[string[i+1]] >= operations[top]):
          postfix += stack.pop()
  
       
  while not stack.isEmpty():
    top = stack.pop()
    if top == "(":
      raise ValueError("Invalid input regex")
    postfix += top
  
  return postfix

class ThompsonConstruction:
  def __init__(self, regex: str):
    self.regex = regex
    standardRegex = standardizeRegex(regex)
    self.postfix = infixToPostfix(standardRegex)

  def toNFA(self) -> 'TCNFA':
    """
    Converts the postfix regex to an NFA using Thompson's construction.
    This method will implement the actual NFA construction logic.
    """
    if not self.postfix:
      raise ValueError("Postfix expression is empty, cannot construct NFA")
    
    stack = Stack[TCNFA]()
    
    for char in self.postfix:
      if char == 'ε':
        stack.push(self.nullSymbol())
      elif char not in operations:
        stack.push(self.symbolToNFA(char))
      elif char == '|':
        nfa2 = stack.pop()
        nfa1 = stack.pop()
        
        if nfa1 is None or nfa2 is None:
          raise ValueError("Invalid NFA stack state for union operation")
        
        newNFA = self.union(nfa1, nfa2)
        stack.push(newNFA)
      elif char == '.':
        nfa2 = stack.pop()
        nfa1 = stack.pop()
        
        if nfa1 is None or nfa2 is None:
          raise ValueError("Invalid NFA stack state for concatenation operation")
        
        newNFA = self.concatenation(nfa1, nfa2)
        stack.push(newNFA)
      else:
        nfa = stack.pop()
        
        if nfa is None:
          raise ValueError("Invalid NFA stack state for Kleene closure operation")
        
        newNFA = self.kleeneClosure(nfa)
        stack.push(newNFA)
        
    NFA = stack.pop()
    if NFA is None or not stack.isEmpty():
      raise ValueError("Invalid NFA stack state after processing all characters")
    
    return NFA
    
    
  def nullSymbol(self) -> 'TCNFA':
    """
    Creates an NFA that accepts the empty string (null symbol).
    This method will implement the logic to create an NFA for the null symbol.
    """
    nfa = TCNFA(
      states={0, 1},
      alphabet=set(),
      transition={(0, 'ε'): {1}},
      startState=0,
      acceptState=1
    )
    return nfa
    
  def symbolToNFA(self, symbol: str) -> 'TCNFA':
    """
    Converts a single symbol to an NFA.
    This method will implement the logic to create an NFA for a single symbol.
    """
    nfa = TCNFA(
      states={0, 1},
      alphabet={symbol},
      transition={(0, symbol): {1}},
      startState=0,
      acceptState=1
    )
    return nfa
  
  def union(self, nfa1: 'TCNFA', nfa2: 'TCNFA') -> 'TCNFA':
    """
    Creates an NFA that represents the union of two NFAs.
    This method will implement the union logic for NFAs.
    """
    m = len(nfa1.states)
    n = len(nfa2.states)
    
    nfa1 = nfa1.remapStates(lambda x: x + 1)
    nfa2 = nfa2.remapStates(lambda x: x + len(nfa1.states) + 1)
    
    nfa1.addTransition(nfa1.acceptState, 'ε', m + n + 1)
    nfa2.addTransition(nfa2.acceptState, 'ε', m + n + 1)
    
    newNFA = TCNFA(
      states={0, m + n + 1},
      alphabet=set(),
      transition={
        (0, 'ε'): {nfa1.startState, nfa2.startState},
      },
      startState=0,
      acceptState=m + n + 1
    )
    
    newNFA.mergeNFA(nfa1)
    newNFA.mergeNFA(nfa2)
    
    return newNFA
  
  def concatenation(self, nfa1: 'TCNFA', nfa2: 'TCNFA') -> 'TCNFA':
    """
    Concatenates two NFAs.
    This method will implement the concatenation logic for NFAs.
    """
    nfa2 = nfa2.remapStates(lambda x: x + len(nfa1.states) - 1)
    
    newNFA = TCNFA(
      states=nfa1.states.union(nfa2.states),
      alphabet=nfa1.alphabet.union(nfa2.alphabet),
      transition={**nfa1.transitions, **nfa2.transitions},
      startState=nfa1.startState,
      acceptState=nfa2.acceptState
    )
    
    return newNFA
  
  def kleeneClosure(self, nfa: 'TCNFA') -> 'TCNFA':
    """
    Applies the Kleene closure operation to the given NFA.
    This method will implement the Kleene closure logic.
    """
    n = len(nfa.states)
    
    nfa = nfa.remapStates(lambda x: x + 1)
    nfa.addTransition(nfa.acceptState, 'ε', nfa.startState)
    nfa.addTransition(nfa.acceptState, 'ε', n+1)
    
    newNFA = TCNFA(
      states={0, n+1},
      alphabet=set(),
      transition={
        (0, 'ε'): {nfa.startState, n+1},
      },
      startState=0,
      acceptState=n+1
    )
    
    newNFA.mergeNFA(nfa)
    
    return newNFA


class TCNFA:
  nullCache: dict[int, set[int]]
  def __init__(self, states: set[int], alphabet: set[str], transition: dict[tuple[int, str], set[int]], startState: int, acceptState: int):
    self.startState = startState
    self.states = states
    self.acceptState = acceptState
    self.transitions = transition
    self.alphabet = alphabet
    self.nullCache = dict()
    
  def addTransition(self, src: int, symbol: str, *dest: int):
    """
    Adds a transition to the NFA.
    This method will implement the transition addition logic.
    """
    if (src, symbol) in self.transitions:
      self.transitions[(src, symbol)].update(dest)
    else:
      self.transitions[(src, symbol)] = set(dest)
      
  def remapStates(self, x: Callable[[int], int]) -> 'TCNFA':
    """
    Remaps the states of the NFA using the provided mapping function.
    This method will implement the state remapping logic.
    """
    newStates = set(x(s) for s in self.states)
    newStartState = x(self.startState)
    newAcceptState = x(self.acceptState)
    
    newTransitions = {}
    for (src, symbol), dest in self.transitions.items():
      newTransitions[(x(src), symbol)] =  set(x(s) for s in dest)
    
    return TCNFA(newStates, self.alphabet, newTransitions, newStartState, newAcceptState)
  
  def mergeNFA(self, other: 'TCNFA'):
    """
    Merges this NFA with another NFA.
    This method will implement the NFA merging logic.
    """
    newStates = self.states.union(other.states)
    newAlphabet = self.alphabet.union(other.alphabet)
    
    newTransitions = self.transitions.copy()
    for (src, symbol), dest in other.transitions.items():
      if (src, symbol) in newTransitions:
        newTransitions[(src, symbol)].update(dest)
      else:
        newTransitions[(src, symbol)] = set(dest)
    
    self.states = newStates
    self.alphabet = newAlphabet
    self.transitions = newTransitions
    
  def read(self, inputString: str) -> bool:
    """
    Reads an input string and checks if it is accepted by the NFA.
    This method will implement the NFA acceptance logic.
    """
    currentStates = self.nonDeterministicRead(self.startState, cache=self.nullCache)
    
    for symbol in inputString:
      nextStates = set()
      if symbol == "ε":   # null sentinel not allowed in input
        raise ValueError("Input string cannot contain null symbol 'ε'")
      for state in currentStates:
        if (state, symbol) in self.transitions:
          nextStates.update(*[self.nonDeterministicRead(s, cache=self.nullCache) for s in self.transitions[(state, symbol)]])
          
      currentStates = nextStates
    
    if self.acceptState in currentStates:
      return True
    
    return False
    
  def nonDeterministicRead(self, state: int, cache: dict[int, set[int]] | None = None, processing: set[int] | None = None) -> set[int]:
    """
    Returns all null reachable states from the given state.
    This method will implement the logic to find all null reachable states.
    Caches in 'cache'
    """
    # keep track of states being processed to avoid deadlock 0 -> 1 -> 2 -> 0
    # will lead to infinite loop it 0 is still being processed
    if not processing:
      processing = set()
    if state in processing:
      return {state}
    else:
      processing.add(state)
    
    if cache is None:
      cache = dict()
      
    if state in cache:
      processing.remove(state)
      return cache[state]
    
    reachableStates = {state}
    
    if (state, 'ε') in self.transitions:
      reachableStates.update(*[self.nonDeterministicRead(s, cache, processing=processing) for s in self.transitions[(state, 'ε')]])
    
    cache[state] = {*reachableStates}
    processing.remove(state)

    return reachableStates
  def __str__(self) -> str:
    return {
      "state": self.states,
      "alphabet": self.alphabet,
      "transitions": self.transitions,
      "start": self.startState,
      "accept": self.acceptState
    }.__str__()
  


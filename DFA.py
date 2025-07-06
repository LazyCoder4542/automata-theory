from typing import Callable, Literal
import queue

class DFA():
  stateMap: dict[str, int] = dict()   # map literal state to standard id
  stateMapRev: dict[int, str] = dict()        # map standard state to literal
  states: list[str]                   # set of state in literal
  transitions: list[list[int]]      # transition matrix (n X m) n -> accessible states, m -> input alphabet 
  alphabet: list[str]                 # input alphabet for the machine
  alphabetMap: dict[str, int]
  initialState: str                   # literal for initial state
  trapState: int | None = None
  trapStateSym = "Z"
  acceptState: set[str] = set()
  def __init__(self, states: list[str], alphabet: list[str], transitions: dict[str, list[str | None]], initialState: str, acceptStates: set[str]):
    self.states = states
    self.alphabet = alphabet
    self.initialState = initialState
    self.acceptState = acceptStates
    
    n = len(states)
    m = len(alphabet)
    
    self.alphabetMap = dict([(alphabet[i], i) for i in range(m)])
    self.transitions = self.standardizeFSA(transitions)
    
    self.drawStateTable()
        
          
  def standardizeFSA(self, transitions: dict[str, list[str | None]]) -> list[list[int]]:
    n = len(self.states)
    m = len(self.alphabet)
    
    trapState: int | None = None
    
    transitionsMatrix: list[list[int]] = []
    
    # map literal state to standard id, states are assigned a proper id and are added to the queue (to process their next states in-order))
    
    currentId = 0
    currentStates: queue.Queue[str] = queue.Queue()
    self.map(self.initialState, 0)
    currentStates.put(self.initialState)
    
    while not currentStates.empty():
      _state = currentStates.get()
      transition: list[int] = []
      nextStates = transitions[_state] if _state in transitions else []
      for i in range(m):
        nextState = self.trapStateSym
        id = trapState
        
        if i < len(nextStates):
          nextState = nextStates[i] or self.trapStateSym
        
        if nextState in self.stateMap:              # next state mapped 
          id = self.stateMap[nextState]
        else:
          currentId += 1
          if nextState == self.trapStateSym:
            trapState = currentId
          self.map(nextState, currentId)
          id = currentId
          currentStates.put(nextState)
        transition.append(id)
      transitionsMatrix.append(transition)
      
    self.trapState = trapState
    print(self.stateMap)
    print(f'trapState Z = {trapState}')
    
    return transitionsMatrix
  
  def generateEquivalence(self, printout: bool = False) -> list[int]:
    n = len(self.transitions)
    m = len(self.alphabet)
    equivalence: list[list[int]] = [[1 if self.isAcceptState(x) else 0 for x in range(n)]]
    keys: list[list[list[int]]] = [self.transitions]

    i = 0   # counter for current equivalence generated
    while i < 1 or equivalence[i] != equivalence[i - 1]:
      patternDict: dict[str, int] = dict()
      patterns: list[str] = list()
      newTransitions: list[list[int]] = []
      currentId = 0   #id attach to a pattern
      for j in range(n):
        pattern = f"{equivalence[i][j]}"
        newTransition = []
        for k in range(m):
          pattern += str(equivalence[i][self.transitionFunc(j, k)])
          newTransition.append(equivalence[i][self.transitionFunc(j, k)])
        newTransitions.append(newTransition)
        patterns.append(pattern)
        if pattern not in patternDict:
          patternDict[pattern] = currentId
          currentId += 1
      keys.append(newTransitions)
      equivalence.append([patternDict[p] for p in patterns])
      i += 1
    
    
    separator = "+" + "+".join("-" * (3) for _ in range((i + 1) * (m + 1) + 1)) + "+"
    header = "    |" + "|".join([f"{itm}" for j in range(i + 1) for itm in [*[f" {k} " for k in range(m)], f" \u2261{chr(0x2080 + j)}"]]) + "|"
    row: Callable[[int], str] = lambda x: f"  {x} " + "|" + "|".join([f" {itm} " for j in range(i + 1) for itm in [*[ keys[j][x][l] for l in range(m)], equivalence[j][x]]]) + "|"

    if printout:
      print({"equiv": equivalence})
      print(header)
      print(separator)
      for _i in range(n):
        
        print(row(_i))
        print(separator)
        
    return equivalence[i]
    
  
  def removeEquivalentStates(self):
    equivalence = self.generateEquivalence(printout=True)
    group: dict[int, list[int]] = {}  # group state by equivalence class
    remap: dict[int, int] = {}
    for (idx, equ) in enumerate(equivalence):
      if equ not in group:
        group[equ] = []
      group[equ].append(idx)
      
      remap[idx] = equ
    
    self.remapFSA(group, remap)
    
    self.drawStateTable()
        
  def isAcceptState(self, S: int) -> bool:
    if S in self.stateMapRev and self.stateMapRev[S] in self.acceptState:
      return True
    return False
  
  def drawStateTable(self):
    m = len(self.alphabet)
    print(m)
    separator = "+" + "+".join("-" * (3) for i in range(m + 1)) + "+"
    header = "    " + "|" + "|".join(f" {self.alphabet[i]} " for i in range(m)) + "|"
    row: Callable[[int, str], str] = lambda x, y: f" {x}  " + "|" + "|".join(f" {self.transitionFunc(x, i)} " for i in range(m)) + "|" + f" {y}"
    print(header)
    print(separator)
    for i in range(len(self.transitions)):
      literal = self.stateMapRev[i]
      label = f"{literal}"
      if self.isAcceptState(i):
        label += "*"
      print(row(i, label))
      print(separator)
  
  def map(self, literal: str, id: int):
    self.stateMap[literal] = id
    self.stateMapRev[id] = literal
    
  def remapFSA(self, group: dict[int, list[int]], remap: dict[int, int]):
    
    self.transitions = [[remap[self.transitions[i][j]] for j in range(len(self.alphabet))]
                      for i in range(len(self.transitions))
                      if i in group]  # remove empty transitions

    
    newStateMap: dict[str, int] = {}
    newStateMapRev: dict[int, str] = {}
    newAcceptStates: set[str] = set()
    newTrapState = None
    
    for (k, v) in group.items():
      newLiteral = self.stateMapRev[v[0]]  # use the first state in the group as the representative
      if v[0] == self.trapState:
        newTrapState = k
      if self.isAcceptState(v[0]):
        newAcceptStates.add(newLiteral)
      newStateMap[newLiteral] = k
      newStateMapRev[k] = newLiteral
      
    self.stateMap = newStateMap
    self.stateMapRev = newStateMapRev
    self.acceptState = newAcceptStates
    self.trapState = newTrapState
  
  def transitionFunc(self, S: int, a: int ) -> int:
    return self.transitions[S][a]
  
  def read(self, input: str) -> Literal["accept", "reject"]:
    currentState = 0
    for alpha in input:
      if currentState == self.trapState: # smart break
        break
      if alpha not in self.alphabetMap:
        raise Exception("Input string is invalid")
      currentState = self.transitionFunc(currentState, self.alphabetMap[alpha])
    # input has been fully scanned
    if self.isAcceptState(currentState):
      return "accept" 
    return "reject"
  
nfa1 = DFA(
  states=["A", "B"],
  alphabet=["0", "1"],
  transitions={
    "A": ["A", "B"]
  },
  initialState="A",
  acceptStates={"A"}
)
string = "111111"

print(f"{string} -> {nfa1.read(string)}")
nfa1.removeEquivalentStates()
print(f"{string} -> {nfa1.read(string)}")
nfa1.removeEquivalentStates()
print(f"{string} -> {nfa1.read(string)}")


# nfa2 = DFA(
#   states=["A", "B", "C"],
#   alphabet=["0", "1"],
#   transitions={
#     "A": ["C", "B"],
#     "B": ["B", "B"],
#     "C": ["C", "C"]
#   },
#   initialState="A",
#   acceptStates={"B", "C"}
# )

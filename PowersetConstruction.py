from typing import Callable
from queue import Queue
from ThompsonConstruction import TCNFA


class PowersetConstruction:
  nullClosures: dict[int, set[int]]
  newStatesInv: dict[int, int]
  newStates: dict[int, set[int]]
  acceptStates: set[int]
  newTransitions: dict[tuple[int, str], int]
  nfa: 'TCNFA'
  def __init__(self, nfa: 'TCNFA'):
    self.nfa = nfa
    self.nullClosures = dict()
    
    self.newStates = dict()
    self.newStatesInv = dict()
    self.acceptStates = set()
    self.newTransitions = dict()

  def toDFA(self) -> 'DFA':
    count = 0     #number of items in the system (processed + in queue)
    done = 0      #number if items waiting (in queue)
    currentSet = Queue[set[int]]()
    start = self.nfa.nonDeterministicRead(self.nfa.startState, self.nullClosures)

    self.addState(count, {*start})
    if self.nfa.acceptState in start:
        self.acceptStates.add(count)
    count += 1
    
    currentSet.put({*start})
    
    while not currentSet.empty():
      #pop item
      newState = currentSet.get()
      done += 1
      
      #process transitions
      nrStates = set[int]()     # null reachable states
      for i in newState:
        nrStates.update(self.nfa.nonDeterministicRead(i, self.nullClosures))
      
      for symbol in self.nfa.alphabet:
        rStates = set[int]()    # reachable states via symbol
        for i in nrStates:
          if (i, symbol) in self.nfa.transitions:
            for dest in self.nfa.transitions[(i, symbol)]:
              rStates.update(self.nfa.nonDeterministicRead(dest, self.nullClosures))
        
        if len(rStates) == 0 or rStates in newState:
          continue
        
        #add to new states and transition
        bitmask = self.to_bitmask(rStates)
        id: int
        if bitmask in self.newStatesInv:
          id = self.newStatesInv[bitmask]
        else:
          id = count
          self.addState(id, rStates)
          if self.nfa.acceptState in rStates:
              self.acceptStates.add(id)
          #add next states to queue
          currentSet.put(rStates)
          count += 1
        self.newTransitions[(done - 1, symbol)] = id   #id of predecessor state is done - 1
    
    self.introduceTrapState()
         
    return DFA(
      states={*self.newStates.keys()},
      alphabet=self.nfa.alphabet,
      transition=self.newTransitions,
      startState=0,
      acceptStates=self.acceptStates
    )
  
  def introduceTrapState(self):
    """
    Introduces a trap state to the DFA.
    This method will implement the logic to add a trap state.
    """
    isNeeded = False
    trapState = max(self.newStates.keys()) + 1
    
    for state in self.newStates:
      for symbol in self.nfa.alphabet:
        if (state, symbol) not in self.newTransitions:
          isNeeded = True
          self.newTransitions[(state, symbol)] = trapState
    
    if isNeeded:
      for symbol in self.nfa.alphabet:
        self.newTransitions[(trapState, symbol)] = trapState
      self.newStates[trapState] = set()
  
  def addState(self, id: int, old: set[int]):
    self.newStates[id] = old
    self.newStatesInv[self.to_bitmask(old)] = id
    
  def to_bitmask(self, s: set[int]):
    bitmask = 0
    for val in s:
      bitmask |= (1<<val)
    return bitmask
  
class DFA:
  def __init__(self, states: set[int], alphabet: set[str], transition: dict[tuple[int, str], int], startState: int, acceptStates: set[int]):
    self.startState = startState
    self.states = states
    self.acceptStates = acceptStates
    self.transitions = transition
    self.alphabet = alphabet
    
  def changeTransition(self, src: int, symbol: str, dest: int):
    """
    Changes a transition in the NFA.
    This method will implement the transition change logic.
    """
    self.transitions[(src, symbol)] = dest
    
  def read(self, inputString: str) -> bool:
    """
    Reads an input string and checks if it is accepted by the NFA.
    This method will implement the NFA acceptance logic.
    """
    currentState = self.startState
    
    for symbol in inputString:
      currentState = self.transitions[(currentState, symbol)]
    
    if currentState in self.acceptStates:
      return True
    
    return False

  def __str__(self) -> str:
    return {
      "state": self.states,
      "alphabet": self.alphabet,
      "transitions": self.transitions,
      "start": self.startState,
      "accept": self.acceptStates
    }.__str__()
  

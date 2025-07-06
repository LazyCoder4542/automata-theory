from PowersetConstruction import DFA


class Hopcroft:
  P: set[frozenset[int]]      # partitions
  def __init__(self, dfa: 'DFA'):
    self.P = set()
    self.P.add(frozenset(dfa.acceptStates))
    self.P.add(frozenset(dfa.states.difference(dfa.acceptStates)))
    
    self.dfa = dfa
    
  def coarsePartition(self):
    changeMade = False
    while not changeMade:
      newP = set()
      for p in self.P:
        for c in self.dfa.alphabet:
          A = frozenset({s for s in p if self.dfa.transitions[s, c] in self.dfa.acceptStates})
          NA = p.difference(A)
          if len(A) != 0 and len(NA) != 0:
            newP.add(A)
            newP.add(NA)
            changeMade = True
            break
        else:
          newP.add(p)
      self.P = newP.copy()
  
  def minimize(self):
    self.coarsePartition()
    partition = list(self.P)
    partition.sort(key= lambda x: min(x))
    classes = dict[int, int]()      # maps states to their equivalence class
    for i, c in enumerate(partition):
      for s in c:
        classes[s] = i
    
    transitions = dict[tuple[int, str], int]()
    for (src, sym), dest in self.dfa.transitions.items():
      transitions[(classes[src], sym)] = classes[dest]
    
    return DFA(
      states=set(range(len(self.P))),
      alphabet=self.dfa.alphabet,
      transition=transitions,
      startState=0,
      acceptStates={classes[s] for s in self.dfa.acceptStates}
    )
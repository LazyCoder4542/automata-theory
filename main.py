from Hopcroft import Hopcroft
from ThompsonConstruction import ThompsonConstruction
from PowersetConstruction import PowersetConstruction
from utils.draw import drawDFA, drawNFA
# from utils import draw

def main():
  tc = ThompsonConstruction("ε|a*.b")
  nfa = tc.toNFA()
  drawNFA(nfa, "nfa")
  pc = PowersetConstruction(nfa)
  dfa = pc.toDFA()
  drawDFA(dfa)
  hp = Hopcroft(dfa)
  dfa_min = hp.minimize()
  drawDFA(dfa_min, filename="dfa_min", comment="DFA minimized")
  print(dfa_min)

if __name__ == "__main__":
  main()
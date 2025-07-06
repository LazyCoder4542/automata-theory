import unittest
import PowersetConstruction as PC
import ThompsonConstruction as TC
from utils.draw import drawNFA


class TestPowerset(unittest.TestCase):
  def test_powersetConstruction(self):
    tc = TC.ThompsonConstruction("ε|a*.b")
    nfa = tc.toNFA()
    pc = PC.PowersetConstruction(nfa)
    dfa = pc.toDFA()
    
    self.assertIsNotNone(dfa, "DFA should not be None after construction")
    self.assertTrue(dfa.read(""), "Constructed DFA should be valid")
    self.assertTrue(dfa.read("b"), "Constructed DFA should be valid for 'b'")
    self.assertTrue(dfa.read("ab"), "Constructed DFA should be valid for 'ab'")
    self.assertTrue(dfa.read("aab"), "Constructed DFA should be valid for 'aab'")
    
    self.assertFalse(dfa.read("a"), "Constructed DFA should not be valid for 'a'")
    self.assertFalse(dfa.read("aa"), "Constructed DFA should not be valid for 'aa'")
    self.assertFalse(dfa.read("bb"), "Constructed DFA should not be valid for 'bb'")
    
  def test_powersetConstructionRobust(self):
    tc = TC.ThompsonConstruction("(0|(1(01*(00)*0)*1)*)*")
    nfa = tc.toNFA()
    pc = PC.PowersetConstruction(nfa)
    dfa = pc.toDFA()
   
    validStrings = { "", "0", "00", "11", "000", "011", "110", "0000", "0011", "0110", "1001", "1100", "1111", "00000",}
    
    self.assertIsNotNone(dfa, "DFA should not be None after construction")
    
    for s in validStrings:
      self.assertTrue(dfa.read(s), f"Constructed DFA should be valid for '{s}'")
    
if __name__ == '__main__':
  unittest.main()

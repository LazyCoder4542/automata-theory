import unittest
import ThompsonConstruction as TC
from utils.draw import drawNFA

class TestThompson(unittest.TestCase):
  def test_standardizeRegex(self):
    self.assertEqual(TC.standardizeRegex("ab"), "a.b", "Standardize Regex failed for 'ab'")
    self.assertEqual(TC.standardizeRegex("ε|a*b"), "ε|a*.b", "Standardize Regex failed for 'ε|a*b'")
    self.assertEqual(TC.standardizeRegex("(0|(1(01*(00)*0)*1)*)*"), "(0|(1.(0.1*.(0.0)*.0)*.1)*)*", "Standardize Regex failed for 'ε|a*b'")
  def test_infixToPostfix(self):
    self.assertEqual(TC.infixToPostfix("ε|a*.b"), "εa*b.|", "Infix to Postfix conversion failed for 'ε|a*.b'")
    self.assertEqual(TC.infixToPostfix("(0|(1.(0.1*.(0.0)*.0)*.1)*)*"), "0101*00.*0...*1..*|*", "Infix to Postfix conversion failed for 'ε|a*.b'")
    
  def test_thompsonConstruction_null(self):
    tc = TC.ThompsonConstruction("ε")
    self.assertEqual(tc.postfix, "ε", "Thompson Construction failed to convert regex to postfix")
    nfa = tc.toNFA()
    self.assertIsNotNone(nfa, "NFA should not be None after construction")
    self.assertTrue(nfa.read(""), "Constructed NFA should be valid")
    self.assertFalse(nfa.read("   "), "Constructed NFA should not be valid for 'c'")
    
    
  def test_thompsonConstruction_singleton(self):
    tc = TC.ThompsonConstruction("a")
    self.assertEqual(tc.postfix, "a", "Thompson Construction failed to convert regex to postfix")
    nfa = tc.toNFA()
    self.assertIsNotNone(nfa, "NFA should not be None after construction")
    self.assertFalse(nfa.read(""), "Constructed NFA should not be valid")
    self.assertTrue(nfa.read("a"), "Constructed NFA should be valid")
    self.assertFalse(nfa.read("aa"), "Constructed NFA should not be valid")
    
  def test_thompsonConstruction_concatenation(self):
    tc = TC.ThompsonConstruction("a.b")
    self.assertEqual(tc.postfix, "ab.", "Thompson Construction failed to convert regex to postfix")
    nfa = tc.toNFA()
    
    self.assertIsNotNone(nfa, "NFA should not be None after construction")
    self.assertTrue(nfa.read("ab"), "Constructed NFA should be valid")
    self.assertFalse(nfa.read(""), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("a"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("aa"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("b"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("bb"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("ba"), "Constructed NFA should not be valid")
    
  def test_thompsonConstruction_union(self):
    tc = TC.ThompsonConstruction("a|b")
    self.assertEqual(tc.postfix, "ab|", "Thompson Construction failed to convert regex to postfix")
    nfa = tc.toNFA()
    
    self.assertIsNotNone(nfa, "NFA should not be None after construction")
    self.assertTrue(nfa.read("a"), "Constructed NFA should be valid")
    self.assertTrue(nfa.read("b"), "Constructed NFA should be valid")
    self.assertFalse(nfa.read(""), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("ab"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("aa"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("ba"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("bb"), "Constructed NFA should not be valid")
    
    
  def test_thompsonConstruction_kleeneStar(self):
    tc = TC.ThompsonConstruction("a*")
    self.assertEqual(tc.postfix, "a*", "Thompson Construction failed to convert regex to postfix")
    nfa = tc.toNFA()
    
    self.assertIsNotNone(nfa, "NFA should not be None after construction")
    self.assertTrue(nfa.read(""), "Constructed NFA should be valid")
    self.assertTrue(nfa.read("a"), "Constructed NFA should be valid")
    self.assertTrue(nfa.read("aaaa"), "Constructed NFA should be valid")
    self.assertTrue(nfa.read("aaaaaaaaa"), "Constructed NFA should be valid")
    self.assertFalse(nfa.read("b"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("ab"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("ba"), "Constructed NFA should not be valid")
    self.assertFalse(nfa.read("bb"), "Constructed NFA should not be valid")
    with self.assertRaises(ValueError) as context:
      nfa.read("ε")
    self.assertEqual(context.exception.args[0], "Input string cannot contain null symbol 'ε'")    
    
  def test_thompsonConstruction(self):
    tc = TC.ThompsonConstruction("ε|a*.b")
    self.assertEqual(tc.postfix, "εa*b.|", "Thompson Construction failed to convert regex to postfix")
    nfa = tc.toNFA()
    
    self.assertIsNotNone(nfa, "NFA should not be None after construction")
    self.assertTrue(nfa.read(""), "Constructed NFA should be valid")
    self.assertTrue(nfa.read("b"), "Constructed NFA should be valid for 'b'")
    self.assertTrue(nfa.read("ab"), "Constructed NFA should be valid for 'ab'")
    self.assertTrue(nfa.read("aab"), "Constructed NFA should be valid for 'aab'")
    
    self.assertFalse(nfa.read("a"), "Constructed NFA should not be valid for 'a'")
    self.assertFalse(nfa.read("aa"), "Constructed NFA should not be valid for 'aa'")
    self.assertFalse(nfa.read("bb"), "Constructed NFA should not be valid for 'bb'")
    
if __name__ == '__main__':
  unittest.main()

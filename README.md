# Automata Theory

A Python implementation of fundamental automata theory concepts, including NFA and DFA implementations with conversion and minimization algorithms.

## Features

- **Finite Automata Implementations**:
  - Deterministic Finite Automaton (DFA)
  - Non-deterministic Finite Automaton (NFA)
  
- **Conversion Algorithms**:
  - Thompson's Construction (Regex to NFA)
  - Powerset Construction (NFA to DFA)
  
- **Minimization Algorithms**:
  - Hopcroft's Algorithm (DFA minimization)
  
- **Operations**:
  - Automata union, concatenation, and Kleene star
  - Language acceptance testing

## Installation

```bash
git clone https://github.com/LazyCoder4542/automata-theory.git
cd automata-theory
pip install -r requirements.txt
```

## Usage (The set of binary numbers that are multiples of 3)
### Regex to NFA
```python
# from utils import draw
from utils.draw import drawDFA, drawNFA

from ThompsonConstruction import ThompsonConstruction

tc = ThompsonConstruction("(0|(1(01*(00)*0)*1)*)*")
nfa = tc.toNFA()
drawNFA(nfa, "nfa")
```
![nfa](https://github.com/user-attachments/assets/46f29a52-2921-471c-b1dc-7c6ede2a6d83)

### NFA to DFA
```python
from PowersetConstruction import PowersetConstruction

pc = PowersetConstruction(nfa)
dfa = pc.toDFA()
drawDFA(dfa)
```
![dfa](https://github.com/user-attachments/assets/122c4c7c-48c1-4dab-a0ee-9a58264853e7)

### Minimize DFA
```python
from Hopcroft import Hopcroft

hp = Hopcroft(dfa)
dfa_min = hp.minimize()
drawDFA(dfa_min, filename="dfa_min", comment="DFA minimized")
```
![dfa_min](https://github.com/user-attachments/assets/4dc8e445-9285-408f-aa45-aa8bccd26ad0)

## Tests

Run the test suite with:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs or feature requests.

## References

### 📚 Algorithm Foundations
- [Thompson's Construction](https://en.wikipedia.org/wiki/Thompson%27s_construction)  
  Wikipedia article on converting regular expressions to NFAs.
- [Powerset Construction](https://en.wikipedia.org/wiki/Powerset_construction)  
  Theoretical basis for NFA-to-DFA conversion.

### 🎥 Visual Explanations
- [Hopcroft's Algorithm - YouTube Tutorial](https://www.youtube.com/watch?v=D01O7TKCQX8)  
  Step-by-step DFA minimization walkthrough.

### 📖 Books & Papers
- *Introduction to the Theory of Computation* by Michael Sipser  
  Covers core automata concepts (DFA/NFA, minimizations).
- [Brzozowski's Algorithm (PDF)](https://cs.stackexchange.com/questions/61110/brzozowskis-algorithm-for-dfa-minimization)  
  Alternative minimization approach.

## License

MIT License

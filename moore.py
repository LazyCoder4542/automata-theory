from DFA import DFA
class MooreMachine(DFA):
  def __init__(self, states: list[str], alphabet: list[str], transitions: dict[str, list[str | None]], initialState: str, output: set[str], oAlphabet: list[str]):
    # super().__init__(states, alphabet, transitions, initialState, acceptStates)
    pass
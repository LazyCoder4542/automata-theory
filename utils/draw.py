from graphviz import Digraph
from PowersetConstruction import DFA
from ThompsonConstruction import TCNFA

def drawNFA(nfa: 'TCNFA', filename="nfa"):
  """
  Draws the NFA using graphviz and saves it to a file.
  
  :param nfa: The NFA object to draw.
  :param filename: The name of the file to save the drawing to.
  """

  dot = Digraph(comment='NFA')
  
  if len(nfa.states) > 10:
    dot.attr(ranksep="1.2",fontsize = "10");          # Increase vertical spacing  Smaller labels
    dot.graph_attr['rankdir'] = 'TB'
  else:
    dot.graph_attr['rankdir'] = 'LR'  # Left to right layout
    
  
  dot.node_attr['fontname'] = "Helvetica,Arial,sans-serif"
  dot.edge_attr['fontname'] = "Helvetica,Arial,sans-serif"
  dot.edge_attr['arrowhead'] = 'vee'
  
  dot.node("", shape='point', width='0', height='0')
  dot.edge("", str(nfa.startState))  # Connect start state to a dummy node
  
  # Add states
  for state in nfa.states:
    if state == nfa.acceptState:
      dot.node(str(state), shape='doublecircle')  # Accept state
    else:
      dot.node(str(state), shape='circle')

  # Add transitions
  for (src, symbol), dest in nfa.transitions.items():
    for state in dest:
      if symbol == 'ε':
        dot.edge(str(src), str(state), style='dashed', label='ε')
      else:
        dot.edge(str(src), str(state), label=symbol)

  # Save the graph to a file
  dot.render(filename, format='svg', cleanup=True)  # Cleanup removes the intermediate files

def drawDFA(dfa: 'DFA', filename="dfa", comment = "DFA"):
  """
  Draws the DFA using graphviz and saves it to a file.
  
  :param nfa: The DFA object to draw.
  :param filename: The name of the file to save the drawing to.
  """

  dot = Digraph(comment=comment)
  
  if len(dfa.states) > 10:
    dot.attr(ranksep="1.2",fontsize = "10");          # Increase vertical spacing  Smaller labels
    dot.graph_attr['rankdir'] = 'TB'
  else:
    dot.graph_attr['rankdir'] = 'LR'  # Left to right layout
    
  
  dot.node_attr['fontname'] = "Helvetica,Arial,sans-serif"
  dot.edge_attr['fontname'] = "Helvetica,Arial,sans-serif"
  dot.edge_attr['arrowhead'] = 'vee'
  
  dot.node("", shape='point', width='0', height='0')
  dot.edge("", str(dfa.startState))  # Connect start state to a dummy node
  
  # Add states
  for state in dfa.states:
    if state in dfa.acceptStates:
      dot.node(str(state), shape='doublecircle')  # Accept state
    else:
      dot.node(str(state), shape='circle')

  # Add transitions
  n = len(dfa.states)
  edges: list[list[set[str] | None]] = [[None for i in dfa.states] for j in dfa.states]
  for (src, symbol), dest in dfa.transitions.items():
    edge = edges[src][dest]
    if edge is None:
      edges[src][dest] = {symbol}
    else:
      edge.add(symbol)
      
  for src in dfa.states:
    for dest in dfa.states:
      edge = edges[src][dest]
      if edge:
        dot.edge(str(src), str(dest), label=", ".join(sorted(edge)))

  # Save the graph to a file
  dot.render(filename, format='svg', cleanup=True)  # Cleanup removes the intermediate files
from graphviz import Digraph

# States
states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
alphabet = ['yes', 'no']

# Transitions
transitions = {
    ('q0', 'Yes'): 'q1',
    ('q0', 'No'): 'q0',
    ('q1', 'Yes'): 'q2',
    ('q1', 'No'): 'q1',
    ('q2', 'Yes'): 'q3',
    ('q2', 'No'): 'q2',
    ('q3', 'Yes'): 'q4',
    ('q3', 'No'): 'q3',
    ('q4', 'Yes'): 'q5',
    ('q4', 'No'): 'q4',
    
    # Over
    ('q0', 'GameOver'): 'q5',
    ('q1', 'GameOver'): 'q5',
    ('q2', 'GameOver'): 'q5',
    ('q3', 'GameOver'): 'q5',
    ('q4', 'GameOver'): 'q5',
    
    ('q5', 'TryAgain'): 'q0',
}

# Start
start_state = 'q0'
accept_states = ['q5']

# Plot
def plot_dfa():
    global states, alphabet, transitions, start_state, accept_states
    dfa = Digraph(format='svg')
    
    dfa.attr(rankdir='LR', size='12,8', nodesep='0.5', ranksep='1.0')
    
    # Legend
    dfa.attr(label='\n\n\n\nLegend: \nYes = Proceed (iff Life > 0), \nNo = Stay (Loses 1 Life), \nGameOver = Life == 0, \nTryAgain = Life == 3')
    dfa.attr(labelloc='b', labeljust='c') 

    # Nodes
    for state in states:
        if state in accept_states:
            dfa.attr('node', shape='doublecircle', fixedsize='true', width='0.5', height='0.5')
        else:
            dfa.attr('node', shape='circle', fixedsize='true', width='0.5', height='0.5')
        dfa.node(state)

    # Arrow
    dfa.attr('node', shape='none',)
    dfa.edge('', start_state, arrowhead='normal', color='red', penwidth='5', label='Start', fontcolor='red')

    # Transitions
    for (src_state, symbol), dst_state in transitions.items():
        dfa.edge(src_state, dst_state, label=symbol)

    # Render
    dfa.render('dfa_graph', view=True)

# Call
plot_dfa()

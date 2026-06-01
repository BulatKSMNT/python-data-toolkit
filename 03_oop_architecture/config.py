num_of_steps = 3

report_template = """Report\n\nWe have made {observations} observations from tossing a coin: {heads} of them were 
tails and {tails} of them were heads. The probabilities are {heads_percent:.2f}% and {tails_percent:.2f}% respectively. 
Our forecast is that in the next {steps} observations we will have: {predicted_heads} tail and {predicted_tails} heads."""
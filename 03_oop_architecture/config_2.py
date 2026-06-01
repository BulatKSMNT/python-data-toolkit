num_of_steps = 3

report_template = """Report\n\nWe have made {observations} observations from tossing a coin: {heads} of them were 
tails and {tails} of them were heads. The probabilities are {heads_percent:.2f}% and {tails_percent:.2f}% respectively. 
Our forecast is that in the next {steps} observations we will have: {predicted_heads} tail and {predicted_tails} heads."""

log_file = "analytics.log"
log_format = "%(asctime)s %(message)s"

TELEGRAM_WEBHOOK_URL = "https://api.telegram.org/bot7812664344:AAECpDEojwiSxhmEnEyIxsfTCkLQ8Zhqg4k/sendMessage"
TELEGRAM_CHAT_ID = "1251634923"
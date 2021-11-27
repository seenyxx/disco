from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d %H-%M-%S')

def log_msg(text):
    with open(f'./logs/{today}.log', 'a+') as log:
        log_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f'[{log_time}] {text}\n')
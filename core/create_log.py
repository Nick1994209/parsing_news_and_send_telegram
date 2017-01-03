import os

from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_LOG_DIR = BASE_DIR + '/logs/'
if not os.path.exists(BASE_LOG_DIR):
    os.makedirs(BASE_LOG_DIR)


def create(message, log_name):

    print(BASE_LOG_DIR)
    path = BASE_LOG_DIR + log_name

    current_time = timezone.now().strftime('%d.%m.%Y - %H:%M')

    log_message = message + '\t' + current_time

    with open(path, 'a') as log_file:
        log_file.write(log_message + '\n')

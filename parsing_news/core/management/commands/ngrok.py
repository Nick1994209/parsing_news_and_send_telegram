import json
import os
import subprocess
import time
from multiprocessing import Process

from django.core.management import BaseCommand

from ...models import TelegramUser


class Command(BaseCommand):
    help = 'Run application in Internet from localhost'
    # ./manage.py ngrok --ngrok_command='/Users/n.korolkov/Downloads/ngrok' --share_port='8080'

    def add_arguments(self, parser):
        parser.add_argument('--share_port', default='8080', type=str)
        parser.add_argument('--ngrok_command', default='ngrok', type=str)
        # parser.add_argument('--hostname', default='localhost', type=str)

    def handle(self, *args, **options):
        try:
            share_port = options['share_port']
            ngrok_command = options['ngrok_command']
            # hostname = options['hostname']

            run_ngrok = Process(target=self.run_ngrok, args=(ngrok_command, share_port))
            run_ngrok.start()

            time.sleep(10)  # wait start ngrok
            ngrok_urls = ', '.join(self.get_ngrok_urls())  # get urls
            for telegram_user in TelegramUser.objects.iterator():
                telegram_user.send_message(ngrok_urls)

            run_ngrok.join()
        finally:
            self.kill_ngrok()

    @staticmethod
    def run_ngrok(ngrok_command, share_port):
        print(ngrok_command, share_port)
        # subprocess.Popen([ngrok_command, 'http', share_port])
        subprocess.check_call([ngrok_command, 'http', share_port])

    @staticmethod
    def get_ngrok_urls():
        public_urls = []
        tunnels_file = '/tmp/tunnels.json'
        os.system("curl  http://localhost:4040/api/tunnels > /tmp/tunnels.json")

        with open(tunnels_file) as data_file:
            datajson = json.load(data_file)

        for tunnel in datajson['tunnels']:
            public_urls.append(tunnel['public_url'])
        return public_urls

    def kill_ngrok(self):
        subprocess.check_call("kill $(ps | grep ngrok | awk '{print $1}')")

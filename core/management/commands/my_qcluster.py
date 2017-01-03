from django_q.management.commands.qcluster import Command as QClusterCommand
from django.utils.translation import ugettext as _

from django_q.cluster import Cluster


class Command(QClusterCommand):
    def handle(self, *args, **options):
        from core.tasks import create_tasks
        create_tasks()

        super().handle(*args, **options)

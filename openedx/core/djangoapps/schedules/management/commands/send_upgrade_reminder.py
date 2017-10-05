from openedx.core.djangoapps.schedules.management.commands import SendEmailBaseCommand
from openedx.core.djangoapps.schedules.resolvers import UpgradeReminderResolver


class Command(SendEmailBaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.resolver_class = UpgradeReminderResolver
        self.log_prefix = 'Upgrade Reminder'

    def send_emails(self, resolver, *args, **options):
        resolver.send(2, options.get('override_recipient_email'))

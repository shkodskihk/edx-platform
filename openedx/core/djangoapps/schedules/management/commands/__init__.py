import datetime

import pytz
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from openedx.core.djangoapps.schedules.utils import PrefixedDebugLoggerMixin


class SendEmailBaseCommand(BaseCommand, PrefixedDebugLoggerMixin):
    def __init__(self, *args, **kwargs):
        super(SendEmailBaseCommand, self).__init__(*args, **kwargs)
        self.resolver_class = None  # define in subclass
        self.log_prefix = self.__class__.__name__

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            default=datetime.datetime.utcnow().date().isoformat(),
            help='The date to compute weekly messages relative to, in YYYY-MM-DD format',
        )
        parser.add_argument(
            '--override-recipient-email',
            help='Send all emails to this address instead of the actual recipient'
        )
        parser.add_argument('site_domain_name')

    def handle(self, *args, **options):
        resolver = self.make_resolver(*args, **options)
        self.send_emails(resolver, *args, **options)

    def make_resolver(self, *args, **options):
        current_date = datetime.datetime(
            *[int(x) for x in options['date'].split('-')],
            tzinfo=pytz.UTC
        )
        self.log_debug('Args = %r', options)
        self.log_debug('Current date = %s', current_date.isoformat())

        site = Site.objects.get(domain__iexact=options['site_domain_name'])
        self.log_debug('Running for site %s', site.domain)
        return self.resolver_class(site, current_date)

    def send_emails(self, resolver, *args, **options):
        resolver.send(0, options.get('override_recipient_email'))

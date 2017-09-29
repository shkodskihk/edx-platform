from __future__ import print_function

import logging

from openedx.core.djangoapps.schedules.management.commands import SendEmailBaseCommand, BinnedSchedulesBaseResolver
from openedx.core.djangoapps.schedules.tasks import (
    VERIFIED_DEADLINE_REMINDER_NUM_BINS,
    verified_deadline_reminder_schedule_bin
)


LOG = logging.getLogger(__name__)


class VerifiedDeadlineResolver(BinnedSchedulesBaseResolver):
    """
    Send a message to all users whose verified upgrade deadline is at ``self.current_date`` + ``day_offset``.
    """
    def __init__(self, *args, **kwargs):
        super(VerifiedDeadlineResolver, self).__init__(*args, **kwargs)
        self.async_send_task = verified_deadline_reminder_schedule_bin
        self.num_bins = VERIFIED_DEADLINE_REMINDER_NUM_BINS
        self.log_prefix = 'Verified Deadline Reminder'
        self.enqueue_config_var = 'enqueue_verified_deadline_reminder'


class Command(SendEmailBaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.resolver_class = VerifiedDeadlineResolver
        self.log_prefix = 'Verified Deadline Reminder'

    def send_emails(self, resolver, *args, **options):
        logging.basicConfig(level=logging.DEBUG)
        resolver.send(2, options.get('override_recipient_email'))

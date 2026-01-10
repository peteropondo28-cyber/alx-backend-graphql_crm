#!/bin/bash

TIMESTAMP=$(date +"%d/%m/%Y-%H:%M:%S")

DELETED_COUNT=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(order__isnull=True, created_at__lt=one_year_ago)
count = qs.count()
qs.delete()
print(count)
")

echo \"$TIMESTAMP Deleted customers: $DELETED_COUNT\" >> /tmp/customer_cleanup_log.txt

#!/bin/bash

# Navigate to project root (IMPORTANT)
cd /alx-backend-graphql_crm || exit 1

# Run Django shell command
DELETED_COUNT=$(python3 manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(order__isnull=True, created_at__lt=one_year_ago)
count = qs.count()
qs.delete()
print(count)
EOF
)

# Log result with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT" >> /tmp/customer_cleanup_log.txt

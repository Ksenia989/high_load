#!/usr/bin/env python
import django
django.setup()
from sightseens.models import Visit, User, Location
from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404

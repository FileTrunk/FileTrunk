#!/bin/bash
celery -A backend worker -B -l INFO


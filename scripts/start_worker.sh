#!/bin/sh

celery -A workers.tasks worker --loglevel=INFO --concurrency=1
#!/usr/bin/env bash
cd /var/www
cp config/stGermain.local.json config/stGermain.json
python launch.py

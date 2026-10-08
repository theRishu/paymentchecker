#!/bin/bash

# One-time cleanup of any stale process still holding the port from an unclean
# shutdown, then run the service directly. systemd (Restart=always, RestartSec=3)
# already handles crash recovery — the old version of this script additionally
# force-killed (kill -9) and restarted the service on its own every 5 minutes
# regardless of health, creating a recurring ~2s window where the payment
# verification API was completely down. Any UTR submitted during that window
# failed outright, which is exactly the kind of intermittent "doesn't work"
# behavior real users would hit but a quick automated test easily misses.
echo "Cleaning port 8087..."
lsof -ti tcp:8087 | xargs kill -9 2>/dev/null

sleep 1

echo "Starting server..."
exec python3.14 main.py

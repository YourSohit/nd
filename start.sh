#!/bin/bash

if [ -z "$SOURCE_CODE" ]; then
  echo "Cloning main repository..."
  git clone https://github.com/Kousthubhbhat/WEB-Content-Notify-V2.git /WEB-Content-Notify-V2
else
  echo "Cloning custom repository from $SOURCE_CODE..."
  git clone $SOURCE_CODE /WEB-Content-Notify-V2
fi

cd /WEB-Content-Notify-V2

# Install dependencies
pip3 install --upgrade -r requirements.txt

# Apply database migrations (if any)
echo "Applying database migrations..."
python3 manage.py migrate || echo "No migrations to apply."

# Start the bot
echo "Starting Bot..."
python3 -m main

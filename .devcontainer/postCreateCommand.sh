#!/bin/bash

# 1️⃣ Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# 2️⃣ Add auto-activate to bashrc if not already present
grep -qxF "source \$PWD/.venv/bin/activate" ~/.bashrc || echo "source \$PWD/.venv/bin/activate" >> ~/.bashrc

# 3️⃣ Activate venv in current terminal session
source .venv/bin/activate

# 4️⃣ Upgrade pip and install requirements if available
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "✅ Virtual environment is ready and auto-activates on every terminal."

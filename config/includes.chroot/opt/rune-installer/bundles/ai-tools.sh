#!/bin/bash
set -e
curl -fsSL https://ollama.com/install.sh | sh
systemctl enable ollama
systemctl start ollama
sleep 3
ollama pull llama3.2:1b
echo "✓ AI tools installed"

# ── Telegram Bot Dockerfile ──────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir pyTelegramBotAPI requests

# Copy bot files
COPY m.py bot.py ./

# Copy the attack binary and make it executable
# (king.dat must be renamed to 'king' when building)
COPY king ./king
RUN chmod +x ./king

# Persistent data directory (mount a volume here to survive restarts)
VOLUME ["/app/data"]

# Symlink data files into /app so the bot reads/writes from the volume
RUN ln -sf /app/data/users.txt /app/users.txt && \
    ln -sf /app/data/free_users.txt /app/free_users.txt && \
    ln -sf /app/data/log.txt /app/log.txt

CMD ["python3", "bot.py"]

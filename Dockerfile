# ── Telegram Bot Dockerfile ──────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir pyTelegramBotAPI requests

# Copy bot files
COPY m.py bot.py ./

# Copy the attack binary (king.dat) and rename it to 'king'
COPY king.dat ./king
RUN chmod +x ./king

# Persistent data directory (mount a volume here to survive restarts)
VOLUME ["/app/data"]

# Create data files before symlinking so symlinks are never broken
RUN mkdir -p /app/data && \
    touch /app/data/users.txt /app/data/free_users.txt /app/data/log.txt

# Symlink data files into /app so the bot reads/writes from the volume
RUN ln -sf /app/data/users.txt /app/users.txt && \
    ln -sf /app/data/free_users.txt /app/free_users.txt && \
    ln -sf /app/data/log.txt /app/log.txt

CMD ["python3", "bot.py"]

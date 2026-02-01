### Discord Announcements Forwarder
- 📣 **Local POST endpoint** - `POST http://localhost:8091/announcements`
- 🔗 **Discord webhook** - forwards JSON payloads to a Discord Incoming Webhook
- 🧩 **Simple payloads** - accepts `message`, `content`, or `text`
- 🧪 **Health check** - `GET /health`

### Discord Announcements Forwarder

This service exposes a local HTTP endpoint and forwards messages to a Discord Incoming Webhook.

**Environment variable**
- `DISCORD_WEBHOOK_URL`: Discord Incoming Webhook URL used to send messages

**Endpoint**
- `POST http://localhost:8091/announcements`
- JSON body with `message`, `content`, or `text`

**Examples**
```bash
curl -X POST http://localhost:8091/announcements \
  -H 'Content-Type: application/json' \
  -d '{"message": "Hello from composeyourself"}'
```

Sample usage...

1. Simple message
   ```
   curl -X POST http://localhost:8091/announcements \
      -H 'Content-Type: application/json' \
      -d '{"message":"Hello from composeyourself"}'
   ```
1. Explicit Discord payload (content)
   ```
   curl -X POST http://localhost:8091/announcements \
      -H 'Content-Type: application/json' \
      -d '{"content":"Deployment finished ✅"}'
   ```
1. Using jq to build JSON (useful for variable interpolation)
   ```
   msg="Backup completed on $(hostname)"
   curl -X POST http://localhost:8091/announcements \
      -H 'Content-Type: application/json' \
      -d "$(jq -n --arg message "$msg" '{message:$message}')"
   ```
1. Multi-line message with jq
   ```
   msg=$'Service restarted:\n- yt-dlp\n- announcements'
   curl -X POST http://localhost:8091/announcements \
      -H 'Content-Type: application/json' \
      -d "$(jq -n --arg message "$msg" '{message:$message}')"
   ```

**Code overview**
- `services/announcements/app.py` defines a Flask app with `/announcements` and `/health`.
- Incoming JSON is normalized to Discord's `content` field.
- Requests are sent to the Discord webhook using `requests`, returning `{ "status": "sent" }` on success.


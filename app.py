import os
from typing import Any, Dict

from flask import Flask, jsonify, request
import requests


def create_app() -> Flask:
    app = Flask(__name__)

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        app.logger.warning("DISCORD_WEBHOOK_URL is not set")

    @app.get("/health")
    def health() -> Any:
        return jsonify({"status": "ok"})

    @app.post("/announcements")
    def announcements() -> Any:
        if not webhook_url:
            return jsonify({"error": "DISCORD_WEBHOOK_URL is not configured"}), 500

        payload: Dict[str, Any] | None = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Expected JSON body"}), 400

        message = payload.get("message") or payload.get("content") or payload.get("text")
        if message and not payload.get("content"):
            payload = {"content": str(message)}

        if not payload.get("content"):
            return jsonify({"error": "Missing message content"}), 400

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
        except requests.RequestException:
            app.logger.exception("Failed to post to Discord webhook")
            return jsonify({"error": "Failed to reach Discord"}), 502

        if response.status_code >= 400:
            app.logger.error("Discord webhook error: %s", response.text)
            return jsonify({"error": "Discord rejected the message"}), 502

        return jsonify({"status": "sent"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8091")))

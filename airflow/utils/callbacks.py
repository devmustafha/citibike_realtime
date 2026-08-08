import os

import requests


def notify_telegram_failure(context) -> None:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Telegram notification skipped: credentials are not configured.")
        return

    task_instance = context["task_instance"]
    dag_run = context["dag_run"]
    exception = context.get("exception")

    message = (
        "🚨 <b>Airflow Task Failed</b>\n\n"
        f"<b>DAG:</b> {task_instance.dag_id}\n"
        f"<b>Task:</b> {task_instance.task_id}\n"
        f"<b>Run:</b> {dag_run.run_id}\n"
        f"<b>Execution:</b> {context['logical_date']}\n"
        f"<b>Try:</b> {task_instance.try_number}\n\n"
        f"<b>Error:</b>\n"
        f"<code>{exception}</code>\n\n"
        f"<b>Logs:</b> {task_instance.log_url}"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to send Telegram notification: {exc}")

import requests


def send_discord_message(
    webhook_url,
    message
):

    if not webhook_url:

        print(
            "Webhook Discord manquant."
        )

        return

    try:

        response = requests.post(
            webhook_url,
            json={
                "content":
                message
            },
            timeout=10
        )

        print(
            "Discord status:",
            response.status_code
        )

    except Exception as e:

        print(
            f"Discord error: {e}"
        )

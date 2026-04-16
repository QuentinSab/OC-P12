import sentry_sdk


def log_event(message, **data):
    sentry_sdk.capture_message(
        message,
        level="info",
        extras=data
    )

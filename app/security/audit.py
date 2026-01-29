import json
import logging
from flask import request
from flask_login import current_user


def log_event(
    action,
    resource=None,
    resource_id=None,
    success=True,
    authenticated=None,
    extra=None,
):
    logger = logging.getLogger("security.audit")

    # Determine authentication state
    if authenticated is None:
        authenticated = (
            current_user.is_authenticated
            if current_user
            else False
        )

    # Determine user id
    user_id = (
        current_user.id
        if authenticated and hasattr(current_user, "id")
        else None
    )

    event = {
        "action": action,
        "success": success,
        "authenticated": authenticated,
        "user_id": user_id,
        "resource": resource,
        "resource_id": resource_id,
        "ip_address": request.remote_addr if request else None,
        "user_agent": (
            request.user_agent.string
            if request and request.user_agent
            else None
        ),
    }

    # Merge in any extra fields
    if extra and isinstance(extra, dict):
        event.update(extra)

    logger.info(json.dumps(event))
    logger.info(event)

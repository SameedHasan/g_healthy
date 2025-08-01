from collections.abc import Callable
from functools import wraps

import frappe
from frappe import _


def rate_limit(
    key: str | None = None,
    limit: int | Callable = 5,
    seconds: int = 24 * 60 * 60,
    methods: str | list = "ALL",
    ip_based: bool = True,
):
    """Decorator to rate limit an endpoint.

    This will limit Number of requests per endpoint to `limit` within `seconds`.
    Uses redis cache to track request counts.

    :param key: Key is used to identify the requests uniqueness (Optional)
    :param limit: Maximum number of requests to allow with in window time
    :type limit: Callable or Integer
    :param seconds: window time to allow requests
    :param methods: Limit the validation for these methods.
            `ALL` is a wildcard that applies rate limit on all methods.
    :type methods: string or list or tuple
    :param ip_based: flag to allow ip based rate-limiting
    :type ip_based: Boolean

    :returns: a decorator function that limit the number of requests per endpoint
    """

    def ratelimit_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Do not apply rate limits if method is not opted to check
            if not frappe.request or (
                methods != "ALL"
                and frappe.request.method
                and frappe.request.method.upper() not in methods
            ):
                return fn(*args, **kwargs)

            _limit = limit() if callable(limit) else limit

            ip = frappe.local.request_ip if ip_based is True else None

            user_key = frappe.form_dict.get(key, "")

            identity = None

            if key and ip_based:
                identity = ":".join([ip, user_key])

            identity = identity or ip or user_key

            if not identity:
                frappe.throw(_("Either key or IP flag is required."))

            cache_key = frappe.cache.make_key(f"rl:{frappe.form_dict.cmd}:{identity}")

            value = frappe.cache.get(cache_key) or 0
            if not value:
                frappe.cache.setex(cache_key, seconds, 0)

            value = frappe.cache.incrby(cache_key, 1)
            if value > _limit:
                frappe.respond_as_web_page = False
                frappe.local.response.http_status_code = 429  # Too Many Requests
                frappe.local.response.message = (
                    "Rate limit exceeded. Please try again later."
                )
                return

            return fn(*args, **kwargs)

        return wrapper

    return ratelimit_decorator

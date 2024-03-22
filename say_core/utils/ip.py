from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.headers.get("Remote-Addr")
    return ip

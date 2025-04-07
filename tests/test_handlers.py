import pytest
from reports.handlers_report import HandlersReport


def test_handlers_report():
    log_lines = [
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]",
        "2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]",
        "2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: /admin/dashboard/ [192.168.1.29] - ValueError: Invalid input data"
    ]
    strategy = HandlersReport()
    result = strategy.process_log(log_lines)
    assert result['/api/v1/reviews/']['INFO'] == 1
    assert result['/admin/dashboard/']['INFO'] == 1
    assert result['/admin/dashboard/']['ERROR'] == 1

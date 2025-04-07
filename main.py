import sys
import os
from concurrent.futures import ThreadPoolExecutor
from reports.handlers_report import HandlersReport
from reports.base import ReportStrategy


def process_file(file_path: str, strategy: ReportStrategy) -> dict:
    """Обработка одного файла логов."""
    with open(file_path, 'r') as file:
        log_lines = file.readlines()
    return strategy.process_log(log_lines)


def main():
    # Парсинг аргументов командной строки
    if len(sys.argv) < 4 or '--report' not in sys.argv:
        print("Usage: python3 main.py <log_file1> ... --report <report_name>")
        sys.exit(1)

    try:
        report_index = sys.argv.index('--report')
        log_files = sys.argv[1:report_index]
        report_name = sys.argv[report_index + 1]
    except (ValueError, IndexError):
        print("Invalid arguments.")
        sys.exit(1)

    # Проверка существования файлов
    for file_path in log_files:
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            sys.exit(1)

    # Выбор стратегии формирования отчета
    if report_name == 'handlers':
        strategy = HandlersReport()
    else:
        print(f"Unknown report type: {report_name}")
        sys.exit(1)

    # Параллельная обработка файлов
    with ThreadPoolExecutor() as executor:
        results = list(
            executor.map(lambda file: process_file(file, strategy), log_files)
            )

    # Объединение результатов
    merged_data = strategy.merge_results(results)

    # Генерация отчета
    report = strategy.generate_report(merged_data)
    print(report)


if __name__ == "__main__":
    main()

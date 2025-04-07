from typing import Dict, List


class ReportStrategy:
    """Базовый класс для стратегий формирования отчетов."""
    def process_log(self, log_lines: List[str]) -> Dict:
        raise NotImplementedError

    def merge_results(self, results: List[Dict]) -> Dict:
        raise NotImplementedError

    def generate_report(self, data: Dict) -> str:
        raise NotImplementedError

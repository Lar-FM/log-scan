import re
from collections import defaultdict
from typing import Dict, List
from .base import ReportStrategy


class HandlersReport(ReportStrategy):
    LOG_PATTERN = re.compile(
        r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\s+'
        r'(?P<level>\w+)\s+django\.request:\s+'
        r'.+?\s+'
        r'(?P<handler>/[^\s]+).*'
    )

    def process_log(self, log_lines: List[str]) -> Dict:
        stats = defaultdict(lambda: defaultdict(int))
        for line in log_lines:
            match = self.LOG_PATTERN.search(line)
            if match:
                level = match.group('level')
                handler = match.group('handler')
                stats[handler][level] += 1
        return stats

    def merge_results(self, results: List[Dict]) -> Dict:
        merged = defaultdict(lambda: defaultdict(int))
        for result in results:
            for handler, levels in result.items():
                for level, count in levels.items():
                    merged[handler][level] += count
        return merged

    def generate_report(self, data: Dict) -> str:
        levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        total_requests = sum(sum(levels.values()) for levels in data.values())
        handlers = sorted(data.keys())

        header = (
            f"{'HANDLER':<25}" + "".join(f"{level:<10}" for level in levels)
            )
        rows = [header]

        for handler in handlers:
            row = f"{handler:<25}"
            for level in levels:
                row += f"{data[handler].get(level, 0):<10}"
            rows.append(row)

        totals = [""] * len(levels)
        for i, level in enumerate(levels):
            totals[i] = (
                sum(data[handler].get(level, 0) for handler in handlers)
                )
        totals_row = f"{'':<25}" + "".join(f"{total:<10}" for total in totals)
        rows.append(totals_row)

        report = "\n".join(rows)
        report = f"Total requests: {total_requests}\n\n" + report
        return report

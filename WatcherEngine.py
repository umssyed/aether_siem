import psutil
import os


class WatcherEngine:
    def __init__(self, process):
        self.process = process
        self.score = 0
        self.reasons = []

    def analyze(self):
        try:
            if self.high_cpu():
                self.score += 2
                self.reasons.append("High CPU usage")

        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

        return self.score, self.reasons

    def high_cpu(self):
        return self.process.cpu_percent(interval=0.1) > 4.0

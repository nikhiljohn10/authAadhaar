from datetime import datetime

from .data import User


class Collector:
    @staticmethod
    def get_ts() -> str:
        now = datetime.now()
        ts = now.strftime("%Y-%m-%dT%H:%M:%S")
        return ts

    def collect(self):
        self.user = User
        self.ts = self.get_ts()

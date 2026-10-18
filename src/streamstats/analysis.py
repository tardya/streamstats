class Stats:
    def __init__(self):
        self.total = 0
        self.levels = {}
        self.sources = {}
        self.err_src = {}
        self.first_ts = None
        self.last_ts = None
        self.skipped = 0
    def add_event(self, ev):
        self.total += 1

        if ev.level not in self.levels:
            self.levels[ev.level] = 0
        self.levels[ev.level] += 1

        if ev.source not in self.sources:
            self.sources[ev.source] = 0
        self.sources[ev.source] += 1

        if ev.level in ["ERROR", "CRITICAL"]:
            if ev.source not in self.err_src:
                self.err_src[ev.source] = 0
            self.err_src[ev.source] += 1

        if self.first_ts is None or ev.timestamp < self.first_ts:
            self.first_ts = ev.timestamp

        if self.last_ts is None or ev.timestamp > self.last_ts:
            self.last_ts = ev.timestamp

    def add_skipped(self):
        self.skipped += 1

    def get_top_errors(self):
        items = list(self.err_src.items())
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:5]
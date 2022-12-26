class Memento:
    def __init__(self, chart_filename: str):
        self._chart_filename = chart_filename

    def get_chart_filename(self) -> str:
        return self._chart_filename

        
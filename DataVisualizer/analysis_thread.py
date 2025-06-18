from PySide6.QtCore import QThread, Signal

class AnalysisThread(QThread):
    update_progress = Signal(int)
    update_status = Signal(str)
    analysis_complete = Signal(object)
    error_occurred = Signal(str)

    def __init__(self, file_path, options):
        super().__init__()
        self.file_path = file_path
        self.options = options

    def run(self):
        try:
            self.update_status.emit("Загрузка данных...")
            self.update_progress.emit(10)
            visualizer = UnifiedBrowserVisualizer(self.file_path)

            self.update_status.emit("Обработка данных...")
            self.update_progress.emit(30)
            visualizer.process_data(self.options)

            self.update_status.emit("Генерация отчета...")
            self.update_progress.emit(80)
            report_path = visualizer.generate_report()

            self.update_progress.emit(100)
            self.analysis_complete.emit(report_path)
        except Exception as e:
            self.error_occurred.emit(str(e))
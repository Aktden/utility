import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile
import webbrowser
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock

KV = '''
<CustomCheckBox>:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(60)
    spacing: dp(2)
    padding: [dp(5), 0]
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [6]

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(30)
        CheckBox:
            id: checkbox
            size_hint_x: None
            width: dp(30)
            active: root.active
            on_active: root.active = self.active
        Label:
            text: root.label_text
            font_size: '14sp'
            color: 0.1, 0.1, 0.1, 1
            bold: True
            halign: 'left'
            valign: 'middle'
            text_size: self.width, None

    Label:
        id: status_label
        text: ''
        font_size: '12sp'
        color: 0.5, 0.5, 0.5, 1
        halign: 'left'
        valign: 'middle'
        size_hint_y: None
        height: dp(20)
        markup: True

<OptionGroup@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    spacing: dp(5)
    padding: [dp(10), dp(5)]
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 0.8
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [6]

BoxLayout:
    orientation: 'vertical'
    padding: dp(15)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: 0.93, 0.96, 1, 1  # Светло-голубой фон Telegram
        Rectangle:
            pos: self.pos
            size: self.size

    # --- Заголовок ---
    Label:
        text: "Визуализатор данных"
        font_size: '24sp'
        bold: True
        color: 0.14, 0.51, 0.9, 1  # Telegram Blue
        size_hint_y: None
        height: dp(40)

    # --- Выбор файла ---
    BoxLayout:
        size_hint_y: None
        height: dp(60)
        spacing: dp(10)
        padding: [0, dp(5), dp(10), dp(5)]
        canvas.before:
            Color:
                rgba: 0.9, 0.9, 0.9, 0.8
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [6]
        Button:
            id: select_file_btn
            text: "Выбрать файл"
            size_hint_x: 0.4
            font_size: '16sp'
            bold: True
            background_color: 0.14, 0.51, 0.9, 1
            color: 1, 1, 1, 1
            on_press: app.choose_file()
            canvas.before:
                Color:
                    rgba: 0.1, 0.45, 0.85, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [6]
        Label:
            id: selected_file_label
            text: "Файл не выбран"
            font_size: '14sp'
            color: 0.14, 0.51, 0.9, 1
            halign: 'left'
            valign: 'middle'
            text_size: self.width, None
            shorten: True
            shorten_from: 'right'
            markup: True
        Button:
            id: clear_file_btn
            text: "×"
            size_hint_x: None
            width: dp(40)
            font_size: '20sp'
            bold: True
            background_color: 0.9, 0.2, 0.2, 1
            color: 1, 1, 1, 1
            on_press: app.clear_file_selection()
            canvas.before:
                Color:
                    rgba: 0.85, 0.15, 0.15, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [6]

    # --- Группы чекбоксов ---
    GridLayout:
        cols: 2
        size_hint_y: None
        height: dp(200)
        spacing: dp(10)
        padding: [0, dp(5)]
        OptionGroup:
            Label:
                text: "Основные графики"
                font_size: '16sp'
                bold: True
                color: 0.14, 0.51, 0.9, 1
                size_hint_y: None
                height: dp(30)
            CustomCheckBox:
                label_text: "Информация о данных"
                id: info_check
            CustomCheckBox:
                label_text: "Гистограммы"
                id: hist_check
            CustomCheckBox:
                label_text: "Boxplot"
                id: box_check
            CustomCheckBox:
                label_text: "Диаграмма рассеивания"
                id: scatter_check
        OptionGroup:
            size_hint_y: None
            height: dp(200)
            Label:
                text: "Дополнительно"
                font_size: '16sp'
                bold: True
                color: 0.14, 0.51, 0.9, 1
                size_hint_y: None
                height: dp(30)
            CustomCheckBox:
                label_text: "Матрица корреляций"
                id: corr_check
            CustomCheckBox:
                label_text: "Линейный график"
                id: line_check
            CustomCheckBox:
                label_text: "Круговая диаграмма"
                id: pie_check
            CustomCheckBox:
                label_text: "Все графики"
                id: all_check

  # --- Отступ перед кнопкой ---
    Widget:
        size_hint_y: None
        height: dp(90)

    # --- Кнопка запуска ---
    Button:
        text: "Сгенерировать отчет"
        size_hint_y: None
        height: dp(55)
        font_size: '18sp'
        bold: True
        background_color: 0.14, 0.51, 0.9, 1
        color: 1, 1, 1, 1
        on_press: app.run_analysis()
        canvas.before:
            Color:
                rgba: 0.1, 0.45, 0.85, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [6]

    # --- Лог программы ---
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.3
        spacing: dp(5)
        Label:
            text: "Лог выполнения:"
            font_size: '14sp'
            bold: True
            color: 0.14, 0.51, 0.9, 1
            size_hint_y: None
            height: dp(25)
        ScrollView:
            bar_width: dp(8)
            TextInput:
                id: log_output
                readonly: True
                font_size: '13sp'
                foreground_color: 0.1, 0.1, 0.1, 1
                background_color: 1, 1, 1, 1
                multiline: True
                text: ""
                padding: [dp(10), dp(10)]
                canvas.before:
                    Color:
                        rgba: 0.95, 0.95, 0.95, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [6]
'''


class CustomCheckBox(BoxLayout):
    label_text = StringProperty("")
    active = BooleanProperty(False)


class UnifiedBrowserVisualizer:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.figures = []
        self.load_data()

    def load_data(self):
        path = Path(self.file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл '{self.file_path}' не найден")
        if path.suffix == '.csv':
            self.data = pd.read_csv(path)
        elif path.suffix in ['.xlsx', '.xls']:
            self.data = pd.read_excel(path)
        else:
            raise ValueError("Неподдерживаемый формат файла. Используйте CSV или Excel.")

    def add_data_info(self):
        try:
            info_df = pd.DataFrame({
                'Столбец': self.data.columns,
                'Тип': self.data.dtypes.astype(str),
                'Пропуски': self.data.isna().sum(),
                'Уникальные значения': self.data.nunique()
            })
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(info_df.columns)),
                cells=dict(values=[info_df[col] for col in info_df.columns])
            )])
            fig.update_layout(title="Структура данных")
            self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка информации о данных: {str(e)}")

    def add_histogram(self, column, bins=10):
        try:
            fig = px.histogram(self.data, x=column, nbins=bins, title=f'Гистограмма: {column}', marginal='box')
            self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка гистограммы: {str(e)}")

    def add_boxplot(self, column):
        try:
            fig = px.box(self.data, y=column, title=f'Boxplot: {column}')
            self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка boxplot: {str(e)}")

    def add_line_chart(self):
        try:
            numeric_cols = self.data.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 1:
                fig = px.line(self.data, y=numeric_cols[0], title=f'Линейный график: {numeric_cols[0]}')
                self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка линейного графика: {str(e)}")

    def add_scatter(self, x_col, y_col):
        try:
            fig = px.scatter(self.data, x=x_col, y=y_col, title=f'Диаграмма рассеивания: {x_col} vs {y_col}')
            self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка scatter plot: {str(e)}")

    def add_correlation_matrix(self):
        try:
            numeric_cols = self.data.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 2:
                corr = self.data.corr(numeric_only=True)
                fig = go.Figure(data=go.Heatmap(
                    z=corr.values, x=corr.columns, y=corr.columns,
                    colorscale='RdBu', zmin=-1, zmax=1
                ))
                fig.update_layout(title="Матрица корреляций")
                self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка матрицы корреляций: {str(e)}")

    def generate_report(self):
        if not self.figures:
            raise ValueError("Нет данных для отчета. Сначала добавьте визуализации.")
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head><meta charset="UTF-8"><title>Отчет</title></head>
        <body style="font-family: Arial; margin: 40px;">
        <h1>Отчет анализа данных</h1>
        <p>Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Источник данных: {self.file_path}</p>
        <hr>
        """
        for i, fig in enumerate(self.figures, 1):
            plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
            html_content += plot_html
            if i < len(self.figures):
                html_content += "<hr>"
        html_content += """
        </body></html>
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        webbrowser.open(f"file://{temp_path}")
        return temp_path


class VisualizerApp(App):

    def update_checkbox_status(self):
        if not self.current_file:
            for cb in [
                self.root.ids.info_check,
                self.root.ids.hist_check,
                self.root.ids.box_check,
                self.root.ids.scatter_check,
                self.root.ids.corr_check,
                self.root.ids.line_check
            ]:
                cb.ids.status_label.text = '[color=999999]Файл не выбран[/color]'
            return

        try:
            data = pd.read_csv(self.current_file) if self.current_file.endswith('.csv') else pd.read_excel(
                self.current_file)
            numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
            has_numeric = len(numeric_cols) >= 1
            has_two_numeric = len(numeric_cols) >= 2

            # Информация о данных всегда доступна
            self.root.ids.info_check.ids.status_label.text = '[color=2ecc71]Доступно[/color]'

            # Гистограммы и boxplot требуют числовых данных
            if has_numeric:
                self.root.ids.hist_check.ids.status_label.text = '[color=2ecc71]Доступно[/color]'
                self.root.ids.box_check.ids.status_label.text = '[color=2ecc71]Доступно[/color]'
            else:
                self.root.ids.hist_check.ids.status_label.text = '[color=e74c3c]Нет числовых данных[/color]'
                self.root.ids.box_check.ids.status_label.text = '[color=e74c3c]Нет числовых данных[/color]'

            # Диаграмма рассеивания и корреляция требуют минимум 2 числовых столбца
            if has_two_numeric:
                self.root.ids.scatter_check.ids.status_label.text = '[color=2ecc71]Доступно[/color]'
                self.root.ids.corr_check.ids.status_label.text = '[color=2ecc71]Доступно[/color]'
            else:
                self.root.ids.scatter_check.ids.status_label.text = '[color=e74c3c]Нужно 2 числовых столбца[/color]'
                self.root.ids.corr_check.ids.status_label.text = '[color=e74c3c]Нужно 2 числовых столбца[/color]'

            # Линейный график — хотя бы один числовой
            if has_numeric:
                self.root.ids.line_check.ids.status_label.text = '[color=2ecc71]Доступно[/color]'
            else:
                self.root.ids.line_check.ids.status_label.text = '[color=e74c3c]Нет числовых данных[/color]'

        except Exception as e:
            print(f"Ошибка проверки данных: {str(e)}")
            for cb in [
                self.root.ids.info_check,
                self.root.ids.hist_check,
                self.root.ids.box_check,
                self.root.ids.scatter_check,
                self.root.ids.corr_check,
                self.root.ids.line_check
            ]:
                cb.ids.status_label.text = '[color=e74c3c]Ошибка проверки[/color]'

    def build(self):
        self.title = "Визуализатор данных"
        Window.clearcolor = (0.97, 0.97, 0.97, 1)
        Window.minimum_width = 800
        Window.minimum_height = 600
        self.current_file = None
        return Builder.load_string(KV)

    def choose_file(self):
        Tk().withdraw()
        filename = askopenfilename(
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.current_file = filename
            file_name = os.path.basename(filename)
            self.root.ids.selected_file_label.text = f"[color=1a73e8][b]{file_name}[/b][/color]"
            self.log(f"Выбран файл: {filename}")
            self.update_checkbox_status()  # ← новый вызов

    def clear_file_selection(self):
        self.current_file = None
        self.root.ids.selected_file_label.text = "Файл не выбран"
        self.log("Выбор файла сброшен")
        self.update_checkbox_status()

    def run_analysis(self):
        if not self.current_file:
            self.log("❌ Ошибка: Файл не выбран!")
            return

        self.log("🔍 Начинаем анализ данных...")
        try:
            visualizer = UnifiedBrowserVisualizer(self.current_file)
            self.log(f"✅ Загружено: {len(visualizer.data)} строк, {len(visualizer.data.columns)} столбцов")

            # Обработка чекбоксов
            if self.root.ids.all_check.active or self.root.ids.info_check.active:
                visualizer.add_data_info()
                self.log("Добавлена информация о данных")

            numeric_cols = visualizer.data.select_dtypes(include=['number']).columns

            if self.root.ids.all_check.active or self.root.ids.hist_check.active:
                if len(numeric_cols) > 0:
                    for col in numeric_cols[:3]:
                        visualizer.add_histogram(col)
                    self.log("Добавлены гистограммы")

            if self.root.ids.all_check.active or self.root.ids.box_check.active:
                if len(numeric_cols) > 0:
                    for col in numeric_cols[:3]:
                        visualizer.add_boxplot(col)
                    self.log("Добавлены boxplot")

            if self.root.ids.all_check.active or self.root.ids.scatter_check.active:
                if len(numeric_cols) >= 2:
                    visualizer.add_scatter(numeric_cols[0], numeric_cols[1])
                    self.log("Добавлена диаграмма рассеивания")

            if self.root.ids.all_check.active or self.root.ids.corr_check.active:
                if len(numeric_cols) >= 2:
                    visualizer.add_correlation_matrix()
                    self.log("Добавлена матрица корреляций")

            if self.root.ids.all_check.active or self.root.ids.line_check.active:
                if len(numeric_cols) >= 1:
                    visualizer.add_line_chart()
                    self.log("Добавлен линейный график")

            report_path = visualizer.generate_report()
            self.log(f"✅ Отчет успешно сгенерирован")
            self.log(f"📄 Открыт в браузере: {report_path}")

        except Exception as e:
            self.log(f"❌ Критическая ошибка: {str(e)}")

    def log(self, message):
        log_box = self.root.ids.log_output
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_box.text += f"\n[{timestamp}] {message}"
        # Автопрокрутка вниз
        Clock.schedule_once(lambda dt: setattr(log_box, 'cursor', (0, len(log_box.text))))


if __name__ == "__main__":
    VisualizerApp().run()
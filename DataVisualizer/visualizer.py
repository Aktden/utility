import base64
import io
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
            with open(path, 'r', encoding='utf-8') as f:
                first_lines = [next(f) for _ in range(100)]

            try:
                self.data = pd.read_csv(path, low_memory=False)
            except:
                self.data = pd.read_csv(path, header=None, low_memory=False)

        elif path.suffix in ['.xlsx', '.xls']:
            self.data = pd.read_excel(path)
        else:
            raise ValueError("Неподдерживаемый формат файла. Используйте CSV или Excel.")

        self.optimize_memory()

    def optimize_memory(self):
        if self.data is not None:
            for col in self.data.select_dtypes(include=['object']):
                if self.data[col].nunique() / len(self.data) < 0.5:
                    self.data[col] = self.data[col].astype('category')

            for col in self.data.select_dtypes(include=['int']):
                c_min = self.data[col].min()
                c_max = self.data[col].max()
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    self.data[col] = self.data[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    self.data[col] = self.data[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    self.data[col] = self.data[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    self.data[col] = self.data[col].astype(np.int64)

            for col in self.data.select_dtypes(include=['float']):
                self.data[col] = pd.to_numeric(self.data[col], downcast='float')

    def process_data(self, options):
        if options.get("data_info", False):
            self.add_data_info()

        numeric_cols = self.data.select_dtypes(include=['number']).columns.tolist()
        category_cols = self.data.select_dtypes(include=['category', 'object']).columns.tolist()

        if options.get("histograms", False) and numeric_cols:
            for col in numeric_cols[:3]:
                self.add_histogram(col)

        if options.get("boxplot", False) and numeric_cols:
            for col in numeric_cols[:3]:
                self.add_boxplot(col)

        if options.get("scatter", False) and len(numeric_cols) >= 2:
            self.add_scatter(numeric_cols[0], numeric_cols[1])

        if options.get("correlation", False) and len(numeric_cols) >= 2:
            self.add_correlation_matrix()

        if options.get("line_chart", False) and numeric_cols:
            self.add_line_chart()

        if options.get("bar_chart", False) and numeric_cols and category_cols:
            self.add_bar_chart()

        if options.get("pie_chart", False) and category_cols:
            self.add_pie_chart()

        if options.get("violin_plot", False) and numeric_cols and category_cols:
            self.add_violin_plot()

        if options.get("scatter_matrix", False) and len(numeric_cols) >= 2:
            self.add_scatter_matrix()

    def add_boxplot(self, column):
        """Добавляет диаграмму размаха для указанного столбца"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))

            # Создаем boxplot с настройками стиля
            boxprops = dict(facecolor='lightblue', color='blue')
            whiskerprops = dict(color='black', linestyle='-')
            medianprops = dict(color='red', linewidth=2)

            ax.boxplot(self.data[column].dropna(),
                       patch_artist=True,
                       boxprops=boxprops,
                       whiskerprops=whiskerprops,
                       medianprops=medianprops,
                       capprops=dict(color='black'))

            # Настройки оформления
            ax.set_title(f'Диаграмма размаха: {column}', pad=20)
            ax.set_ylabel(column, labelpad=10)
            ax.grid(True, linestyle='--', alpha=0.5)

            plt.tight_layout()
            self.figures.append(fig)

        except Exception as e:
            print(f"Ошибка при создании диаграммы размаха: {str(e)}")

    def add_scatter(self, x_col, y_col):
        """Добавляет диаграмму рассеивания"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))

            # Создаем scatter plot с настройками
            ax.scatter(self.data[x_col],
                       self.data[y_col],
                       color='green',
                       alpha=0.6,
                       edgecolor='w')

            # Настройки оформления
            ax.set_title(f'Диаграмма рассеивания: {x_col} vs {y_col}', pad=20)
            ax.set_xlabel(x_col, labelpad=10)
            ax.set_ylabel(y_col, labelpad=10)
            ax.grid(True, linestyle='--', alpha=0.5)

            plt.tight_layout()
            self.figures.append(fig)

        except Exception as e:
            print(f"Ошибка при создании диаграммы рассеивания: {str(e)}")

    def add_line_chart(self):
        """Добавляет линейный график"""
        try:
            numeric_cols = self.data.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 1:
                fig, ax = plt.subplots(figsize=(10, 6))

                # Создаем линейный график
                ax.plot(self.data[numeric_cols[0]],
                        color='blue',
                        linewidth=2,
                        marker='o',
                        markersize=4)

                # Настройки оформления
                ax.set_title(f'Линейный график: {numeric_cols[0]}', pad=20)
                ax.set_xlabel('Индекс', labelpad=10)
                ax.set_ylabel(numeric_cols[0], labelpad=10)
                ax.grid(True, linestyle='--', alpha=0.5)

                plt.tight_layout()
                self.figures.append(fig)

        except Exception as e:
            print(f"Ошибка при создании линейного графика: {str(e)}")

    def add_histogram(self, column, bins=10):
        """Добавляет гистограмму для указанного столбца"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(self.data[column].dropna(), bins=bins, color='skyblue', edgecolor='black')
            ax.set_title(f'Гистограмма: {column}')
            ax.set_xlabel(column)
            ax.set_ylabel('Частота')
            ax.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка при создании гистограммы: {str(e)}")

    def add_data_info(self):
        try:
            info_df = pd.DataFrame({
                'Столбец': self.data.columns,
                'Тип': self.data.dtypes.astype(str),
                'Пропуски': self.data.isna().sum(),
                'Уникальные значения': self.data.nunique()
            })

            numeric_stats = self.data.describe().transpose()
            info_df = info_df.join(numeric_stats, on='Столбец', how='left')
            info_df = info_df.sort_values(by=['Пропуски', 'Уникальные значения'], ascending=[False, True])

            # Динамический размер фигуры в зависимости от количества столбцов и строк
            fig_width = 12 + len(info_df.columns) * 0.5
            fig_height = 4 + len(info_df) * 0.3
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))

            ax.axis('off')

            # Создаем таблицу с автоматическим переносом текста
            table = ax.table(
                cellText=info_df.values,
                colLabels=info_df.columns,
                loc='center',
                cellLoc='center',
                colWidths=[0.15] * len(info_df.columns),
                bbox=[0, 0, 1, 1]  # Растягиваем таблицу на всю фигуру
            )

            # Настройки шрифта
            table.auto_set_font_size(False)
            table.set_fontsize(10)

            # Автоматический перенос текста в ячейках
            for key, cell in table.get_celld().items():
                cell.set_text_props(wrap=True)

            plt.tight_layout()
            self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка информации о данных: {str(e)}")

    def add_bar_chart(self):
        try:
            numeric_cols = self.data.select_dtypes(include=['number']).columns
            category_cols = self.data.select_dtypes(include=['category', 'object']).columns

            if len(numeric_cols) >= 1 and len(category_cols) >= 1:
                col_num = numeric_cols[0]
                col_cat = category_cols[0]
                grouped = self.data.groupby(col_cat)[col_num].mean().reset_index()

                # Динамический размер фигуры в зависимости от количества категорий
                fig, ax = plt.subplots(figsize=(10 + len(grouped) * 0.2, 6))
                bars = ax.bar(grouped[col_cat], grouped[col_num], color='teal')

                # Добавляем значения на столбцы
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                            f'{height:.2f}',
                            ha='center', va='bottom', fontsize=10)

                ax.set_title(f'Столбчатая диаграмма: {col_num} по {col_cat}', pad=20)
                ax.set_xlabel(col_cat, labelpad=10)
                ax.set_ylabel(f'Среднее {col_num}', labelpad=10)
                ax.grid(True, linestyle='--', alpha=0.7)

                # Автоматический поворот подписей и регулировка отступов
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка столбчатой диаграммы: {str(e)}")

    def add_pie_chart(self):
        try:
            category_cols = self.data.select_dtypes(include=['category', 'object']).columns
            if len(category_cols) >= 1:
                col = category_cols[0]
                counts = self.data[col].value_counts()

                # Ограничиваем количество секторов для читаемости
                if len(counts) > 10:
                    others = counts[10:].sum()
                    counts = counts[:10]
                    counts['Другие'] = others

                # Автоматическое вынесение подписей наружу при большом количестве секторов
                if len(counts) > 5:
                    pctdistance = 0.85
                    labeldistance = 1.1
                else:
                    pctdistance = 0.6
                    labeldistance = 1.1

                fig, ax = plt.subplots(figsize=(10, 8))
                wedges, texts, autotexts = ax.pie(
                    counts,
                    labels=counts.index,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=plt.cm.Paired.colors,
                    pctdistance=pctdistance,
                    labeldistance=labeldistance,
                    textprops={'fontsize': 10})

                # Улучшаем читаемость подписей
                for text in texts + autotexts:
                    text.set_fontsize(10)

                ax.set_title(f'Круговая диаграмма: {col}', pad=20)
                ax.axis('equal')
                plt.tight_layout()
                self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка круговой диаграммы: {str(e)}")

    def add_violin_plot(self):
        try:
            numeric_cols = self.data.select_dtypes(include=['number']).columns
            category_cols = self.data.select_dtypes(include=['category', 'object']).columns

            if len(numeric_cols) >= 1 and len(category_cols) >= 1:
                num_col = numeric_cols[0]
                cat_col = category_cols[0]

                # Ограничиваем количество категорий для читаемости
                unique_cats = self.data[cat_col].unique()
                if len(unique_cats) > 10:
                    unique_cats = unique_cats[:10]

                data_to_plot = [self.data[self.data[cat_col] == cat][num_col].dropna()
                                for cat in unique_cats]

                # Динамический размер фигуры
                fig, ax = plt.subplots(figsize=(8 + len(unique_cats), 6))
                parts = ax.violinplot(data_to_plot, showmeans=True, showmedians=True)

                # Настройка цветов
                for pc in parts['bodies']:
                    pc.set_facecolor('skyblue')
                    pc.set_edgecolor('black')
                    pc.set_alpha(0.7)

                ax.set_title(f'Диаграмма скрипки: {num_col}', pad=20)
                ax.set_xticks(range(1, len(unique_cats) + 1))
                ax.set_xticklabels(unique_cats, rotation=45, ha='right')
                ax.set_ylabel(num_col, labelpad=10)
                ax.grid(True, linestyle='--', alpha=0.7)

                plt.tight_layout()
                self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка диаграммы скрипки: {str(e)}")

    def add_scatter_matrix(self):
        try:
            numeric_cols = self.data.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 2:
                cols = numeric_cols[:4]  # Ограничиваем количество столбцов

                # Создаем сетку графиков вручную
                n = len(cols)
                fig, axes = plt.subplots(n, n, figsize=(12, 12))

                for i in range(n):
                    for j in range(n):
                        ax = axes[i, j]
                        if i == j:
                            # Диагональ - гистограммы
                            ax.hist(self.data[cols[i]], color='skyblue', edgecolor='black')
                        else:
                            # Остальные - scatter plots
                            ax.scatter(self.data[cols[j]], self.data[cols[i]],
                                       alpha=0.5, s=20, edgecolor='none')

                        # Настройка подписей
                        if i == n - 1:
                            ax.set_xlabel(cols[j], fontsize=8)
                        if j == 0:
                            ax.set_ylabel(cols[i], fontsize=8)

                        ax.tick_params(labelsize=6)

                plt.suptitle("Матрица диаграмм рассеивания", y=0.95, fontsize=12)
                plt.tight_layout()
                self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка при создании матрицы диаграмм рассеивания: {str(e)}")

    def add_correlation_matrix(self):
        try:
            numeric_cols = self.data.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 2:
                corr = self.data[numeric_cols].corr(numeric_only=True)

                # Динамический размер фигуры
                fig_size = 6 + len(corr.columns) * 0.8
                fig, ax = plt.subplots(figsize=(fig_size, fig_size))

                # Тепловая карта корреляции
                cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
                fig.colorbar(cax, shrink=0.8)

                # Настройка подписей
                ax.set_xticks(range(len(corr.columns)))
                ax.set_yticks(range(len(corr.columns)))
                ax.set_xticklabels(
                    corr.columns,
                    rotation=45,
                    ha='left',
                    fontsize=10)
                ax.set_yticklabels(
                    corr.columns,
                    fontsize=10)

                # Добавление значений корреляции
                for i in range(len(corr.columns)):
                    for j in range(len(corr.columns)):
                        ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                                ha='center', va='center',
                                color='white' if abs(corr.iloc[i, j]) > 0.5 else 'black',
                                fontsize=8)

                ax.set_title("Матрица корреляций", pad=20)
                plt.tight_layout()
                self.figures.append(fig)
        except Exception as e:
            print(f"Ошибка матрицы корреляций: {str(e)}")

    def figure_to_html_img(self, fig):
        """Конвертирует matplotlib figure в base64 для вставки в HTML с улучшенным качеством"""
        buf = io.BytesIO()

        # Увеличиваем DPI и качество сохранения
        fig.savefig(buf,
                    format='png',
                    bbox_inches='tight',
                    dpi=150,  # Высокое качество
                    pad_inches=0.5)  # Добавляем отступы

        plt.close(fig)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return f'<img src="data:image/png;base64,{img_str}" style="max-width:100%; height:auto;">'

    def generate_report(self):
        if not self.figures:
            raise ValueError("Невозможно сгенерировать отчет: не создано ни одной визуализации. "
                             "Проверьте, что выбранные типы графиков поддерживаются для ваших данных.")

        html_content = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Отчет анализа данных</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    line-height: 1.6;
                }}
                h1, h2 {{
                    color: #2b5278;
                    margin-bottom: 15px;
                }}
                .report-header {{
                    background-color: #f5f5f5;
                    padding: 20px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .plot-container {{
                    margin: 30px 0;
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    overflow-x: auto;  # Добавляем горизонтальную прокрутку при необходимости
                }}
                .plot-title {{
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    color: #2b5278;
                    word-wrap: break-word;  # Перенос длинных названий
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 10px auto;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                    word-wrap: break-word;  # Перенос текста в таблицах
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="report-header">
                <h1>Отчет анализа данных</h1>
                <p><strong>Сгенерировано:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Источник данных:</strong> {self.file_path}</p>
                <p><strong>Размер данных:</strong> {len(self.data)} строк, {len(self.data.columns)} столбцов</p>
                <p><strong>Использовано памяти:</strong> {self.data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB</p>
            </div>
        """

        for i, fig in enumerate(self.figures, 1):
            plot_html = self.figure_to_html_img(fig)

            # Получаем заголовок графика
            title = ""
            if fig._suptitle is not None:
                title = fig._suptitle.get_text()
            elif len(fig.axes) > 0 and fig.axes[0].get_title() != "":
                title = fig.axes[0].get_title()
            else:
                title = f"График {i}"

            html_content += f"""
            <div class="plot-container">
                <div class="plot-title">{title}</div>
                {plot_html}
            </div>
            """
            if i < len(self.figures):
                html_content += "<hr>"

        html_content += """
        </body>
        </html>
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name

        webbrowser.open(f"file://{temp_path}")
        return temp_path
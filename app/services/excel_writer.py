from openpyxl import Workbook

def create_excel_report(stats: dict, output_path: str):
    wb = Workbook()
    ws = wb.active
    ws.title = "Статистика слов"

    ws.append(["Словоформа", "Всего", "По строкам"])

    for word, total in stats["total"].items():
        line_str = ",".join(map(str, stats["per_line"][word]))
        ws.append([word, total, line_str])
    wb.save(output_path)
import openpyxl
from goods.models import Variation

def update_stock_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        sku = row[0]  # SKU
        quantity = row[6]  # Остаток

        try:
            variation = Variation.objects.get(sku=sku)
            variation.quantity = quantity
            variation.save()
            print(f'✅ Остаток для {sku} обновлён на {quantity}')
        except Variation.DoesNotExist:
            print(f'⚠️ Вариация с SKU {sku} не найдена.')

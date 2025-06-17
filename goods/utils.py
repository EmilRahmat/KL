import openpyxl
from goods.models import Variation, ProcessedReceipt
from django.db import transaction

# Обновление по остаткам (старый способ)
def update_stock_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        sku = row[0]
        quantity = row[6]

        try:
            variation = Variation.objects.get(sku=sku)
            variation.quantity = quantity
            variation.save()
            print(f'✅ Остаток для {sku} обновлён на {quantity}')
        except Variation.DoesNotExist:
            print(f'⚠️ Вариация с SKU {sku} не найдена.')


# Обновление по чекам (новый способ)
def update_stock_by_receipts(file_path):
    

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    receipt_id = None
    items_to_process = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        col_2 = str(row[2]).strip() if row[2] else ""
        sku = str(row[10]).strip() if row[10] else ""
        qty = row[12]

        if col_2.startswith("Чек"):
            # Обработка предыдущего чека
            if receipt_id and items_to_process:
                if ProcessedReceipt.objects.filter(receipt_id=receipt_id).exists():
                    print(f'🔁 Чек {receipt_id} уже обработан — пропускаем.')
                else:
                    try:
                        with transaction.atomic():
                            for sku_val, qty_val in items_to_process:
                                try:
                                    variation = Variation.objects.get(sku=sku_val)
                                    variation.quantity = max(0, variation.quantity - int(qty_val))
                                    variation.save()
                                    print(f'🛒 {qty_val} списано из {sku_val}, осталось {variation.quantity}')
                                except Variation.DoesNotExist:
                                    print(f'❌ Вариация с SKU {sku_val} не найдена.')
                            ProcessedReceipt.objects.create(receipt_id=receipt_id)
                    except Exception as e:
                        print(f'⚠️ Ошибка при обработке чека {receipt_id}: {e}')

            # Начинаем новый чек
            receipt_id = col_2
            items_to_process = []

        elif receipt_id and sku and qty:
            items_to_process.append((sku, qty))

    # Обработка последнего чека (если есть)
    if receipt_id and items_to_process:
        if not ProcessedReceipt.objects.filter(receipt_id=receipt_id).exists():
            try:
                with transaction.atomic():
                    for sku_val, qty_val in items_to_process:
                        try:
                            variation = Variation.objects.get(sku=sku_val)
                            variation.quantity = max(0, variation.quantity - int(qty_val))
                            variation.save()
                            print(f'🛒 {qty_val} списано из {sku_val}, осталось {variation.quantity}')
                        except Variation.DoesNotExist:
                            print(f'❌ Вариация с SKU {sku_val} не найдена.')
                    ProcessedReceipt.objects.create(receipt_id=receipt_id)
            except Exception as e:
                print(f'⚠️ Ошибка при обработке последнего чека {receipt_id}: {e}')
        else:
            print(f'🔁 Последний чек {receipt_id} уже обработан — пропускаем.')


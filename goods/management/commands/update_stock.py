from django.core.management.base import BaseCommand
from goods.utils import update_stock_from_excel  # ты уже сделал эту функцию

class Command(BaseCommand):
    help = 'Обновляет остатки товаров из Excel'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\emill\Desktop\PTH Учусь\Дайбог создам сайт)\data.xlsx'
        update_stock_from_excel(file_path)
        self.stdout.write(self.style.SUCCESS('✅ Остатки успешно обновлены из Excel'))
from django.core.management.base import BaseCommand, CommandError
from ... models import Post, Category


class Command(BaseCommand, CommandError):
    help = 'Удаление всех новостей определённой катеории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no: ')

        if answer != 'yes':     # в случае неправильного подтверждения говорим, что в доступе отказано
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(nameCategory=options['category'])
            Post.objects.filter(categoryPost=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалены все новости из категории {category.nameCategory}'))

        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию'))

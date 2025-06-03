from django.core.management.base import BaseCommand
from main.models import Employee
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Update all employees photos with default avatar'

    def handle(self, *args, **kwargs):
        # Путь к дефолтной аватарке
        default_avatar_path = os.path.join(settings.BASE_DIR, 'pharmacy', 'static', 'img', 'default-avatar.png')
        if not os.path.exists(default_avatar_path):
            # Попробуем альтернативный путь
            default_avatar_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'default-avatar.png')
            if not os.path.exists(default_avatar_path):
                self.stdout.write(self.style.ERROR(f'Default avatar not found at {default_avatar_path}'))
                return

        # Создаем директорию для фотографий сотрудников, если её нет
        employees_media_dir = os.path.join(settings.MEDIA_ROOT, 'employees')
        os.makedirs(employees_media_dir, exist_ok=True)

        # Обновляем фото для каждого сотрудника
        employees = Employee.objects.all()
        for employee in employees:
            # Формируем имя файла для нового аватара
            new_avatar_name = f'default-avatar-{employee.user.username}.png'
            new_avatar_path = os.path.join(employees_media_dir, new_avatar_name)

            # Копируем дефолтную аватарку
            with open(default_avatar_path, 'rb') as source_file:
                with open(new_avatar_path, 'wb') as dest_file:
                    dest_file.write(source_file.read())

            # Обновляем поле photo у сотрудника
            with open(new_avatar_path, 'rb') as avatar_file:
                employee.photo.save(
                    new_avatar_name,
                    File(avatar_file),
                    save=True
                )

            self.stdout.write(
                self.style.SUCCESS(f'Updated photo for employee: {employee.user.get_full_name()}')
            ) 
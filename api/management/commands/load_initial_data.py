from django.core.management.base import BaseCommand
from api.models import Status, Task


class Command(BaseCommand):
    help = 'Load initial data for Status and Task models'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...')

        # Create Status records
        status_data = [
            {'name': 'Por Hacer', 'hexa_color': '#6B7280'},
            {'name': 'En Progreso', 'hexa_color': '#3B82F6'},
            {'name': 'Completado', 'hexa_color': '#10B981'},
            {'name': 'Bloqueado', 'hexa_color': '#EF4444'},
        ]

        statuses = {}
        for status_info in status_data:
            status, created = Status.objects.get_or_create(
                name=status_info['name'],
                defaults={'hexa_color': status_info['hexa_color']}
            )
            statuses[status_info['name']] = status
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Status created: {status.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'- Status already exists: {status.name}'))

        # Create Task records
        task_data = [
            {'name': 'Crear función de suma', 'content': 'Implementar una función que sume dos números', 'status': 'Por Hacer'},
            {'name': 'Implementar bucle for', 'content': 'Crear un bucle for que itere sobre una lista de elementos', 'status': 'Por Hacer'},
            {'name': 'Declarar variables', 'content': 'Declarar variables de diferentes tipos: string, int, float y boolean', 'status': 'En Progreso'},
            {'name': 'Crear clase Usuario', 'content': 'Definir una clase Usuario con atributos nombre, email y edad', 'status': 'En Progreso'},
            {'name': 'Escribir comentarios en código', 'content': 'Agregar comentarios descriptivos a las funciones principales', 'status': 'Completado'},
            {'name': 'Hacer commit en git', 'content': 'Realizar un commit con los cambios recientes en el repositorio', 'status': 'Completado'},
            {'name': 'Revisar pull request', 'content': 'Revisar y aprobar el PR #123 del compañero de equipo', 'status': 'Por Hacer'},
            {'name': 'Actualizar dependencias', 'content': 'Actualizar las dependencias del proyecto a sus últimas versiones', 'status': 'Bloqueado'},
            {'name': 'Corregir error de sintaxis', 'content': 'Corregir el error de sintaxis en el archivo main.py línea 45', 'status': 'En Progreso'},
            {'name': 'Agregar validación de datos', 'content': 'Implementar validación de entrada de datos en el formulario de registro', 'status': 'Por Hacer'},
        ]

        tasks_created = 0
        tasks_existing = 0

        for task_info in task_data:
            status = statuses[task_info['status']]
            task, created = Task.objects.get_or_create(
                name=task_info['name'],
                defaults={
                    'content': task_info['content'],
                    'status': status
                }
            )
            if created:
                tasks_created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Task created: {task.name}'))
            else:
                tasks_existing += 1
                self.stdout.write(self.style.WARNING(f'- Task already exists: {task.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Statuses: {len(statuses)} total'))
        self.stdout.write(self.style.SUCCESS(f'Tasks: {tasks_created} created, {tasks_existing} already existed'))
        self.stdout.write(self.style.SUCCESS(f'Initial data loaded successfully!'))

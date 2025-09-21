from django.core.management.base import BaseCommand
from salon.models import ColorPalette


class Command(BaseCommand):
    help = 'Populate predefined color palettes'

    def handle(self, *args, **options):
        # Default Pink Theme (Current)
        default_palette, created = ColorPalette.objects.get_or_create(
            name='default',
            defaults={
                'display_name': 'Default Pink Theme',
                'is_active': True,
                'primary_color': '#e91e63',
                'primary_light': '#f8bbd9',
                'primary_dark': '#c2185b',
                'secondary_color': '#ff4081',
                'accent_color': '#f50057',
                'text_dark': '#2c2c2c',
                'text_medium': '#4a4a4a',
                'text_light': '#6b6b6b',
                'text_muted': '#9b9b9b',
                'bg_white': '#ffffff',
                'bg_light': '#f8f9fa',
                'bg_cream': '#fefcf9',
                'border_light': '#e8e8e8',
                'border_medium': '#d0d0d0',
            }
        )

        # Dark Theme
        dark_palette, created = ColorPalette.objects.get_or_create(
            name='dark',
            defaults={
                'display_name': 'Dark Theme',
                'is_active': True,
                'primary_color': '#bb86fc',
                'primary_light': '#d1c4e9',
                'primary_dark': '#7c4dff',
                'secondary_color': '#03dac6',
                'accent_color': '#ff6b6b',
                'text_dark': '#ffffff',
                'text_medium': '#e0e0e0',
                'text_light': '#b0b0b0',
                'text_muted': '#808080',
                'bg_white': '#121212',
                'bg_light': '#1e1e1e',
                'bg_cream': '#2c2c2c',
                'border_light': '#333333',
                'border_medium': '#404040',
            }
        )

        # Blue Theme
        blue_palette, created = ColorPalette.objects.get_or_create(
            name='blue',
            defaults={
                'display_name': 'Blue Theme',
                'is_active': True,
                'primary_color': '#2196f3',
                'primary_light': '#bbdefb',
                'primary_dark': '#1976d2',
                'secondary_color': '#03a9f4',
                'accent_color': '#00bcd4',
                'text_dark': '#1a237e',
                'text_medium': '#283593',
                'text_light': '#3949ab',
                'text_muted': '#5c6bc0',
                'bg_white': '#ffffff',
                'bg_light': '#f3f8ff',
                'bg_cream': '#e8f4fd',
                'border_light': '#e3f2fd',
                'border_medium': '#bbdefb',
            }
        )

        # Yellow Theme
        yellow_palette, created = ColorPalette.objects.get_or_create(
            name='yellow',
            defaults={
                'display_name': 'Yellow Theme',
                'is_active': True,
                'primary_color': '#ffc107',
                'primary_light': '#fff9c4',
                'primary_dark': '#f57f17',
                'secondary_color': '#ffeb3b',
                'accent_color': '#ff9800',
                'text_dark': '#3e2723',
                'text_medium': '#5d4037',
                'text_light': '#795548',
                'text_muted': '#8d6e63',
                'bg_white': '#ffffff',
                'bg_light': '#fffef7',
                'bg_cream': '#fffde7',
                'border_light': '#fff8e1',
                'border_medium': '#ffecb3',
            }
        )

        # Light Red Theme
        light_red_palette, created = ColorPalette.objects.get_or_create(
            name='light_red',
            defaults={
                'display_name': 'Light Red Theme',
                'is_active': True,
                'primary_color': '#f44336',
                'primary_light': '#ffcdd2',
                'primary_dark': '#d32f2f',
                'secondary_color': '#e91e63',
                'accent_color': '#ff5722',
                'text_dark': '#2c2c2c',
                'text_medium': '#4a4a4a',
                'text_light': '#6b6b6b',
                'text_muted': '#9b9b9b',
                'bg_white': '#ffffff',
                'bg_light': '#fef7f7',
                'bg_cream': '#fce4ec',
                'border_light': '#ffebee',
                'border_medium': '#ffcdd2',
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created color palettes')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Color palettes already exist')
            )


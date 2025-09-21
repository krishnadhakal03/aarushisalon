# Generated manually for Color Palette system

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0008_revert_theme_changes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorPalette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('default', 'Default Pink'), ('dark', 'Dark Theme'), ('blue', 'Blue Theme'), ('yellow', 'Yellow Theme'), ('light_red', 'Light Red Theme')], max_length=50, unique=True)),
                ('display_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('primary_color', models.CharField(help_text='Primary color (hex code)', max_length=7)),
                ('primary_light', models.CharField(help_text='Light variant of primary color', max_length=7)),
                ('primary_dark', models.CharField(help_text='Dark variant of primary color', max_length=7)),
                ('secondary_color', models.CharField(help_text='Secondary color (hex code)', max_length=7)),
                ('accent_color', models.CharField(help_text='Accent color (hex code)', max_length=7)),
                ('text_dark', models.CharField(help_text='Dark text color', max_length=7)),
                ('text_medium', models.CharField(help_text='Medium text color', max_length=7)),
                ('text_light', models.CharField(help_text='Light text color', max_length=7)),
                ('text_muted', models.CharField(help_text='Muted text color', max_length=7)),
                ('bg_white', models.CharField(help_text='White background', max_length=7)),
                ('bg_light', models.CharField(help_text='Light background', max_length=7)),
                ('bg_cream', models.CharField(help_text='Cream background', max_length=7)),
                ('border_light', models.CharField(help_text='Light border color', max_length=7)),
                ('border_medium', models.CharField(help_text='Medium border color', max_length=7)),
                ('success_color', models.CharField(default='#28a745', help_text='Success color', max_length=7)),
                ('warning_color', models.CharField(default='#ffc107', help_text='Warning color', max_length=7)),
                ('danger_color', models.CharField(default='#dc3545', help_text='Danger color', max_length=7)),
                ('info_color', models.CharField(default='#17a2b8', help_text='Info color', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Color Palette',
                'verbose_name_plural': 'Color Palettes',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='themesettings',
            name='color_palette',
            field=models.ForeignKey(blank=True, help_text='Select a predefined color palette', null=True, on_delete=models.SET_NULL, to='salon.colorpalette'),
        ),
        migrations.AddField(
            model_name='themesettings',
            name='custom_accent_color',
            field=models.CharField(blank=True, help_text='Override accent color (hex code)', max_length=7),
        ),
        migrations.AddField(
            model_name='themesettings',
            name='custom_primary_color',
            field=models.CharField(blank=True, help_text='Override primary color (hex code)', max_length=7),
        ),
        migrations.AddField(
            model_name='themesettings',
            name='custom_secondary_color',
            field=models.CharField(blank=True, help_text='Override secondary color (hex code)', max_length=7),
        ),
    ]


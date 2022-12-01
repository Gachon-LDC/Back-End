from django.apps import AppConfig
import os


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'
    
    
class SaveFile:
    def save_file_at_dir(dir_path, filename, file_content, mode='wb'):
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, filename), mode) as f:
            f.write(file_content)

import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Kullanıcı rollerini (Patron, Şube Müdürü, Muhasebe) ve izinlerini ayarlar.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Kullanıcı rolleri ve izinleri yapılandırma işlemi başlatılıyor..."))

        # ContentType temizleme işlemi
        self.stdout.write("ContentType temizleme işlemi başlatılıyor...")
        try:
            with transaction.atomic():
                content_types_by_model = {}
                for ct in ContentType.objects.filter(app_label='yonetim').order_by('id'):
                    if ct.model not in content_types_by_model:
                        content_types_by_model[ct.model] = []
                    content_types_by_model[ct.model].append(ct)

                for model_name, cts in content_types_by_model.items():
                    if len(cts) > 1:
                        self.stdout.write(self.style.WARNING(f"  '{model_name}' modeli için {len(cts)} adet ContentType nesnesi bulundu. Fazlalıklar siliniyor..."))
                        for ct_to_delete in cts[1:]:
                            self.stdout.write(f"    Siliniyor: ContentType id={ct_to_delete.id}, model={ct_to_delete.model}")
                            ct_to_delete.delete()
                        self.stdout.write(self.style.SUCCESS(f"  '{model_name}' modeli için fazlalık ContentType nesneleri silindi."))
                    else:
                        self.stdout.write(f"  '{model_name}' modeli için yinelenen ContentType nesnesi bulunamadı veya zaten bir tane var.")

            self.stdout.write(self.style.SUCCESS("ContentType temizleme işlemi tamamlandı."))

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"Veritabanı bütünlüğü hatası oluştu: {e}. Lütfen veritabanınızı kontrol edin."))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"ContentType temizleme sırasında beklenmeyen bir hata oluştu: {e}"))
            return

        # Rol ve İzin yapılandırma işlemi
        role_permissions_map = {
            "Patron": [
                "yonetim.view_gelirgider",
            ],
            "Şube Müdürü": [
                "yonetim.view_personel",
                "yonetim.add_personel",
                "yonetim.change_personel",
                "yonetim.delete_personel",
                "yonetim.view_mesai",
                "yonetim.add_mesai",
                "yonetim.change_mesai",
                "yonetim.delete_mesai",
            ],
            "Muhasebe": [],
        }

        all_yonetim_permissions = Permission.objects.filter(content_type__app_label='yonetim')
        role_permissions_map["Muhasebe"] = [f"{p.content_type.app_label}.{p.codename}" for p in all_yonetim_permissions]

        for role_name, perms_list_str in role_permissions_map.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"'{role_name}' grubu oluşturuldu."))
            else:
                self.stdout.write(self.style.WARNING(f"'{role_name}' grubu zaten mevcut."))

            group.permissions.clear()
            self.stdout.write(f"'{role_name}' grubunun mevcut izinleri temizlendi.")

            for perm_str in perms_list_str:
                app_label, codename = perm_str.split('.')
                try:
                    perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"  Uyarı: '{perm_str}' izni mevcut değil. Atlanıyor."))
            self.stdout.write(self.style.SUCCESS(f"'{role_name}' grubunun izinleri güncellendi."))

        self.stdout.write(self.style.SUCCESS("\nRol yapılandırması tamamlandı. Kullanıcılarınıza rolleri atamayı unutmayın!"))

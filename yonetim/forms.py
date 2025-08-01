from django import forms
from .models import Sube, Personel, GelirGider, Mesai
from django.utils import timezone


class SubeForm(forms.ModelForm):
    class Meta:
        model = Sube
        fields = ["ad", "tur", "adres", "telefon", "yonetici"]
        widgets = {
            "ad": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Şube adını girin",
                }
            ),
            "tur": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                }
            ),
            "adres": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "rows": 3,
                    "placeholder": "Şube adresini girin",
                }
            ),
            "telefon": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Telefon numarasını girin",
                }
            ),
            "yonetici": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Yönetici adını girin",
                }
            ),
        }


class PersonelForm(forms.ModelForm):
    class Meta:
        model = Personel
        fields = [
            "sube",
            "ad",
            "soyad",
            "pozisyon",
            "ise_baslama_tarihi",
            "telefon",
            "email",
        ]
        widgets = {
            "sube": forms.Select(attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"}),
            "ad": forms.TextInput(
                attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500", "placeholder": "Adını girin"}
            ),
            "soyad": forms.TextInput(
                attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500", "placeholder": "Soyadını girin"}
            ),
            "pozisyon": forms.TextInput(
                attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500", "placeholder": "Pozisyonunu girin"}
            ),
            "ise_baslama_tarihi": forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "type": "date",
                }
            ),
            "telefon": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Telefon numarasını girin",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "E-posta adresini girin",
                }
            ),
        }


class MesaiForm(forms.ModelForm):
    sube = forms.ModelChoiceField(
        queryset=Sube.objects.all(),
        label="Şube",
        required=True,
        widget=forms.Select(attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["personel"].queryset = Personel.objects.none()

        if "sube" in self.data:
            try:
                sube_id = int(self.data.get("sube"))
                self.fields["personel"].queryset = Personel.objects.filter(
                    sube_id=sube_id
                ).order_by("ad")
            except (ValueError, TypeError):
                pass  # Hatalı giriş, queryset boş kalır
        elif self.instance.pk:
            self.initial["sube"] = self.instance.personel.sube
            self.fields["personel"].queryset = Personel.objects.filter(
                sube=self.instance.personel.sube
            ).order_by("ad")

        if not self.instance.pk and "tarih" not in self.initial:
            self.initial["tarih"] = timezone.localtime().date()

    class Meta:
        model = Mesai
        fields = ["sube", "personel", "tarih", "saat", "aciklama"]
        widgets = {
            "personel": forms.Select(attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"}),
            "tarih": forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "type": "date",
                }
            ),
            "saat": forms.NumberInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Mesai saatini girin",
                    "min": "0",
                    "step": "1",
                }
            ),
            "aciklama": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "rows": 3,
                    "placeholder": "Mesai açıklaması girin (opsiyonel)",
                }
            ),
        }


class GelirGiderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and "tarih" not in self.initial:
            self.initial["tarih"] = timezone.localtime().date()

    class Meta:
        model = GelirGider
        fields = ["sube", "tip", "kategori", "aciklama", "tutar", "tarih"]
        widgets = {
            "sube": forms.Select(attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"}),
            "tip": forms.Select(attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"}),
            "kategori": forms.Select(attrs={"class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"}),
            "aciklama": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "rows": 3,
                    "placeholder": "Açıklama girin (opsiyonel)",
                }
            ),
            "tutar": forms.NumberInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Tutarı girin",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "tarih": forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "type": "date",
                }
            ),
        }

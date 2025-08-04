import os
import sys
import django
from pathlib import Path

BASE_DIRE = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIRE))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from travel.models import Destination, TravelStyle
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'تخصیص stylesی سفر به مقاصد بر اساس استان و ویژگی‌ها'

    def handle(self, *args, **options):
        styles = {
            "ماجراجویی": TravelStyle.objects.get(name="ماجراجویی"),
            "تفریحی": TravelStyle.objects.get(name="تفریحی"),
            "فرهنگی": TravelStyle.objects.get(name="فرهنگی"),
            "طبیعت‌گردی": TravelStyle.objects.get(name="طبیعت‌گردی"),
            "زیارتی": TravelStyle.objects.get(name="زیارتی"),
            "شهری": TravelStyle.objects.get(name="شهری"),
            "ساحلی": TravelStyle.objects.get(name="ساحلی"),
            "توریستی": TravelStyle.objects.get(name="توریستی")
        }

        PROVINCE_STYLE= {
            # استان‌های شمالی
            "گیلان": ["طبیعت‌گردی", "ساحلی", "تفریحی", "فرهنگی"],
            "مازندران": ["طبیعت‌گردی", "ساحلی", "تفریحی", "ماجراجویی"],
            "گلستان": ["طبیعت‌گردی", "ساحلی", "فرهنگی"],
            
            # استان‌های غربی
            "آذربایجان شرقی": ["فرهنگی", "طبیعت‌گردی", "شهری"],
            "آذربایجان غربی": ["فرهنگی", "طبیعت‌گردی", "ماجراجویی"],
            "کردستان": ["طبیعت‌گردی", "فرهنگی", "ماجراجویی"],
            "کرمانشاه": ["فرهنگی", "طبیعت‌گردی", "زیارتی"],
            "همدان": ["فرهنگی", "طبیعت‌گردی"],
            "زنجان": ["فرهنگی", "طبیعت‌گردی"],
            
            # استان‌های مرکزی
            "تهران": ["شهری", "فرهنگی", "ماجراجویی"],
            "البرز": ["شهری", "طبیعت‌گردی"],
            "مرکزی": ["فرهنگی", "طبیعت‌گردی"],
            "قم": ["زیارتی", "فرهنگی"],
            "اصفهان": ["فرهنگی", "شهری", "زیارتی"],
            "یزد": ["فرهنگی", "زیارتی", "طبیعت‌گردی"],
            "سمنان": ["طبیعت‌گردی", "فرهنگی"],
            
            # استان‌های جنوبی
            "هرمزگان": ["ساحلی", "ماجراجویی", "طبیعت‌گردی"],
            "بوشهر": ["ساحلی", "فرهنگی", "طبیعت‌گردی"],
            "خوزستان": ["فرهنگی", "شهری", "طبیعت‌گردی"],
            "کهگیلویه و بویراحمد": ["طبیعت‌گردی", "ماجراجویی"],
            "فارس": ["فرهنگی", "زیارتی", "طبیعت‌گردی"],
            "کرمان": ["فرهنگی", "طبیعت‌گردی", "زیارتی"],
            "سیستان و بلوچستان": ["طبیعت‌گردی", "ماجراجویی", "فرهنگی"],
            
            # استان‌های شرقی
            "خراسان رضوی": ["زیارتی", "فرهنگی", "طبیعت‌گردی"],
            "خراسان شمالی": ["طبیعت‌گردی", "فرهنگی"],
            "خراسان جنوبی": ["طبیعت‌گردی", "فرهنگی"],
            
            # استان‌های کوهستانی
            "چهارمحال بختیاری": ["طبیعت‌گردی", "ماجراجویی", "فرهنگی"],
            "لرستان": ["طبیعت‌گردی", "ماجراجویی", "فرهنگی"],
            

            
            # استان‌های خاص
            "ایلام": ["طبیعت‌گردی", "فرهنگی"],
            "اردبیل": ["طبیعت‌گردی", "فرهنگی", "زیارتی"]
        }

        # شهرهای خاص با stylesی خاص
        SPECIAL_CITIES = {
            "کیش": ["ساحلی", "تفریحی", "ماجراجویی"],
            "تهران": ["شهری", "فرهنگی"],
            "اصفهان": ["فرهنگی", "شهری"],
            "تبریز": ["فرهنگی", "شهری"],
            "شیراز": ["فرهنگی", "زیارتی"],
            "مشهد": ["زیارتی", "شهری"]
        }

        for dest in Destination.objects.all():
            styles_to_add = set()

            if dest.name in SPECIAL_CITIES:
                for style in SPECIAL_CITIES[dest.name]:
                    styles_to_add.add(styles[style])

            if dest.province in PROVINCE_STYLE:
                for style in PROVINCE_STYLE[dest.province]:
                    styles_to_add.add(styles[style])

            if dest.thrill_activities >= 0.6:
                styles_to_add.add(styles["ماجراجویی"])

            if dest.proximate_nature >= 0.7:
                styles_to_add.add(styles["طبیعت‌گردی"])

            if dest.cultural_sites >= 0.7:
                styles_to_add.add(styles["فرهنگی"])

            if dest.spa_facilities >= 0.6:
                styles_to_add.add(styles["تفریحی"])

            if not styles_to_add:
                styles_to_add.add(styles["توریستی"])

            # اختصاص styles به dest
            dest.travel_styles.set(styles_to_add)

            self.stdout.write(
                f"stylesی {[s.name for s in styles_to_add]} به {dest.name} ({dest.province}) اضافه شد")

        self.stdout.write(self.style.SUCCESS(
            'تخصیص stylesی سفر با موفقیت انجام شد'))
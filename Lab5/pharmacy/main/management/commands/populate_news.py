from django.core.management.base import BaseCommand
from main.models import News
from django.core.files import File
import os
from django.conf import settings
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate database with sample news articles'

    def handle(self, *args, **kwargs):
        news_data = [
            {
                'title': 'New Flu Medication Now Available',
                'content': 'We are pleased to announce the arrival of a new, more effective flu medication. This advanced formula provides faster relief from symptoms and has fewer side effects.',
                'summary': 'A new, more effective flu medication is now available in our pharmacy.',
                'image_name': 'flu-medicine.jpg'
            },
            {
                'title': 'Expanded Range of Vitamin Complexes',
                'content': 'Our vitamin section has been expanded with new premium supplements. The new range includes specialized formulas for different age groups and specific health needs.',
                'summary': 'New vitamin supplements added to our product range.',
                'image_name': 'vitamins.jpg'
            },
            {
                'title': 'Opening of New Orthopedic Products Department',
                'content': 'We are excited to announce the opening of our new orthopedic department. Find a wide range of supports, braces, and other orthopedic aids.',
                'summary': 'New department specializing in orthopedic products now open.',
                'image_name': 'orthopedic.jpg'
            },
            {
                'title': 'Seasonal Sale on Cold and Flu Medications',
                'content': 'Get ready for the cold season with our special offers on cold and flu medications. Find discounts on popular brands and products.',
                'summary': 'Special discounts on cold and flu medications.',
                'image_name': 'sale.jpg'
            },
            {
                'title': 'Implementation of Electronic Prescriptions',
                'content': 'We now accept electronic prescriptions for all medication orders. This new system provides faster and more convenient service for our customers.',
                'summary': 'Electronic prescription service now available.',
                'image_name': 'e-prescription.jpg'
            },
            {
                'title': 'New Diabetes Care Products Line',
                'content': 'Introducing our new comprehensive diabetes care product line. Find everything from glucose meters to specialized dietary supplements.',
                'summary': 'New products for diabetes management available.',
                'image_name': 'diabetes.jpg'
            },
            {
                'title': 'Launch of Baby Care Department',
                'content': 'Visit our new baby care section featuring premium products for infant health and care. Find everything from baby vitamins to care products.',
                'summary': 'New department dedicated to baby care products.',
                'image_name': 'baby-care.jpg'
            },
            {
                'title': 'Health and Wellness Workshop Series',
                'content': 'Join our upcoming health and wellness workshops. Learn about nutrition, exercise, and maintaining a healthy lifestyle from healthcare professionals.',
                'summary': 'Free health education workshops starting next month.',
                'image_name': 'workshop.jpg'
            },
            {
                'title': 'New Natural Cosmetics Collection',
                'content': 'Discover our new range of natural and organic cosmetics. All products are cruelty-free and made with sustainable ingredients.',
                'summary': 'New natural and organic cosmetics now available.',
                'image_name': 'cosmetics.jpg'
            },
            {
                'title': 'Extended Working Hours Announcement',
                'content': 'We are extending our working hours to better serve you. The pharmacy will now be open from 8:00 AM to 10:00 PM every day.',
                'summary': 'New extended pharmacy working hours.',
                'image_name': 'hours.jpg'
            }
        ]

        # Directory for news images
        news_media_dir = os.path.join(settings.MEDIA_ROOT, 'news')
        os.makedirs(news_media_dir, exist_ok=True)

        # Directory for custom news images
        custom_images_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'news')
        default_image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'news-default.jpg')

        # Calculate dates starting from today and going backwards
        today = datetime.now()

        for index, article_data in enumerate(news_data):
            # Set the date for each article, starting from today and going backwards
            article_date = today - timedelta(days=index * 2)  # Each article is 2 days apart

            article, created = News.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'content': article_data['content'],
                    'summary': article_data['summary'],
                    'date_published': article_date
                }
            )

            if created:
                # Try to find custom image first
                custom_image_path = os.path.join(custom_images_dir, article_data['image_name'])
                source_image_path = custom_image_path if os.path.exists(custom_image_path) else default_image_path

                if os.path.exists(source_image_path):
                    # Create a unique name for the image in media directory
                    new_image_name = f'news-{article.id}-{article_data["image_name"]}'
                    new_image_path = os.path.join(news_media_dir, new_image_name)

                    # Copy the image
                    with open(source_image_path, 'rb') as source_file:
                        with open(new_image_path, 'wb') as dest_file:
                            dest_file.write(source_file.read())

                    # Save the image to the model
                    with open(new_image_path, 'rb') as image_file:
                        article.image.save(new_image_name, File(image_file), save=True)

                self.stdout.write(f'Created news article: {article.title}') 
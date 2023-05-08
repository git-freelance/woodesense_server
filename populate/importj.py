import json
import os
import re
import time
import multiprocessing
from urllib import request
from urllib.parse import urlparse
from PIL import Image
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WoodSens.settings')
import django
django.setup()

from core.models import Category, Product, ProductImage


def normalize_sku(string):
    return re.sub('\W', '', string)


def normalize_name(string):
    return re.sub('\s+', ' ', string).strip().lower().capitalize()


def split_list(arr, wanted_parts=1):
    length = len(arr)
    return [arr[i * length // wanted_parts: (i+1) * length // wanted_parts] for i in range(wanted_parts)]


def make_product(arr):
    arr_len = len(arr)
    for i, line in enumerate(arr):
        print('%s from %s' % (i + 1, arr_len))
        cat_name = line.get('name')

        try:
            if cat_name == 'Modern Double Vanities':
                cat_name = 'Modern Double Vanity'
            if cat_name == 'Console Tables':
                cat_name = 'Console Table'
            category = Category.objects.get(name__iexact=cat_name, level=1)
        except:
            print('Category %s not found' % cat_name)
        else:
            sku = normalize_sku(line.get('image_title'))
            prod_name = line.get('image_description')
            image_url = line.get('image_url')
            if prod_name:
                prod_name = normalize_name(prod_name)
            else:
                prod_name = sku

            subategory = category.get_root()
            p = Product(name=prod_name, sku=sku)
            p.save()
            # Image
            if image_url:
                #img = request.urlretrieve('http://www.woodsenseinteriors.com/wp-content/uploads/2017/11/DT_99.jpg')

                def get_img():
                    if urlparse(image_url).netloc:
                        url = image_url
                    else:
                        url = 'http://www.woodsenseinteriors.com' + image_url
                    return request.urlretrieve(url)

                try:
                    img = get_img()
                except Exception as e:
                    print(str(e))
                    time.sleep(3)
                    img = get_img()

                pil_img = Image.open(img[0])
                width, height = pil_img.size
                pil_img = pil_img.convert('RGB')
                if width > 1000:
                    print('Resizing width')
                    new_width = 1000
                    new_height = new_width * height // width
                    pil_img = pil_img.resize((new_width, new_height), Image.ANTIALIAS)

                width, height = pil_img.size
                if height > 1000:
                    print('Resizing height')
                    new_height = 1000
                    new_width = new_height * width // height
                    pil_img = pil_img.resize((new_width, new_height), Image.ANTIALIAS)

                pil_img.save('img.jpg', quality=90)

                pi = ProductImage(product=p)
                pi.image.save('img.jpg', File(open('img.jpg', 'rb')), save=True)

            p.categories.add(category, subategory)


if __name__ == '__main__':
    with open('wppr_tz_plusgallery_item.json', 'r', encoding='utf-8') as file:
        data = json.load(file)[2]['data']
    # NUM_WORKERS = multiprocessing.cpu_count()
    # splitted_list = split_list(data[:4], NUM_WORKERS)
    # pool = multiprocessing.Pool(NUM_WORKERS)
    # pool.map(make_product, splitted_list)

    make_product(data)

import asyncio
import json
import os
import random

from dotenv import load_dotenv
from vkbottle import API, PhotoFaviconUploader, run_sync
from loguru import logger

logger.remove()
logger.add('logs.log')


load_dotenv()
logger.info('Loaded dotenv')
api = API(os.environ["USER_TOKEN"])


async def upload_image():
    uploader = PhotoFaviconUploader(api)
    path_base = 'Z:\_new folder\_animesintheheres'
    with open('used_images.json', encoding='utf-8') as file:
        used_images = json.load(file)

    logger.info('Loaded json')

    available_images = [
        os.path.join(path_base,f)
        for f in os.listdir(path_base)
        if os.path.isfile(os.path.join(path_base,f))
        and f not in used_images
    ]
    if len(available_images) == 0:
        raise ValueError('No More Pictures Left')

    photo = random.choice(available_images)

    logger.info(f'Image candidate: {photo}')

    used_images.append(photo)

    with open('used_images.json', 'w', encoding='utf-8') as write_file:
        json.dump(used_images, write_file, indent=2)

    logger.info('Dumped json')

    post_url = await uploader.upload(photo)

    logger.info(f'Uploaded photo: {post_url=}')

    owner_id = post_url[4:13]
    post_id = post_url[14:]
    await api.wall.delete(owner_id, post_id)

    logger.info(f'Deleted post: {owner_id=} {post_id=}')

asyncio.get_event_loop().run_until_complete(upload_image())


#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import logging
from lib.waveshare_epd import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import requests
import json
from datetime import datetime as dt, timedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")
    
    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    width = 480
    unitHeight=202
    jaFontSmall = ImageFont.truetype('font/BIZUDGothic-Regular.ttf', 16)
    jaFont = ImageFont.truetype('font/BIZUDGothic-Regular.ttf', 24)
    enFont = ImageFont.truetype('font/BebasNeue-Regular.ttf', 50)
    api_url = 'https://api.p2pquake.net/v2/history'
    news = []
    for i in range(3):
        params = { 'limit' : 100, 'offset': i * 100}
        response = requests.get(api_url, params=params)
        tmpNews = json.loads(response.text)
        filteredNews = list(filter(
            lambda detail: 
                detail['code'] == 551 
                and (detail['earthquake'] and detail['earthquake']['maxScale'] > 0) 
                and (detail['earthquake'] and detail['earthquake']['hypocenter']['name']), 
            tmpNews))
        news[len(news):len(news)] = filteredNews
    # 画面クリア
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    for i, detail in enumerate(news):
        draw.text((10, i*50), str(int(detail['earthquake']['maxScale'] / 10)), font = enFont, fill = 0)
        draw.text((70, i*50), detail['earthquake']['hypocenter']['name'], font = jaFont, fill = 0)
        draw.text((70, 30 + i*50), detail['earthquake']['time'], font = jaFontSmall, fill = 0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(5)  
    
    
    # draw.line((70, 50, 20, 100), fill = 0)
    # draw.rectangle((20, 50, 70, 100), outline = 0)
    # draw.line((165, 50, 165, 100), fill = 0)
    # draw.line((140, 75, 190, 75), fill = 0)
    # draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    # draw.rectangle((80, 50, 130, 100), fill = 0)
    
    # epd.display(epd.getbuffer(Himage))
    # time.sleep(2)
    
    # Drawing on the Vertical image
    # logging.info("2.Drawing on the Vertical image...")
    # Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # draw = ImageDraw.Draw(Limage)
    # draw.line((10, 90, 60, 140), fill = 0)
    # draw.line((60, 90, 10, 140), fill = 0)
    # draw.rectangle((10, 90, 60, 140), outline = 0)
    # draw.line((95, 90, 95, 140), fill = 0)
    # draw.line((70, 115, 120, 115), fill = 0)
    # draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
    # draw.rectangle((10, 150, 60, 200), fill = 0)
    # draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
    # epd.display(epd.getbuffer(Limage))
    # time.sleep(2)
    
    # logging.info("3.read bmp file")
    # Himage = Image.open('pic/7in5.bmp')
    # epd.display(epd.getbuffer(Himage))
    # time.sleep(2)
    
    # logging.info("4.read bmp file on window")
    # Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # bmp = Image.open('pic/100x100.bmp')
    # Himage2.paste(bmp, (50,10))
    # epd.display(epd.getbuffer(Himage2))
    # time.sleep(2)

    # logging.info("Clear...")
    # epd.init()
    # epd.Clear()
    
    # logging.info("Goto Sleep...")
    # epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
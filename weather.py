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

def convertWeatherCode(code: int):
    print(code)
    if code == 0:
        return '晴れ'
    if code == 3:
        return '曇り'
    if code == 45:
        return '霧'
    if code == 61:
        return '雨'
    if code == 80:
        return 'にわか雨'
    return str(code)

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
    api_url = 'https://api.open-meteo.com/v1/forecast?latitude=35.6785&longitude=139.6823&hourly=temperature_2m,precipitation,weathercode,windspeed_10m&daily=temperature_2m_max,temperature_2m_min&windspeed_unit=ms&timezone=Asia%2FTokyo&past_days=1'
    response = requests.get(api_url)
    data = json.loads(response.text)
    news = []
    print(epd.height, epd.width)
    # 画面クリア
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    draw.line((250, 0, 250, 800), fill = 0)
    for i in range(12):
        draw.text((80, 0), u'今日の天気', font = jaFont, fill = 0)
        draw.text((300, 0), u'明日の天気', font = jaFont, fill = 0)
        draw.text((10, 60 + i*60), str(i*2), font = jaFont, fill = 0)
        draw.text((80, 60 + i*60), convertWeatherCode(data['hourly']['weathercode'][i*2+24]), font = jaFont, fill = 0)
        draw.text((180, 60 + i*60), str(data['hourly']['temperature_2m'][i*2+24]) + u'℃', font = jaFont, fill = 0)
        draw.text((300, 60 + i*60), convertWeatherCode(data['hourly']['weathercode'][i*2+48]), font = jaFont, fill = 0)
        draw.text((400, 60 + i*60), str(data['hourly']['temperature_2m'][i*2+48])+ u'℃', font = jaFont, fill = 0)
        draw.line((0, 60 + i*60, 480, 60 + i*60), fill = 0)
        try:
            icon = Image.open('pic/' + str(data['hourly']['weathercode'][i*2+24]) +'.jpeg')
            icon = icon.resize((40,40))
            Himage.paste(icon, (35,5 + 60 + i*60))
            icon2 = Image.open('pic/' + str(data['hourly']['weathercode'][i*2+48]) +'.jpeg')
            icon2 = icon2.resize((40,40))
            Himage.paste(icon2, (251,5 + 60 + i*60))
        except:
            continue
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

    logging.info("Clear...")
    epd.init()
    epd.Clear()
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
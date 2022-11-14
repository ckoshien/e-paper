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

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")
    
    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    width = 448
    jaFontSmall = ImageFont.truetype('font/BIZUDGothic-Regular.ttf', 16)
    jaFont = ImageFont.truetype('font/BIZUDGothic-Regular.ttf', 24)
    enFont = ImageFont.truetype('font/BebasNeue-Regular.ttf', 50)
    api_url = 'https://jcbl-score.com/scoresheet/api/v1/game'
    response = requests.get(api_url)
    games = json.loads(response.text)
    slicedGames = list(filter(
        lambda game: 
            dt.strptime(game['updated_at'], '%Y-%m-%d %H:%M:%S')
            + timedelta(days=2) > dt.now()
            , 
        games))
    # 画面クリア
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    for i, game in enumerate(slicedGames[0:4]):
        #tdatetime = dt.strptime(game['updated_at'], '%Y-%m-%d %H:%M:%S')
        #if tdatetime + timedelta(minutes=15) > dt.now():
        #if tdatetime + timedelta(days=2) > dt.now():
        print(game)
        # 255: clear the frame
        firstPosition = width*2/7 - (len(game['first_team_name'])/2 - 1)*24
        lastPosition = width*5/7 - (len(game['last_team_name'])/2 - 1)*24
        draw.text((10, 0 + 200*i), game['name'], font = jaFontSmall, fill = 0)
        draw.text((width - 10*16, 0 + 200*i), game['updated_at'], font = jaFontSmall, fill = 0)
        draw.text((firstPosition, 30 + 200*i), game['first_team_name'], font = jaFontSmall, fill = 0)
        draw.text((lastPosition, 30 + 200*i), game['last_team_name'], font = jaFontSmall, fill = 0)
        draw.text((width*2/7, 60 + 200*i), str(game['first_run']), font = enFont, fill = 0)
        draw.text((width/2 + 60, 60 + 200*i), '-', font = enFont, fill = 0)
        draw.text((width*5/7, 60 + 200*i), str(game['last_run']), font = enFont, fill = 0)
        if game['winner']:
            draw.text((firstPosition, 150 + 200*i), '勝:' + game['winner'], font = jaFontSmall, fill = 0)
        if game['saver']:
            draw.text((lastPosition, 150 + 200*i), 'S:' + game['saver'], font = jaFontSmall, fill = 0)
        if game['loser']:
            draw.text((firstPosition, 175 + 200*i), '敗:' + game['loser'], font = jaFontSmall, fill = 0)
        if game['holder']:
            draw.text((lastPosition, 175 + 200*i), 'H:' + game['holder'], font = jaFontSmall, fill = 0)
        if game['homer']:
            draw.text((firstPosition, 200 + 200*i), 'HR:' + game['homer'], font = jaFontSmall, fill = 0)
        draw.line((0, 200 + 200*i , 448, 200 + 200*i), fill = 0)
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
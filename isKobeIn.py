#!/usr/bin/python

import sys
import getpass
import smtplib
import requests
import time
from bs4 import BeautifulSoup

def error_show_usage():
    print 'Error - Please run the script in this format: python isKobeIn.py <email_address>'
    exit(1)

def is_he_playing(is_in_game):
    game_page = requests.get('https://sports.yahoo.com/nba/utah-jazz-los-angeles-lakers-2016041313/') # CHANGE URL TO ACTUAL GAME URL
    soup = BeautifulSoup(game_page.text, "html.parser")
    player_tables = soup.find_all("table", attrs={"summary": "PLAYERS"})

    for player_table in player_tables:
        player_rows = player_table.find("tbody").find_all("tr")

        for player in player_rows:
            if player.find("div", attrs={"data-entity-type": "player"}) is not None:
                if player.find("div", attrs={"data-entity-type": "player"}).find(text=True, recursive=False) == "Kobe Bryant":
                    if player.find("th", attrs={"class": "on-court"}) is not None:        
                        is_in_game = True
                        return is_in_game
                    else:
                        is_in_game = False
                        return is_in_game

    return is_in_game


def send_notification(email, password, is_in_game):
    if is_in_game:
        content = 'Kobe just got into the game! Go watch!'
    else:
        content = 'Kobe needs a break. I\'ll tell you when he\'s back in!'    

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(email, password)
    mail.sendmail(email,email,content) 
    mail.close()

def main(argv):
    email = ''
    
    if len(sys.argv) != 2:
        error_show_usage()

    email = sys.argv[1]
    password = getpass.getpass(prompt='Email password:')   

    is_in_game = False

    while True:
        temp = is_he_playing(is_in_game)

        if is_in_game is not temp: # If his status has changed, send a notification! Otherwise, don't.
            is_in_game = temp
            send_notification(email, password, is_in_game)

        # Add a sleep to make sure too many requests aren't sent
        time.sleep(60)

if __name__ == "__main__":
    main(sys.argv[1:])    

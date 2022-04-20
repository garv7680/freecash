from bs4 import BeautifulSoup
import requests
import json


def req(id):
    '''
    Returns individual results (not dict)
    '''
    url = requests.get(f"https://freecash.com/user/{id}").text
    soup = BeautifulSoup(url, 'lxml')

    for x in soup.find_all("h5"):
        if (x.text == "Private Profile" or x.text == "Failed to load profile"):
            return -1

    level = soup.find(class_="userProfileLevelInner").text
    user = soup.find(class_="userProfileTopUsername truncate").text.strip("\n")
    stats = soup.find_all(class_="userProfileStatValue")

    script = soup.find(id="almaView").find("script")
    dates = script.text.split("'")[5].split(",")
    earnings = script.text.split("'")[1].split(",")

    moneyEarnings = ""
    for x in range(len(earnings)):
        moneyEarnings += f"{dates[x]}={earnings[x]},"

    return id, user, level, stats, moneyEarnings


def find(sid):
    '''
        Takes in id of user and returns a dict which includes: id,username,level,completed_offers,coins_earned,referrals, and earnings from last 7 days
        Private profiles / Accounts that are not found return -1 
    '''
    if (req(sid) != -1):
        id, user, level, stats, moneyEarnings = req(sid)

        earnings = {
            "earnings_last_7_days": moneyEarnings[:-1]
        }

        jsonstr = {
            "id": id,
            "user": user,
            "level": level,
            "completed_offers": stats[0].text,
            "coins_earned": stats[1].text,
            "ref": stats[2].text,
            "earnings": earnings
        }
        return jsonstr
    else:
        return -1


res = find(89)

print(res['id'])

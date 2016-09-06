#!/usr/bin/env python
"""
Scrapes data from LaundryView for MIT laundry rooms
and dumps number of available washers and dryers
into MySQL Database.

"""

import laundryview_notification_script.check as check
import mysql_credentials as DB
import time
from orm import LaundryViewDataTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


LAUNDRY_ROOMS = [ 1364831,  # 405 Memorial Drive
                  136484,   # Baker House
                  1364811,  # Burton-Conner
                  136488,   # East Campus
                  136486,   # Eastgate
                  1364819,  # Edgerton House Left
                  136482,   # Edgerton House Right
                  136481,   # Green Hall
                  1364815,  # MacGregor
                  1364830,  # Maseeh Hall
                  136487,   # McCormick
                  1364818,  # McCormick Annex
                  136483,   # New Ashdown
                  1364813,  # New House
                  1364812,  # Next House
                  136489,   # Senior House
                  1364821,  # Sidney Pacific
                  1364826,  # Simmons Hall 346
                  1364824,  # Simmons Hall 529
                  1364823,  # Simmons Hall 676
                  1364822,  # Simmons Hall 765
                  1364825,  # Simmons Hall 845
                  1364810,  # Tang Hall
                  1364820,  # Warehouse
                  1364814   # Westgate
                ]


def open_mysql():
    url = 'mysql://%s:%s@%s:3306/%s' % \
            (DB.USERNAME, DB.PASSWORD, DB.HOST, DB.DATABASE)
    if DB.SOCKET != '':
        url += '?unix_socket=%s' % DB.SOCKET
    engine = create_engine(url, echo=False) 
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def scrape_dump_to_db(session, rooms):
    new_records = []
    for room in rooms:
        try:
            status = check.number_available(room)
            new_records.append(LaundryViewDataTable(
                room, status['washer'], status['dryer']))
        except AttributeError:  # Problem scraping data
            continue
    if len(new_records) > 0:
        session.add_all(new_records)
        session.commit()

def main():
    session = open_mysql()
    while True:
        scrape_dump_to_db(session, LAUNDRY_ROOMS)
        time.sleep(300)


if __name__ == '__main__':
    main()

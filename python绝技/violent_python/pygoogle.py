#!/usr/bin/python3.5
# coding: utf-8

"""
WARNING
Ensure that your system has "requests", "BeautifulSoup" and "os". If not, it will not run.
PyGoogle - Developed by Arsh Leak.
$ wget https://github.com/4rsh/
"""

import requests
import BeautifulSoup
import os

os.system("clear")
print ("""
  _____        _____                   _      
 |  __ \      / ____|                 | |     
 | |__) |   _| |  __  ___   ___   ____| | ___ 
 |  ___/ | | | | |_ |/ _ \ / _ \ / _` | |/ _ |
 | |   | |_| | |__| | (_) | (_) | (_| | |  __/
 |_|    \__, |\_____|\___/ \___/ \__, |_|\___|
         __/ |                    __/ |       
        |___/                    |___/        
""")
                
query = input("Type your search:    ")
r = requests.get('https://www.google.com.br/search?q=%s&num=50&start=50' % (query))
if r.status_code != 200:
    print ("Error\n")
else:
    soup = BeautifulSoup.BeautifulSoup(r.content)

    for link in soup.findAll(attrs={'class':'g'}):

        for a in link.findAll('h3', attrs={'class':'r'}):
            title = a.text
            title = title.title()

        for l in link.findAll(attrs={'class':'s'}):
            print (title, "\n", l.cite.text, "\n\n")

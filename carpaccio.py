from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import requests
import sys

# request page, then load only the div tags with 'menu-item' class attribute into memory
url = requests.get('http://www.teiteirobata.com/new-page-2/')
items = bs(url.text, 'html.parser', parse_only=ss('div', class_='menu-item')).contents

# create menu dictionary, then fill it with menu items and their descriptions
menu = {}
for x in range(len(items)):
    # checks to see if a description is available for the menu item
    # note: items with '3' as their length do not have descriptions
    if len(items[x]) == 3:
        item = str(items[x].contents[1].contents[0]).strip()
        desc = ''
    else:
        item = str(items[x].contents[1].contents[0]).strip()
        desc = str(items[x].contents[3].contents[0]).strip()
    menu[item] = desc

# function to perform a search on the menu dictionary
# note:  default search is for carpaccio, because it is awesome.
def find_in_menu(sub='carpaccio'):
    try:
        search = [s for s in menu if sub in s]
        result_item, result_desc = str(search[0]), menu[str(search[0])]
        print(result_item.title() + '\n' + result_desc)
    except:
        print('Sorry, \"' + str(sub) + '\" is not on the menu today.')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        find_in_menu(str(sys.argv[1]))
    else:
        find_in_menu()
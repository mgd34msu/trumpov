import requests
import re

def find_carpaccio():
    r = requests.get('http://www.teiteirobata.com/new-page-2/')
    r_list = re.split(r'<div class="menu-selector">|</div> <!-- END .menu-wrapper -->', r.text)
    menu_list = re.split(r'<div class="menu-section-header">', r_list[1])
    del menu_list[0]
    for i in range(len(menu_list)):
        menu_list[i] = re.sub(r'  |\n', '', menu_list[i])
    menu_list = list(filter(None, re.split('<div[^>]*>|<input[^>]*>|<\/div>', ''.join(menu_list))))
    indices = [i for i, s in enumerate(menu_list) if 'carpaccio' in s]
    try:
        carpaccio = [menu_list[indices[0]], menu_list[indices[0]+1]]
        print('Today\'s Special: ' + carpaccio[0].title() + " -- " + carpaccio[1])
    except:
        print('Sorry, not on the menu today...')

if __name__ == '__main__':
    find_carpaccio()
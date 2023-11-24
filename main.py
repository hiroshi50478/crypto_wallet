import os
import urllib
import requests

import tkinter
from tkinter import ttk
from tkinter.messagebox import showerror
import tkinter.font as font


coin_market_cap_url = 'https://coinmarketcap.com/currencies'
coin_market_cap_coins = dict()
if 'icons' not in os.listdir():
    os.mkdir('icons')

file_name = 'data2.txt'
fee_rate = 0.1
start_balance = []
current_balance = []
downloaded_icons = []


def parse_html(url):
    request = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    )

    data = urllib.request.urlopen(request).read()
    try:
        data = data.decode('utf-8')
    except:
        return parse_html(url)

    return data


def download_icon(short_name):
    print(short_name)
    data = parse_html(f'{coin_market_cap_url}/{coin_market_cap_coins[short_name]}/')

    start_index = 0
    end_index = data.find(f'alt="{short_name}"')
    url = ''

    while True:
        if data[end_index] == '"':
            start_index = end_index - 1
            while data[start_index] != '"':
                start_index -= 1

            if 'https' in data[start_index + 1: end_index]:
                url = data[start_index + 1: end_index]
                break
        end_index -= 1

    print(url)

    response = requests.get(url)
    with open(f'icons/{short_name}.png', 'wb') as file:
        file.write(response._content)


def data_load():
    global fee_rate

    global start_balance
    start_balance = []

    global current_balance
    current_balance = []

    with open(file_name, 'r', encoding='utf-8') as file:
        fee_rate = float(file.readline())

        length = int(file.readline())
        for i in range(length):
            line = file.readline().split(') ')
            line = line[0].split(' (') + [float(line[1])]
            start_balance.append(line)

        length = int(file.readline())
        for i in range(length):
            line = file.readline().split(') ')
            line = line[0].split(' (') + [float(line[1])]
            current_balance.append(line)

    global coin_market_cap_coins
    coin_market_cap_coins = dict()
    with open('coin_market_cap_coins.txt') as file:
        length = int(file.readline())
        for i in range(length):
            line = file.readline().split()
            coin_market_cap_coins[line[0]] = line[1]

    global downloaded_icons
    downloaded_icons = os.listdir('icons')
    for short_name in coin_market_cap_coins.keys():
        if f'{short_name}.png' not in downloaded_icons:
            download_icon(short_name)
            downloaded_icons.append(f'{short_name}.png')


def data_save():
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f'{fee_rate}\n')

        file.write(f'{len(start_balance)}\n')
        for coin in start_balance:
            file.write(f'{coin[0]} ({coin[1]}) {coin[2]}\n')

        file.write(f'{len(current_balance)}\n')
        for coin in current_balance:
            file.write(f'{coin[0]} ({coin[1]}) {coin[2]}\n')


def data_print():
    print(file_name)
    print(fee_rate)
    print(start_balance)
    print(current_balance)
    print(downloaded_icons)
    print(coin_market_cap_coins)


data_load()
data_print()

window = tkinter.Tk()

window_icon = tkinter.PhotoImage(file=f'icons/BTC.png')
window.iconphoto(True, window_icon)
window.title('Crypto Wallet')
window.geometry('500x700+200+150')
window.resizable(True, True)
# window.minsize(400, 400)
# window.maxsize(700, 700)


def end():
    data_save()
    window.destroy()


window.protocol('WM_DELETE_WINDOW', end)
window.update_idletasks()

style = ttk.Style()
style.configure('.', font='Arial 12')

file_frame = ttk.Frame(window, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])

file_entry = ttk.Entry(file_frame, font=style.lookup('.', 'font'))
file_entry.insert(0, file_name)
file_entry.pack(side=tkinter.LEFT)

coins_frame = ttk.Frame(window, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])
icons = []


def show():
    global icons
    icons = []

    for frame in list(coins_frame.children.values()):
        frame.destroy()

    for coin in current_balance:
        frame = ttk.Frame(coins_frame, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])

        if f'{coin[1]}.png' in downloaded_icons:
            icon = tkinter.PhotoImage(file=f'icons/{coin[1]}.png')
        else:
            icon = tkinter.PhotoImage(file=f'icons/BTC.png')

        icon = icon.zoom(2)
        icon = icon.subsample(3)
        icons.append(icon)

        icon_label = ttk.Label(frame, image=icon)
        icon_label.pack(side=tkinter.LEFT)

        long_name_label = ttk.Label(frame, text=coin[0])
        long_name_label.pack(side=tkinter.LEFT)

        short_name_label = ttk.Label(frame, text=coin[1])
        short_name_label.pack(side=tkinter.LEFT)

        count_label = ttk.Label(frame, text=str(coin[2]))
        count_label.pack(side=tkinter.LEFT)

        frame.pack(anchor=tkinter.NW)


def change():
    global file_name
    file_name = file_entry.get()

    data_load()
    data_print()

    show()


file_button = ttk.Button(file_frame, text='Change', command=change)
file_button.pack(side=tkinter.LEFT)

file_frame.pack(fill=tkinter.X)

coins_frame.pack(fill=tkinter.X)

additional_window = None


def create_window():
    global additional_window

    additional_window = tkinter.Toplevel(window)

    ww = window.winfo_width()
    wh = window.winfo_height()
    wx = window.winfo_x()
    wy = window.winfo_y()

    aw = 350
    ah = 250
    additional_window.geometry(f'{aw}x{ah}+{wx + ww + 20}+{wy}')


def normalize(x):
    sign = 1
    if x < 0:
        sign = -1
        x = abs(x)

    s = str(x - int(x))[::-1]

    if s[0] != '0' and s[1:5] == '0000':
        index = 1
        while s[index] == '0':
            index += 1
        s = s[index:][::-1]
        x = int(x) + float(s)

    elif s[0] != '9' and s[1:5] == '9999':
        index = 1
        while s[index] == '9':
            index += 1
        s = s[index:][::-1]
        x = int(x) + float(s) + 10 ** (-(len(s) - 2))

    return sign * x


def buy(buy_name, sell_name, quantity, price):
    sell_count = quantity * price
    buy_count = (100 - fee_rate) / 100 * quantity

    for coin in current_balance:
        if coin[1] == sell_name:
            if sell_count > coin[2]:
                showerror('ERROR', f'Not enought {sell_name}')
                break
            coin[2] -= sell_count
            coin[2] = normalize(coin[2])
    else:
        for coin in current_balance:
            if coin[1] == buy_name:
                coin[2] += buy_count
                coin[2] = normalize(coin[2])

        show()


def create_buy_window():
    create_window()
    additional_window.title('Buy')

    coins_frame = ttk.Frame(additional_window, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])

    buy_frame = ttk.Frame(coins_frame, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])
    buy_label = ttk.Label(buy_frame, text='Buy coin name')
    buy_label.pack()
    buy_entry = ttk.Entry(buy_frame, font=style.lookup('.', 'font'))
    buy_entry.insert(0, 'BTC')
    buy_entry.pack()

    buy_frame.pack(side=tkinter.LEFT)

    sell_frame = ttk.Frame(coins_frame, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])
    sell_label = ttk.Label(sell_frame, text='Sell coin name')
    sell_label.pack()
    sell_entry = ttk.Entry(sell_frame, font=style.lookup('.', 'font'))
    sell_entry.insert(0, 'USDT')
    sell_entry.pack()

    sell_frame.pack(side=tkinter.LEFT)

    coins_frame.pack()

    frame = ttk.Frame(additional_window, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])

    quantity_frame = ttk.Frame(frame, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])
    quantity_label = ttk.Label(quantity_frame, text='Quantity')
    quantity_label.pack()
    quantity_entry = ttk.Entry(quantity_frame, font=style.lookup('.', 'font'))
    quantity_entry.pack()

    quantity_frame.pack(side=tkinter.LEFT)

    price_frame = ttk.Frame(frame, borderwidth=1, relief=tkinter.SOLID, padding=[8, 8])
    price_label = ttk.Label(price_frame, text='Price')
    price_label.pack()
    price_entry = ttk.Entry(price_frame, font=style.lookup('.', 'font'))
    price_entry.pack()

    price_frame.pack(side=tkinter.LEFT)

    frame.pack()

    button = ttk.Button(additional_window, text='Buy',
                        command=lambda: buy(buy_entry.get(), sell_entry.get(), float(quantity_entry.get()), float(price_entry.get()))
                        )
    button.pack()


buy_button = ttk.Button(window, text='Buy', command=create_buy_window)
buy_button.pack()


show()
window.mainloop()

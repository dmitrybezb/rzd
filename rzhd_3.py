# -*- coding: utf-8 -*
from selenium import webdriver # virtual browser
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from pyvirtualdisplay import Display # virtual display
# email
import smtplib   
from email.mime.text import MIMEText 
# /email
import time
from datetime import datetime as dt
# import winsound as w
# import imp
def send_email(mailbox, text):
    me = 'python_sms@mail.ru'
    you = mailbox
    smtp_server = 'smtp.mail.ru'
    msg = MIMEText(text)
    msg['Subject'] = 'I found tickets, buy it NOW!!!'
    msg['From'] = me
    msg['To'] = you
    # Credentials (if needed)  
    username = 'python_sms@mail.ru'  
    password = 'stupidpassword1'

    s = smtplib.SMTP(smtp_server)
    s.starttls()  
    s.login(username,password)  
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    print "Email-notification to " + mailbox + " send"

def create_url():
    """
    Ask for a trip and return url as string
    """
    cities_codes={'sar':'2020000','msk':'2000000','spb':'2004000','kzn':'2060500', 'nn' : '2060001'}
    print
    print 'CityList: ', cities_codes.keys()
    # default cities:
    st0def='msk' 
    st1def='nn'
    print 'default: ' + st0def + ' -> ' + st1def

    st0=raw_input('From...')
    if st0 not in cities_codes.keys():
        st0 = st0def
    st1=raw_input('To...')
    if st1 not in cities_codes.keys():
        st1 = st1def

    st0='code0='+ cities_codes[st0] +'|'
    st1='code1='+ cities_codes[st1] +'|'

    day=raw_input("What day? (For ex: 12): ")
    if day not in range(1, 32):
        day = str(dt.now().day)
    month=raw_input("What month? (For ex: 07): ")
    if month not in range(1,13):
        month = str(dt.now().month)
    start=raw_input("Since what time? (For ex: 19): ")
    if start not in range(0,25):
        start = '00'
    end=raw_input("Until what time? (For ex: 24): ")
    if end not in range(0,25):
        end = '24'

    date="dt0="+ day +'.'+ month +".2013|"
    time='ti0='+ start +'-' + end +'|' # asking for time

    url = "http://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735&layer_id=5354&refererVpId=1&refererPageId=704&refererLayerId=4065#dir=0|tfl=3|checkSeats=1|"+st0+date+time+st1

    return url


def choose_place():
    place_types={'1':u'\u041f\u043b\u0430\u0446\u043a\u0430\u0440\u0442\u043d\u044b\u0439', '2':u'\u041a\u0443\u043f\u0435', '3':u'\u0421\u0438\u0434\u042F\u0427\u0438\u0439'}
    place=raw_input('Input type of place (1 - plac(default), 2 - kupe, 3 - sidya4ka): ')
    if place=="":
        place='1'

    return place_types[place]

def find_train(url, place_type):
    """
    Get url of direction as a string and searching for availiable Place
    """
    ## get the Firefox profile object
    firefoxProfile = FirefoxProfile()
    ## Disable CSS
    firefoxProfile.set_preference('permissions.default.stylesheet', 2)
    ## Disable images
    firefoxProfile.set_preference('permissions.default.image', 2)
    ## Disable Flash
    firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
    # Запускаем локальную сессию firefox
    browser = webdriver.Firefox(firefoxProfile)

    # url = "http://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735&layer_id=5354&refererVpId=1&refererPageId=704&refererLayerId=4065#dir=0|tfl=3|checkSeats=1|st0=%D0%9C%D0%9E%D0%A1%D0%9A%D0%92%D0%90%7Ccode0=2000000|dt0=12.07.2013|st1=%D0%A1%D0%90%D0%9D%D0%9A%D0%A2-%D0%9F%D0%95%D0%A2%D0%95%D0%A0%D0%91%D0%A3%D0%A0%D0%93%7Ccode1=2004000|dt1=28.06.2013"
    browser.get(url) # Загружаем страницу
    ## browser.set_window_size(80,60) # Комментируем чтобы видеть экран
    time.sleep(2) # Пусть страница загрузится. Вдруг у нас медленный интернет...

    t=1
    start = time.clock()
    place_block=[]
    while len(place_block) == 0:
        try:
            print "Searching for html-element with trains..."
            # поиск элементов-поездов
            
            # place_block = browser.find_elements_by_class_name("trlist__trlist-row") # List of WebElements with trains
            place_block = browser.find_elements_by_class_name("trlist__table-price")
            place_block2 = browser.find_element_by_xpath('/html/body/div/table/tbody/tr/td[2]/div[6]/div[6]/table/tbody/tr')

        except NoSuchElementException:
            if (time.clock() - start) >= 20: # Если минуту не можем найти нужный блок, то возвращаем False (нет мест) и далее по ходу выполнения перезагружаем браузер
                print "Can't find element_by_xpath for 20 seconds. Probably server does not respond. Restart browser..."
                return False
            else:
                time.sleep(1)
            # print "can't open url"
        time.sleep(1)

    trains = [] #пустой список подходящих поездов
    print len(place_block), " - number of trains"
    print 'First element_by_xpath'
    print place_block2.text
    # Идём по всему списку Элементов-поездов и ищем наш тип места
    for n in range(0,len(place_block)):
        place_info = place_block[n].text
        print n, "-ii poezd"
        print place_info
        if place_info.find(place_type)>=0:
            print 'Found it! - place #', place_info.find(place_type)
            print n
            trains.append(n+1) # запоминаем порядковые номера поездов с подходящим типом места.
    # Проверяем нашлось ли что-то                    
    if len(trains) != 0:
        good_trains={} # пустой словарик для подходящих поездов
        print "Poezda - ", trains
        time.sleep(5)
        # Для каждого поезда
        for tn in trains:
            # Выбираем поезд (для 1 строчки особый случай)
            print "try to mark checkbox"
            start = time.clock()
            if tn == 1:
                checkbox = browser.find_element_by_xpath("/html/body/div/table/tbody/tr/td[2]/div[6]/div[6]/table/tbody/tr/td/input")
                checkbox.click()
            else:
                while True:
                    try:
                        checkbox = browser.find_element_by_xpath("/html/body/div/table/tbody/tr/td[2]/div[6]/div[6]/table/tbody/tr[" + str(tn) + "]/td/input")
                        checkbox.click()
                        print "Checkbox clicked!"
                        break
                    except NoSuchElementException:
                        print "Cant find it.."
                        if (time.clock() - start) >= 20: # Если минуту не можем найти нужный блок, то возвращаем False (нет мест) и далее по ходу выполнения перезагружаем браузер
                            print "Can't find element_by_xpath for 20 seconds. Probably server does not respond. Restart browser..."
                            return False
                        time.sleep(1)
            # Жмем на "Продолжить"
            print checkbox.is_selected()
            print "Press Continue..."
            browser.find_element_by_id("continueButton").click()
            
            # Собираем список доступных вагонов
            start = time.clock()
            cars = []
            while len(cars) == 0:
                try:
                    print "Searching for cars..."
                    cars = browser.find_elements_by_class_name("car-item")
                    print str(len(cars)) + "Cars found!"
                except NoSuchElementException:
                    print "Cant find it.."
                    if (time.clock() - start) >= 20: # Если минуту не можем найти нужный блок, то возвращаем False (нет мест) и далее по ходу выполнения перезагружаем браузер
                        print "Can't find element_by_xpath for 20 seconds. Probably server does not respond. Restart browser..."
                        return False
                time.sleep(1) # Ждём в этот момент, т.к. даже при недозагруженной страницу он находит элементы-вагоны о_О

            #Для каждого вагона
            print "Co to cars"
            for c in range(0, len(cars)):
                n=c+1 #реальный номер строки вагона
                # Ecли вагон подходит нашему запросу
                if place_type in cars[c].text:
                    print "looking at car #" + str(n)
                    # Составляем список доступных мест
                    if n == 1:
                        seats=browser.find_element_by_xpath("/html/body/div/table/tbody/tr/td[2]/div[3]/div/div/table[2]/tbody[2]/tr/td[7]/div")
                    else:
                        seats=browser.find_element_by_xpath("/html/body/div/table/tbody/tr/td[2]/div[3]/div/div/table[2]/tbody[2]/tr[" + str(n) + "]/td[7]/div")
                    
                    # Составляем список небоковушек из доступных мест
                    print seats.text.encode('utf-8','replace')
                    seats=seats.text.split('\n')
                    good_seats=[]
                    for i in range(0, len(seats)):
                        # Если не боковушка, то:
                        if u'\u0431\u043e\u043a\u043e\u0432\u044b\u0435' not in seats[i]:
                            good_seats.append(seats[i])
                            print seats[i], "  Good place!"

                    # Проверяем нашлись ли небоковушки
                    if len(good_seats) != 0:                    
                        # Запоминаем данные о поезде
                        
                        print "------Remembering the train-------"
                        train_data=browser.find_element_by_class_name("trlist-brief").text
                        if train_data not in good_trains.keys():
                            good_trains[train_data] = good_seats
                        else:
                            good_trains[train_data] += ['----'] + good_seats
                        for gs in good_seats:
                            print gs

                        print 

            # возвращаемся на страничку поездов
            print "go to the poezda-page"
            browser.back()
                    
        if len(good_trains) != 0:
            print
            print str(len(good_trains)) + " trains founded"
            print
            print "Founded trains :"
            for gt in good_trains.keys():
                print '---------------'
                print gt.encode('utf-8','replace') #Названия поездов
                print
                for s in good_trains[gt]:
                    print s # Доступные места
                print '---------------'
            return True
    # Если ничего не нашлось, то смотрим на часы, закрываем браузер и возвращаем False
    print "=("
    print time.asctime()
    print "--------------------------------------------------"
    print
    browser.quit()
    return False


#----------------------------------wrapper-----------------------------------------------------------
def rzhd():
    directions=[create_url(),]

    while raw_input('Want to add more directions? y/n ')=='y':
        directions.append(create_url())
        print "------------------"
    # n=raw_input('Check tickets every ...(seconds)? ')
    n = 60

    place=choose_place()
    i = 0
    display = Display(visible=0, size=(5, 5))
    display.start() # Запускаем вирутальный дисплей
    while len(directions)!=0:
        i+=1
        print
        print "----------------->Searching for PLATSKART<-----------------"

        print "try #",i
        print time.asctime()
        print

        for url in directions:
            if find_train(url, place)==True:
                send_email('dimka_b@inbox.ru', url)
                if raw_input('Did you buy ticket? y/n ')=='y':
                    directions.remove(url)
                    if len(directions) == 0:
                        print "Successfully bought all tickets!"
                        return True                
            print str(n)+" seconds until next try..."
            time.sleep(float(n)) # Дадим браузеру корректно завершиться
    display.stop() # Закрываем виртуальный дисплей
#----------------------------------/wrapper-----------------------------------------------------------

rzhd()

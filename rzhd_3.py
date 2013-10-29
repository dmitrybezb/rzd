# -*- coding: utf-8 -*
from selenium import webdriver # virtual browser
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display # virtual display
# email
import smtplib   
from email.mime.text import MIMEText 
# /email
import time
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
    if st0 == "":
        st0 = st0def
    st1=raw_input('To...')
    if st1 == "":
        st1 = st1def

        

    st0='code0='+ cities_codes[st0] +'|'
    st1='code1='+ cities_codes[st1] +'|'


    date="dt0="+raw_input("What day? (For ex: 12): ")+'.'+ raw_input("What month? (For ex: 07): ")+".2013|"
    time='ti0='+ raw_input("Since what time? (For ex: 19): ") +'-' + raw_input("Until what time? (For ex: 24): ")+'|' # asking for time

    url = "http://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735&layer_id=5354&refererVpId=1&refererPageId=704&refererLayerId=4065#dir=0|tfl=3|checkSeats=0|"+st0+date+time+st1

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


    browser = webdriver.Firefox() # Запускаем локальную сессию firefox
    # url = "http://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735&layer_id=5354&refererVpId=1&refererPageId=704&refererLayerId=4065#dir=0|tfl=3|checkSeats=1|st0=%D0%9C%D0%9E%D0%A1%D0%9A%D0%92%D0%90%7Ccode0=2000000|dt0=12.07.2013|st1=%D0%A1%D0%90%D0%9D%D0%9A%D0%A2-%D0%9F%D0%95%D0%A2%D0%95%D0%A0%D0%91%D0%A3%D0%A0%D0%93%7Ccode1=2004000|dt1=28.06.2013"
    browser.get(url) # Загружаем страницу
    time.sleep(2) # Пусть страница загрузится. Вдруг у нас медленный интернет...

    t=1
    while t !=0:
        try:
            print "Searching for element"
            place_block = browser.find_element_by_xpath("/html/body/div/table/tbody/tr/td[2]/div[6]/div[6]") #XPath требуемого элемента получить очень легко например при помощи firebug в firefox или devtools в chrome/safari.
            place_info = place_block.text
    ##            place_name  = place_info[1].split(',')[0] # Нас интересует только название, без типа заведения
    ##            place_address = place_info[2]
    ##            string_for_file = "Название: " +place_name+ "\tАдрес: " + place_address + "\n"
    ##            f = open("/home/user_name/my_pizza_list.txt", "a") # Если вы уже ведете такой список. Иначе не забудьте добавить правильный ключ для создания файла. Или создайте файл вручную.
    ##            f.write(string_for_file)
            t=0
        except NoSuchElementException:
            time.sleep(1)
            # print "can't open url"

            # assert 0, "can't open url"


    if place_info.find(place_type)>=0:
        # print place_info
        print 'Found it! - place #', place_info.find(place_type)
        # w.Beep(500,1000)
        return True
    else:
        print "=("
        print time.asctime()
        print "--------------------------------------------------"
        print
        browser.close()
        return False


#---------------------------------------------------------------------------------------------
def rzhd():
    directions=[create_url(),]

    while raw_input('Want to add more directions? y/n ')=='y':
        directions.append(create_url())
        print "------------------"
    n=raw_input('Check tickets every ...(seconds)? ')

    place=choose_place()
    i = 0
    display = Display(visible=0, size=(1024, 768))
    display.start() # Запускаем вирутальный дисплей
    while len(directions)!=0:
        i+=1
        print
        print "-----------------searching for PLATSKART---------------------------------"

        print "try #",i
        print time.asctime()
        print

        for url in directions:
            if find_train(url, place)==True:
                send_email('dmitrybezb@gmail.com', url)
                if raw_input('Did you buy ticket? y/n ')=='y':
                    directions.remove(url)
                

            if url==directions[-1]:
                print str(n)+" seconds until next try..."
                time.sleep(float(n)) # Дадим браузеру корректно завершиться
    display.stop()
rzhd()
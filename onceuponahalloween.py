import time
import telebot
import random
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3 as sq
#from scratch import passwords
#from scratch import used_passes


# bot = telebot.TeleBot(TOKEN)
bot = telebot.TeleBot("2094654197:AAEcnYfbcac5yawuLR4TV_v_rRQBFldRL5c")

users_timer = {}
paroles = ["112131"]
gods = ["Стрибог", "Симаргл", "Перун", "Дажьбог", 1]
foundgods = []
tips = []
# Моя попытка ввести переменную, которая считает все штрафы и поощрения,
# а в конце приплюсовывается к общему времени прохождения


def cTime(second):
    ts = time.gmtime(second)
    hour = time.strftime("%H", ts)
    min = time.strftime("%M", ts)
    sec = time.strftime("%S", ts)
    return f"{hour}ч:{min}м:{sec}с"


@bot.message_handler(commands=["start"])
def start_message(msg):
    cid = msg.chat.id
    con = sq.connect("questplayers.db", check_same_thread=False)
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS questplayers(
                    Username TEXT,
                    ID INTEGER
                    )""")
    con.commit()

    player_id = msg.chat.id
    cur.execute(f"SELECT ID FROM questplayers WHERE ID = {player_id}")
    data = cur.fetchone()
    if data is None:
        user_name = msg.from_user.username
        con.execute("INSERT INTO questplayers (Username, ID) VALUES (?, ?);", (user_name, cid))
        con.commit()

    bot.send_chat_action(cid, 'typing')
    time.sleep(3)
    bot.send_message(cid, "***Дисклеймер\n\n"
                          "Данный квест носит исключительно развлекательно-философский характер "
                          "и почти не ставит перед собой цель кого-то обидеть/оскорбить/унизить, неженки вы наши.\n"
                          "Чувство юмора автора и Ваше также могут отличаться, такое бывает.\n"
                          "Любые совпадения с событиями из жизни, реальными людьми и именами чисто случайны...\n"
                          "Или нет?\n"
                          "В общем, увидимся в суде! А пока что...***", parse_mode="Markdown")
    bot.send_chat_action(cid, "typing")
    time.sleep(6)
    bot.send_message(cid, "Здравствуйте, охотники за нечистью.\n"
                          "Новости пестрят заголовками о пропажах людей в районах Hradčany и Dejvice,\n"
                          "но до сих пор неизвестно, кто стоит за похищениями.")
    bot.send_chat_action(cid, "typing")
    time.sleep(6)
    bot.send_message(cid, "Учитывая, что даже я, хранитель этого мира квестов, не могу обнаружить виновного,"
                          "похоже, мы имеем дело с потусторонними силами.")
    bot.send_chat_action(cid, "typing")
    time.sleep(6)
    bot.send_message(cid, "Но вам нужно поторопиться, иначе другие охотники за нечистью разберутся с этим быстрее"
                          "и заберут всю славу себе!")
    bot.send_chat_action(cid, "typing")
    time.sleep(6)
    bot.send_message(cid, "***Введите пароль: ***", parse_mode="Markdown")
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    bot.send_message(cid, "***Но только после того, как прибудете на станцию метро Hradčanská,\n"
                          "чтобы не включить таймер раньше нужного.***", parse_mode="Markdown")
    bot.register_next_step_handler(msg, passright)


@bot.message_handler(content_types=["text"])
def passright(msg):
    cid = msg.chat.id
    abc = msg.text
    uid = msg.from_user.id
    chat = cid == uid and uid or cid

    #подключаемся к БД и открываем курсор
    connection = sq.connect("passwords.db", check_same_thread=False)
    cursor = connection.cursor()

    #проверяем правильность введенного пароля
    cursor.execute("SELECT keys FROM passes WHERE keys = ?", (abc,))
    rows = cursor.fetchall()

    #если нам вернулся один результат, значит пароль введен верный
    if len(rows) == 1:
        #пароль верный, удаляем пароль из базы данных, делаем коммит и закрываем коннект и курсор
        cursor.execute("DELETE from passes WHERE keys = ?", (abc,))
        connection.commit()
        cursor.close()
        connection.close()
        #запускаем сюжет
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Пароль верный, таймер запущен! "
                              "Удачной игры и приятных впечатлений!***", parse_mode="Markdown")

        users_timer[chat] = {'general_timer': int(time.time()), 'kikimora_trapped': 0,
                             'kikimora_place': 0, 'embrion_destroy': 0,
                             'wrong_time': 0, 'bonus_time': 0, 'kikimora_trapped_end': False,
                             'kikimora_place_end': False,
                             'embrion_destroy_end': False}

        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Ранее тут проходил важный торговый путь, "
                              "поэтому нам стоит поискать купцов и спросить, "
                              "не видели ли они чего-то необычного.\n")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Торговцы часто ездят по разным странам за пределами Евросоюза "
                              "и узнают много чего интересного и полезного, "
                              "так что купец-иностранец с какой-нибудь восточной страны, "
                              "богатой на фольклор – тот, кто нам нужен.\n\nИтак, "
                              "чьё народное творчество вам ближе всего?")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, '***На протяжении всего квеста у вас есть 3 бесплатные подсказки,\n'
                              'остальные же будут штрафоваться - чем больше спрашиваете,\nтем больше времени уйдёт '
                              'на прохождение.\nЧтобы получить помощь, напишите боту слово "Подсказка", '
                              'только и всего.***', parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "***Напишите название магазина, "
                              "где, по вашему мнению,\nмы сможем добыть нужную информацию: ***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, rus_shop)
    elif msg.text == "kikimora":
        bot.register_next_step_handler(msg, kikimora_place)
    elif msg.text == "leshy":
        bot.register_next_step_handler(msg, enterleshy)
    elif msg.text == "portal":
        bot.register_next_step_handler(msg, cheburekin)
    elif msg.text == "koshey":
        bot.register_next_step_handler(msg, mirror)
    elif msg.text == "embrion":
        bot.register_next_step_handler(msg, embrion)
    elif msg.text in paroles:
        cursor.close()
        connection.close()
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Пароль верный, таймер запущен! "
                              "Удачной игры и приятных впечатлений!***", parse_mode="Markdown")

        users_timer[chat] = {'general_timer': int(time.time()), 'kikimora_trapped': 0,
                             'kikimora_place': 0, 'embrion_destroy': 0,
                             'wrong_time': 0, 'bonus_time': 0, 'kikimora_trapped_end': False,
                             'kikimora_place_end': False,
                             'embrion_destroy_end': False}

        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Ранее тут проходил важный торговый путь, "
                              "поэтому нам стоит поискать купцов и спросить, "
                              "не видели ли они чего-то необычного.\n")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "Торговцы часто ездят по разным странам за пределами Евросоюза "
                              "и узнают много чего интересного и полезного, "
                              "так что купец-иностранец с какой-нибудь восточной страны, "
                              "богатой на фольклор – тот, кто нам нужен.\n\nИтак, "
                              "чьё народное творчество вам ближе всего?")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, '***На протяжении всего квеста у вас есть 3 бесплатные подсказки,\n'
                              'остальные же будут штрафоваться - чем больше спрашиваете,\nтем больше времени уйдёт '
                              'на прохождение.\nЧтобы получить помощь, напишите боту слово "Подсказка", '
                              'только и всего.***', parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "***Напишите название магазина, "
                              "где, по вашему мнению,\nмы сможем добыть нужную информацию: ***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, rus_shop)
    else:
        #пароль неверный, в любом случае закрываем коннект и курсор
        cursor.close()
        connection.close()
        #отправляем соответствующее сообщение
        bot.send_message(cid, "***Пароль неверный, а хотелось бы верный. Попробуйте ещё раз.***",
                        parse_mode="Markdown")
        bot.register_next_step_handler(msg, passright)


@bot.message_handler(content_types=["text"])
def rus_shop(msg):
    cid = msg.chat.id
    answer = ["Не думаю, что там могут что-то знать.",
              "Попробуйте поискать что-то более подходящее.",
              "Станут ли они вообще с вами говорить?",
              "Я бы к этим ребятам не совался!",
              "Они точно будут держать рот на замке.",
              "Меньше знаешь – крепче спишь, это их девиз по жизни!",
              "Не уверен, что это нам подходит."]
    if msg.text == "Ruske potraviny" or msg.text == "Ruské potraviny" or msg.text == "ruske potraviny" \
            or msg.text == "ruské potraviny" or msg.text == "Ruske Potraviny" or msg.text == "Ruské potraviny":
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "Хм, отличный вариант, уверен, там мы раздобудем нужную информацию и, "
                              "может, даже найдём какие-нибудь полезные артефакты.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Кстати, насчёт них. Пока вы собираете информацию, я продолжу свои исследования…\n"
                              "А вы спросите у купца, «знает ли он что-то о происшествиях в этих районах».")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "***В магазине вы получите красный символ с надписью, нужный для продолжения.\n"
                              "Введите сюда имя того, кому он принадлежит: ***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, scan_shop)
    elif msg.text.lower().strip() == "подсказка":
        if 1 not in tips:
            tips.append(1)
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, "Думаю, нам нужен магазинчик с привычными продуктами, по которым вы тоскуете, "
                                  "находясь здесь, в Чехии. Найдите его на карте и напишите название.")
            bot.register_next_step_handler(msg, rus_shop)
        else:
            bot.send_chat_action(cid, 'typing')
            time.sleep(2)
            bot.send_message(cid, "По-моему, подсказки лучше и быть не может: "
                                  "каких продуктов вам не хватает здесь, на чужбине?")
            bot.register_next_step_handler(msg, rus_shop)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(1)
        bot.send_message(cid, random.choice(answer))
        bot.register_next_step_handler(msg, rus_shop)
# Игроки пришли в магазин, получили папку с местом, ввели кодовое слово


@bot.message_handler(content_types=["text"])
def scan_shop(msg):
    cid = msg.chat.id
    if msg.text.lower().strip() == "велес":
        bot.send_chat_action(cid, 'typing')
        time.sleep(1)
        bot.send_message(cid, "Отличная работа, отправляемся туда!\n"
                              "А этот «артефакт», ну или его половину, "
                              "пока приберегите – чувствую, она нам ох как пригодится.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "***Придя на место, найдите наклейку "
                              "и введите сюда кодовое слово: ***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(2)
        bot.send_photo(cid, open("Location #1.png", "rb"))
        bot.register_next_step_handler(msg, kikimora_place)
    elif msg.text.lower().strip() == "подсказка":
        if 2 not in tips:
            tips.append(2)
            bot.send_chat_action(cid, 'typing')
            time.sleep(2)
            bot.send_message(cid, 'Красный символ с надписью? Что это, перевёрнутая "а"?')
            bot.register_next_step_handler(msg, scan_shop)
        elif 2 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(2)
            bot.send_message(cid, 'Это имя носит так называемый "скотий бог".')
            bot.register_next_step_handler(msg, scan_shop)
    else:
        bot.send_message(cid, "***Неверное кодовое слово. Вы сможете ввести правильный вариант, "
                              "я в вас верю!***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, scan_shop)

#Бот отследил геолокацию игроков и выдал им следующее сообщение, когда они пришли к парку


@bot.message_handler(content_types=["text"])
def kikimora_place(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid

    if msg.text.lower().strip() == "kidnapped":
        bot.send_chat_action(cid, 'typing')
        time.sleep(1)
        bot.send_message(cid, "Согласно информации, что вы добыли у купца, "
                              "последние следы похищений ведут к этой локации.\n"
                              "Поищем какие-нибудь зацепки, кто или что мог такое сделать.")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(8)
        bot.send_video(cid, open("Kikimora-Intro.mp4", "rb"), timeout=60)
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(70)
        bot.send_audio(cid, open("Kikimora #1.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(30)
        bot.send_message(cid, "Подождите, она сказала «Кикимора»? Хм, секундочку…\n"
                              "Персонаж старославянского фольклора, есть два типа: домовая и болотная.\n"
                              "Но её общая основная особенность в том, "
                              "что она невидима для обычного человеческого глаза, "
                              "поэтому мы лишь слышим её противный голос.")
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(15)
        bot.send_audio(cid, open("Kikimora #2.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(65)
        bot.send_message(cid, "Нам срочно нужно найти какую-то информацию об этой Кикиморе, "
                              "наверняка, ваши далёкие предки умели справляться с такими штуками, "
                              "не то, что нынешнее поколение!")
        bot.send_chat_action(cid, 'typing')
        time.sleep(15)
        bot.send_message(cid, "Что, не смотрите на меня! "
                              "Википедии нельзя верить, там же кто угодно может внести правки! "
                              "Эти существа были задолго до моего создания, а вот люди уже жили на этой планете, "
                              "поэтому вы должны знать какие-то слабости у этой Кикиморы, "
                              "может, она боится какого-то предмета, камня, амулета, да чего угодно?")
        bot.send_chat_action(cid, 'typing')
        time.sleep(12)
        bot.send_message(cid, "Для начала, осмотритесь вокруг, вдруг, мы найдём что-то полезное? "
                              "Только побыстрее, похоже, она настроена серьёзно!")
        bot.send_chat_action(cid, 'typing')
        time.sleep(8)
        bot.send_message(cid, "***У вас есть 5 минут, "
                              "чтобы найти решение и избежать наказания***", parse_mode="Markdown")
        users_timer[chat]['kikimora_place'] = int(time.time())
# Игроки ищут на локации кодовое слово.
# Запускается таймер в 3 минуты. После его истечения в общий зачёт идёт + 1 минута.
# Если слово найдено вовремя, то -30 секунд
        bot.register_next_step_handler(msg, kikimora_trapped)
    elif msg.text.lower().strip() == "подсказка":
        if 3 not in tips:
            tips.append(3)
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, "Кажется, стрелка на карте чётко показывает, где искать наклейку со словом.")
            bot.register_next_step_handler(msg, kikimora_place)
        elif 3 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, "Наклейка не липнет к деревьям или земле. Остаются столбы?")
            bot.register_next_step_handler(msg, kikimora_place)

    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Неверное кодовое слово. Ищите внимательнее, ей богу, "
                              "первый раз в Праге?***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, kikimora_place)
# Игроки нашли наклейку с рисунком "куриного Бога" и кодовым словом


@bot.message_handler(content_types=['text'])
def kikimora_trapped(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid

    text = msg.text
    if users_timer[chat]['kikimora_place'] + 300 <= int(time.time()) and users_timer[chat]['kikimora_place_end'] == False:
        users_timer[chat]['wrong_time'] += 120  # время штрафа в секундах, когда таймер запустили на 3 минуты
        users_timer[chat]['kikimora_place_end'] = True
        bot.send_message(cid, "***+2 минуты к общему времени за медлительность***", parse_mode="Markdown")

    if text.lower().strip() == "апотропей":
        if users_timer[chat]['kikimora_place_end'] == False:
            bot.send_message(cid, "***-1 минута от общего времени за скорость!***", parse_mode="Markdown")
            users_timer[chat]['bonus_time'] += 60
            # вычисление остатка таймера на 30 секунд, эти бонусные секунды идут с минусом, отнимаем общее время

        bot.send_chat_action(cid, 'record_voice')
        time.sleep(3)
        bot.send_audio(cid, open("Kikimora Trapped #1.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(15)
        bot.send_message(cid, "Это что, «Куриный бог»? Ну и название...\n"
                              "Зато сам камушек довольно действенный. "
                              "Но вряд ли эффект долго продержится, нужно парализовать её!")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, '***4 конца, словно стороны света,\n'
                              'Он символ у старых и новых заветов.\n'
                              'Хоть всюду кричат, что жизнь он даёт,\n'
                              'Пойди против Бога – мигом убьёт!\n'
                              'Он признак распутья и знак тупика,\n'
                              'Он – место на карте, где наверняка\n'
                              'Зарыт чей-то клад, не взирая на то,\n'
                              'Что с лёгкостью ты им закроешь окно.***', parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_message(cid, "Что это?")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "***У вас есть 45 секунд, чтобы верно ответить "
                              "и избежать наказания***", parse_mode="Markdown")
        users_timer[chat]['kikimora_trapped'] = int(time.time())
# Таймер на 30 секунд, по истечении которого, а также за неверный ответ добавляется 30 секунд в общее время
        bot.register_next_step_handler(msg, kikimora_final)
    else:
        bot.send_message(cid, "***Ищите внимательнее и поторопитесь - "
                              "время играет против вас!***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, kikimora_trapped)


@bot.message_handler(content_types=['text'])
def kikimora_final(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid

    text = msg.text
    if users_timer[chat]['kikimora_trapped'] + 45 <= int(time.time()) and users_timer[chat]['kikimora_trapped_end'] == False:  # выполнит, если время вышло
        users_timer[chat]['wrong_time'] += 60  # время штрафа в секундах, когда таймер запустили на 30 секунд
        users_timer[chat]['kikimora_trapped_end'] = True
        bot.send_message(cid, "***+1 минута к общему зачёту за вальяжность***", parse_mode="Markdown")

    if text.lower().strip() == "крест":
        if users_timer[chat]['kikimora_trapped_end'] == False:
            bot.send_message(cid, "***-15 секунд от общего времени за скорость.***", parse_mode="Markdown")
            users_timer[chat]['bonus_time'] += 15

        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("KikimoraKrest.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_message(cid, "Фух, кажется, справились.\n"
                              "Ох уж эти древнеславянские приёмчики… "
                              "Итак, Кикимора, ты вполне способна навести суету среди людей, "
                              "но не похоже, чтоб ты их похищала… ")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Kikimora's End #1.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(20)
        bot.send_message(cid, "Подожди, что? Ты сказала «Лешего»?")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(7)
        bot.send_video(cid, open("Kikimora's End #2.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(20)
        bot.send_message(cid, "То есть, кроме тебя с Лешим есть кто-то ещё? Кто?")
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(8)
        bot.send_video(cid, open("Kikimora's End #3.mp4", "rb"))
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(25)
        bot.send_photo(cid, open("Mask.jpg", "rb"))
        bot.send_message(cid, "***Achievement “Masks Off, Masks On”\n"
                              "Поможет в диалоге с Лешим,\n"
                              "в борьбе – не поможет ничто!***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(7)
        bot.send_photo(cid, open("Half Sign.jpg", "rb"))
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(15)
        bot.send_photo(cid, open("Letter B.png", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "Что это за чёрный символ?\n"
                              "Хм, возможно, он подойдёт в этот шифр, который нам дали в лавке?\n"
                              "А эта половинка красного символа кажется знакомой…")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "***Сложите две половинки и напишите имя бога, обладателя этого символа, "
                              "чтобы зачаровать свой смартфон***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "***Ч.. меня, ... .\n.у. я сижу у окна.\n ..р я первый.***", parse_mode="Markdown")
        bot.send_photo(cid, open("Leshy Map.png", "rb"))
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(10)
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(10)
        bot.send_photo(cid, open("Location #2.png", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "А здесь мы найдём Лешего!")
        bot.register_next_step_handler(msg, roadtoleshy)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Неверный ответ.\n+30 секунд к общему времени***", parse_mode="Markdown")
            
        users_timer[chat]['wrong_time'] += 30
        
        bot.register_next_step_handler(msg, kikimora_final)


@bot.message_handler(content_types=['text'])
def roadtoleshy(msg):
    cid = msg.chat.id
    if msg.text.lower().strip() == "чур":
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, '***«Вы зачаровали свой смартфон и теперь через него '
                              'сможете видеть существ из другого измерения»***', parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Отлично, теперь даже я смогу видеть этих существ.\n"
                              "Ну что, отправляемся к Лешему, пора уже остановить эти похищения!")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "***На месте найдите кодовое слово и введите его сюда: ***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(25)
        bot.send_video(cid, open("Portal #1.mp4", "rb"))
        bot.register_next_step_handler(msg, enterleshy)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Ничего не произошло, попробуйте другой символ***", parse_mode="Markdown")
        bot.send_message(cid, "Ну ребята. Что вы, как не славяне?")
        bot.register_next_step_handler(msg, roadtoleshy)


@bot.message_handler(content_types=['text'])
def enterleshy(msg):
    cid = msg.chat.id
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if msg.text.lower().strip() == "лешачиха":
        bot.send_message(cid, "Так, и где нам тут искать Лешего? Я Лешачихой притворяться не буду, "
                              "среди нас есть персонажи куда обаятельнее.")
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy Intro.mp3", "rb"))
        bot.send_chat_action(cid, 'record_video')
        time.sleep(20)
        bot.send_video(cid, open("EnterLeshy.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        kb.row_width = 1
        button_a1 = types.KeyboardButton("Это ты нам говоришь?\nПохищаешь людей, "
                                         "а затем просишь сострадания?")
        button_b1 = types.KeyboardButton("Извини, но что именно ты имеешь ввиду?\nО какой жестокости идёт речь?")
        button_c1 = types.KeyboardButton("Ты же Леший, верно?\n"
                                         "Кикимора рассказала нам, что ты стоишь за похищениями людей.")
        kb.add(button_a1, button_b1, button_c1)
        bot.send_message(cid, "Ну и махина! Такого громилу так просто, как Кикимору, не остановишь…\n"
                              "Но помните, нам ещё нужно узнать о других существах.", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_first_choice)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Нет, неверно. Как зовут лешего-женщину?***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, enterleshy)


@bot.message_handler(content_types=['text'])
def leshy_first_choice(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    a = ReplyKeyboardRemove()
    if msg.text == "Это ты нам говоришь?\nПохищаешь людей, а затем просишь сострадания?":
        kb.row_width = 1
        button_b2 = types.KeyboardButton("Мы схватили Кикимору и получили от неё артефакт, который даёт иммунитет к твоим феромонам.")
        button_c2 = types.KeyboardButton("Ох, судьба действительно жестоко с тобой обошлась.")
        button_a2 = types.KeyboardButton("После того, как мы связали Кикимору, "
                                         "она дала нам артефакт, который предотвращает эффект твоих феромонов.")
        kb.add(button_b2, button_c2, button_a2)
        bot.send_message(cid, "***+1 минута к общему времени.***", parse_mode="Markdown", reply_markup=a)

        users_timer[chat]['wrong_time'] += 60

        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy A1.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(60)
        bot.send_message(cid, "_До сих пор нет гипнотизирующего эффекта, интересно, почему?_",
                         parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_test_choice)
    elif msg.text == "Ты же Леший, верно?\nКикимора рассказала нам, что ты стоишь за похищениями людей.":
        kb.row_width = 1
        button_b2 = types.KeyboardButton("Мы схватили Кикимору и получили от неё артефакт, который даёт иммунитет к твоим феромонам.")
        button_c2 = types.KeyboardButton("Ох, судьба действительно жестоко с тобой обошлась.")
        button_a2 = types.KeyboardButton("После того, как мы связали Кикимору, "
                                         "она дала нам артефакт, который предотвращает эффект твоих феромонов.")
        kb.add(button_c2, button_b2, button_a2)
        bot.send_message(cid, "***Выбор не повлиял "
                              "на общее время прохождения.***", parse_mode="Markdown", reply_markup=a)

        users_timer[chat]['bonus_time'] += 0
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy C1.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(55)
        bot.send_message(cid, "_До сих пор нет гипнотизирующего эффекта, интересно, почему?_",
                         parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_test_choice)
    elif msg.text == "Извини, но что именно ты имеешь ввиду?\nО какой жестокости идёт речь?":
        kb.row_width = 1
        button_b2 = types.KeyboardButton("Мы схватили Кикимору и получили от неё артефакт, который даёт иммунитет к твоим феромонам.")
        button_c2 = types.KeyboardButton("Ох, судьба действительно жестоко с тобой обошлась.")
        button_a2 = types.KeyboardButton("После того, как мы связали Кикимору, "
                                         "она дала нам артефакт, который предотвращает эффект твоих феромонов.")
        kb.add(button_b2, button_c2, button_a2)
        bot.send_message(cid, "***-30 секунд от общего времени.***", parse_mode="Markdown", reply_markup=a)

        users_timer[chat]['bonus_time'] += 30

        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy B1.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(45)
        bot.send_message(cid, "_До сих пор нет гипнотизирующего эффекта, интересно, почему?_",
                         parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_test_choice)


@bot.message_handler(content_types=['text'])
def leshy_test_choice(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    a = ReplyKeyboardRemove()
    if msg.text == "Мы схватили Кикимору и получили от неё артефакт, который даёт иммунитет к твоим феромонам.":
        kb.row_width = 1
        button_c3 = types.KeyboardButton("Да уж, не позавидуешь такой участи.")
        button_a3 = types.KeyboardButton("Значит, несмотря на своё нутро, ты всё равно выходил и, "
                                         "по сути, убивал людей, повесив на это ярлык «поиска любви»?")
        button_b3 = types.KeyboardButton("Ужасная история.")
        kb.add(button_c3, button_a3, button_b3)
        bot.send_message(cid, "***+1 минута к общему времени.***", parse_mode="Markdown", reply_markup=a)

        users_timer[chat]['wrong_time'] += 60

        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "Не тебе говорить о жестокости, "
                              "когда одно твоё естество убивает невинных людей, "
                              "которым не повезло встретиться с тобой! Почему они вообще на тебя натыкались?")
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy A2.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(95)
        bot.send_message(cid, "_Побудьте с моё в одиночестве и "
                              "совершенно по-другому взглянете на эти вещи!_",
                         parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_third_choice)
    elif msg.text == "После того, как мы связали Кикимору, "\
                     "она дала нам артефакт, который предотвращает эффект твоих феромонов.":
        kb.row_width = 1
        button_c3 = types.KeyboardButton("Да уж, не позавидуешь такой участи.")
        button_a3 = types.KeyboardButton("Значит, несмотря на своё нутро, ты всё равно выходил и, "
                                         "по сути, убивал людей, повесив на это ярлык «поиска любви»?")
        button_b3 = types.KeyboardButton("Ужасная история.")
        kb.add(button_c3, button_a3, button_b3)
        bot.send_message(cid, "***Выбор не повлиял "
                              "на общее время прохождения.***", parse_mode="Markdown", reply_markup=a)

        users_timer[chat]['bonus_time'] += 0
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "И после сказанного не особо похоже, что ты не наслаждался мучениями жертв. "
                              "Более того, ты продолжал выходить к людям, зная, какой конец ждёт большинство из них. "
                              "Ведь так? Что ты хотел там найти?")
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy C2.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(70)
        bot.send_message(cid, "_Но чем больше я смотрел за людьми, за их отношениями…_",
                         parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_third_choice)
    elif msg.text == "Ох, судьба действительно жестоко с тобой обошлась.":
        kb.row_width = 1
        button_c3 = types.KeyboardButton("Да уж, не позавидуешь такой участи.")
        button_a3 = types.KeyboardButton("Значит, несмотря на своё нутро, ты всё равно выходил и, "
                                         "по сути, убивал людей, повесив на это ярлык «поиска любви»?")
        button_b3 = types.KeyboardButton("Ужасная история.")
        kb.add(button_c3, button_a3, button_b3)
        bot.send_message(cid, "***-30 секунд от общего времени.***", parse_mode="Markdown", reply_markup=a)

        users_timer[chat]['bonus_time'] += 30
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "После того, как мы связали Кикимору, она дала нам артефакт, "
                              "который предотвращает эффект феромонов, полагаю, "
                              "на других существ из твоего мира они тоже не действуют?")
        bot.send_chat_action(cid, 'typing')
        time.sleep(6)
        bot.send_message(cid, "Но, если ты прячешься вдали от людей, "
                              "как те попадали под гипнотическое влияние и шли за тобой? "
                              "Всё-таки это довольно мучительный конец… Разве все люди до единого его заслужили?")

        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy B2.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(85)
        bot.send_message(cid, "_Конечно, такое не у всех, но обратные случаи я могу по пальцам пересчитать._",
                         parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_third_choice)


@bot.message_handler(content_types=['text'])
def leshy_third_choice(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    a = ReplyKeyboardRemove()
    if msg.text == "Да уж, не позавидуешь такой участи.":
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Выбор не повлиял "
                              "на общее время прохождения.***", parse_mode="Markdown", reply_markup=a)

        users_timer[chat]['bonus_time'] += 0
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "Но, с другой стороны, тебя не остановили все эти жертвы, "
                              "ты просто принял ситуацию как должное.\n")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "Хотя сам говорил, что в твоём измерении у всех иммунитет на твои феромоны. "
                              "Почему бы не поискать любовь там? Кстати, ты ведь попал сюда через портал? "
                              "Кто ещё вместе с тобой и Кикиморой прошёл через него?")
        kb.row_width = 1
        button_c4 = types.KeyboardButton("Что ж, значит, пора положить конец этим непреднамеренным, "
                                         "но убийствам...")
        button_a4 = types.KeyboardButton("Это мы уже сами решим. У неё точно должна быть какая-то слабость.")
        button_b4 = types.KeyboardButton("Как будто, тебе нужно было родиться в другом измерении, "
                                         "например, нашем.")
        kb.add(button_b4, button_c4, button_a4)
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy C3.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(40)
        bot.send_message(cid, "_Никто не переживал встречи с ней._", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_forth_choice)
    elif msg.text == "Значит, несмотря на своё нутро, ты всё равно выходил и, " \
                     "по сути, убивал людей, повесив на это ярлык «поиска любви»?":
        users_timer[chat]['wrong_time'] += 60
        bot.send_message(cid, "***+1 минута к общему времени.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "Знаешь, кто ты? Ты – жестокий эгоист, который заботится только о себе, "
                              "готовый пойти по головам, лишь бы не быть одному. ")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "А как же тебе не быть одному, когда ты убиваешь всех вокруг себя? "
                              "Да ты настоящий монстр, может, у вас в измерении это норма, но не здесь, "
                              "поэтому мы остановим этот беспредел!\n"
                              "Кто ещё вместе с тобой и Кикиморой вышел из портала?")
        kb.row_width = 1
        button_c4 = types.KeyboardButton("Что ж, значит, пора положить конец этим непреднамеренным, "
                                         "но убийствам...")
        button_a4 = types.KeyboardButton("Это мы уже сами решим. У неё точно должна быть какая-то слабость.")
        button_b4 = types.KeyboardButton("Как будто, тебе нужно было родиться в другом измерении, "
                                         "например, нашем.")
        kb.add(button_b4, button_c4, button_a4)
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy A3.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(40)
        bot.send_message(cid, "_Никто не переживал встречи с ней._", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_forth_choice)
    elif msg.text == "Ужасная история.":
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        users_timer[chat]['bonus_time'] += 30
        bot.send_message(cid, "***-30 секунд от общего времени.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "Особенно иронично то, что ты прав: люди, "
                              "которым доступны все эти тёплые моменты, "
                              "в большинстве своём совершенно их не ценят или ищут тепло там, "
                              "где давно холод, но отвергают то, что им дают другие.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "А ты всё это время смотришь и мечтаешь хотя бы о половине этого. "
                              "Но если для людей так опасны эти феромоны, "
                              "а на существ с твоего измерения они не действуют, может, "
                              "стоит поискать кого-то там? Кстати, ты же сюда попал через портал? "
                              "Не помнишь, кто ещё вместе с тобой и Кикиморой выходил через него?")
        kb.row_width = 1
        button_c4 = types.KeyboardButton("Что ж, значит, пора положить конец этим непреднамеренным, "
                                         "но убийствам...")
        button_a4 = types.KeyboardButton("Это мы уже сами решим. У неё точно должна быть какая-то слабость.")
        button_b4 = types.KeyboardButton("Как будто, тебе нужно было родиться в другом измерении, "
                                         "например, нашем.")
        kb.add(button_b4, button_c4, button_a4)
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy B3.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(38)
        bot.send_message(cid, "_Никто не переживал встречи с ней._", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_forth_choice)


@bot.message_handler(content_types=['text'])
def leshy_forth_choice(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    a = ReplyKeyboardRemove()
    if msg.text == "Что ж, значит, пора положить конец этим непреднамеренным, но убийствам...":
        kb.row_width = 1
        button_c5 = types.KeyboardButton("Хорошо, мы выясним, что за место и тут же отправимся туда.")
        button_a5 = types.KeyboardButton("Да уж, не густо, но хотя бы так.")
        button_b5 = types.KeyboardButton("Мы тут же отправимся туда...")
        kb.add(button_c5, button_a5, button_b5)
        bot.send_message(cid, "***Выбор не повлиял "
                              "на общее время прохождения.***", parse_mode="Markdown", reply_markup=a)

        users_timer[chat]['bonus_time'] += 0
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "А Баба-Яга… "
                              "Даже у такого могущественного существа должна быть слабость, "
                              "это же баланс всего живого во Вселенной.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "А раз она в нашем измерении, значит, что-то из этого окружения может на неё повлиять. "
                              "Более того, в славянском фольклоре множество упоминаний о ней.\n"
                              "Леший, скажи, где нам искать информацию о слабостях Бабы-Яги?")
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy ABC4.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(35)
        bot.send_message(cid, "_Там могут что-то знать о Бабе-Яге._", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_fifth_choice)
    elif msg.text == "Это мы уже сами решим. У неё точно должна быть какая-то слабость.":
        kb.row_width = 1
        button_c5 = types.KeyboardButton("Хорошо, мы выясним, что за место и тут же отправимся туда.")
        button_a5 = types.KeyboardButton("Да уж, не густо, но хотя бы так.")
        button_b5 = types.KeyboardButton("Мы тут же отправимся туда...")
        kb.add(button_c5, button_a5, button_b5)
        users_timer[chat]['wrong_time'] += 60
        bot.send_message(cid, "***+1 минута к общему времени.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "Почему Баба-Яга снова пришла в наше измерение?" 
                         "А если люди про неё и вообще про вас всех столько раз упоминали в фольклоре, "
                              "значит, кто-то наверняка обнаружил нечто, что может нам помочь.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Сделай наконец доброе дело, если так хочешь, "
                              "чтобы в тебе перестали видеть монстра – скажи, "
                              "где мы можем найти информацию о слабостях Бабы-Яги?")
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy ABC4.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(35)
        bot.send_message(cid, "_Там могут что-то знать о Бабе-Яге._", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_fifth_choice)
    elif msg.text == "Как будто, тебе нужно было родиться в другом измерении, например, нашем.":
        kb.row_width = 1
        button_c5 = types.KeyboardButton("Хорошо, мы выясним, что за место и тут же отправимся туда.")
        button_a5 = types.KeyboardButton("Да уж, не густо, но хотя бы так.")
        button_b5 = types.KeyboardButton("Мы тут же отправимся туда...")
        kb.add(button_c5, button_a5, button_b5)
        users_timer[chat]['bonus_time'] += 30
        bot.send_message(cid, "***-30 секунд от общего времени.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "У тебя всё-таки доброе сердце, "
                              "но перспектива быть уничтоженным Бабой-Ягой, конечно, не радужная.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(6)
        bot.send_message(cid, "Хоть даже у такого могущественного существа должна быть слабость, "
                              "это же баланс всего живого во Вселенной.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "А раз она в нашем измерении, "
                              "значит, что-то из этого окружения может на неё повлиять. "
                              "Более того, в славянском фольклоре множество упоминаний о ней, "
                              "а вот в сети нет ничего об этом.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(6)
        bot.send_message(cid, "Леший, помоги, пожалуйста, где нам искать информацию о слабостях Бабы-Яги?")
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Leshy ABC4.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(35)
        bot.send_message(cid, "_Там могут что-то знать о Бабе-Яге._", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, leshy_fifth_choice)


@bot.message_handler(content_types=['text'])
def leshy_fifth_choice(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    if msg.text == "Хорошо, мы выясним, что за место и тут же отправимся туда.":
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Выбор не повлиял "
                              "на общее время прохождения.***", parse_mode="Markdown")

        users_timer[chat]['bonus_time'] += 0
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "А тебе всё же лучше вернуться в своё измерение. "
                              "И да, мы оставили Кикимору в одном парке, думаю, вам есть что обсудить, "
                              "т.к. одно лишь упоминание о тебе заставило её кровь кипеть. "
                              "Не просто так это всё…")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(10)
        bot.send_video(cid, open("Leshy Final.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_photo(cid, open("cheburek.png", "rb"))
        bot.send_message(cid, "***Achievement “Sniff-snoff”\n"
                              "Чувствуете? Это запах приключений!***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_photo(cid, open("Letter C.png", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, 'Кажется, я что-то слышал о заведении, которое пытался вспомнить Леший. '
                              'Для обычных людей оно выглядит довольно "экзотическим" - '
                              'уж очень много странных личностей любит там появляться.')
        bot.send_chat_action(cid, 'typing')
        time.sleep(8)
        bot.send_message(cid, "Только никак не могу вспомнить название, реально, какое-то чудное...")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "***Так что, куда идём?***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Portal #2.mp4", "rb"))
        bot.register_next_step_handler(msg, cheburekin)
    elif msg.text == "Да уж, не густо, но хотя бы так.":
        users_timer[chat]['wrong_time'] += 60
        bot.send_message(cid, "***+1 минута к общему времени.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "А тебе следует скорее вернуться обратно в своё измерение, "
                              "пока ещё дров тут не наломал.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "И Кикимору захвати, вы друг друга стоите, как раз отличная пара получится. "
                              "Эх, было бы понятнее, будь ты просто злым…")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(10)
        bot.send_video(cid, open("Leshy Final.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_photo(cid, open("cheburek.png", "rb"))
        bot.send_message(cid, "***Achievement “Sniff-snoff”\n"
                              "Чувствуете? Это запах приключений!***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_photo(cid, open("Letter C.png", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, 'Кажется, я что-то слышал о заведении, которое пытался вспомнить Леший. '
                              'Для обычных людей оно выглядит довольно "экзотическим" - '
                              'уж очень много странных личностей любит там появляться.')
        bot.send_chat_action(cid, 'typing')
        time.sleep(8)
        bot.send_message(cid, "Только никак не могу вспомнить название, реально, какое-то чудное...")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "***Так что, куда идём?***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Portal #2.mp4", "rb"))
        bot.register_next_step_handler(msg, cheburekin)
    elif msg.text == "Мы тут же отправимся туда...":
        users_timer[chat]['bonus_time'] += 30
        bot.send_message(cid, "***-30 секунд от общего времени.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "Большое спасибо! "
                              "А тебе, пожалуй, стоит вернуться в своё измерение. "
                              "Кстати, насчёт светлых чувств и силы… ")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "Каким бы странным это ни казалось, но, кажется, ты нравишься Кикиморе. "
                              "Так что по пути обратно пройди мимо одного парка, "
                              "где мы её оставили, и выясните наконец, что между вами происходит. Счастливо!")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(10)
        bot.send_video(cid, open("Leshy Final.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_photo(cid, open("cheburek.png", "rb"))
        bot.send_message(cid, "***Achievement “Sniff-snoff”\n"
                              "Чувствуете? Это запах приключений!***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_photo(cid, open("Letter C.png", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, 'Кажется, я что-то слышал о заведении, которое пытался вспомнить Леший. '
                              'Для обычных людей оно выглядит довольно "экзотическим" - '
                              'уж очень много странных личностей любит там появляться.')
        bot.send_chat_action(cid, 'typing')
        time.sleep(8)
        bot.send_message(cid, "Только никак не могу вспомнить название, реально, какое-то чудное...")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "***Так что, куда идём?***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Portal #2.mp4", "rb"))
        bot.register_next_step_handler(msg, cheburekin)


@bot.message_handler(content_types=['text'])
def cheburekin(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    places = ['Не уверен, что это то место.', 'Определённо не это.',
              'Таверной, где собираются охотники за нечистью, даже не пахнет.',
              'Здесь мы точно ничего не узнаем.']
    if msg.text == "Ceburekin" or msg.text == "Čeburekin" or msg.text == "ceburekin":
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, 'Точно, теперь всё встало на свои места. '
                              'А ещё я слышал, что там отменная еда, и по одному лишь заказу местные сразу поймут, '
                              '"свой" ли перед ними или обычный зевака.')
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, 'Поэтому вот, что вы должны сказать:\n\n'
                              '"***Нам, пожалуйста, чебуреки (*выберите, кому какой, с мясом или 5 сырами*). '
                              'И погорячее!"***\n\n'
                              'Тогда хозяин таверны поймёт, что вы тоже охотники за нечистью, '
                              'и разговор будет идти уже по-другому.', parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "***На месте вам покажут символ, напишите здесь имя того, "
                              "кто там изображён: ***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, cult_portal)
    elif msg.text.lower().strip() == "подсказка":
        if len(tips) > 3:
            users_timer[chat]['wrong_time'] += 120
            bot.send_message(cid, "***Превышение кол-ва подсказок!\n"
                                  "+2 минуты за неуверенность в своих силах.***", parse_mode="Markdown")
        if 4 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, "Фото чебурека...\n"
                                  "Возможно, оно как-то намекает на название таверны?")
            bot.register_next_step_handler(msg, cheburekin)
        elif 4 not in tips:
            tips.append(4)
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, 'Он сказал "на зелёной улице рядом с одноимённой остановкой".\n'
                                  'Думаю, найти это место на карте не составит труда.')
            bot.register_next_step_handler(msg, cheburekin)

    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, random.choice(places))
        bot.register_next_step_handler(msg, cheburekin)


@bot.message_handler(content_types=['text'])
def cult_portal(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    if msg.text == "Бафомет" or msg.text == "бафомет":
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid,
                         "***Бесконечная сила старославянских предков и ваших пустых желудков "
                         "остановила таймер на 30 минут, "
                         "чтобы вы успели хорошенько подкрепиться.***", parse_mode="Markdown")

        users_timer[chat]['bonus_time'] += 1800

        bot.send_chat_action(cid, 'record_voice')
        time.sleep(10)
        bot.send_audio(cid, open("Satanist #1.mp3", "rb"))
        bot.send_chat_action(cid, 'record_video')
        time.sleep(30)
        bot.send_video(cid, open("Portal Final.mp4", "rb"))
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(100)
        bot.send_audio(cid, open("Satanist #2.mp3", "rb"))
        bot.send_chat_action(cid, 'record_voice')
        bot.send_chat_action(cid, 'typing')
        time.sleep(95)
        bot.send_message(cid, '"Памятник... Мост...\n'
                              'Король нечисти..."\nХм...'
                              'Вас тоже бесит обилие многоточий?\n'
                              'Что Кощей не побрезгует использовать в качестве своего тотема?\n'
                              'Он же - аристократия среди нечисти!')
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_message(cid, 'Думаю, ваши зачарованные телефоны смогут распознать, '
                              'тотем ли это или нет, если вы опишете предполагаемый объект, встав рядом с ним.')
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, '***Найдите аббревиатуру на предполагаемом тотеме '
                              'и напишите её сюда: ***', parse_mode="Markdown")
        bot.register_next_step_handler(msg, enterkoshey)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***Нет, этот символ называется по-другому.\n"
                              "Есть в нём что-то потустороннее...***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, cult_portal)


@bot.message_handler(content_types=['text'])
def enterkoshey(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    wrong_answer = ["Неверная аббревиатура, присмотритесь внимательнее.", "Не думаю, что там написано именно это.",
                    "Этого на тотеме точно нет.", "Попробуйте по-другому.", "Нет, видимо, это не тотем Кощея",
                    "Не зря же Кощея зовут Царём или Королём нечисти.",
                    "Мостом между мирами для Кощея это точно не станет."]
    if msg.text.strip() == "KQASLU":
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_message(cid, "Сейчас же должно что-то произойти, верно? Не силён я в этих ваших языческих штучках...")
        bot.send_video(cid, open("Koshey Intro.mp4", "rb"))
        bot.send_chat_action(cid, 'record_video')
        time.sleep(50)
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row_width = 1
        button_1 = types.KeyboardButton("Ты знаешь, как остановить Бабу-Ягу?")
        button_2 = types.KeyboardButton("Ты действительно Кощей Бессмертный?")
        button_3 = types.KeyboardButton("Ты же вселяешься в эти «тотемы», как ты хочешь разломить кого-то пополам?")
        kb.add(button_2, button_3, button_1)
        bot.send_message(cid, "_Зачем вы связались со мной?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, koshey_intro)
    elif msg.text.lower().strip() == "подсказка":
        if len(tips) > 3:
            users_timer[chat]['wrong_time'] += 120
            bot.send_message(cid, "***Превышение кол-ва подсказок!\n"
                                  "+2 минуты за неуверенность в своих силах.***", parse_mode="Markdown")
        if 5 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, "А что, если памятник и мост носят одно имя? Кто такой великий в Чехии?\n"
                                  "Менее значимый предмет Кощей бы не выбрал в качестве тотема.")
            bot.register_next_step_handler(msg, enterkoshey)
        elif 5 not in tips:
            tips.append(5)
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, 'Наверно, это памятник какому-то королю, так ещё и рядом с мостом?\n'
                                  'На нём как раз аббревиатура, а значит, подпись, что это, кому это.')
            bot.register_next_step_handler(msg, enterkoshey)

    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, random.choice(wrong_answer))
        bot.register_next_step_handler(msg, enterkoshey)


@bot.message_handler(content_types=['text'])
def koshey_intro(msg):
    cid = msg.chat.id
    if msg.text == "Ты действительно Кощей Бессмертный?":
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Koshey Optional #2.mp4", "rb"))
        time.sleep(30)
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row_width = 1
        button_1 = types.KeyboardButton("Ты знаешь, как остановить Бабу-Ягу?")
        button_3 = types.KeyboardButton("Ты же вселяешься в эти «тотемы», как ты хочешь разломить кого-то пополам?")
        kb.add(button_3, button_1)
        bot.send_message(cid, "_Для чего вы вышли со мной на контакт?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, koshey_intro)
    elif msg.text == "Ты же вселяешься в эти «тотемы», как ты хочешь разломить кого-то пополам?":
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Koshey Optional #1.mp4", "rb"))
        time.sleep(30)
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row_width = 1
        button_1 = types.KeyboardButton("Ты знаешь, как остановить Бабу-Ягу?")
        button_3 = types.KeyboardButton("Ты действительно Кощей Бессмертный?")
        kb.add(button_3, button_1)
        bot.send_message(cid, "_Для чего вы вышли со мной на контакт?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, koshey_intro)
    elif msg.text == "Ты знаешь, как остановить Бабу-Ягу?":
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Koshey Main #1.mp4", "rb"))
        time.sleep(70)
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row_width = 1
        button_1 = types.KeyboardButton("Да")
        button_2 = types.KeyboardButton("Нет")
        kb.add(button_1, button_2)
        bot.send_message(cid, "_Готовы?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, first_riddle)


@bot.message_handler(content_types=['text'])
def first_riddle(msg):
    cid = msg.chat.id
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    notready = ['Что ж, можете подождать, пока Баба-Яга уничтожит человечество, мне спешить некуда.',
                "Разве вы не ограничены во времени? Всё-таки я здесь древнее существо, а не вы.",
                "Хорошо, подготовьтесь как следует.", "Понимаю, но времени на подготовку у вас не так много."]
    if msg.text == "Да":
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "- Начнём с простого:\n\n"
                              "***“ Он с жадностью пьет —\n"
                              "А не чувствует жажды.\n"
                              "Он бел —\n"
                              "А купается только однажды:\n"
                              "Он смело ныряет\n"
                              "В кипящую воду\n"
                              "Себе на беду,\n"
                              "Но на радость народу...\n"
                              "И добрые люди\n"
                              "(Вот это загадка!)\n"
                              "Не скажут:\n"
                              "— Как жалко...\n"
                              "А скажут:\n"
                              "— Как сладко!”***\n\n"
                              "Что это?", parse_mode="Markdown")
        bot.register_next_step_handler(msg, sugar)
    else:
        kb.row_width = 1
        button_1 = types.KeyboardButton("Да")
        button_2 = types.KeyboardButton("Нет")
        kb.add(button_1, button_2)
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, random.choice(notready))
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "_Готовы?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, first_riddle)


@bot.message_handler(content_types=['text'])
def sugar(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    notsugar = ['Не разочаровывайте меня, это же элементарно.',
                "Кажется, человечество обречено, раз вы не можете справиться с такой лёгкой загадкой.",
                "Серьёзно? Ничего лучше в голову не лезет?", "Нет, с Бабой-Ягой вам так не совладать."]
    if msg.text.lower().strip() == "сахар" or msg.text.lower().strip() == "кусок сахара":
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(3)
        bot.send_audio(cid, open("Koshey Sugar #1.mp3", "rb"))
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(75)
        bot.send_audio(cid, open("Koshey Sugar #2.mp3", "rb"))
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(75)
        bot.send_audio(cid, open("Koshey Sugar #3.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(40)
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row_width = 1
        button_1 = types.KeyboardButton("Нет, спасибо")
        button_3 = types.KeyboardButton("Да, пожалуйста")
        kb.add(button_1, button_3)
        bot.send_message(cid, "_Сладенького?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, koshey_first_choice)
    elif msg.text.lower().strip() == "подсказка":
        if len(tips) > 3:
            users_timer[chat]['wrong_time'] += 180
            bot.send_message(cid, "***Превышение кол-ва подсказок!\n"
                                  "+3 минуты за нежелание брать на себя ответственность!***", parse_mode="Markdown")
        if 6 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, '"А скажут:\n'
                                  '"— Как сладко!"\n\n'
                                  'Что может быть сладким?')
            bot.register_next_step_handler(msg, sugar)
        elif 6 not in tips:
            tips.append(6)
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, 'Наверно, это что-то, что растворяется в воде?')
            bot.register_next_step_handler(msg, sugar)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        users_timer[chat]['wrong_time'] += 60
        bot.send_message(cid, "***Неверный ответ.\n +1 минута к общему времени.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, random.choice(notsugar))
        bot.register_next_step_handler(msg, sugar)


@bot.message_handler(content_types=['text'])
def koshey_first_choice(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    if msg.text == "Нет, спасибо":
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "_+2 минуты к общему времени за недоверчивость!\n"
                              "Или это, наоборот, доверчивость?_", parse_mode="Markdown")
        users_timer[chat]['wrong_time'] += 120
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Koshey Sugar Lie.mp3", "rb"))
    elif msg.text == "Да, пожалуйста":
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "_+2 минуты к общему времени за наивность!\n"
                              "Или вы не поняли всей аллегории, что я тут рассказывал?!_", parse_mode="Markdown")
        users_timer[chat]['wrong_time'] += 120
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(5)
        bot.send_audio(cid, open("Koshey Sugar Reject.mp3", "rb"))
    bot.send_chat_action(cid, 'typing')
    time.sleep(30)
    bot.send_message(cid, "Следующий вопрос:\n\n"
                          "***Я молча смотрю на всех,\n"
                          "И смотрят все на меня.\n"
                          "Веселые видят смех,\n"
                          "С печальными плачу я.\n"
                          "Глубокое, как река,\n"
                          "Я дома, на вашей стене.\n"
                          "Увидит старик — старика,\n"
                          "Ребенок — ребенка во мне…***\n\n"
                          "Что это?", parse_mode="Markdown")
    bot.register_next_step_handler(msg, mirror)


@bot.message_handler(content_types=['text'])
def mirror(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    notmirror = ['Что ж такое? Нельзя быть настолько глупыми, соберитесь!',
                 "Мне казалось, это одна из самых простых загадок",
                 "Давайте перенесём спасение человечества на другой жизненный цикл, тут ловить, похоже, нечего",
                 "Почему именно на вас легла такая важная задача? И так провалиться на подобной загадке?"]
    if msg.text == "Зеркало" or msg.text == "зеркало":
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(3)
        bot.send_audio(cid, open("Koshey Mirror #1.mp3", "rb"))
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(75)
        bot.send_audio(cid, open("Koshey Mirror #2.mp3", "rb"))
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(75)
        bot.send_audio(cid, open("Koshey Mirror #3.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(40)
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row_width = 1
        button_1 = types.KeyboardButton("Себя")
        button_3 = types.KeyboardButton("Другого человека")
        kb.add(button_1, button_3)
        bot.send_message(cid, "_Что вы видите в зеркале?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, koshey_second_choice)
    elif msg.text.lower().strip() == "подсказка":
        if len(tips) > 3:
            users_timer[chat]['wrong_time'] += 180
            bot.send_message(cid, "***Превышение кол-ва подсказок!\n"
                                  "+3 минуты за страх перед неизвестным.***", parse_mode="Markdown")
        if 7 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, 'Эта вещь что, "отражает" смотрящего?')
            bot.register_next_step_handler(msg, mirror)
        elif 7 not in tips:
            tips.append(7)
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, 'Каждый в нём видит что-то своё...')
            bot.register_next_step_handler(msg, mirror)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "***Неверный ответ.\n +1 минута к общему времени.***", parse_mode="Markdown")
        users_timer[chat]['wrong_time'] += 60
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, random.choice(notmirror))
        bot.register_next_step_handler(msg, mirror)


@bot.message_handler(content_types=['text'])
def koshey_second_choice(msg):
    cid = msg.chat.id
    if msg.text == "Себя":
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row_width = 1
        button_1 = types.KeyboardButton("Да, я люблю себя.")
        button_2 = types.KeyboardButton("Нет, мне мерзко на него смотреть.")
        kb.add(button_1, button_2)
        bot.send_message(cid, "_Вам нравится ваше отражение?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, koshey_myself)
    elif msg.text == "Другого человека":
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row_width = 1
        button_1 = types.KeyboardButton("Да, наши отношения нельзя назвать здоровыми.")
        button_2 = types.KeyboardButton("Нет, он не специально, это было необходимо.")
        kb.add(button_1, button_2)
        bot.send_message(cid, "_Этот человек принёс вам много боли, не так ли?_", parse_mode="Markdown", reply_markup=kb)
        bot.register_next_step_handler(msg, koshey_other)


@bot.message_handler(content_types=['text'])
def koshey_myself(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    if msg.text == "Да, я люблю себя.":
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(3)
        bot.send_audio(cid, open("Love Yourself.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(50)
        bot.send_message(cid, "***+2 минуты к общему времени***", parse_mode="Markdown")
        users_timer[chat]['wrong_time'] += 120
    elif msg.text == "Нет, мне мерзко на него смотреть.":
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(3)
        bot.send_audio(cid, open("Change Yourself.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(50)
        bot.send_message(cid, "***+2 минуты к общему времени***", parse_mode="Markdown")
        users_timer[chat]['wrong_time'] += 120
    bot.send_chat_action(cid, 'record_video')
    time.sleep(5)
    bot.send_video(cid, open("Koshey End #1.mp4", "rb"))
    bot.send_chat_action(cid, 'record_video')
    time.sleep(60)
    bot.send_video(cid, open("Koshey End #2.mp4", "rb"))
    bot.send_chat_action(cid, 'upload_photo')
    time.sleep(40)
    bot.send_photo(cid, open("Letter D.png", "rb"))
    bot.send_chat_action(cid, 'typing')
    time.sleep(7)
    bot.send_message(cid, "Да уж, вот это персонаж, поболтать мастак. "
                          "Конечно, вам решать, насколько его речи были правдивы и полезны, "
                          "но мне всё показалось вполне логичным. ")
    bot.send_chat_action(cid, 'typing')
    time.sleep(3)
    bot.send_message(cid, "Вот только один скриптик, отвечающий за чутьё, подсказывает мне, "
                          "что не всё тут так просто…")
    bot.send_chat_action(cid, 'typing')
    time.sleep(7)
    bot.send_message(cid, "Но ладно, у нас сейчас есть дела поважнее. "
                          "Остановим Бабу-Ягу, а потом я уже исследую тотемы Кощея и "
                          "разберу всю информацию о его происхождении…")
    bot.send_chat_action(cid, 'typing')
    time.sleep(5)
    bot.send_message(cid, "***Найдя нужный объект, в качестве пароля введите сюда все цифры с таблички: ***",
                     parse_mode="Markdown")
    bot.register_next_step_handler(msg, embrion)
#   elif msg.text == "Нет, мне мерзко на него смотреть.":
    #   bot.send_chat_action(cid, 'record_voice')
    #   time.sleep(3)
    #   bot.send_audio(cid, open("Change Yourself.mp3", "rb"))
    #   bot.send_chat_action(cid, 'typing')
    #   time.sleep(50)
    #   bot.send_message(cid, "***+2 минуты к общему времени***", parse_mode="Markdown")
    #   users_timer[chat]['wrong_time'] += 120
    #   bot.send_chat_action(cid, 'record_video')
    #   time.sleep(5)
    #   bot.send_video(cid, open("Koshey End #1.mp4", "rb"))
    #   bot.send_chat_action(cid, 'record_video')
    #   time.sleep(60)
    #   bot.send_video(cid, open("Koshey End #2.mp4", "rb"))
    #   bot.send_chat_action(cid, 'upload_photo')
    #   time.sleep(40)
    #   bot.send_photo(cid, open("Letter D.png", "rb"))
    #   bot.send_chat_action(cid, 'upload_photo')
    #   time.sleep(3)
    #   bot.send_photo(cid, open("psycholog.png", "rb"))
    #   bot.send_message(cid, '*** Achievement "Stop It, Get Some Help"\n'
    #                         'Лучшая помощь от бессмертного специалиста!***', parse_mode="Markdown")
    #   time.sleep(5)
    #   bot.send_message(cid, "Да уж, вот это персонаж, поболтать мастак. "
    #                         "Конечно, вам решать, насколько его речи были правдивы и полезны, "
    #                         "но мне всё показалось вполне логичным. ")
    #   bot.send_chat_action(cid, 'typing')
    #   time.sleep(3)
    #   bot.send_message(cid, "Вот только один скриптик, отвечающий за чутьё, подсказывает мне, "
    #                         "что не всё тут так просто…")
    #   bot.send_chat_action(cid, 'typing')
    #   time.sleep(7)
    #   bot.send_message(cid, "Но ладно, у нас сейчас есть дела поважнее. "
    #                         "Остановим Бабу-Ягу, а потом я уже исследую тотемы Кощея и "
    #                         "разберу всю информацию о его происхождении…")
    #   bot.send_chat_action(cid, 'typing')
    #   time.sleep(5)
    #   bot.send_message(cid, "***Найдя нужный объект, в качестве пароля введите сюда все цифры с таблички: ***",
    #                    parse_mode="Markdown")
    #   bot.register_next_step_handler(msg, embrion)


@bot.message_handler(content_types=['text'])
def koshey_other(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    if msg.text == "Да, наши отношения нельзя назвать здоровыми.":
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(3)
        bot.send_audio(cid, open("Appreciate Yourself.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(50)
        bot.send_message(cid, "***+2 минуты к общему времени***", parse_mode="Markdown")
        users_timer[chat]['wrong_time'] += 120
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Koshey End #1.mp4", "rb"))
        bot.send_chat_action(cid, 'record_video')
        time.sleep(60)
        bot.send_video(cid, open("Koshey End #2.mp4", "rb"))
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(40)
        bot.send_photo(cid, open("Letter D.png", "rb"))
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(5)
        bot.send_photo(cid, open("psycholog.png", "rb"))
        bot.send_message(cid, '*** Achievement "Stop It, Get Some Help"\n'
                              'Лучшая помощь от бессмертного специалиста!***', parse_mode="Markdown")
        time.sleep(5)
        bot.send_message(cid, "Да уж, вот это персонаж, поболтать мастак. "
                              "Конечно, вам решать, насколько его речи были правдивы и полезны, "
                              "но мне всё показалось вполне логичным. ")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Вот только один скриптик, отвечающий за чутьё, подсказывает мне, "
                              "что не всё тут так просто…")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "Но ладно, у нас сейчас есть дела поважнее. "
                              "Остановим Бабу-Ягу, а потом я уже исследую тотемы Кощея и "
                              "разберу всю информацию о его происхождении…")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "***Найдя нужный объект, в качестве пароля введите сюда все цифры с таблички: ***",
                         parse_mode="Markdown")
        bot.register_next_step_handler(msg, embrion)
    elif msg.text == "Нет, он не специально, это было необходимо.":
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(3)
        bot.send_audio(cid, open("Don't be Dumbass.mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(50)
        users_timer[chat]['wrong_time'] += 120
        bot.send_message(cid, "***+2 минуты к общему времени***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Koshey End #1.mp4", "rb"))
        bot.send_chat_action(cid, 'record_video')
        time.sleep(60)
        bot.send_video(cid, open("Koshey End #2.mp4", "rb"))
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(40)
        bot.send_photo(cid, open("Letter D.png", "rb"))
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(7)
        bot.send_photo(cid, open("psycholog.png", "rb"))
        bot.send_message(cid, '*** Achievement "Stop It, Get Some Help"\n'
                              'Лучшая помощь от бессмертного специалиста!***', parse_mode="Markdown")
        time.sleep(5)
        bot.send_message(cid, "Да уж, вот это персонаж, поболтать мастак. "
                              "Конечно, вам решать, насколько его речи были правдивы и полезны, "
                              "но мне всё показалось вполне логичным. ")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Вот только один скриптик, отвечающий за чутьё, подсказывает мне, "
                              "что не всё тут так просто…")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Но ладно, у нас сейчас есть дела поважнее. "
                              "Остановим Бабу-Ягу, а потом я уже исследую тотемы Кощея и "
                              "разберу всю информацию о его происхождении…")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "***Найдя нужный объект, в качестве пароля введите сюда "
                              "все цифры с таблички рядом с ним: ***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, embrion)


@bot.message_handler(content_types=['text'])
def embrion(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    noembrio = ['Пожалуй, это не те цифры не в том месте.', "Не работает. Вы уверены?",
                "Сильно сомневаюсь, что это и есть ключ.",
                '"Плод, замаскированный под скульптуру" и что-то ещё про театр...']
    if msg.text.strip() == "188203209211":
        bot.send_chat_action(cid, 'record_video')
        time.sleep(5)
        bot.send_video(cid, open("Embrion #1.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(25)
        bot.send_message(cid, "Нет, не видели, но остановить её обязаны.\nОна – угроза для нашего мира!")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(10)
        bot.send_video(cid, open("Embrion #2.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(17)
        bot.send_message(cid, "Твоя мама не появляется, потому что любит тебя и хочет защитить.\n"
                              "За ней идёт охота, и она боится, что ты можешь пострадать")
        bot.send_chat_action(cid, 'typing')
        time.sleep(12)
        bot.send_message(cid, "_Пока я убаюкиваю его, осмотритесь вокруг. "
                              "Нужно наложить печать, и, думаю, эти старославянские символы, "
                              "что мы собирали на протяжении всего похода, нам в этом помогут._", parse_mode="Markdown")
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(5)
        bot.send_photo(cid, open("Location #3.png", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_message(cid, "***Введите сюда имена тех, кому принадлежат найденные вами символы, "
                              "а затем напишите получившееся слово-печать, "
                              "чтобы покончить со всем этим!***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "***У вас есть 10 минут, "
                              "прежде чем Баба-Яга с огромной вероятностью заметит неладное.***", parse_mode="Markdown")
        users_timer[chat]['embrion_destroy'] = int(time.time())
        bot.register_next_step_handler(msg, embrion_destroy)
    elif msg.text.lower().strip() == "подсказка":
        if len(tips) > 3:
            users_timer[chat]['wrong_time'] += 300
            bot.send_message(cid, "***Превышение кол-ва подсказок!\n"
                                  "+5 минут за нерешительность.***", parse_mode="Markdown")
        if 8 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, 'Неродившийся плод - это же эмбрион? Есть в Праге такая скульптура?')
            bot.register_next_step_handler(msg, embrion)
        elif 8 not in tips:
            tips.append(8)
            bot.send_chat_action(cid, 'typing')
            time.sleep(5)
            bot.send_message(cid, 'Он сказал: "ребёнок, неродившийся плод в виде скульптуры, чтобы люди не увидели, '
                                  'что спрятано за кулисами этого театра..."')
            bot.register_next_step_handler(msg, embrion)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, random.choice(noembrio))
        bot.send_message(cid, "***+1 минута к общему времени.***", parse_mode="Markdown")
        users_timer[chat]['wrong_time'] += 60
        bot.register_next_step_handler(msg, embrion)


@bot.message_handler(content_types=['text'])
def embrion_destroy(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    a = msg.text
    rightgod = ['Всё верно!', "Да, это он!", "Правильно!", "Отлично!"]
    wasgod = ['Он уже был.', "Вы уже называли его.", "Нам нужны и другие боги, кроме этого.",
              "Здесь от него дважды толку не будет"]
    wronggod = ['Нет, это не то.', "Это не тот бог, что нам нужен.", "Здесь нет такого символа!",
                "Неверно, поищите лучше."]
    if users_timer[chat]['embrion_destroy'] + 600 <= int(time.time()) and users_timer[chat]['embrion_destroy_end'] == False:  # выполнит, если время вышло
        users_timer[chat]['wrong_time'] += 900  # время штрафа в секундах, когда таймер запустили на 30 секунд
        users_timer[chat]['embrion_destroy_end'] = True
        bot.send_message(cid, "***+15 минут к общему зачёту за халатность!\n"
                              "У нас тут, вообще-то, жизнь всего человечества на кону!***", parse_mode="Markdown")

    if a in gods:
        if a == "Дажьбог":
            bot.send_chat_action(cid, 'typing')
            time.sleep(2)
            bot.send_message(cid, random.choice(rightgod))
            gods.remove(a)
            foundgods.append(a)
            bot.send_chat_action(cid, 'typing')
            time.sleep(2)
            bot.send_message(cid, "Постойте. Кажется, у этого бога был ещё один, не менее важный символ...")
            if gods == [1]:
                if users_timer[chat]['embrion_destroy_end'] == False:
                    users_timer[chat]['bonus_time'] += 180
                    bot.send_chat_action(cid, 'typing')
                    time.sleep(3)
                    bot.send_message(cid, "***Отлично, все символы совпали с именами всех богов,\n"
                                          " -3 минуты из общего зачёта!***", parse_mode="Markdown")
                bot.send_chat_action(cid, 'typing')
                time.sleep(2)
                bot.send_message(cid, "***Теперь составьте слово-печать, "
                                      "чтобы уничтожить источник силы Бабы-Яги!***", parse_mode="Markdown")
                bot.register_next_step_handler(msg, embrion_final)
            else:
                bot.register_next_step_handler(msg, embrion_destroy)
        else:
            bot.send_chat_action(cid, 'typing')
            time.sleep(2)
            bot.send_message(cid, random.choice(rightgod))
            gods.remove(a)
            foundgods.append(a)
            if gods == [1]:
                if users_timer[chat]['embrion_destroy_end'] == False:
                    users_timer[chat]['bonus_time'] += 180
                    bot.send_chat_action(cid, 'typing')
                    time.sleep(3)
                    bot.send_message(cid, "***Отлично, все символы совпали с именами всех богов,"
                                          " -3 минуты из общего зачёта!***", parse_mode="Markdown")
                bot.send_chat_action(cid, 'typing')
                time.sleep(3)
                bot.send_message(cid, "***Теперь составьте слово-печать, "
                                      "чтобы уничтожить источник силы Бабы-Яги!***", parse_mode="Markdown")
                bot.register_next_step_handler(msg, embrion_final)
            else:
                bot.register_next_step_handler(msg, embrion_destroy)
    elif msg.text.lower().strip() == "подсказка":
        if len(tips) > 3:
            users_timer[chat]['wrong_time'] += 300
            bot.send_message(cid, "***Превышение кол-ва подсказок!\n"
                                  "+5 минут за невнимательность.***", parse_mode="Markdown")
        if 9 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, 'Нужно узнать имена богов по описаниям с наклеек,\n'
                                  'вписать их одно за другим, а затем из букв, что означают чёрные символы,\n'
                                  'составить слово-печать.')
            bot.register_next_step_handler(msg, embrion)
        elif 9 not in tips:
            tips.append(9)
            bot.send_chat_action(cid, 'typing')
            time.sleep(5)
            bot.send_message(cid, 'Мы же всё это время натыкались на наклейки?\n'
                                  'Думаю, и сейчас не исключительный случай, поищите их вокруг.')
            bot.register_next_step_handler(msg, embrion)
    elif a in foundgods:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, random.choice(wasgod))
        bot.register_next_step_handler(msg, embrion_destroy)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, random.choice(wronggod))
        bot.send_chat_action(cid, 'typing')
        time.sleep(1)
        bot.send_message(cid, "***+1 минута к общему времени.***", parse_mode="Markdown")
        users_timer[chat]['wrong_time'] += 60

        bot.register_next_step_handler(msg, embrion_destroy)


@bot.message_handler(content_types=['text'])
def embrion_final(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    noabort = ['Нет, это слово не поможет.', "Оно не является печатью, составляйте лучше!",
               "В этом слове нет никакой магии, поэтому найдите другое.",
               "По-моему, не его вы составляли из тех символов"]
    if msg.text.strip() == "аборт" or msg.text.strip() == "Аборт":
        kb.row_width = 1
        but1 = types.KeyboardButton("Сделать это!")
        but2 = types.KeyboardButton("Я не могу!")
        kb.add(but1, but2)
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "Скорее, сделайте это! "
                              "Остался последний шаг и весь мир, всё человечество будут спасены!\n"
                              "УБЕЙТЕ МЛАДЕНЦА! ", reply_markup=kb)
        bot.register_next_step_handler(msg, embrio_theend)
    elif msg.text.lower().strip() == "подсказка":
        if len(tips) > 3:
            users_timer[chat]['wrong_time'] += 300
            bot.send_message(cid, "***Превышение кол-ва подсказок!\n"
                                  "+5 минут за несамостоятельность.***", parse_mode="Markdown")
        if 9 in tips:
            bot.send_chat_action(cid, 'typing')
            time.sleep(3)
            bot.send_message(cid, 'У Дажьбога же есть два символа!\n'
                                  'И нам как раз не хватает одной цифры, что в начале описаний богов,\n'
                                  'а значит, и буквы.')
            bot.register_next_step_handler(msg, embrion_final)
        elif 9 not in tips:
            tips.append(9)
            bot.send_chat_action(cid, 'typing')
            time.sleep(5)
            bot.send_message(cid, 'Думаю, цифры в начале описаний тоже тут неспроста.')
            bot.register_next_step_handler(msg, embrion_final)
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, random.choice(noabort))
        users_timer[chat]['wrong_time'] += 300
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "***+5 минут к общему зачёту!***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, embrion_final)


@bot.message_handler(content_types=['text'])
def embrio_theend(msg):
    cid = msg.chat.id
    if msg.text == "Сделать это!":
        bot.send_chat_action(cid, 'record_video')
        time.sleep(2)
        bot.send_video(cid, open("Embrion Death.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(15)
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(7)
        bot.send_photo(cid, open("kinder.jpg", "rb"))
        bot.send_message(cid, '***Achievement\n"Women And Children First"\n'
                              'Ма-Ма не закон!\nЯ закон! (с) Аборт***', parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "Наконец-то. А у вас рука не дрогнула. И кто-то ещё меня назовёт бездушной машиной.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Но главное, что мы победили. Хотя какой-то великой радости не чувствуется…")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "Потому что нам нужно сдать задание! "
                              "Отправляемся в таверну, окутанную дымом, там уже дух и переведём.")
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(4)
        bot.send_photo(cid, open("Final location.png", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(8)
        bot.send_message(cid, "***В таверне на дверях вы найдёте кодовое слово - "
                              "введите его и вам придёт подтверждение того, что задание выполнено. "
                              "Покажите его бармену и получите заслуженное вознаграждение.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "***Остаться ли подольше и взять что-то ещё, это уже исключительно на вас.***",
                         parse_mode="Markdown")
        bot.register_next_step_handler(msg, steampunk)
    elif msg.text == "Я не могу!":
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "Что ж, я знал, вы слишком человечны, "
                              "чтобы убить младенца пусть и могущественной чародейки, "
                              "пусть и ради спасения человечества. "
                              "Простите, но тогда я сделаю это сам…")
        bot.send_chat_action(cid, 'record_video')
        time.sleep(2)
        bot.send_video(cid, open("Embrion Death.mp4", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(15)
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(5)
        bot.send_photo(cid, open("kinder.jpg", "rb"))
        bot.send_message(cid, '***Achievement\n"Women And Children First"\n'
                              'Ма-Ма не закон!\nЯ закон! (с) Аборт***', parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "Наконец-то. Пусть уж лучше меня называют бездушной машиной, чем вас убийцами.")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "Но главное, что мы победили. Хотя какой-то великой радости не чувствуется…")
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, "Потому что нам нужно сдать задание! "
                              "Отправляемся в таверну, окутанную дымом, там уже дух и переведём.")
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(5)
        bot.send_photo(cid, open("Final location.png", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(8)
        bot.send_message(cid, "***В таверне на дверях вы найдёте кодовое слово - "
                              "введите его и вам придёт подтверждение того, что задание выполнено. "
                              "Покажите его бармену и получите заслуженное вознаграждение.***", parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(5)
        bot.send_message(cid, "***Остаться ли подольше и взять что-то ещё, это уже исключительно на вас.***",
                         parse_mode="Markdown")
        bot.register_next_step_handler(msg, steampunk)


@bot.message_handler(content_types=['text'])
def steampunk(msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    chat = cid == uid and uid or cid
    steampook = ['Нет, не то.', "Нет, это не он.", "Не-а, его зовут не так.", "Так нелепо споткнётесь у самого финиша?",
                 "Ну же, поднажмите, нужно лишь назвать имя и фамилию!"]
    if msg.text == "Кевин Джетер":
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(3)
        bot.send_photo(cid, open("Steam.jpg", "rb"))
        bot.send_message(cid, '***Achievement \n"Smells Like A Steam Spirit"\n'
                              'Любимое место для охотников за нечистью.\n'
                              'Хотя нечисти здесь тоже хватает...***', parse_mode="Markdown")
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_message(cid, '***Поздравляем!\n'
                              'Вы прошли квест "Однажды в Хэллоуин"!'
                              f"\nОбщее время прохождения: {cTime((int(time.time()) - users_timer[chat]['general_timer']) - users_timer[chat]['bonus_time'] + users_timer[chat]['wrong_time'])}***", parse_mode="Markdown")
        del users_timer[chat]
        bot.send_chat_action(cid, 'typing')
        time.sleep(7)
        bot.send_message(cid, '***Надеемся, отныне вы станете частым гостем в мире квестов от Questino!\n'
                              'Также приглашаем вас поучаствовать в розыгрыше в честь нашего дебюта.\n'
                              'Главный приз - игра "Эксперимент" в эскейп-руме\nот "Questroom.cz".\n'
                              'Условия участия - ниже по ссылке.***', parse_mode="Markdown")
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        markup.add(InlineKeyboardButton("Instagram", url="https://www.instagram.com/questino.bot"))
        markup.add(InlineKeyboardButton("VK", url="https://vk.com/questino_bot"))
        markup.add(InlineKeyboardButton("Условия розыгрыша", url="https://www.instagram.com/p/CWQglfSoBj-/"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(10)
        bot.send_message(cid, '***Подписывайтесь на наши соцсети, следите за анонсами и новыми релизами квестов, '
                              'получайте скидки и промокоды, \n'
                              'участвуйте в розыгрышах и даже находите новых знакомых '
                              'по интересам!\n\n'
                              'До новых встреч в мире квестов, и помните: \n'
                              'Весь город - твоя головоломка!***', parse_mode="Markdown", reply_markup=markup)
        bot.send_chat_action(cid, 'record_voice')
        time.sleep(120)
        bot.send_audio(cid, open("....mp3", "rb"))
        bot.send_chat_action(cid, 'typing')
        time.sleep(155)
        bot.send_message(cid, "***Продолжение следует...\n"
                              "Весной 2022 года на всех (почти) улицах Праги***", parse_mode="Markdown")
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, random.choice(steampook))
        bot.register_next_step_handler(msg, steampunk)




if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    bot.polling(none_stop=True)

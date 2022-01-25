import threading
import random
from bs4 import BeautifulSoup
import lxml
import requests
import datetime
from loguru import logger
import vk_api, os, time, json, math, io
from PIL import Image, ImageFont, ImageDraw, ImageOps
from vk_api.longpoll import VkLongPoll, VkEventType
from time import sleep
from vk_api.upload import VkUpload
from io import BytesIO
from colorama import init, Fore
from colorama import Back
from colorama import Style

# ✅✅✅ Метод отправки
def msg_edit(text):
    vk.method("messages.edit",{"peer_id":event.peer_id, "keep_forward_messages": 1, "message_id":event.message_id, "message": "{}\n\n🌐PingTime: {} сек.".format(text, str(float("{:.2f}".format(time.time() - event.timestamp))).replace("-", "")), "random_id": 0})

# ✅✅✅ Вечный онлайн
def on_online():
    while True:
        if onl == 1:
            vk.method("account.setOnline")
            time.sleep(180)
        else:
            time.sleep(3)
# ✅✅✅ Вечный Оффлайн
def off_online():
    while True:
        if onl == 2:
            vk.method("account.setOffline")
            time.sleep(180)
        else:
            time.sleep(3)


# ✅✅✅ Поиск Айди
def search_id(event, vk, owner_info, pos=2):
    text = event.text.split(" ", maxsplit=5)
    try:
        akk_id = vk.method("messages.getById", {"message_ids": event.message_id})['items'][0]['reply_message']['from_id']

    except:
        try:
            akk_id = text[pos]
        except:
            return owner_info["id"]
        else:
            try:
                akk_id.index("vk.com/id")
            except:
                try:
                    akk_id.index("vk.com/")
                except:
                    return akk_id.partition('id')[2].partition('|')[0]
                else:
                    akk_id = vk.method("users.get", {"user_ids": akk_id.partition('com/')[2]})[0]["id"]
                    return akk_id
            else:
                return akk_id.partition('id')[2]
    else:
        return akk_id


#  ✅✅✅ Поиск Имя-Фамилия
def user(name_case = None):
    user_get = vk.method("users.get", {"user_ids": search_id(event, vk, owner_info,), "name_case": name_case})
    user_get = user_get[0]
    first_name = user_get['first_name']
    last_name = user_get['last_name']
    return first_name, last_name

# ✅✅✅ Добавление в друзья
def friends_add(vk, akk_id):
    try:
        otv = vk.method("friends.add", {"user_id": akk_id})
        if otv == 1:
            return f"[id{akk_id}| ✅Заявка в друзья отправлена.]"
            logger.info(Fore.RED + f"отправлена заявка {first_name} {last_name}")
        if otv == 2:
            return f"[id{akk_id}|✅ Добавлен в друзья.]"
            logger.info(Fore.RED + f" {first_name} {last_name} Добавлен в друзья")
        if otv == 4:
            return f"[id{akk_id}|✅ Повторная заявка отправлена.]"
            logger.info(Fore.RED + f"отправвил повторную заявку {first_name} {last_name}")
    except Exception as error:
        return f"Ошибка {error}"


# ✅✅✅ Удаление из друзей
def friends_delet(vk, akk_id):
    try:
        otv = vk.method("friends.delete", {"user_id": akk_id})
        if otv.get("friend_deleted") != None:
            return f"[id{akk_id}| ✅Удален из друзей.]"
            logger.info(Fore.RED + f"{first_name} {last_name} Удален из друзей")
        if otv.get("in_request_deleted") != None:
            return f"[id{akk_id}|✅ Bходящая заявка отклонена.]"
            logger.info(Fore.RED + f"отменил заявку от {first_name} {last_name}")
        if otv.get("out_request_deleted") != None:
            return f"[id{akk_id}|✅ Входящая завявка отклонена.]"
    except Exception as error:
        return f"Ошибка {error}"
onl = 0
threading.Thread(target=on_online, args=()).start()
threading.Thread(target=off_online, args=()).start()
vk = vk_api.VkApi(token="c689f231c5bf8883019e03aa5966395e09bf6b7a655b9329bdc47ace616f5b2d51f7d3137160636e689df")
command = "cls"
os.system(command)
vk._auth_token()
logger.info(Fore.RED + "Добро пожаловать,Сергей Романов!")
lp = VkLongPoll(vk)
owner_info = vk.method("account.getProfileInfo")


while True:
    try:
        for event in lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.from_me == True:
                if event.text.startswith(".м") and event.text.split(" ")[1] == "+лайк":
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user("gen")
                    profile = "profile"
                    photos=vk.method("photos.get",{"owner_id":akk_id,"album_id":profile,"rev":1,"count":1})['items']
                    for ph in photos:
                        photo_id = "{}".format(photos[0]['id'])
                        photo="photo"
                        lakes = vk.method("likes.add",{"type":photo,"owner_id":akk_id,"item_id":photo_id})
                        msg_edit(f"❤Плюс сердешко😇 у [id{akk_id}|{first_name} {last_name}]\n Теперь на фоточке {lakes['likes']} сердешек")
                        logger.info(Fore.GREEN + f"Произошлa команда: '+лайк' ")


                if event.text.startswith(".м")and event.text.split(" ")[1] == "-лайк":
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user("gen")
                    profile = "profile"
                    photos=vk.method("photos.get",{"owner_id":akk_id,"album_id":profile,"rev":1,"count":1})['items']
                    for ph in photos:
                        photo_id = "{}".format(photos[0]['id'])
                        photo="photo"
                        lake=vk.method("likes.delete",{"type":photo,"owner_id":akk_id,"item_id":photo_id})
                        msg_edit(f"💔 минус сердешко 😔 у [id{akk_id}|{first_name} {last_name}]\n Теперь на фоточке {lake['likes']} сердешек ")
                        logger.info(Fore.GREEN + f"Произошлa команда: '-лайк' ")


                if event.text.startswith(".м")and event.text.split(" ")[1] == "ид":
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user()
                    msg_edit(f"🗓 ID [id{akk_id}|{first_name} {last_name}] Pавен:")
                    vk.method("messages.send", {"peer_id":event.peer_id, "message": f"{akk_id}", "random_id": 0})
                    logger.info(Fore.GREEN + f"Произошлa команда: 'ид' ")

                if event.text.startswith(".м")and event.text.split(" ")[1] == "+онлайн":
                    if onl == 1:
                        text = "✅ Вечный онлайн уже включен."
                        logger.warning(Fore.RED + "Вечный онлайн уже был включен!!!")
                    else:
                        onl = 1
                        text = "💅🏻 Были изменены следующие настройки:\n✅ Включен вечный онлайн"
                    msg_edit(f"{text}")
                    logger.info(Fore.GREEN + f"Был включен вечный онлайн! ")


                if event.text.startswith(".м")and event.text.split(" ")[1] == "-онлайн":
                    if onl == 2:
                        text = "✅ Вечный оффлайн уже включен."
                        logger.warning(Fore.RED + "Вечный оффлайн уже был включен!!!")
                    else:
                        onl = 2
                        text = "💅🏻 Были изменены следующие настройки:\n✅ Включен вечный оффлайн"
                        logger.info(Fore.GREEN + f"был включен вечный оффлайн!")
                    msg_edit(f"{text}")


                if event.text.startswith(".м"):
                    texts = event.text.split("\n", maxsplit=1)
                    text = texts[0].split(" ", maxsplit=2)
                    if text[1] == "статус":
                        try:
                            vk.method("status.set", {"text": texts[1]})
                        except:
                            msg_edit("❎ Не удалось установить статус.‍")
                            logger.error(Fore.RED + f"Произошлa ошибка: 'Статус не установлен' ")
                        else:
                            text = texts[1]
                            msg_edit(f"✅ Установлен статус.‍\n{text}")
                            logger.info(Fore.GREEN + f"был поставлен статус: {text} ")


                if event.text.startswith(".м")and event.text.split(" ")[1] == "+чс":
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user()
                    try:
                        a = vk.method("account.ban", {"owner_id": akk_id})
                        if a == 1:
                            msg_edit(f"✅[id{akk_id}|{first_name} {last_name}] Добавлен в список кончей.")
                            logger.info(Fore.GREEN + f"{first_name} {last_name} попал в чс ")
                    except Exception as error:
                        if str(error) == "[15] Access denied: user already blacklisted":
                            msg_edit(f"Ты еблан? {first_name} и так в списке кончей")
                            logger.error(Fore.RED + f"Произошла ошибка {error}")


                if event.text.startswith(".м")and event.text.split(" ")[1] == "-чс":
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user()
                    try:
                        a = vk.method("account.unban", {"owner_id": akk_id})
                        if a == 1:
                            msg_edit(f"✅[id{akk_id}|{first_name} {last_name}] Убран из списка кончей.")
                            logger.info(Fore.GREEN + f"{first_name} {last_name} убран из чс ")
                    except Exception as error:
                        if str(error) == "[15] Access denied: user not blacklisted":
                            msg_edit(f"Ты еблан? {first_name} не в списке кончей")
                        logger.error(Fore.RED + f"Произошла ошибка {error}")




                if event.text.startswith(".м")and event.text.split(" ")[1] == "+др":
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user()
                    friend = friends_add(vk, akk_id)
                    msg_edit(friend)



                if event.text.startswith(".м")and event.text.split(" ")[1] == "-др":
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user()
                    friend = friends_delet(vk, akk_id)
                    msg_edit(friend)



                if event.text.startswith(".м")and event.text.split(" ")[1] == "+ава":
                    upload = VkUpload(vk)
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user("gen")
                    url = vk.method("users.get", {"user_ids": akk_id, "fields": "photo_max_orig"})[0]["photo_max_orig"]
                    photo = io.BytesIO(
                    requests.get(url).content
                    )
                    photo_vk = upload.photo_profile(photo)
                    profile = "profile"
                    photos = vk.method("photos.get",{"owner_id":akk_id,"album_id":profile,"rev":1,"count":1})['items']
                    for ph in photos:
                        photo_id = "{}".format(photos[0]['id'])
                        photo="photo"
                        item = "photo" + str(ph["owner_id"]) + '_' + str(ph["id"])
                        vk.method("messages.edit",{"peer_id":event.peer_id, "keep_forward_messages": 1, "message_id":event.message_id, "message": f"Аватарка спизжена у\n{first_name} {last_name}", "attachment": item, "random_id": 0})
                        logger.info(Fore.GREEN + f"Взял аватарку у {first_name} {last_name} ")

                if event.text.startswith(".м")and event.text.split(" ")[1] == "-ава":
                    try:
                        response = vk.method("photos.get", {"rev": 1, "album_id": "profile", "count": 1})
                        vk.method("photos.delete", {"owner_id": response["items"][0]["owner_id"], "photo_id": response["items"][0]["id"]})
                        msg_edit("✅Аватарка успешно удалена.")
                        logger.info(Fore.GREEN + f"Была удадена аватарка.")
                    except Exception as error:
                        msg_edit(f"Ошибка,подробнее\n{error}")

                if event.text.startswith(".м")and event.text.split(" ")[1] == "кик":
                    try:
                        akk_id = search_id(event, vk, owner_info,)
                        first_name, last_name = user("gen")
                        a = vk.method("messages.removeChatUser", {"chat_id": event.peer_id -2000000000, "user_id": akk_id, "member_id": akk_id})
                        print(a)
                        msg_edit(f"[id{akk_id}|{first_name} {last_name}]Нахуй послан")
                        logger.info(Fore.GREEN + f"Кикнул {first_name} {last_name}")
                    except Exception as error:
                        if str(error) == "[15] Access denied: can't remove this user":
                            msg_edit("Хуйня какая та,походу я не админ")
                            logger.error(Fore.RED + f"Произошла ошибка {error}")


                if event.text.startswith(".м")and event.text.split(" ")[1] == "репорт":
                    akk_id = search_id(event, vk, owner_info,)
                    first_name, last_name = user("gen")
                    vk.method("users.report", {"user_id": akk_id, "type": "insult", "comment": "Оскорбляет и унижает личность людей."})
                    msg_edit(f"Ебанул жалобу на [id{akk_id}|{first_name} {last_name}]✅")
                    logger.info(Fore.GREEN + f"Была подана жалоба на {first_name} {last_name}")

                if event.text.startswith(".м")and event.text.split(" ")[1] == "+сохра":
                    try:
                        e, count = vk.method("messages.getById", {"message_ids": event.message_id}), 0
                        if e['items'][0]['reply_message']["attachments"] == []:
                            text = "Нету вложений"
                        else:
                            for i in e ['items'][0]['reply_message']["attachments"]:
                                if i["type"] == "photo":
                                    id = i["photo"]["id"]
                                    owner = i["photo"]["owner_id"]
                                    key = i["photo"]["access_key"]
                                    vk.method("photos.copy", {"owner_id": owner, "photo_id": id, "access_key": key})
                                    count += 1
                                    text = f"все́ ахуенно,доабвил сохр: {count}"
                                    msg_edit(f"{text}")
                                    logger.info(Fore.GREEN + f"Было добавлено сохраненок: {count}")
                    except Exception as error:
                        logger.error(Fore.RED + f"Произошла ошибка: {error}")



                if event.text.startswith(".м")and event.text.split(" ")[1] == "цитата":
                    QUOTE_FONT = ImageFont.truetype("Montserrat-Light.ttf", 70)
                    QUOTE_FONT_SEC = ImageFont.truetype("Montserrat-MediumItalic.ttf", 70)
                    responce = vk.method("messages.getById", {"message_ids": event.message_id})['items'][0]
                    reply_text = "„"+responce["reply_message"]["text"]+"“"
                    reply_user_id = responce["reply_message"]["from_id"]
                    reply_response = vk.method("users.get", {"user_id": reply_user_id, "fields": "first_name, last_name, photo_400_orig"})
                    author_name = (f"""©{reply_response[0]["first_name"]} {reply_response[0]["last_name"]}""")
                    author_photo = BytesIO(requests.get(reply_response[0]["photo_400_orig"]).content)

                    reply_text_width = QUOTE_FONT.getsize_multiline(reply_text)[0]
                    author_name_width = QUOTE_FONT.getsize_multiline(author_name)[0]
                    if author_name_width > reply_text_width:
                        width = author_name_width + 70
                    else:
                        width = reply_text_width + 310
                    quote = Image.new("RGBA", (width + 400, 399), "#22212A")
                    draw = ImageDraw.Draw(quote)
                    width, height = quote.size
                    author_photo = Image.open(author_photo).convert("RGB")
                    author_photo = author_photo.resize((350, 350), Image.ANTIALIAS)
                    background = Image.new("RGB", author_photo.size, "#22212A")
                    mask = Image.new("L", author_photo.size, 0)
                    draw_mask = ImageDraw.Draw(mask)
                    draw_mask.ellipse(
                        (
                            0,
                            0,
                            author_photo.size[0],
                            author_photo.size[1],
                        ),
                        fill=255,
                    )
                    mask = Image.composite(author_photo, background, mask)

                    quote.paste(mask, (25, 25))

                    draw.text(
                        (width - author_name_width - 30, height - 115),
                        author_name,
                        font=QUOTE_FONT,
                        fill="white",
                    )

                    draw.text(
                        ((width+310-reply_text_width)/2, 140),
                        reply_text,
                        font=QUOTE_FONT_SEC,
                        fill="white",
                    )

                    image_handle = BytesIO()
                    quote.save(image_handle, "PNG")
                    image_handle.seek(0)
                    upload = VkUpload(vk)
                    photo_vk = upload.photo_messages(image_handle, peer_id=event.peer_id)
                    atts = "photo{}_{}_{}".format(photo_vk[0]["owner_id"], photo_vk[0]["id"], photo_vk[0]["access_key"])
                    vk.method("messages.edit", {"peer_id": event.peer_id ,"keep_forward_messages": 1,"message": "🌐PingTime: {} сек.".format(str(float("{:.2f}".format(time.time() - event.timestamp))).replace("-", "")), "attachment": atts, "message_id": event.message_id, "random_id": 0})





                if event.text.startswith("мем"):
                    try:
                        params = {"q": event.text.split(" ", maxsplit=1)[1], "sort": 3, "adult": 1, "filters": "short", "count": 10, "extended": 1}
                        print(params)
                        logger.info(Fore.GREEN + f"Запросил видосик с названием {q}")
                        response, atts = vk.method("video.search", params)["items"], []
                        for i in response:
                            atts.append(f"""video{i["owner_id"]}_{i["id"]}""")
                        random.shuffle(atts)
                        atts = atts[0]
                        params = {"peer_id": event.peer_id ,"keep_forward_messages": 1, "message": "🌐PingTime: {} сек.".format(str(float("{:.2f}".format(time.time() - event.timestamp))).replace("-", "")), "attachment": atts, "message_id": event.message_id, "random_id": 0}
                        vk.method("messages.edit", params)
                    except Exception as error:
                        msg_edit(f"Ошибка\n{error}")
                        logger.info(Fore.GREEN + f"")


                if event.text.startswith(".м")and event.text.split(" ")[1] == "рег":
                    first_name, last_name = user("gen")
                    akk_id = search_id(event, vk, owner_info,)
                    response = requests.get(f"https://vk.com/foaf.php?id={akk_id}")
                    xml = response.text
                    soup = BeautifulSoup(xml, 'lxml')
                    created = soup.find('ya:created').get('dc:date').split('+')[0].replace('T', " ")
                    puk= created
                    x = ''.join(puk)
                    t = created
                    timka = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y %H:%M:%S')
                    msg_edit(f"Дата регистрации {first_name} {last_name}\n{timka}")
                    logger.info(Fore.GREEN + f"Дата регистрации {first_name} {last_name}\n{timka}" )


                if event.text.startswith(f"мрп") and event.from_me == True:
                    try:
                        akk_id = vk.method("messages.getById", {"message_ids": event.message_id})['items'][0]['reply_message']['from_id']
                    except:
                        akk_id = owner_info["id"]
                    finally:
                        try:
                            action = event.text.split("\n", maxsplit=3)[0].split(" ", maxsplit=3)[1]
                        except:
                            vk.method("messages.edit", {"peer_id": event.peer_id ,"keep_forward_messages": 1,"message": f"⚠️ Необходимо указать действие.", "message_id": str(event.message_id), "random_id": 0})
                        else:
                            try:
                                    stiker = event.text.split("\n", maxsplit=3)[0].split(" ", maxsplit=3)[2]
                            except:
                                    stiker = "😈"
                            finally:
                                    users = vk.method("users.get", {"user_ids": akk_id, "name_case": "acc"})[0]
                                    user_ids, user_first_name, user_last_name = users["id"], users["first_name"], users["last_name"]
                                    owner_ids, owner_first_name, owner_last_name = owner_info["id"], owner_info["first_name"], owner_info["last_name"]
                                    try:
                                        replic = event.text.split("\n", maxsplit=1)[1]
                                    except:
                                        vk.method("messages.edit", {"peer_id": event.peer_id ,"keep_forward_messages": 1,"message": f"{stiker} | [id{owner_ids}|{owner_first_name} {owner_last_name}] {action} [id{user_ids}|{user_first_name} {user_last_name}]", "message_id": str(event.message_id), "random_id": 0})
                                    else:
                                        vk.method("messages.edit", {"peer_id": event.peer_id ,"keep_forward_messages": 1,"message": f"{stiker} | [id{owner_ids}|{owner_first_name} {owner_last_name}] {action} {replic} [id{user_ids}|{user_first_name} {user_last_name}]", "message_id": str(event.message_id), "random_id": 0})
    except Exception as error:
        msg_edit(f"Произошла ошибка,подробнее:\n{error}")
        logger.error(Fore.RED + f"Произошла ошибка,подробнее:\n{error}")

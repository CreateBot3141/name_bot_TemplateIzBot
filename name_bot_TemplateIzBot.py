
def get_free_dialog (user_id1,user_id2,dilog,zakaz):
    import iz_func
    import iz_telegram
    db,cursor = iz_func.connect ()
    sql = "select id,name,url,id_chat from telegram_chat where status = '' limit 1;".format()    
    cursor.execute(sql)
    data = cursor.fetchall()
    id  = 0
    url = 0
    id_chat = ''
    name = "Нет"
    for rec in data: 
        id,name,url,id_chat = rec.values() 
        sql = "UPDATE telegram_chat SET status = 'start' WHERE id = "+str(id)+""
        cursor.execute(sql)
        db.commit() 
        sql = "UPDATE telegram_chat SET user_id1 = '"+str(user_id1)+"' WHERE id = "+str(id)+""
        cursor.execute(sql)
        db.commit() 
        sql = "UPDATE telegram_chat SET user_id2 = '"+str(user_id2)+"' WHERE id = "+str(id)+""
        cursor.execute(sql)
        db.commit() 
        sql = "UPDATE telegram_chat SET dilog = '"+str(dilog)+"' WHERE id = "+str(id)+""
        cursor.execute(sql)
        db.commit()         
        sql = "UPDATE telegram_chat SET zakaz = '"+str(zakaz)+"' WHERE id = "+str(id)+""
        cursor.execute(sql)
        db.commit() 
    return url,name,id_chat

def send_user_message (user_id,namebot,word):
    import iz_func
    import iz_telegram
    db,cursor = iz_func.connect ()
    sql = "select id,user_id from bot_user where namebot = '{}'".format(namebot)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:  
        id,user_id_send = rec.values() 
        markup = iz_telegram.get_key_command (user_id_send,namebot,"Ответить","proekt_"+str(word))
        message_out = get_activ_proekt (user_id_send,namebot,word)
        answer = iz_telegram.bot_send (user_id_send,namebot,message_out,markup,0) 

def message_tovar (user_id,namebot,message_id,kod_produkta,regim):    
    name = ''
    price = 0
    about = ''
    import iz_func    
    db,cursor = iz_func.connect ()
    sql = "select id,name,price,kod_1c,about from bot_product where kod_1c = "+str(kod_produkta)+"" 
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,name,price,kod_1c,about  = rec.values()    

def get_activ_proekt (user_id,namebot,lastid):
    import iz_func
    import iz_telegram
    db,cursor = iz_func.connect ()
    sql = "select id,user_id,adress,`system`,`komment`,project,summ from bot_active_user where id = {} limit 1;".format(lastid)
    message_out,menu = iz_telegram.get_message (user_id,'Созданный проект',namebot)
    tip_jab = ""
    about   = ""
    param03 = ""
    param04 = ""
    komment = ""
    lesson  = ""
    price   = 0
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    user_id_m = 0
    for rec in data: 
        id,user_id_m,tip_jab,about,komment,lesson,price = rec.values() 
        lesson =  lesson.replace(' ','_')
    message_out = message_out.replace('%%tip_jab%%',str(tip_jab))   
    message_out = message_out.replace('%%about%%'  ,str(about))
    message_out = message_out.replace('%%lesson%%' ,str(lesson))
    message_out = message_out.replace('%%price%%',str(price))
    message_out = message_out.replace('%%param03%%',str(param03))
    message_out = message_out.replace('%%param04%%',str(param04))
    if str(user_id) == str(user_id_m):
        message_out = message_out.replace('%%komment%%',str(komment))
    else:    
        message_out = message_out.replace('%%komment%%','')
        message_out = message_out.replace('Ваша заметка:','')    

    param07 = "https://t.me/TemplateIzBot?start="+str(lastid)
    message_out = message_out.replace('%%ССылкаНаЗаказ%%',str(param07))

    return message_out

def get_proekt (word):
    import iz_func
    user_id = ''
    db,cursor = iz_func.connect ()
    sql = "select id,user_id,komment from bot_active_user where id = {} limit 1;".format(word)
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,user_id,get_proekt = rec.values() 
    return user_id,get_proekt

def get_dialog (word):
    import iz_func
    user1 = ''
    user2 = ''

    db,cursor = iz_func.connect ()
    sql = "select id,user_id_1,user_id_2,message_out from bot_dialog where id = {} limit 1;".format(word)
    print (sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,user_id_1,user_id_2,message_out = rec.values() 
    return user_id_1,user_id_2,message_out    

def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import time
    import iz_func
    import iz_telegram    
    import datetime
    
    if message_in.find ('/start') != -1:
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ""        
        word  = message_in.replace('/start','')
        try:
           word = int (word)
        except Exception as e:
           word = '' 
        if word != '':
            markup = iz_telegram.get_key_command (user_id,namebot,"Ответить","proekt_"+str(word))
            message_out = get_activ_proekt (user_id,namebot,word)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

    if message_in == '/test':
        message_out = "TEST"
        markup = ''
        answer = iz_telegram.bot_send ('-562241287',namebot,message_out,markup,0)
    

    if message_in == 'Назад':
        backend = iz_telegram.load_variable (user_id,namebot,"backend")
        
        if backend == '':
            message_in = 'Отменить'
        if backend == 'Выбери название предмета':
            message_in = 'Создать заказ'
        if backend == 'Категории предметов':
            message_in = 'add'
        if backend == 'Каталог товаров':
            message_in = 'Ручной поиск'
        if backend == 'Календарь':    
            message_in = 'Ручной поиск'
        if backend == 'Подробнее проект':  
            message_in = 'katalog_0'
            status = ""
        if backend == 'Укажи цену':    
            message_in = 'data_0'
            status = ""            
        if backend == 'Добавь заметку':    
            message_in = '111111111111111111111111111111111111111111111111111111111111111111111'
            status = "Подробнее проект"            

        if backend == 'Отправь все необходимые материалы':
            message_in = '0'
            status = "Укажи цену" 

        if backend == 'Отправить проект':
            message_in = '  '
            status = "Добавь заметку" 

    if message_in.find ('next_sql_') != -1:
        word  = message_in.replace('next_sql_','')
        iz_telegram.next_menu_tovar (user_id,namebot,word)
        markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,'',word,2)
        message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in == 'Отменить':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Отмена','S',0)
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ""

    if message_in == 'Создать заказ' or message_in == 'Я Заказчик':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Создать заказ ссылка','S',0)
        message_out,menu = iz_telegram.get_message (user_id,'Выбери тип работы из списка',namebot)
        list = iz_telegram.get_tovar (user_id,namebot,'Тип работы')
        markup = iz_telegram.simple_menu (user_id,namebot,list)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        iz_telegram.save_variable (user_id,namebot,"Тип курсовой",'')
        iz_telegram.save_variable (user_id,namebot,"status",'Тип работы')
        iz_telegram.save_variable (user_id,namebot,"backend",'')

    if message_in.find ('add') != -1:
        iz_telegram.save_variable (user_id,namebot,"status","Выбери название предмета")
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Выбери название предмета','S',0) 
        iz_telegram.save_variable (user_id,namebot,"Тип курсовой",message_in)
        iz_telegram.save_variable (user_id,namebot,"Урок","")
        iz_telegram.save_variable (user_id,namebot,"backend",'Выбери название предмета')

    if message_in == 'Ручной поиск' or message_in == 'Поиск по словам' :
        label = 'no send'
        parents = "Родитель Продукта в 1С не указан"
        #sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0',parents)
        #markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents,sql_id,2)
        #message_out,menu = iz_telegram.get_message (user_id,'Категории предметов',namebot)
        #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)
        iz_telegram.save_variable (user_id,namebot,"status",'Категории предметов') 
        iz_telegram.save_variable (user_id,namebot,"backend",'Категории предметов') 

    if message_in.find ('katalog_') != -1:
        word  = message_in.replace('katalog_','')
        label = 'no send'
        parents = word
        if_grup = iz_telegram.if_grup (user_id,namebot,word)        
        if if_grup == 'Да':
            sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0',parents)
            #sql_id = iz_telegram.start_list (user_id,namebot,parents,0,'не равно 0','не равно 0')
            markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents,sql_id,2)
            message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)
            iz_telegram.save_variable (user_id,namebot,"status","Каталог товаров")
            iz_telegram.save_variable (user_id,namebot,"backend","Каталог товаров")

        if if_grup == 'Нет' or if_grup == '' or word == '0': 
            db,cursor = iz_func.connect ()
            sql = "UPDATE bot_select_tovar SET koll = 1 WHERE `id_tovar` = '"+str(word)+"'"
            cursor.execute(sql)
            db.commit()   
            message_out = "Календарь"
            iz_telegram.save_variable (user_id,namebot,"Урок",message_in)
            iz_telegram.save_variable (user_id,namebot,"Календарь","")
            iz_telegram.save_variable (user_id,namebot,"status","Календарь")
            d = datetime.date.today()
            markup = iz_telegram.calc_menu (user_id,namebot,2021,5,d.day)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)
            iz_telegram.save_variable (user_id,namebot,"backend",'Календарь') 

    if message_in.find ('data_') != -1:
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Дата выбрана','S',message_id)
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Подробнее проект','S',0)
        iz_telegram.save_variable (user_id,namebot,"status", 'Подробнее проект')
        iz_telegram.save_variable (user_id,namebot,"backend",'Подробнее проект')
        iz_telegram.save_variable (user_id,namebot,"Календарь",message_in)
        iz_telegram.save_variable (user_id,namebot,"Подробнее","")

    if status == 'Подробнее проект':
        dl = len(message_in)
        if dl > 15 and dl<500:  
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Укажи цену','S',0)            
            iz_telegram.save_variable (user_id,namebot,"status",'Укажи цену')
            iz_telegram.save_variable (user_id,namebot,"backend",'Укажи цену')
            iz_telegram.save_variable (user_id,namebot,"Подробнее",message_in)
            iz_telegram.save_variable (user_id,namebot,"Цена","")
        else:
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Ошибка, описание должно','S',0)

    if status == 'Укажи цену':

        if message_in == "Пропустить":
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Добавь заметку','S',0)
            iz_telegram.save_variable (user_id,namebot,"status", 'Добавь заметку')
            iz_telegram.save_variable (user_id,namebot,"backend",'Добавь заметку')
            iz_telegram.save_variable (user_id,namebot,"Заметка","")
        else:    
            try:
                price = float(message_in)  
            except Exception as e:            
                price = ''
            if price != '':
                message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Добавь заметку','S',0)
                iz_telegram.save_variable (user_id,namebot,"status", 'Добавь заметку')
                iz_telegram.save_variable (user_id,namebot,"backend",'Добавь заметку')
                iz_telegram.save_variable (user_id,namebot,"Цена",message_in)
                iz_telegram.save_variable (user_id,namebot,"Заметка","")
            if price == '':
                message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Ошибка, введите только число','S',0)

    if status == 'Добавь заметку':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Отправь все необходимые материалы','S',0)
        iz_telegram.save_variable (user_id,namebot,"status",'Отправь все необходимые материалы')
        iz_telegram.save_variable (user_id,namebot,"backend",'Отправь все необходимые материалы')
        iz_telegram.save_variable (user_id,namebot,"Заметка",message_in)

    if message_in == 'Готово':
        iz_telegram.save_variable (user_id,namebot,"backend","Отправить проект")
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Отправить проект','S',0)        
        param01 = iz_telegram.load_variable (user_id,namebot,"Тип курсовой")
        param01 = param01.replace('add_','')
        param01 = iz_telegram.get_tovar_in_id (user_id,namebot,param01)
        param02 = iz_telegram.load_variable (user_id,namebot,"Цена")
        param03 = iz_telegram.load_variable (user_id,namebot,"Урок")
        param03 = param03.replace('katalog_','')        
        param03 = iz_telegram.get_tovar_in_kod_1c (user_id,namebot,param03)
        param04 = iz_telegram.load_variable (user_id,namebot,"Подробнее")
        param05 = iz_telegram.load_variable (user_id,namebot,"Заметка")
        db,cursor = iz_func.connect ()
        try:
            sql = "INSERT INTO bot_active_user (`adress`,`komment`,`language`,`login`,`namebot`,`project`,`summ`,`system`,`telefon`,user_id,wallet) VALUES ('{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}')".format (param01,param05,'','',namebot,param03,param02,param04,'',user_id,'')        
            cursor.execute(sql)
            db.commit()               
            lastid = cursor.lastrowid 
            iz_telegram.save_variable (user_id,namebot,"Номер проекта",str(lastid))
        except Exception as e:            
            lastid = 0
        message_out = get_activ_proekt (user_id,namebot,lastid)        
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
    
    if message_in.find ('Отправить проект') != -1:
        word = iz_telegram.load_variable (user_id,namebot,"Номер проекта")
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Сообщение отправлено",'S',0) 
        send_user_message (user_id,namebot,word)

        user_send = -1001439234875    #### https://t.me/info_314
        from telebot import types 
        markup = types.InlineKeyboardMarkup()
        key01  = types.InlineKeyboardButton(text='Взять заказ', url='https://t.me/TemplateIzBot?start='+str(word))
        markup.add(key01)
        message_out = get_activ_proekt     (user_send,namebot,word)
        answer      = iz_telegram.bot_send (user_send,namebot,message_out,markup,0)  

    if message_in.find ('proekt_') != -1:
        word        = message_in.replace('proekt_','')
        db,cursor   = iz_func.connect ()
        user_send,nameproekt = get_proekt (word) 
        dialog_1 = ''
        dialog_2 = ''
        sql = "INSERT INTO bot_dialog (message_out,user_id_1,user_id_2,title,title_id,namebot,dialog_1,dialog_2) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format (nameproekt,user_id,user_send,"","","",dialog_1,dialog_2)
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid 
        url1,dialog_1,id_chat_1 = get_free_dialog (user_id,user_send,lastid,word)
        url2,dialog_2,id_chat_2 = get_free_dialog (user_id,user_send,lastid,word)


        message_out,menu = iz_telegram.get_message (user_id,'Вступителное слово чата',namebot)
        #message_out = message_out.replace('%%Процент%%',str(minmin))   
        #message_out = message_out.replace('%%Заявка%%',str(command))
        #markup = ''
        markup = ''
        markup = ''
        answer = iz_telegram.bot_send (id_chat_1,namebot,message_out,markup,0) 
        answer = iz_telegram.bot_send (id_chat_2,namebot,message_out,markup,0) 




        sql = "UPDATE bot_dialog SET dialog_1 = '"+dialog_1+"' WHERE id = "+str(lastid)+""
        cursor.execute(sql)
        db.commit() 
        sql = "UPDATE bot_dialog SET dialog_2 = '"+dialog_2+"' WHERE id = "+str(lastid)+""
        cursor.execute(sql)
        db.commit() 
        message_out,menu = iz_telegram.get_message (user_send,'Согласие исполнителя',namebot)
        message_out = message_out.replace('%%Номер исполнителя%%',str(lastid))   
        message_out = message_out.replace('%%Номер заказа%%',str(word))        
        message_out = message_out.replace('%%Ссылка приглашение%%',str(url1))        
        message_out = message_out.replace('%%Автор%%',str("Скрыто")) 


        markup = ''
        answer = iz_telegram.bot_send (user_send,namebot,message_out,markup,0) 
        message_out,menu = iz_telegram.get_message (user_send,'Ссылка на чат',namebot)
        message_out = message_out.replace('%%Ссылка приглашение%%',str(url2))   
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 

    if message_in.find ('message_start_') != -1:
        word = message_in.replace('message_start_','')
        user1,user2,namedialog = get_dialog (word)
        message_out,menu = iz_telegram.get_message (user_id,'Введите текст послания',namebot)
        message_out = message_out.replace('%%Задача%%',str(namedialog)) 
        message_out = message_out.replace('%%Получатель%%',str(word))
        markup = ""
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)  
        iz_telegram.save_variable (user_id,namebot,"status",'Отправка сообшения клиенту')
        iz_telegram.save_variable (user_id,namebot,"user1",user1)
        iz_telegram.save_variable (user_id,namebot,"user2",user2)
        iz_telegram.save_variable (user_id,namebot,"dialog",word)

    if status == 'Отправка сообшения клиенту':
        dialog = iz_telegram.load_variable (user_id,namebot,"dialog")        
        user1,user2,namedialog = get_dialog (dialog)
        markup = iz_telegram.get_key_command (user_id,namebot,"Ответить","message_start_"+str(dialog))
        message_out,menu = iz_telegram.get_message (user_id,'Новое сообщение',namebot)
        message_out = message_out.replace('%%Отправитель%%',str(dialog))   
        message_out = message_out.replace('%%Задача%%',str(namedialog))   
        message_out = message_out.replace('%%Текст сообщения%%',str(message_in))           
        answer = iz_telegram.bot_send (user1,namebot,message_out,markup,0) 
        answer = iz_telegram.bot_send (user2,namebot,message_out,markup,0) 
        iz_telegram.save_variable (user_id,namebot,"status",'')
 
    if message_in == 'Меню исполнителя':
        message_out,menu = iz_telegram.get_message (user_id,'Создать заказ ссылка',namebot)
        from telebot import types  
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu11 = "Отправить номер"
        menu12 = "Пропустить"
        menu11 = iz_telegram.get_namekey (user_id,namebot,menu11)
        menu12 = iz_telegram.get_namekey (user_id,namebot,menu12)
        markup.row(menu11,menu12)
        menu12 = "Назад"
        menu12 = "Отменить"
        menu11 = iz_telegram.get_namekey (user_id,namebot,menu11)
        menu12 = iz_telegram.get_namekey (user_id,namebot,menu12)
        markup.row(menu11,menu12)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

    if message_in.find ('nextL_') != -1:
        word  = message_in.replace('next_','')
        markup = iz_telegram.calc_menu (user_id,namebot,2021,int(word),0)
        message_out = "ТЕКСТ"
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in.find ('prev_L') != -1:
        word  = message_in.replace('prev_','')
        markup = iz_telegram.calc_menu (user_id,namebot,2021,int(word),0)
        message_out = "ТЕКСТ"
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

            
        
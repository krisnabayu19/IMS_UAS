import requests
import time
import pymysql

db = pymysql.connect("localhost","root","","db_message")
cursor = db.cursor()



request_params = {'token': 'cqLYrD1u0yXHRNBShbmVT5BJr7ZpFwfFL8WvjWBu'}


def insert_msg():
    response = requests.get('https://api.groupme.com/v3/groups/49949239/messages', params=request_params)
    # If there are new messages, check whether any of them are making queries to the bot
    if (response.status_code == 200):
        response_messages = response.json()['response']['messages']



        # Iterate through each message, checking its text
        for message in reversed(response_messages):

            pesan = message["text"]

        print(pesan)
        select = "select *from tb_message"
        cursor.execute(select)
        hasil_select = cursor.fetchall()
        db.commit()
        success=0


    for input_message in hasil_select :
        input_message_db = input_message[1]
        if pesan == input_message_db:
            print("data sama")
            success +=1
            to_send = input_message[2]
            print(message['id'])
            sql = "insert into tb_inbox values (null,'%s','%s','%s','1')" % (message['id'],input_message_db, time.strftime("%Y-%m-%d %H:%M:%S"))
            print(sql)
            cursor.execute(sql)
            db.commit()



        if success >0 :
            print("Pesan akan dibalas")
            post_params = {'bot_id': 'da1e8953c5d0709b0af1bb2110', 'text': to_send}
            requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
            request_params['since_id'] = message['id']
            # sql = "insert into tb_outbox values (null,'%s','%s','%s','0')" %(message['id'],to_send,time.strftime("%Y-%m-%d %H:%M:%S"))
            # print(sql)
            # cursor.execute(sql)
            # db.commit()




        else :

            print("Pesan tidak akan dibalas")
            to_send = input_message[3]
            # post_params = {'bot_id': 'da1e8953c5d0709b0af1bb2110', 'text': to_send}
            # requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
            print(message['id'])
            break


        


while True:
    insert_msg()
    time.sleep(1)

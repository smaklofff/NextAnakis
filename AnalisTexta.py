
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from threading import Thread
import pymorphy2

def pos(word, morth=pymorphy2.MorphAnalyzer()):
    return morth.parse(word)[0].tag.POS


def get_history(id):
    message1 = vk.messages.getHistory(
        offset=-1,
        count=200,
        user_id=id,
        start_message_id=0, )
    count = message1['count']
    offset = -200
    all_messages = []
    while offset >= -(count) - 200:
        message = []
        message = vk.messages.getHistory(
            offset=offset,
            count=200,
            user_id=id,
            start_message_id=0, )
        offset -= 200
        all_messages.extend(message['items'])
    return all_messages, count


def name_editor(name, count, count_of_out_msg, att1, att, pastmxmsg, k, km):
    return ('Пользователь, с которым ведется диалог: {}\n'
            'Общее количество сообщений между мной и тобой: {}\n'
            'Количество отправленных тобой сообщений: {}\n'
            'Количество отправленных мной сообщений: {}\n'
            'Наибольшее количество сообщений за 1 день: {}\n'
            'Количество вложений, отправленных мне: {}\n'
            'Количество вложений, отправленных мной: {}\n'
            'Количество слов в диалоге: {}\n'
            'Количество слов, отправленных мной: {}\n'
            'Количество слов, отправленных тобой: {}\n'.format(name, count, count_of_out_msg,
                                              count - count_of_out_msg,
                                              pastmxmsg + 1, att1, att, k, k - km, km))


class main(Thread):
    def __init__(self, id, name):
        Thread.__init__(self)
        self.all_massage, self.count = get_history(id)
        self.name = name
        self.id = id

    def run(self):
        day, count_of_out_msg, pastday, mxmsgpday, pastmxmsg, att, att1, text, text1 = 0, 0, 0, 0, 0, 0, 0, '', ''
        p, kslovm, finish_words_list = [], [], []
        for i in range(len(self.all_massage)):
            if self.all_massage[i]['from_id'] != 222754285:
                count_of_out_msg += 1
                text1 = text1 + ' ' + self.all_massage[i]['text']
            kslovm = text1.split(' ')
            """Наибольшее количество сообщений в день"""
            day = time.gmtime(self.all_massage[i]['date'])
            day = time.strftime('%j', day)
            if pastday == day:
                pastday = day
                mxmsgpday += 1
            else:
                pastday = day
                if pastmxmsg < mxmsgpday:
                    pastmxmsg = mxmsgpday
                mxmsgpday = 0
            '''Количество вложений'''
            if len(self.all_massage[i]['attachments']) > 0:
                if self.all_massage[i]['from_id'] == 222754285:
                    att += 1
                else:
                    att1 += 1

            text = text + ' ' + self.all_massage[i]['text']
        list = text.split(' ')
        counter = []
        morph = pymorphy2.MorphAnalyzer()
        for i in list:
            try:
                p = morph.parse(i)[0]
                finish_words_list.append(p.normal_form)
            except:
                None

        filter_s = {"NOUN", "ADJF", "ADJS", "COMP", 'VERB', 'INFN',
                    'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'NPRO',
                    'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ', 'NUMB'}

        for i in finish_words_list:
            if pos(i) in filter_s:
                counter.append(i)
        return print(name_editor(self.name, self.count, count_of_out_msg, att1, att,
                                 pastmxmsg, len(counter), len(kslovm)))


def login(access_token):
    """Авторизация"""
    vk_session = vk_api.VkApi(token=access_token)
    return vk_session.get_api(), VkUpload(vk_session), vk_session, VkLongPoll(vk_session)


if __name__ == "__main__":
    vk, upload, vk_session, longpoll = login(
        '*******************************************')
    my_thread1 = main('**********', 'Саша М.')
    my_thread2 = main('*********', 'Никита')

    my_thread1.start()
    my_thread2.start()
    # my_thread3.start()
    # my_thread4.start()


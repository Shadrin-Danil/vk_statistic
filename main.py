import os.path
import requests

import pandas as pd
from ignore.auth_data import token, version
from datetime import datetime, timedelta
from time import sleep

# url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=15&access_token={token}&v={version}"
# req = requests.get(url)
#
# print(req.text)


def get_posts(group_name, members, res_posts):
    if group_name == "soopr_altstu":
        url = f"https://api.vk.com/method/wall.get?domain=soopr_altstu&count=5&axtended=1&" \
              f"access_token={token}&v={version}"
        n = 5
    else:
        url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=15&axtended" \
              f"=1&access_token={token}&v={version}"
        n = 15
    req = requests.get(url)
    src = req.json()
    # n = 15

    all_posts = 0
    likes = 0
    views = 0
    reposts = 0
    comments = 0

    posts = src['response']['items']
    # print(posts[0]['likes']['count'])
    # print(req.text)

    for i in range(n-1):
        if datetime.now() - datetime.fromtimestamp(posts[i]['date']) <= timedelta(7):

            all_posts += 1
            views += posts[i]['views']['count']
            likes += posts[i]['likes']['count']
            reposts += posts[i]['reposts']['count']
            comments += posts[i]['comments']['count']

    res_posts.append([])
    res_posts[len(res_posts)-1].append(group_name)
    res_posts[len(res_posts)-1].append(all_posts)
    res_posts[len(res_posts)-1].append(views)
    res_posts[len(res_posts)-1].append(likes)
    res_posts[len(res_posts)-1].append(reposts)
    res_posts[len(res_posts)-1].append(comments)
    res_posts[len(res_posts)-1].append(members)


def get_members(group_name):
    url = f"https://api.vk.com/method/groups.getMembers?group_id={group_name}&access_token={token}&v={version}"
    req = requests.get(url)
    src = req.json()

    # print(req.text)
    print(src)
    # print(f'Members: {src["response"]["count"]}')
    return src["response"]["count"]


def get_all_pars_vk():
    group_names = ['kpok_altgtu', 'kpos_astu', 'kpop_sp', 'altstu_kvs', 'sgmedia_altstu', 'volonter_altstu',
                   'trening_agtu', 'tutorcentr', 'so_sp_altgtu', 'altstu_feat', 'fit_official',
                   'stf_altstu', 'altgtu_fst', 'ef_altgtu', 'so_altstu', 'utk2018', 'inarchdiz_altgtu', 'inbiohim',
                   'ieiu_astu', 'soopr_altstu']

    res_posts = []

    for i in group_names:
        print(i)
        get_posts(i, get_members(i), res_posts)
        sleep(2)

    # soopr('soopr_altstu', get_members('soopr_altstu'), res_posts)

    res_posts_for_write = [['КпоК'],
                           ['КпоС'],
                           ['КпоП'],
                           ['КВС'],
                           ['Медиацентр'],
                           ['Волонтерский центр'],
                           ['Треннинг центр'],
                           ['Центр Тьюторов'],
                           ['СП'],
                           ['ФЭАТ'],
                           ['ФИТ'],
                           ['СТФ'],
                           ['ФСТ'],
                           ['ЭФ'],
                           ['Студ отряды'],
                           ['УТК'],
                           ['ИнАрхДиз'],
                           ['ИнБиоХим'],
                           ['ИЭиУ'],
                           ['СООПР'],
                           ]

    for item in range(len(res_posts_for_write)):
        res_posts_for_write[item].append(res_posts[item][1])
        res_posts_for_write[item].append(res_posts[item][2])
        res_posts_for_write[item].append(res_posts[item][3])
        res_posts_for_write[item].append(res_posts[item][4])
        res_posts_for_write[item].append(res_posts[item][5])
        res_posts_for_write[item].append(res_posts[item][6])

    for item in res_posts_for_write:
        print(*item)

    new_columns = ['Группы/кол-во', 'Постов', 'Просмотров', 'Лайков', 'Репосотв', 'Комментариев', 'Подписок']

    data_for_excel = pd.DataFrame(res_posts_for_write, columns=new_columns)

    return data_for_excel


def main():

    # /Users/admin/Desktop/excel

    # print(os.path.isdir('\n/Users/admin/Desktop/excel/\n'))


    # За семь прошлых дней
    start_week = datetime.now() - timedelta(7)
    end_week = datetime.now()


    # Подстановка нужной даты
    # start_week = datetime.now() - timedelta(7)
    # end_week = datetime.now() - timedelta(1)
    # print(start_week, end_week)

    if not os.path.exists(f"/Users/admin/Desktop/excel/{start_week.month}_{start_week.day} - {end_week.month}_"
                          f"{end_week.day}.xlsx"):
        print("\nФайла с собранной статистикой по данным групп нет, создаю... \n")

        data_for_excel = get_all_pars_vk()
        print(data_for_excel)
        data_for_excel.to_excel(f"/Users/admin/Desktop/excel/{start_week.month}_{start_week.day} - "
                                f"{end_week.month}_{end_week.day}.xlsx",
                                sheet_name='statistic', index=False)

        print("\nФайл заполнен!\n")

    else:
        print("\nФайл с собранной статистикой по группам есть \n")

    print(
        f"Смотри в дирректории /Users/admin/Desktop/excel/ \n"
        f"Название файла: {start_week.month}_{start_week.day} - {end_week.month}_{end_week.day}.xlsx\n"
          )


if __name__ == '__main__':
    main()

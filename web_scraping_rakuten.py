# -*- coding:utf-8 =*=
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

# 口コミページのURL
url = "https://xxxxxxxx.co.jp"

html = urllib2.urlopen(url)
bsObj = BeautifulSoup(html,"html.parser")

# クチコミリスト
textList = bsObj.findAll("div",{"class":"commentBox"})

for item in textList:

	# 総合
	s_sougou = item.find("span",{"class":"rate"}).text

	# ニックネーム / 性別・年齢
	itemtext = item.find("dl",{"class":"commentReputation"}).find("span",{"class":"user"}).text.strip()
	itemtext = itemtext.split("\n")

	age = None
	gender = None
	if len(itemtext) == 1:
		# ニックネーム
		nickname = itemtext[0].strip()
	elif len(itemtext) == 2:
		# ニックネーム
		nickname = itemtext[0].strip()

		# 性別 / 年齢
		s = itemtext[1].strip().replace(u"[", "")
		s = s.strip().replace(u"]", "")
		s = s.split("/")

		# 年齢
		age = s[0].strip()

		# 性別
		gender = s[1].strip()

	# 投稿日時
	toukou_datetime = item.find("dl",{"class":"commentReputation"}).find("span",{"class":"time"}).text
	toukou_datetime = toukou_datetime.replace(u"年", "/")
	toukou_datetime = toukou_datetime.replace(u"月", "/")
	toukou_datetime = toukou_datetime.replace(u"日", "")

	# 投稿日
	toukou_date = toukou_datetime[0:10]

	# クチコミ
	kuchikomi = item.find("dl",{"class":"commentReputation"}).find("p",{"class":"commentSentence"})
	kuchikomi = str(kuchikomi)
	kuchikomi = kuchikomi.replace('<p class="commentSentence">', '')
	kuchikomi = kuchikomi.replace('</p>', '')

	# 利用用途 / 同伴者 / 宿泊年月
	itemtext = item.find("dl",{"class":"commentReputation"}).find("dl",{"class":"commentPurpose"}).text.strip()
	itemtext = itemtext.split("\n")

	# 利用用途
	r_youto = itemtext[1].strip()

	# 同伴者
	r_douhan = itemtext[3].strip()

	# 宿泊年月
	s = itemtext[5].strip().replace(u"月", "")
	s = s.strip().replace(u"年", "/")
	s = s.split(u"/")

	r_shukuhaku_year = s[0].strip()
	r_shukuhaku_month = s[1].strip()

	# 返信日時
	hensin_datetime = item.find("dl",{"class":"commentHotel"})
	if hensin_datetime != None:
		hensin_datetime = hensin_datetime.find("span",{"class":"time"})
		hensin_datetime = hensin_datetime.text
		hensin_datetime = hensin_datetime.replace(u"年", "/")
		hensin_datetime = hensin_datetime.replace(u"月", "/")
		hensin_datetime = hensin_datetime.replace(u"日", "")

	# 返信コメント
	hensin_comment = item.find("dl",{"class":"commentHotel"})
	if hensin_comment != None:
		hensin_comment = hensin_comment.find("p",{"class":"commentSentence"})
		hensin_comment = str(hensin_comment)
		hensin_comment = hensin_comment.replace('<p class="commentSentence">', '')
		hensin_comment = hensin_comment.replace('</p>', '')

	# 利用プラン / 利用部屋
	rp = item.find("div",{"class":"commentNote"}).findAll("dt")

	r_plan_flg = False
	r_room_flg = False

	for r in rp:
		if r.text == u"ご利用の宿泊プラン":
			r_plan_flg = True
		elif r.text == u"ご利用のお部屋":
			r_room_flg = True

	# 利用プラン
	rp = item.find("div",{"class":"commentNote"}).findAll("dd")

	i = 0
	r_plan = None
	r_room = None
	for r in rp:
		if r_plan_flg == True and r_room_flg == True:
			if i == 0:
				r_plan = r.text
				r_plan = r_plan.strip()
			elif i == 1:
				r_room = r.text
				r_room = r_room.strip()
				r_room = r_room[1:]
				r_room = r_room[:-1]

		elif r_plan_flg == True and r_room_flg == False:
			if i == 0:
				r_plan = r.text
				r_plan = r_plan.strip()

		elif r_plan_flg == False and r_room_flg == True:
			if i == 0:
				r_room = r.text
				r_room = r_room.strip()
				r_room = r_room[1:]
				r_room = r_room[:-1]

		elif r_plan_flg == False and r_room_flg == False:
			r_plan = None
			r_room = None

		i += 1
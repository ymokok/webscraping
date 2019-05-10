# -*- coding:utf-8 =*=
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

# 口コミページのURL
url = "https://xxxxxxxx.co.jp"

html = urllib2.urlopen(url)
bsObj = BeautifulSoup(html,"html.parser")

# ユーザークチコミリスト
textList = bsObj.findAll("div",{"class":"kuchikomi-list-cassette"})

for item in textList:

	# ユーザー
	u_item = item.findAll("div",{"class":"user-kuchikomi"})

	for ui in u_item:

		# ニックネーム / 性別 / 年齢
		list = ui.find("p",{"class":"user-name"})
		list = list.text.split("\n")

		# 改行で分割
		i = 0
		for li in list:
			if li.strip() != "":

				i = i + 1

				if i == 1:
					# ニックネーム
					nickname = li
				elif i == 2:
					# 性別 / 年齢
					s = li.split("/")

					# 性別
					gendar = s[0].strip()

					# 年齢
					age = s[1].strip()

		# 投稿日
		list = ui.find("p",{"class":"post-date"})
		toukou_date = list.text.replace(u"投稿日：", "")

		# タイトル / 口コミ
		list = ui.find("p",{"class":"text"})
		list = list.text.split("\n")

		# 改行で分割
		i = 0
		for li in list:
			if li.strip() != "":

				i = i + 1

				if i == 1:
					# タイトル
					title = li.strip()

				elif i == 2:
					# クチコミ
					kuchikomi = li

		# 評価
		list = ui.find("div",{"class":"rate"})
		list = list.text.split("\n")

		# 改行で分割
		i = 0
		for li in list:
			if li.strip() != "":

				# ☆総合
				s_sougou = li[2:3]
				# ☆部屋
				s_room = li[5:6]
				# ☆風呂
				s_bath = li[8:9]
				# ☆朝食
				s_breakfast = li[15:16]
				# ☆夕食
				s_dinner = li[22:23]
				# ☆サービス
				s_service = li[30:31]
				# ☆清潔感
				s_clean = li[34:35]

				break

		# 利用データ
		list = ui.find("p",{"class":"use-data"})
		list = list.text.split("\n")

		i = 0
		for li in list:
			if li.strip() != "":

				i = i + 1

				if i == 1:

					# 宿泊 年
					r_shukuhaku_year = li[1:5]

					# 宿泊 月
					r_shukuhaku_month = li[6:8]

					# 利用用途
					ry = li[13:].replace(u"】", "")

					if ry == u"一人旅":
						r_youto = 1
					elif ry == u"家族旅行":
						r_youto = 2
					elif ry == u"恋人旅行":
						r_youto = 3
					elif ry == u"友達旅行":
						r_youto = 4
					elif ry == u"夫婦旅行":
						r_youto = 5
					elif ry == u"子連れ旅行":
						r_youto = 6
					elif ry == u"団体旅行":
						r_youto = 7
					elif ry == u"出張":
						r_youto = 8
					elif ry == u"その他":
						r_youto = 9

				elif i == 3:
					# 価格帯
					r_kakakutai = li.strip()

				elif i == 4:
					# 宿泊プラン
					r_plan = li.replace(u"【宿泊プラン】", "").strip()

	# 返信
	h_item = item.findAll("div",{"class":"yado-message"})

	hensin_date = None
	hensin_comment = None
	for hi in h_item:

		# 返信日
		list = hi.find("p",{"class":"post-date"})
		hensin_date = list.text.replace(u"返信日：", "")

		# 返信コメント
		hensin_comment = hi.find("p",{"class":"text"})
		hensin_comment = str(hensin_comment)
		hensin_comment = hensin_comment.replace('<p class="text" style="word-wrap:break-word;">', "")
		hensin_comment = hensin_comment.replace('</p>', "")
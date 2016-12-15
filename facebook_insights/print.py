import matplotlib.pyplot as plt

data = [
    {
      "name": "page_story_adds_by_age_gender_unique",
      "period": "day",
      "values": [
        {
          "value": {
            "U.25-34": 4,
            "U.35-44": 3,
            "U.45-54": 4,
            "U.55-64": 4,
            "U.65+": 4,
            "F.13-17": 27,
            "F.18-24": 214,
            "F.25-34": 147,
            "F.35-44": 126,
            "F.45-54": 132,
            "F.55-64": 107,
            "F.65+": 78,
            "M.13-17": 101,
            "M.18-24": 428,
            "M.25-34": 358,
            "M.35-44": 207,
            "M.45-54": 187,
            "M.55-64": 114,
            "M.65+": 52
          },
          "end_time": "2016-12-01T08:00:00+0000"
        },
        {
          "value": {
            "U.25-34": 5,
            "U.35-44": 1,
            "U.45-54": 7,
            "U.55-64": 6,
            "U.65+": 9,
            "F.13-17": 40,
            "F.18-24": 196,
            "F.25-34": 136,
            "F.35-44": 126,
            "F.45-54": 105,
            "F.55-64": 132,
            "F.65+": 179,
            "M.13-17": 119,
            "M.18-24": 436,
            "M.25-34": 362,
            "M.35-44": 221,
            "M.45-54": 254,
            "M.55-64": 228,
            "M.65+": 269,
            "U.18-24": 2
          },
          "end_time": "2016-12-02T08:00:00+0000"
        },
        {
          "value": {
            "U.25-34": 1,
            "U.35-44": 5,
            "U.55-64": 3,
            "U.65+": 3,
            "F.13-17": 36,
            "F.18-24": 168,
            "F.25-34": 170,
            "F.35-44": 112,
            "F.45-54": 115,
            "F.55-64": 93,
            "F.65+": 116,
            "M.13-17": 95,
            "M.18-24": 436,
            "M.25-34": 381,
            "M.35-44": 215,
            "M.45-54": 197,
            "M.55-64": 124,
            "M.65+": 131,
            "U.13-17": 1
          },
          "end_time": "2016-12-03T08:00:00+0000"
        },
        {
          "value": {
            "U.18-24": 2,
            "U.25-34": 3,
            "U.35-44": 4,
            "U.45-54": 6,
            "U.55-64": 4,
            "U.65+": 5,
            "F.13-17": 34,
            "F.18-24": 212,
            "F.25-34": 159,
            "F.35-44": 119,
            "F.45-54": 118,
            "F.55-64": 92,
            "F.65+": 88,
            "M.13-17": 116,
            "M.18-24": 609,
            "M.25-34": 602,
            "M.35-44": 451,
            "M.45-54": 479,
            "M.55-64": 251,
            "M.65+": 163
          },
          "end_time": "2016-12-04T08:00:00+0000"
        }
      ],
      "title": "Daily Demographics: People Talking About This",
      "description": "Daily: The number of People Talking About the Page by user age and gender (Unique Users)",
      "id": "xxx/insights/page_story_adds_by_age_gender_unique/day"
    }
  ]

gender_age_brackets = ('U.13-17','U.18-24','U.25-34','U.35-44','U.45-54','U.55-64','U.65+','F.13-17','F.18-24','F.25-34','F.35-44','F.45-54','F.55-64','F.65+','M.13-17','M.18-24','M.25-34','M.35-44','M.45-54','M.55-64','M.65+')
gender_tag = ('U', 'F', 'M')
age_tag = ('13-17','18-24','25-34','35-44','45-54','55-64','65+')

ptat_dic = dict.fromkeys(gender_age_brackets)
#Iterate through the response
values = data[0]['values']
#print(values)
for item in values:
  date = item['end_time']
  for v in item['value']:
    ptat_list = []
    age_list = []
    for key in gender_age_brackets:
      ufm = item['value'].get(key, 0)
      ptat_dic[key] = ufm
      ptat_list.append(ufm)
      gender=key[0]
      age=key[2:]
      age_list.append(age)
#  print(age_list)
  print(date)
  print(ptat_list)
  print(len(ptat_list))
  print(ptat_dic)
  plt.bar(range(len(ptat_dic)), ptat_dic.values(), align='center')
  plt.xticks(range(len(ptat_dic)), ptat_dic.keys())
  plt.show()
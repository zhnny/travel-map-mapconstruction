import requests
from lxml import etree
import json
import time

page_num = 1
track_num_arr = []
keyword = "岳麓山"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
page_url = "http://www.foooooot.com/search/trip/all/1/all/time/descent/?page=" + str(page_num) + "&keyword=" + keyword

next_page = True
while(next_page):
    response = requests.get(page_url,timeout=5, headers=headers)
    tree = etree.HTML(response.text)
    trip_list = tree.xpath('//p[@class="trip-title"]/a/@href')
    if(len(trip_list) == 30):
        page_num = page_num + 1
        page_url = "http://www.foooooot.com/search/trip/all/1/all/time/descent/?page=" + str(page_num) + "&keyword=" + keyword
    else:
        next_page = False
    for trip in trip_list:
        track_num_arr.append(trip.split('/')[2])
    time.sleep(6)

print(len(track_num_arr))

num = 0 
for track_num in track_num_arr:
    try:
        #设置重连次数
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        # 设置连接活跃状态为False
        s.keep_alive = False
        time.sleep(6)
        footprint_url = "http://www.foooooot.com/trip/" + str(track_num) + "/footprintsjson/"
        trackjson_url = "http://www.foooooot.com/trip/" + str(track_num) + "/trackjson/"
        footprint_res = requests.get(footprint_url,headers=headers,stream=False,timeout= 10)
        trackjson_res = requests.get(trackjson_url,headers=headers,stream=False,timeout= 10)
        try:
            trackjson = json.loads(trackjson_res.text)
            footprint = json.loads(footprint_res.text)
            with open("./trackdata/origin/trackjson" +  str(track_num) + ".json","w") as tf:
                json.dump(trackjson,tf)
            with open("./trackdata/origin/footprint" +  str(track_num) + ".json","w") as ff:
                json.dump(footprint,ff)
            for track in trackjson:
                with open("./trackdata/trip_" +  str(track_num) + ".txt","a") as tf:
                    tf.write(str(track[1]) + " " + str(track[2]) + " " + str(track[3]) + " " + str(int(track[0])) + "\n")
                with open("./trackdata/all.csv","a") as af:
                    af.write(str(num) + "," + str(track[2]) + "," + str(track[1]) + "," + str(track[3]) + "," + str(track_num) + "," + str(int(track[0])) + "\n")
                    num = num + 1
            footprint_res.close()
            trackjson_res.close()
            del(footprint_res)
            del(trackjson_res) 
        except Exception as we:
            print(we)
            print("ERROR: " + track_num)
            with open("./trackdata/error.txt","a") as af:
                af.write(str(track_num) + '\n')
            footprint_res.close()
            trackjson_res.close()
            del(footprint_res)
            del(trackjson_res) 
    except Exception as ce:
        print(ce)
        time.sleep(60)
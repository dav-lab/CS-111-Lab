import json
import datetime
import ast
import requests
import xmltodict
import bisect

APIKEY='YOUR_KEY_HERE'
VIDEOID='VIDEO_ID'
info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
vidLength=info['items'][0]['contentDetails']['duration']

if info['items'][0]['contentDetails']['caption']=='true':
    subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
    a=xmltodict.parse(subs)
    listOfSubs=a['transcript']['text']

def getSub(time,subList):
    startTimes=[]
    text=[]
    for i in subList:
        startTimes.append(float(i['@start']))
        try:
            text.append(i['#text'])
        except KeyError:
            text.append('No sub')
    breakpoints=startTimes[1:]
    i=bisect.bisect(breakpoints,time)
    return text[i]




file=json.load(open('aonsimJ'))
video=[]

for i in file:
    if i['event_type']=='pause_video' or i['event_type']=='play_video':
        d = json.loads(ast.literal_eval(i['event']))
        videoDict=dict((k,v) for (k,v) in d.items())
        videoDict['time']=datetime.datetime.utcfromtimestamp(i['timestamp']/1000.0)
        videoDict['type']=i['event_type']
        video.append(videoDict)

count={}
for k in video:
    code=k['code']
    if code not in count:
        count[code]=[(k['type'],k['time'],k['currentTime'])]
    else:
        count[code].append((k['type'],k['time'],k['currentTime']))


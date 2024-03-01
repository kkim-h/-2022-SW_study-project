from selenium import webdriver
import time
import pandas as pd
from googleapiclient.discovery import build
import re


api_key = 'AIzaSyBQWXnuUyHN7aJliDTw8DavfcS3aTr2Qx4' #유튜브 데이터를 불러오기 위한 api key


video_ids = ['https://www.youtube.com/watch?v=beIeDDsdcys',
'https://www.youtube.com/watch?v=QCsbVXxY8jw',
'https://www.youtube.com/watch?v=Qg-iFi-HBxY',
'https://www.youtube.com/watch?v=HroOUNq6f3c',
'https://www.youtube.com/watch?v=c6SbVvvm2OU',
'https://www.youtube.com/watch?v=WeeYX1Mfvyk',
'https://www.youtube.com/watch?v=c1RQVN1ighs']
#영상 URL 삽입



filename = 'allcomment_2.csv' # csv로 뽑을 파일명

for i in range(len(video_ids)):
    video_ids[i] = video_ids[i][-11:]



comment_ = []
for i in range(len(video_ids)):
    video_id = video_ids[i]
    comments = list()
    api_obj = build('youtube', 'v3', developerKey=api_key)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=150).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])
     
        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=150).execute()
        else:
            break

#댓글 내용 / 작성자명 / 게시 날짜 / 좋아요 수 크롤링


df = pd.DataFrame()
real = [i[0] for i in comments]

comments_ = []

for i in real:
    pattern=re.compile(r'\s\s+')
    i=re.sub(pattern,' ',i)
    i=re.sub('[^ 가-힣]','',i)
    i=re.sub(' +', ' ', i)
    i=i.strip()
    if len(i) > 5:
        comments_.append(i)
#간단한 전처리


print(comments_[:3])
print(len(comments_))

df['comment'] = comments_
#댓글 내용만 추출하여 dataframe화

df.to_csv(filename, header=['comment'],encoding = 'utf-8-sig', index=None)#csv로 추출
    

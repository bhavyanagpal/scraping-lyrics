import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import json
import plotly.express as px

from plotly.offline import download_plotyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

import plotly.graph_objects as go


#importing data and pritnig head
with open('json file', encoding ='utf8') as f:
    data=json.load(f);

print(data[:5])    


#converrting to dataframe
history=pd.DataFrame()

def extract_json(col_name):
    return[i[col_name] for i in data]

history['artist_name'] =extract_json('artistName')
history['end_time'] = extract_json('endTime')
history['ms_played'] = extract_json('msPlayed')
history['track_time'] = extract_json('trackName')

history.info()

history_og = history
#repeat and append in ase 2 files


#converting endtime from string to datetime
history['end_time'] = pd.to_datetime(history['end_time'])

#divide ms played by suitable number 

history['minutes_played'] = history.ms_played.divide(60000)
history.drop('ms_played', axis=1, inplace-True)

#most played artist by count
most_played_artist_by_count = history.groupby(by='artist_name')['track_name'].count().sort_values(ascending=False)[:15]
print("The most played artists by count of songs are: \n\n{}".format(most_played_artist_by_count))

colors = ['RGB(103,0,31)','RGB(178,24,43)','RGB(214,96,77)','RGB(244,165,130)','RGB(253,219,199)',
           'RGB(247,247,247)','RGB(209,229,240)','RGB(146,197,222)','RGB(67,147,195)','RGB(22,102,172)'
           ,'RGB(5,48,97)' ]

layout =go.Layout(title='Popularity of Artists by Number of Their Song was Played',
                    yaxis=dict(title='Number of times Played',griscolor='rgb(255,255,255',
                    zerolinewidth=1,ticklen=5, gridwidth=2, titlefont=dict(size=5)),
                    xaxis=dict(title="Artist Name") )


fig =go.Figure(data=[go.Bar(x=most_played_artist_by_count.index, y=most_played_artist_by_count,
                            textposition='auto',opacity=1, marker_color=colors)]) 

fig.show()

#most played artist by total time spent
most_played_artist_by_time = history.groupby(by='artist_name')['minutes_played'].sum().sort_values(ascending=False)[:15]
print("The most played artists by total minutes played are: \n\n{}".format(most_played_artist_by_count))

colors = ['RGB(103,0,31)','RGB(178,24,43)','RGB(214,96,77)','RGB(244,165,130)','RGB(253,219,199)',
           'RGB(247,247,247)','RGB(209,229,240)','RGB(146,197,222)','RGB(67,147,195)','RGB(22,102,172)'
           ,'RGB(5,48,97)' ]

layout =go.Layout(title='Popularity of Artists by Total Time of Their Songs was Played',
                    yaxis=dict(title='Amount of time Played',griscolor='rgb(255,255,255',
                    zerolinewidth=1,ticklen=5, gridwidth=2, titlefont=dict(size=5)),
                    xaxis=dict(title="Artist Name") )


fig =go.Figure(data=[go.Bar(x=most_played_artist_by_time.index, y=most_played_artist_by_time,
                            textposition='auto',opacity=1, marker_color=colors)]) 

fig.show()
 

 #total time spent listening to music
history['day']=[d.date() for d in history['end_time']]
history['time']=[d.time() for d in history['end_time']]
history.drop('end_time', axis=1, inplace = True)

day=history.groupby(by=['day'], as_index=False).sum()

fig =px.line(day, x="day", y="minutes played",
            labels={"day":"Month",
                    "minutes_played":"Minutes Played"},
                    color_discrete_sequence=px.colors.sequential.RdBu, title="Timeline of my Streaming History")

fig.show()


#time spent listening to music everyday
date= history_og
date['minutes_played'] = date.ms_played.divide(60000)
date.drop('ms_played', axis=1, inplace=True)

date['day']=pd.DatetimeIndex(date['end_time']).day_time()

date = date.groupby(by=['day'], as_index=False).sum()

fig = px.pie(date, names="day", values="minutes_played", color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()

#artists and songs
artist= history_og
artist['minutes_played'] = artist.ms_played.divide(60000)
artist.drop('ms_played', axis=1, inplace=True)
artist.drop('end_time', axis=1, inplace=True)

artist_1 = artist.drop_duplicates(subset= ["track_name"])
artist_q.drop('minutes_played', axis=1, inplace=True)

artist_1=artist_1.groupby(by=['artist_name'], as_index=False).count()
artist_1 = .artist_1.rename(columns={"track_name":"unique songs"})

artist_1

time = artist.groupby(by=['artist_name'], as_index=False).sum()
time.head()

#top 20 artists
top_artist = pd.merge(artist_1, time, on='artist_name')
top_artist = top_artist.sort_values(by='unique_songs', ascending=False).head(20)
top_artist

fig =px.scatter(top_artist, x="aritst name", y="minutes played", title="Total amount of time spent listening to each artist"
                , size="unique_songs", color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()

#most listened to song
song = history_og
song['minutes_played'] = song.ms_played.divide(60000)
song.drop(['ms_played'], axis=1, inplace=True)

song=song.groupby(by=['track_name'], as_index=False).sum()
song = song.sort_values(by='minutes_played', ascending=False)

song

song_artist = history_og
song_artist = song_artist.sort_values(by='track_name', ascending=False)
song_artist.drop('end_time', axis=1, inplace=True)
song_artist.drop('ms_played', axis=1, inplace=True)
song_artist.head(10)

song_artist= song_artist.drop_duplicates(subset=['track_name'])
#song_artist

song.pd.merge(song_artist, song, on='track_name')
song =song.sort_values(by='minutes_played', ascending=False)
#song

song =song.sort_values(by='minutes_played', ascending=False).head(16)
song.reset_index(inplace=True, drop=True)

songs= song.drop(song.index[0])

fig = px.bar(songs, x="track_name", y="minutes_played", title="Most Listened to Songs",
            color="artist_name", color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()



#top 50 songs
top_50 = history_og
top_50['minutes_played'] = top_50.ms_played.divide(60000)
top_50.drop('ms_played', axis=1, inplace=True)

top_50 = top_50.groupby(['track_name'], as_index=False).sum()
top_50=top_50.sort_values(by='minutes_played', ascending=False).head(51)
top_50.reset_index(inplace=True, drop=True)

top_50.drop(top_50.index[0])

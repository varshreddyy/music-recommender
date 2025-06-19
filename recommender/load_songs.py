import pandas as pd
from recommender.models import Song

def run():
    df = pd.read_csv('spotify_millsongdata.csv')
    df = df[['artist', 'song', 'text']].dropna()

    for _, row in df.iterrows():
        Song.objects.create(artist=row['artist'], song=row['song'], text=row['text'])

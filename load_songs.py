import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_recommender.settings')
django.setup()

from recommender.models import Song

def run():
    df = pd.read_csv('spotify_millsongdata.csv')
    df = df[['artist', 'song', 'text']].dropna()

    for _, row in df.iterrows():
        Song.objects.create(
            artist=row['artist'],
            song=row['song'],
            text=row['text']
        )

    print(f"✅ Loaded {len(df)} songs into the database.")

if __name__ == '__main__':
    run()
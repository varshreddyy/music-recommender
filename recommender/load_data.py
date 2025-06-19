import csv
import os
from recommender.models import Song

def run():
    # Delete existing entries (optional but recommended for reloads)
    Song.objects.all().delete()

    # Load full dataset from Downloads folder
    csv_path = os.path.expanduser("~/Downloads/spotify_millsongdata.csv")

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            if row['artist'] and row['song'] and row['text']:
                Song.objects.create(
                    song=row['song'],
                    artist=row['artist'],
                    text=row['text']
                )
                count += 1
        print(f"✅ Loaded {count} songs into the database.")


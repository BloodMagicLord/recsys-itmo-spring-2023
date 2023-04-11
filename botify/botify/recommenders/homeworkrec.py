import random

from .contextual import Contextual
from .random import Random
from .recommender import Recommender


class HomeworkRec(Recommender):
    good_tracks = {}

    def __init__(self, tracks_redis, catalog):
        self.tracks_redis = tracks_redis
        self.catalog = catalog
        self.random = Random(tracks_redis)
        self.contextual = Contextual(tracks_redis, catalog)

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        if prev_track_time > 0.5:
            self.good_tracks.setdefault(user, []).append(prev_track)

        if self.good_tracks.setdefault(user, []):
            prev_track = random.choice(self.good_tracks[user])
        else:
            return self.random.recommend_next(user, prev_track, prev_track_time)

        return self.contextual.recommend_next(user, prev_track, prev_track_time)

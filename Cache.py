import threading
import datetime

CACHE_MAX_SIZE = 10
MAX_ENTRY_TIME_DELTA = datetime.timedelta(days=1)
CHECK_FOR_CACHE_CLEAR = datetime.timedelta(days=1)


class DuneQueryCache:

    def __init__(self, ):
        super().__init__()
        self.cache = {}
        self.last_cache_clear = datetime.datetime.now()

    def add_to_cache(self, query_id, data):
        self.delete_too_old_entries()
        if len(self.cache) >= 9:
            self.delete_last_entry()
        self.cache[query_id] = (datetime.datetime.now(), data)

    def get_from_cache(self, query_id):
        self.delete_too_old_entries()
        if self.is_in_cache(query_id):
            return self.cache[query_id][1]
        return None

    def is_in_cache(self, query_id) -> bool:
        return query_id in self.cache.keys()

    def delete_from_cache(self, query_id):
        self.cache.pop(query_id)

    def delete_last_entry(self):
        oldest_datetime = None
        oldest_key = None
        for key, value in self.cache.items():
            if oldest_datetime is None or oldest_datetime > value[0]:
                oldest_datetime = value[0]
                oldest_key = key
        self.delete_from_cache(oldest_key)

    def delete_too_old_entries(self):
        if self.last_cache_clear - datetime.datetime.now() > CHECK_FOR_CACHE_CLEAR:
            print('Deleting too old entries')
            for key, value in self.cache.items():
                time_passed_since_creation = datetime.datetime.now() - value[0]
                if time_passed_since_creation > MAX_ENTRY_TIME_DELTA:
                    self.delete_from_cache(key)

from django.core.cache import caches


class BaseCache(object):
    CACHE = 'default'
    CACHE_KEY = ''
    CACHE_KEY_BULK = ''
    TIMEOUT = 300

    @classmethod
    def cache_key(cls, obj_id):
        return cls.CACHE_KEY + '-' + str(obj_id)

    @classmethod
    def _get_cache(cls, cache_key):
        cache = caches[cls.CACHE]
        return cache.get(cache_key)

    @classmethod
    def set_cache(cls, obj_id, data, timeout=300):
        cache = caches[cls.CACHE]
        cache.set(cls.cache_key(obj_id), data, int(timeout) if timeout else None)

    @classmethod
    def get_cache(cls, obj_id, user=None):
        cache = caches[cls.CACHE]
        data = cache.get(cls.cache_key(obj_id))
        if not data:
            # obj = cls.objects.get(id=obj_id)
            return cls.json(obj_id, check_cache=False, user=user)
        return data

    @classmethod
    def _del_cache(cls, key):
        cache = caches[cls.CACHE]
        return cache.delete(key)

    @classmethod
    def del_cache(cls, obj_id):
        return cls._del_cache(cls.cache_key(obj_id))

    @classmethod
    def _set_cache(cls, key, value, timeout=300):
        cache = caches[cls.CACHE]
        cache.set(key, value, int(timeout) if timeout else None)

    @classmethod
    def clear_caches(cls, obj_id):
        cls._del_cache(cls.cache_key(obj_id))
        cls._del_cache(cls.CACHE_KEY_BULK)

    @classmethod
    def bulk_list(cls, timeout=300):

        if timeout is None:
            timeout = cls.TIMEOUT

        cache_data = cls.get_cache(cls.CACHE_KEY_BULK)

        if cache_data:
            return cache_data

        data = cls.objects.filter()
        result = []
        for d in data:
            result.append(d.json(d.id))

        cls._set_cache(cls.CACHE_KEY_BULK, result, timeout)

        return result

    @classmethod
    def json(cls, obj_id, check_cache=True, timeout=300, user=None):
        if check_cache:
            cache_data = cls.get_cache(obj_id)
            if cache_data:
                return cache_data

        try:
            obj = cls.objects.get(id=obj_id)
            data = obj._json()
        except Exception:
            return None

        # if settings.CACHE:
        cls.set_cache(obj_id, data, timeout)

        return data

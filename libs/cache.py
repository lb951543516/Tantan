import pickle
from redis import Redis
from Tantan.config import REDIS


class MyRedis(Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False, keepttl=False):
        pickled_value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        return super().set(name, pickled_value, ex, px, nx, xx, keepttl)

    def get(self, name, default=None):
        # 使用父类的get方法
        pickled_value = super().get(name)
        if pickled_value is None:
            return default

        try:
            value = pickle.loads(pickled_value)
        except(KeyError, EOFError, pickle.UnpicklingError):
            return pickled_value
        else:
            return value


rds = MyRedis(**REDIS)

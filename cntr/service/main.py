import web

from cntr.service import Handle
from cntr.graph import jieba_initialize
from cntr.utils import get_data_path

def add_global_hook():
    g = web.storage({"reply_msg_cache": dict()})
    def _wrapper(handler):
        web.ctx.globals = g
        return handler()
    return _wrapper

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    jieba_initialize(
        type_path=get_data_path('data/type.txt'),
        name_path=get_data_path('data/name.txt')
    )

    app = web.application(urls, globals())
    app.add_processor(add_global_hook())
    app.run()
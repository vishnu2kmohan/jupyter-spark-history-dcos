import os
import re

from bs4 import BeautifulSoup
from notebook.utils import url_path_join
from traitlets.config import LoggingConfigurable
from traitlets.traitlets import Unicode

# try importing lxml and use it as the BeautifulSoup builder if available
try:
    import lxml  # noqa
except ImportError:
    BEAUTIFULSOUP_BUILDER = 'html.parser'
else:
    BEAUTIFULSOUP_BUILDER = 'lxml'  # pragma: no cover

# a tuple of tuples with tag names and their attribute to automatically fix
PROXY_ATTRIBUTES = (
    (('a', 'link'), 'href'),
    (('img', 'script'), 'src'),
)


class SparkHistory(LoggingConfigurable):
    """
    A config object that is able to replace URLs of the Spark frontend
    on the fly.
    """
    url = Unicode(
        'http://{}:{}'.format(
            os.getenv('MESOS_CONTAINER_IP', '127.0.0.1'),
            os.getenv('PORT_SPARKHISTORY', '18080')),
        help='The URL of Spark History Server',
    ).tag(config=True)

    proxy_root = Unicode(
        '/sparkhistory/',
        help='The URL path under which the Spark History will be proxied',
    )

    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.pop('base_url')
        super(SparkHistory, self).__init__(*args, **kwargs)
        self.proxy_url = url_path_join(self.base_url, self.proxy_root)

    def backend_url(self, request):
        request_path = request.uri[len(self.proxy_url):]
        return url_path_join(self.url, request_path)

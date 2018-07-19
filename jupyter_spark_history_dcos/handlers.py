import json
import os

import tornado.web
from notebook.base.handlers import IPythonHandler
from tornado import httpclient


class SparkHistoryHandler(IPythonHandler):

    def initialize(self, spark_history):
        self.spark_history = spark_history

    @tornado.web.asynchronous
    def get(self):
        """
        Fetch the requested URI from the Spark History Server, replace the
        URLs in the response content for HTML responses or return
        the verbatim response.
        """
        http = httpclient.AsyncHTTPClient()
        url = self.spark_history.backend_url(self.request)
        backend_ip = os.getenv('MESOS_CONTAINER_IP', '127.0.0.1')
        backend_port = os.getenv('PORT_SPARKHISTORY', '18080')
        self.spark_history.log.debug('Fetching from Spark History %s', url)
        http.fetch(url, self.handle_response)

    def handle_response(self, response):
        if response.error:
            content_type = 'application/json'
            content = json.dumps({'error': 'SPARK_HISTORY_SERVER_NOT_RUNNING'},
                                 {'backend_url': url},
                                 {'backend_ip': backend_ip},
                                 {'backend_port': backend_port})
        # else:
        #     content_type = response.headers['Content-Type']
        #     if 'text/html' in content_type:
        #         content = self.spark_history.replace(response.body)
        #     else:
        #         # Probably binary response, send it directly.
        #         content = response.body
        self.set_header('Content-Type', content_type)
        self.write(content)
        self.finish()

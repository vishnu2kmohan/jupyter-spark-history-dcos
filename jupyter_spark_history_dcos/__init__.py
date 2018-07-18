from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


def _jupyter_server_extension_paths():  # pragma: no cover
    return [{
        'module': 'jupyter_spark_history_dcos',
    }]


def load_jupyter_server_extension(nbapp):  # pragma: no cover
    from .spark_history import SparkHistory
    from .handlers import SparkHistoryHandler

    spark_history = SparkHistory(
        # add access to NotebookApp config, too
        parent=nbapp,
        base_url=nbapp.web_app.settings['base_url'],
    )

    nbapp.web_app.add_handlers(
        r'.*',  # match any host
        [(spark_history.proxy_url + '.*', 
          SparkHistoryHandler, 
          {'spark_history': spark_history})]
    )
    nbapp.log.info("Jupyter-Spark-History enabled!")

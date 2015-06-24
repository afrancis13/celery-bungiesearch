from bungiesearch import Bungiesearch


def get_model_index(model):
    return Bungiesearch.get_model_index(model.__name__)


def get_model_indexing_query(model):
    return Bungiesearch.get_model_index(model.__name__).Meta.indexing_query

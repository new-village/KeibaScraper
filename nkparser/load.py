'''load.py
'''
from nkparser.helper import load_html, create_url, load_json
from nkparser.parse import NkParser

def load(data_type, entity_id):
    """ Load netkeiba.com data.
    :param data_type: data type of target such as ENTRY, RESULT, ODDS and HORSE
    :param entity_id: entity id of target such as race id or horse id
    :return: :class:`Response <Response>` object
    """
    if data_type == "ENTRY":
        loader = EntryLoader(data_type, entity_id)
    elif data_type == "ODDS":
        loader = OddsLoader(data_type, entity_id)
    elif data_type == "RESULT":
        loader = ResultLoader(data_type, entity_id)
    elif data_type == "HORSE":
        loader = HorseLoader(data_type, entity_id)
    else:
        raise ValueError(f"Unexpected data type: {data_type}")

    return loader.exec()

class NkLoader():
    """ base class of Loaders """
    def __init__(self, data_type, entity_id):
        self.data_type = data_type
        self.entity_id = entity_id
        self.race = None
        self.table = None

class EntryLoader(NkLoader):
    """ Entry data Loader """
    def __init__(self, data_type, entity_id):
        super().__init__(data_type, entity_id)
        base_url = "https://race.netkeiba.com/race/shutuba.html?race_id={ID}"
        self.text = load_html(create_url(base_url, self.entity_id))

    def exec(self):
        """ Description
        """
        parser = NkParser()
        self.race = parser.parse("RACE", self.text)
        self.table = parser.parse(self.data_type, self.text)
        return self

class OddsLoader(NkLoader):
    """ Odds data Loader """
    def __init__(self, data_type, entity_id):
        super().__init__(data_type, entity_id)
        base_url = "https://race.netkeiba.com/api/api_get_jra_odds.html?race_id={ID}&type=1&action=init"
        self.text = load_json(create_url(base_url, self.entity_id))

    def exec(self):
        """ Description
        """
        parser = NkParser()
        self.table = parser.parse(self.data_type, self.text)
        return self

class ResultLoader(NkLoader):
    """ Result data Loader """
    def __init__(self, data_type, entity_id):
        super().__init__(data_type, entity_id)
        base_url = "https://race.netkeiba.com/race/result.html?race_id={ID}"
        self.text = load_html(create_url(base_url, self.entity_id))

    def exec(self):
        """ Description
        """
        parser = NkParser()
        self.race = parser.parse("RACE", self.text)
        self.table = parser.parse(self.data_type, self.text)
        return self

class HorseLoader(NkLoader):
    """ Horse data Loader """
    def __init__(self, data_type, entity_id):
        super().__init__(data_type, entity_id)
        base_url = "https://db.netkeiba.com/horse/{ID}"
        self.text = load_html(create_url(base_url, self.entity_id))

    def exec(self):
        """ Description
        """
        parser = NkParser()
        self.race = parser.parse("RACE", self.text)
        self.table = parser.parse(self.data_type, self.text)
        return self

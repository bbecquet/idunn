import requests
from idunn import settings


class KuzzleClient:
    def __init__(self):
        self.session = requests.Session()

    @property
    def kuzzle_url(self):
        return settings.get('KUZZLE_CLUSTER_URL')

    @property
    def enabled(self):
        return bool(self.kuzzle_url)

    def fetch_event_places(self, bbox, size) -> list:
        if not self.enabled:
            raise Exception('Kuzzle is not enabled')

        left, bot, right, top = bbox[0], bbox[1], bbox[2], bbox[3]

        url_kuzzle = f'{self.kuzzle_url}/opendatasoft/events/_search'
        query = {
            'query': {
                'bool': {
                    'filter': {
                        'geo_bounding_box': {
                            'geo_loc': {
                                'top_left': {
                                    'lat': top,
                                    'lon': left
                                },
                                'bottom_right': {
                                    'lat': bot,
                                    'lon': right
                                }
                            }
                        }
                    },
                    'must': {
                        'range': {
                            'date_end': {
                                'gte': 'now/d',
                                'lte': 'now+31d/d'
                            }
                        }
                    }
                }
            },
            'size': size
        }
        bbox_places = self.session.post(url_kuzzle, json=query)
        bbox_places = bbox_places.json()
        bbox_places = bbox_places.get('result', {}).get('hits', [])
        return bbox_places

kuzzle_client = KuzzleClient()
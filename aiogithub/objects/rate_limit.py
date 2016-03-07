from datetime import datetime

from dateutil.tz import tzutc

from aiogithub.objects.base_object import BaseResponseObject
from aiogithub.utils import return_key


class RateLimitDetail(BaseResponseObject):
    def _normalise_key(self, document, key):
        if key == 'reset' and not isinstance(document['reset'], datetime):
            document['reset'] = datetime.fromtimestamp(document['reset'],
                                                       tz=tzutc())

    @property
    @return_key
    def limit(self) -> int:
        pass

    @property
    @return_key
    def reset(self) -> datetime:
        pass

    @property
    @return_key
    def remaining(self) -> int:
        pass


class RateLimit(BaseResponseObject):
    _url = 'rate_limit'

    @staticmethod
    def _get_key_mappings():
        return {
            'core': RateLimitDetail,
            'search': RateLimitDetail
        }

    def _normalise_document(self, document):
        if document:
            document = document['resources']

        return super()._normalise_document(document)

    @property
    @return_key
    def core(self) -> RateLimitDetail:
        pass

    @property
    @return_key
    def search(self) -> RateLimitDetail:
        pass

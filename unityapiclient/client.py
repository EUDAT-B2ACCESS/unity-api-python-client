import logging
import requests

logger = logging.getLogger(__name__)

DEFAULT_REST_ADMIN_PATH = 'rest-admin'
DEFAULT_API_VERSION = 'v1'
DEFAULT_CERT_VERIFY = True

class UnityApiClient:

    def __init__(self, server_base_url, **kwargs):
        """Constructs a new :class:`UnityApiClient <UnityApiClient>`.

        :param server_base_url: base URL of the Unity IDM server.
        :param rest_admin_path: API endpoint path. Defaults to 
            `rest-admin`.
        :param api_version: API version. Defaults to `v1`.
        :param auth: (optional) Auth tuple to enable HTTP Auth.
        :param cert_verify: (optional) whether the server SSL cert
            will be verified. A CA_BUNDLE path can also be provided. 
            Defaults to ``True``.
        """

        self.__session = requests.Session()
        if 'auth' in kwargs:
            self.__session.auth = kwargs['auth']
        self.__session.verify = kwargs.setdefault('cert_verify', 
            DEFAULT_CERT_VERIFY)
        self.__api_base_url = self._build_api_base_url(
            server_base_url,
            kwargs.setdefault('rest_admin_path', DEFAULT_REST_ADMIN_PATH),
            kwargs.setdefault('api_version', DEFAULT_API_VERSION))

    def get_groups(self):
        try:
            response = self.__session.get(self.__api_base_url + '/group/%2F')
            response.raise_for_status()
            response = response.json()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

        return response

    def _build_api_base_url(self,
        server_base_url, 
        rest_admin_path, 
        api_version):
        
        return '{0}/{1}/{2}'.format(server_base_url, 
                                    rest_admin_path, 
                                    api_version) 

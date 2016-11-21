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

    def get_group(self, group_path=None):
        """Returns all members and subgroups of the specified group.

        If ``group_path`` is not supplied, then the method returns all
        root-level groups and members. 

        @param group_path: (optional) path to group whose subgroups
            and members to retrieve. 

        Example response::

             {
               "subGroups" : [ ],
               "members" : [ 3 ]
             }

        """
        if group_path is not None:
            path = '/group/' + group_path
        else:
            path = '/group/%2F'
        try:
            response = self.__session.get(self.__api_base_url + path)
            response.raise_for_status()
            response = response.json()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

        return response

    def get_entity(self, entity_id):
        """Returns information about the identified entity, including
        its status and all identities.

        @param entity_id: numeric identifier of the entity whose status
            and identities to retrieve.

        Example response::

             {
               "id" : 3,
               "state" : "valid",
               "identities" : [ {
                 "typeId" : "userName",
                 "value" : "tested",
                 "target" : null,
                 "realm" : null,
                 "local" : true,
                 "entityId" : 3,
                 "comparableValue" : "tested"
               }, {
                 "typeId" : "persistent",
                 "value" : "129ffe63-63b9-4467-ae24-6bc889327b0d",
                 "target" : null,
                 "realm" : null,
                 "local" : true,
                 "entityId" : 3,
                 "comparableValue" : "129ffe63-63b9-4467-ae24-6bc889327b0d"
               } ],
               "credentialInfo" : {
                 "credentialRequirementId" : "cr-pass",
                 "credentialsState" : {
                   "credential1" : {
                     "state" : "notSet",
                     "extraInformation" : ""
                   }
                 }
               }
             }

        """
        path = '/entity/' + str(entity_id)
        try:
            response = self.__session.get(self.__api_base_url + path)
            response.raise_for_status()
            response = response.json()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

        return response

    def get_entity_groups(self, entity_id):
        """Returns all groups of the identified entity.

        @param entity_id: numeric identifier of the entity whose groups to 
            retrieve.

        Example response::

             ["/example/sub","/example","/"]

        """
        path = '/entity/' + str(entity_id) + '/groups'
        try:
            response = self.__session.get(self.__api_base_url + path)
            response.raise_for_status()
            response = response.json()
        except (requests.HTTPError, requests.ConnectionError), error:
            raise Exception(error.message)

        return response

    def get_entity_attributes(self, entity_id, group_path=None, 
                              effective=True):
        """Returns all attributes of the identified entity.

        If ``group_path`` is not supplied, then the method returns the 
        attributes in all groups the entity is member of. 

        @param entity_id: numeric identifier of the entity whose attributes to 
            retrieve.
        @param group_path: (optional) path to the group associated with the 
            attributes to retrieve.
        @param effective: (optional) whether to retrieve only directly defined
            or effective attributes (by default True).

        Example response::

            [ 
              {
                "values" : [ "/9j/4AAQSk .... KKKKACiiigD//2Q==" ],
                "direct" : true,
                "name" : "jpegA",
                "groupPath" : "/example",
                "visibility" : "full",
                "syntax" : "jpegImage"
              }, 
              {
                "values" : [ "value" ],
                "direct" : true,
                "name" : "stringA",
                "groupPath" : "/example",
                "visibility" : "full",
                "syntax" : "string"
              } 
            ]

        """
        path = '/entity/' + str(entity_id) + '/attributes'
        params = {'effective': effective}
        if group_path is not None:
            params['group'] = group_path
        try:
            response = self.__session.get(self.__api_base_url + path, 
                                          params=params)
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

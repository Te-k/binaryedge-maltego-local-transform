from canari.maltego.entities import Domain
from canari.maltego.transform import Transform
from canari.framework import EnableDebugWindow
from pybinaryedge import BinaryEdge, BinaryEdgeException, BinaryEdgeNotFound

__author__ = 'Tek'
__copyright__ = 'Copyright 2019, binaryedge Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Tek'
__email__ = 'tek@randhome.io'
__status__ = 'Development'


@EnableDebugWindow
class GetSubdomains(Transform):
    """Returns subdomains of a domain"""

    # The transform input entity type.
    input_type = Domain

    def do_transform(self, request, response, config):
        be = BinaryEdge(config['binaryedge.local.api_key'])
        domain = request.entity.value

        try:
            # Only consider the fist page
            res = be.domain_subdomains(domain)
        except BinaryEdgeException as e:
            raise MaltegoException('BinaryEdge error: %s' % e.msg)
        else:
            for e in res["events"]:
                if e != domain:
                    response += Domain(e)
        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass

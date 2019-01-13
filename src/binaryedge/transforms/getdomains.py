from canari.maltego.entities import IPv4Address, Domain
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
class GetDomains(Transform):
    """Return DNS entries associated with a domain."""

    # The transform input entity type.
    input_type = IPv4Address

    def do_transform(self, request, response, config):
        ip = request.entity.value
        be = BinaryEdge(config['binaryedge.local.api_key'])

        try:
            res = be.domain_ip(ip)
        except BinaryEdgeException as e:
            raise MaltegoException('BinaryEdge error: %s' % e.msg)
        else:
            already = []
            for e in res['events']:
                if e['domain'] not in already:
                    response += Domain(e['domain'])
                    already.append(e['domain'])

        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass

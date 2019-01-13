from canari.maltego.entities import Domain, IPv4Address, MXRecord, NSRecord
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
class GetDNSEntries(Transform):
    """Returns DNS Entries for a domain"""

    # The transform input entity type.
    input_type = Domain

    def do_transform(self, request, response, config):
        be = BinaryEdge(config['binaryedge.local.api_key'])
        domain = request.entity.value

        try:
            # Only consider the fist page
            res = be.domain_dns(domain)
        except BinaryEdgeException as e:
            raise MaltegoException('BinaryEdge error: %s' % e.msg)
        else:
            already = [domain]
            for event in res['events']:
                if 'A' in event:
                    for ip in event['A']:
                        if ip not in already:
                            response += IPv4Address(ip)
                            already.append(ip)
                if 'domain' in event:
                    if event['domain'] not in already:
                        response += Domain(event['domain'])
                        already.append(event['domain'])
                if 'MX' in event:
                    for mx in event['MX']:
                        if mx not in already:
                            response += MXRecord(mx)
                            already.append(mx)
                if 'NS' in event:
                    for ns in event['NS']:
                        if ns not in already:
                            response += NSRecord(ns)
                            already.append(ns)
        return response

        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass

from canari.maltego.entities import IPv4Address, Banner, Domain, Port
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
class GetIPInfo(Transform):
    """Returns any interesting information from the last scan"""

    # The transform input entity type.
    input_type = IPv4Address

    def do_transform(self, request, response, config):
        be = BinaryEdge(config['binaryedge.local.api_key'])
        ip = request.entity.value

        try:
            res = be.host(ip)
        except BinaryEdgeException as e:
            raise MaltegoException('BinaryEdge error: %s' % e.msg)
        else:
            already = []
            for port in res['events']:
                response += Port(port['port'])
                for result in port['results']:
                    if result['origin']['type'] == 'ssl':
                        cert = result['result']['data']['cert_info']['certificate_chain'][0]
                        # How to return a certificate ?
                        if 'commonName' in cert['as_dict']['subject']:
                            d = cert['as_dict']['subject']['commonName']
                            if d not in already:
                                response += Domain(d)
                                already.append(d)
                        if 'extensions' in cert['as_dict']:
                            if 'X509v3 Subject Alternative Name' in cert['as_dict']['extensions']:
                                for domain in cert['as_dict']['extensions']['X509v3 Subject Alternative Name']['DNS']:
                                    if domain not in already:
                                        response += Domain(domain)
                                        already.append(domain)
                    if result['origin']['type'] in ['http', 'grabber']:
                        if 'server' in result['result']['data']['response']['headers']:
                            banner = result['result']['data']['response']['headers']['server']
                            if banner not in already:
                                response += Banner(banner)
                                already.append(banner)
        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass

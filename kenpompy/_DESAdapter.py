from sys import version_info
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

CIPHERS = (
    ':@SECLEVEL=2:ECDH+AESGCM:ECDH+CHACHA20:ECDH+AES:DHE+AES:!aNULL:!eNULL:!aDSS:!SHA1:!AESCCM'
)

def environment_requires_DES_adapter():
    return version_info.major == 3 and version_info.minor < 11

class DESAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests to avoid Cloudflare filtering based on SSL profiling
    Adapted from the research provided by Nick Ostendorf (@nickostendorf) in https://github.com/j-andrews7/kenpompy/issues/33
    """

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)

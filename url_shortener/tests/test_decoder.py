from unittest import TestCase

from decoders import Base62


class DecoderTests(TestCase):
    def test_encode(self):
        assert Base62.encode(0) == '0'
        assert Base62.encode(999) == 'g7'

    def test_decode(self):
        assert Base62.decode('g7') == 999
        assert Base62.decode('0') == 0

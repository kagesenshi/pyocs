from base import registerDecoder
from person import xml_decoder as persondecoder

registerDecoder('xml', 'person', persondecoder)

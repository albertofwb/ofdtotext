import io
from zipfile import PyZipFile
import cssselect2
from defusedxml import ElementTree


class OFDFile(object):
    header = None
    zf:PyZipFile

    def __init__(self, fobj):
        self.zf = fobj if isinstance(fobj, PyZipFile) else PyZipFile(fobj)
        self.node_tree = self.read_node('OFD.xml')

        # parse node
        self.document_node = self.read_node(self.node_tree['DocBody']['DocRoot'].text)
        self.document = OFDDocument(self.zf, self.document_node)

    def read_node(self, location):
        document = self.zf.read(location)
        tree = ElementTree.fromstring(document)
        root = cssselect2.ElementWrapper.from_xml_root(tree)
        return Node(root)

    def get_text(self):
        for i in self.document.pages:
            for j in i.content.layer.text_code:
                print(j.text)


class OFDDocument(object):
    def __init__(self, _zf, node, n=0):
        self.pages = []
        self.name = f'Doc_{n}'
        self.node = node
        self.physical_box = [float(i) for i in node['CommonData']['PageArea']['PhysicalBox'].text.split(' ')]
        if isinstance(node['Pages']['Page'], list):
            sorted_pages = sorted(node['Pages']['Page'], key=lambda x: int(x.attr['ID']))
        else:
            sorted_pages = [node['Pages']['Page']]
        for i, p in enumerate(sorted_pages):
            document = _zf.read(self.name + '/' + sorted_pages[i].attr['BaseLoc'])
            tree = ElementTree.fromstring(document)
            root = cssselect2.ElementWrapper.from_xml_root(tree)
            page_node = Node(root)
            self.pages.append(OFDPage(self, f'Page_{i}', page_node))


class TextCode:
    def __init__(self, text_code):
        self.text = text_code.text


class TextObject:
    def __init__(self, text_obj):
        self.text_code = [TextCode(i['TextCode']) for i in text_obj.children]


class Layer:
    def __init__(self, layer):
        self.text_obj = layer['TextObject']


class Content:
    def __init__(self, content):
        self.layer = TextObject(content['Layer'])


class OFDPage(object):
    def __init__(self, parent: OFDDocument, name, page_node):
        self.parent = parent
        self.content = Content(page_node['Content'])


class Node(dict):
    def __init__(self, element):
        super().__init__()
        self.element = element
        node = element.etree_element

        self.children = []
        self.text = node.text
        self.tag = (element.local_name
                    if element.namespace_url in ('', 'http://www.ofdspec.org/2016') else
                    '{%s}%s' % (element.namespace_url, element.local_name))
        self.attr = node.attrib
        for child in element.iter_children():
            child_node = Node(child)
            self.children.append(child_node)
            if child_node.tag:
                if child_node.tag in self:
                    if isinstance(self[child_node.tag], list):
                        self[child_node.tag].append(child_node)
                    else:
                        self[child_node.tag] = [self[child_node.tag], child_node]
                else:
                    self[child_node.tag] = child_node

    def __repr__(self):
        return f'Tag: {self.tag}, Attr: {self.attr}, Text: {self.text}'

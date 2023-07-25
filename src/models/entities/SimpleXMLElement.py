import xml.dom.minidom
class SimpleXMLElement:
    "Clase para Manejo simple de XMLs"
    def __init__(self, text = None, element = None, document = None):
        if text:
            self.__document = xml.dom.minidom.parseString(text)
            self.__element = self.__document.documentElement
        else:
            self.__element = element
            self.__document = document
    def addChild(self,tag,text=None):
        element = self.__document.createElement(tag)
        if text:
            element.appendChild(self.__document.createTextNode(str(text)))
        self.__element.appendChild(element)
    def asXML(self,filename=None):
        return self.__document.toxml('utf8')
    def __getattr__(self,tag):
        try:
            return SimpleXMLElement(
                element=self.__element.getElementsByTagName(tag)[0],
                document=self.__document)
        except:
            raise RuntimeError("Tag not found: %s" % tag)
    def __getitem__(self,item):
        return getattr(self,item)
    def __contains__( self, item):
        return self.__element.getElementsByTagName(item)
    def __unicode__(self):
        return self.__element.childNodes[0].data
    def __str__(self):
        return self.__element.childNodes[0].data.encode("utf8","ignore")
    def __repr__(self):
        return repr(self.__str__())
    def __int__(self):
        return int(self.__str__())
    def __float__(self):
        return float(self.__str__())
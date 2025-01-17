class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            html = ''
            for prop in self.props:
                html += ' ' + prop + '="' + str(self.props[prop]) + '"'
            return html

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        
        html = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return html

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

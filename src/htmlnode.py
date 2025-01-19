class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, HtmlNode):
            return False
        if type(self) != type(other):
            return False

        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            html = ''
            for prop in self.props:
                html += ' ' + prop + '="' + str(self.props[prop]) + '"'
            return html
        return ''

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if not self.children:
            raise ValueError("Invalid HTML: no children")
        child_html = ''
        for child in self.children:
            child_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

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

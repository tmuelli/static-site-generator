from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None or self.tag == "":
            return self.value

        formatted_props = ""
        if self.props is not None:
            formatted_props = self.props_to_html()

        return f"<{self.tag}{formatted_props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTML node with tag {self.tag} and value {self.value} has as props {self.props}."
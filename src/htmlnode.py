class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented yet.")

    def props_to_html(self):
        if self.props is None or self.props == "":
            return ""

        formatted_props = ""
        for prop in self.props:
            formatted_props += f" {prop}=\"{self.props[prop]}\""
        return formatted_props

    def __repr__(self):
        return f"HTML node with tag {self.tag} and value {self.value} has as children {self.children} and as props {self.props_to_html()}."
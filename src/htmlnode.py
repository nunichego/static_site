class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError

    def to_html(self):
        if self.tag == None:
            return f"{self.value}"
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("tag is missing")
        if children is None:
            raise ValueError("children parameter value is missing")
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is missing")
        if self.children is None:
            raise ValueError("children parameter value is missing")
        result = f"<{self.tag}{self.props_to_html()}>"
        return result + "".join(
            list(map(lambda x: x.to_html(),self.children))) + f"</{self.tag}>"
    
parent1 = ParentNode("div", [LeafNode(
            "some text", "p")], {"class": "container", "id": "main"})
    
print(parent1.to_html())
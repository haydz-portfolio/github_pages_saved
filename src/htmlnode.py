class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props



    def to_html(self):
        raise NotImplementedError("to_html method not implemented")


    def props_to_html(self):
        props = self.props
        if props is None:
            return ""
        hold = []
        for prop in props:
            hold.append(f' {prop}="{self.props[prop]}"')
        return "".join(hold)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag,value, None, props)
        #self.tag = tag
#        self.value = value
       # self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
      #  if self.props is None:
      #      props = ""
      #  else:
       #     props = super().props_to_html()
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self,  tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = None

    def to_html(self):
        if self.tag == "":
            raise ValueError("Missing a tag")
        if self.children == "":
            raise ValueError("Missing Children")
        
        children = ""
        for child in self.children:
            if child == "":
                return None
            children += child.to_html()

            #what is base case? if self.children is blank
        return f"<{self.tag}>{self.props_to_html()}{children}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"





















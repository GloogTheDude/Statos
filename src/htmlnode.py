
class HTMLNode():
    
    def __init__(self, tag=None, value=None,children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props= props
    
    def __repr__(self):
        return f"""tag = {self.tag},
                value = {self.value},
                children = {self.children},
                props = {self.props}"""

    def __eq__(self,value):
        if self.tag != value.tag: return False
        if self.value != value.value: return False
        if self.children!= value.children: return False
        if self.props != value.props : return False
        return True
        

    def to_html(self):
        raise NotImplemented("need to be overriden")
    
    def props_to_html(self):
        s =""
        if self.props is not None:
            for d in self.props.keys():
                s +=f" {d}=\"{self.props[d]}\""
        return s
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def __repr__(self):
        return f"""tag = {self.tag},
                value = {self.value},
                props = {self.props}"""
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Value shouldn't be None") 
        if self.tag is None or "":
            return self.value
        return(f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag not defined")
        if self.children is None:
            raise ValueError("Children not defined")
        props_string= self.props_to_html()
        s = f"<{self.tag}{props_string}>"
        for c in self.children:
            s+= f"{c.to_html()}" 
        s+= f"</{self.tag}>"

        return s
    
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
from anytree.exporter import DotExporter
from anytree import NodeMixin, RenderTree

# "type": [PROGRAMA, ID, SE]
# "scope": [Node's scope]
# "operation": [What this Node do?]
# "visible_scopes": [What attributes this Node can access?]
# "callable": [It's a function?]
# "variable": [It's a variable?]
# "dimentions": [If is a vector, yours dimentions]
# "return_type": [Node return type ('inteiro'|'flutuante'|'vazio')]
# "identifier": [Name|Number found in code]
# "children": [Adjacent Nodes in tree]
# "params_types": [If is a function, yours parameters attributes]

node_sequence = 0

class MyNode(NodeMixin):  # Add Node feature   

  def __init__(self, name, parent=None, id=None, type=None, label=None, children=None):
    super(MyNode, self).__init__()
    global node_sequence

    if (id):
      self.id = id
    else:
      self.id = str(node_sequence) + ': ' + str(name)
        
    self.label = name
    self.name = name
    node_sequence = node_sequence + 1
    self.type = type
    self.parent = parent
    if children:
      self.children = children

  def nodenamefunc(node):
    return '%s' % (node.name)

  def nodeattrfunc(node):
    return '%s' % (node.name)

  def edgeattrfunc(node, child):
    return ''

  def edgetypefunc(node, child):
    return '--'

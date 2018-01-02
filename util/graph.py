from parse.ast import Node
import re
from antlr4 import *

def graphviz(t, is_root_node, node_text, get_children, relations=[], labels={}, node_key=0):
    child_key = node_key

    labels[node_key] = sanitize_graphviz_label(node_text(t))

    if is_root_node(t):
        return node_key, relations, labels

    for child in get_children(t):
        child_key += 1
        relations.append((node_key, child_key))
        child_key += graphviz(child, is_root_node, node_text, get_children,  relations, labels, child_key)[0]

    return child_key, relations, labels


def graphviz_output(relations, labels):
    out = ""
    out += "digraph g {\n"
    for relation in relations:
        out += "\t{} -> {}\n".format(relation[0], relation[1])
    for k, v in labels.items():
        out += "\t{}[label=\"{}\"]\n".format(k, v)
    out += "}\n"

    return out


def ctx_text(ctx, symbolic_names):
    if isinstance(ctx, tree.Tree.TerminalNodeImpl):
        pattern = re.compile(r'\s+')
        text = re.sub(pattern, '', ctx.symbol.text)

        if len(text) > 0:
            return "{}({})".format(symbolic_names[ctx.symbol.type], text)
        else:
            return "{}".format(text)

    else:
        return ctx.__class__.__name__.replace("Context", "")


def sanitize_graphviz_label(text):
    return text.replace("\"", "\\\"")


def draw_syntax_tree(theTree, symbolic_names):
    out = graphviz(theTree, lambda t: isinstance(t, tree.Tree.TerminalNodeImpl), lambda x: ctx_text(x, symbolic_names), lambda x: x.getChildren())
    write_gv_output(out)


def draw_ast(ast : Node):
    out = graphviz(ast, lambda t: len(ast.get_children()) == 0, lambda x: x.__str__(), lambda x : x.get_children())
    write_gv_output(out)


def write_gv_output(output):
    gv = graphviz_output(output[1], output[2])
    f = open("graphviz", "w+")
    f.write(gv)
    f.close()

from dash import dcc
from dash import html

def explanation_component(md_file,id=None,header=None):
    if not id:
        id = md_file.replace(".md","")
    comp_list = []
    if header:
        h1 = html.H1(children=header)
        comp_list.append(h1)
    with open(f"text_scripts/{md_file}","r") as f:
        txt = f.read()
    md_element = dcc.Markdown(txt)
    comp_list.append(md_element)

    inner_div = html.Div(
        comp_list,
        style = {
            "width":"800px"
        }
    )

    outer_div = html.Div(
        inner_div,
        style={
            "display":"flex",
            "flex-direction":"column",
            "align-items":"center",
            "background-color":"tan"
        }
    )
    return outer_div
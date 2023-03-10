import re

from flask import Flask, request, render_template
app = Flask(__name__)

file = open("templates/index.html", "r")

html_content = file.read().replace("\n", "")

class Element:
    def __init__(self, tag, attrs=None, parent=None, content=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.parent = parent
        self.children = []
        self.content = content

    def __repr__(self):
        attrs = " ".join(f"{k}='{v}'" for k, v in self.attrs.items())
        return f"<{self.tag} {attrs}>"

def parseHtml(html_content, stack=[]):
    pattern = re.compile(r"<(\w+)(.*?)>(.*?)</\1>|<(\w+)(.*?)\s*/?>")

    for match in re.finditer(pattern, html_content):
        tag = ""
        attrs = ""
        content = None

        tag1, attrs1, content1, tag2, attrs2 = match.groups()
        if tag1:
            tag, attrs, content = tag1, attrs1, content1

            # Remove unescaped whitespace
            content = " ".join(content.split())
        else:
            tag, attrs, content = tag2, attrs2, None

        attrs = dict(re.findall(r'(\w+)=[\'"](.*?)[\'"]', attrs))
        element = Element(tag, attrs, stack[-1], content)
        stack[-1].children.append(element)

        if content is not None:
            stack.append(element)
            content = parseHtml(content, stack)
            stack.pop()

    return stack[0]

def findElement(tagName, element, result=None):
    if element.tag == tagName:
        result = element

    for child in element.children:
        result = findElement(tagName, child, result)

    return result

def print_dom(element, level=0):
    prefix = "  " * level

    print(f"{prefix}<{element.tag} {' '.join(f'{k}={v}' for k, v in element.attrs.items())}>")
    
    for child in element.children:
        print_dom(child, level + 1)

    print(f"{prefix}</{element.tag}>")

def dom_to_string(element):
    result = "<div class='element-container'><span>"
    
    if len(element.children) > 0:
        result += "<div class='toggle-child-button'></div>"

    result += element.tag + "</span>"

    if len(element.children) > 0:
        result += "<div class='element-child-container'>"

        for child in element.children:
            result += dom_to_string(child)

        result += "</div>"

    elif element.content:
        result += "<div class='element-content'>" + element.content + "</div>"

    result += "</div>"

    return result

@app.route('/', methods=['GET'])
def index():
    dom = parseHtml(html_content, [Element("document")])

    return render_template('index.html', domContent=dom_to_string(dom))

if __name__ == '__main__':
    app.run()

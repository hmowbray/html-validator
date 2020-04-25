import shlex

html = """<!DOCTYPE html>
<html>
    <body>
        <!-- comment -->
        <n style="color:white;padding:20px;">
            <br />
            <applet></applet>
            <h2 style="color:blue;font-size:18px;">London</h2>
            <p id="para">London is the capital city of England.</p>
            <p align="center">There are 13 million people</p>
            <textarea class="harris text" disabled></textarea>
        </div> 
    </l>"""

HTMLElements = {
    "!--",
    "!DOCTYPE",
    "a",
    "abbr", 
    "acronym", 
    "address", 
    "applet", 
    "area", 
    "article", 
    "aside", 
    "audio", 
    "b", 
    "base", 
    "basefont", 
    "bdi", 
    "bdo", 
    "big", 
    "blockquote", 
    "body", 
    "br", 
    "button", 
    "canvas", 
    "caption", 
    "center", 
    "cite", 
    "code", 
    "col", 
    "colgroup", 
    "data", 
    "datalist",  
    "dd", 
    "del", 
    "details", 
    "dfn", 
    "dialog", 
    "dir", 
    "div", 
    "dl", 
    "dt", 
    "em", 
    "embed", 
    "fieldset", 
    "figcaption", 
    "figure", 
    "font", 
    "footer", 
    "form", 
    "frame", 
    "frameset", 
    "h1", 
    "h2", 
    "h3", 
    "h4", 
    "h5", 
    "h6", 
    "head", 
    "header", 
    "hr", 
    "html", 
    "i", 
    "iframe", 
    "img", 
    "input", 
    "ins", 
    "kbd", 
    "label", 
    "legend", 
    "li", 
    "link", 
    "main", 
    "map", 
    "mark", 
    "meta", 
    "meter", 
    "nav", 
    "noframes", 
    "noscript", 
    "object", 
    "ol", 
    "optgroup", 
    "option", 
    "output", 
    "p", 
    "param", 
    "picture", 
    "pre", 
    "progress", 
    "q", 
    "rp", 
    "rt", 
    "ruby",  
    "s", 
    "samp", 
    "script", 
    "section", 
    "select", 
    "small", 
    "source", 
    "span", 
    "strike", 
    "strong", 
    "style", 
    "sub", 
    "summary", 
    "sup", 
    "svg", 
    "table", 
    "tbody", 
    "td", 
    "template", 
    "textarea", 
    "tfoot", 
    "th", 
    "thead", 
    "time", 
    "title", 
    "tr", 
    "track", 
    "tt", 
    "u", 
    "ul", 
    "var", 
    "video", 
    "wbr", 
}

deprecatedHTMLElements = {
    "acronym": "use <abbr>",
    "applet": "use <embed> or <object>",
    "basefont": "use CSS",
    "big": "use CSS",
    "center": "use CSS",
    "dir": "use <ul>",
    "font": "use CSS",
    "frame": "use <iframe>",
    "frameset": "use <iframe>",
    "noframes": "use <iframe>",
    "strike": "use <del> or <s>",
    "tt": "use CSS",
}


colors = {
    "invalid": "\033[101m",
    "expected": "\033[101m",
    "unexpected": "\033[101m",
    "deprecated": "\033[105m",
}

deprecatedHTMLAttributes = {
    "align": "use CSS",
    "bgcolor": "use CSS",
    "border": "use CSS",
    "color": "use CSS",
    "dropzone": "attribute no longer available",
    "translate": "attribute no longer available",
}

def throwError(type, text, lineNumber):
    print(colors[type.split(" ")[0]] + "error: " + type + text + (">" if (type.endswith("<") or (type.endswith("</"))) else "'") + " @ Line " + str(lineNumber) + "\033[0m")
def validate(html):
    for h in html.split("\n"):
        print("\033[94m" + h + "\033[0m")
    arr = []
    html = html.replace("<", "~<")
    html = html.replace(">", ">~")
    html = html.split("\n")
    linenum = 1
    while (linenum <= len(html)):
        line = html[linenum-1]
        line = line.split("~")
        for l in line:
            if (l.startswith("<")):
                if (l[1] != "/"):
                    element = l[1:len(l)-1].split(" ")[0]
                    #check validity of new element and add to arr's stack
                    if (not (element in HTMLElements)):
                        throwError("invalid element <", element, linenum)
                    elif (not(element.startswith("!"))):
                        if(not(l.endswith("/>"))):
                            arr.append(element)
                        if(element in deprecatedHTMLElements.keys()):
                            throwError("deprecated element <", element, linenum)
                            print("\033[105m" + deprecatedHTMLElements[element] + "\033[0m")
                        attributeArray = shlex.split(l[1:len(l)-1])
                        attributeArray.pop(0)
                        for at in attributeArray:
                            if (at.split("=")[0] in deprecatedHTMLAttributes):
                                throwError("deprecated attribute '", at.split("=")[0], linenum)
                else:
                    #remove from arr's stack
                    element = l[2:len(l)-1]
                    if(arr[len(arr)-1] == element):
                        arr.pop(-1)
                    elif (element in arr):
                        arr.reverse()
                        ind = arr.index(element)
                        arr.reverse()
                        ind = len(arr) - ind
                        newarr = arr[ind:len(arr)]
                        for r in arr[ind:len(arr)]:
                            throwError("expected </", r, linenum)
                        arr = arr[0:ind-1]
                    else:
                        if(not(element in HTMLElements)):
                            throwError("unexpected and invalid </", element, linenum)
                        else:
                            throwError("unexpected </", element, linenum)
        linenum+=1
    arr.reverse()
    for a in arr:
        throwError("expected </", a, (len(html)-1))


validate(html)

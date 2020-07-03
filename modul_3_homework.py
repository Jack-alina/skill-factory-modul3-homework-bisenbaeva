class HTML:
    def __init__(self, tag):
        self.tag = tag
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        my_html.write("<html>" + "\n") # пишем в test.html открывающий тэг html и перенос строки
        for child in self.children:
            my_html.write(child.all_self +"\n") # пишем в test.html то, что получили из дочерних классов, и перенос строки
        my_html.write("</html>") # пишем в test.html закрывающий тэг html и перенос строки


class TopLevelTag(HTML):
    def __init__(self, tag):
        self.tag = tag
        self.children = []
        self.all_self = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        all_child_self = ""
        for child in self.children:
            all_child_self += "  " + child.all_self + "\n" # выделили в отдельную переменную то, что вернули нам все дочерние классы, и добавили "  " для отступа в html-файле
            self.all_self = "<%s>" % self.tag + "\n"  + all_child_self + "</%s>" % self.tag # собираем воедино открывающий тэг, child.all_self и закрывающий тэг с необходимым переносом строки       

class Tag:
    def __init__(self, tag, is_single=False):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.children = []
        self.is_single = is_single
        self.all_self = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs) #разделяем пробелом атрибуты тэгов

        if self.children:
            all_child_self = ""
            for child in self.children:
                all_child_self += "  " + child.all_self + "\n" + "  " # выделили в отдельную переменную то, что вернули нам все дочерние классы, и добавили "  " для отступов в html-файле
                self.all_self = "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs) + "\n" + "  " + all_child_self + "</%s>" % self.tag # собираем воедино открывающий тэг, child.all_self и закрывающий тэг с необходимым переносом строки       

        else:    
            if self.is_single:
                self.all_self = "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)

            elif len(attrs) == 0: #если у тега нет атрибутов, то после названия тэга пробел не нужен
                self.all_self = "<{tag}{attrs}>{text}</{tag}>".format(
                        tag=self.tag, attrs=attrs, text=self.text
                    )
            else: #если у тэга есть хотя бы один атрибут, то нужен пробел после названия тэга 
                self.all_self = "<{tag} {attrs}>{text}</{tag}>".format(
                        tag=self.tag, attrs=attrs, text=self.text
                    )
my_html = open("test.html", "w")
with HTML("html") as doc:
    with TopLevelTag ("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head.children.append(title)
        doc.children.append(head)

    with TopLevelTag ("body") as body:
        with Tag("h1") as h1:
            h1.text = "Test"
            h1.attributes["class"] = "main-text"
            body.children.append(h1)
        doc.children.append(body)

        with Tag("div") as div:
            div.attributes["class"] = "container container-fluid"
            div.attributes["id"] = "lead"
            body.children.append(div)
            
            with Tag("p") as p:
                p.text = "another test"
                div.children.append(p)

            with Tag("img") as img:
                img.is_single = True
                img.attributes["src"] = "/icon.png"
                img.attributes["data_image"] = "responsive"
                div.children.append(img)
my_html.close()
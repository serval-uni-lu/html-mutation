from html_mutation.html import dom


def test_find_all_one_result():
    tree = dom.parse(get_simple_dom())
    child = tree.find_all("p")[0]
    assert "{http://www.w3.org/1999/xhtml}p" == child.tag


def test_get_xpath():
    tree = dom.parse(get_simple_dom())
    child = tree.find_all("p")[0]
    assert "/html/body/p" == tree.get_xpath(child)


def get_simple_dom():
    return """
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>"""

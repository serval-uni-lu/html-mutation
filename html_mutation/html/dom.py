import base64
import pathlib
from io import BytesIO
from xml.etree.ElementTree import Element, ElementTree

import html5lib
from PIL import Image
from selenium import webdriver

from html_mutation.html.tags import Tag

class DomTree:
    def __init__(self, tree: ElementTree) -> None:
        self.tree = tree

    def find_by_xpath(self, query: str) -> ElementTree:
        return self.tree.xpath(query, namespaces=self.tree.getroot().nsmap)

    def find_by_tag(self, tags: set[Tag] | Tag) -> list[Element]:
        if isinstance(tags, Tag):
            query = ".//html:{}".format(tags.value)
        else:
            query = ".//*[{}]".format(" or ".join("self::html:" + tag.value for tag in tags))
        
        return self.tree.xpath(
            query, namespaces=self.tree.getroot().nsmap
        )

    def get_xpath(self, element: Element) -> str:
        return self.tree.getpath(element)


def parse(dom_content: str) -> DomTree:
    return DomTree(html5lib.parse(dom_content, treebuilder="lxml"))


class DomInfo:
    def __init__(self, path: pathlib.Path, dom: DomTree, image: Image) -> None:
        self.path = path
        self.dom = dom
        self.image = image


class DomInfoBuilder:
    def __init__(
        self, driver: webdriver.Chrome, base_folder: str = None
    ) -> None:
        self.driver = driver

        if base_folder is None:
            self.base_path = None
        else:
            base_path = pathlib.Path(base_folder)
            if not base_path.exists() or not base_path.is_dir():
                raise IOError(
                    "base_folder should be None"
                    " or a valid folder on the file system"
                )
            self.base_path = base_path

    def build(self, html_path: str) -> DomInfo:
        path = pathlib.Path(html_path)

        if self.base_path:
            path = self.base_path / path

        self.driver.get(path.as_uri())
        dom = html5lib.parse(self.driver.page_source(), treebuilder="lxml")
        screenshot_base64 = self.driver.get_screenshot_as_base64()
        screenshot_bytes = base64.b64decode(screenshot_base64)
        screenshot = Image.open(BytesIO(screenshot_bytes))

        return DomInfo(path, dom, screenshot)

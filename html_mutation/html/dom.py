import base64
import pathlib
from io import BytesIO

from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver


class DomInfo:
    def __init__(
        self, path: pathlib.Path, dom: BeautifulSoup, image: Image
    ) -> None:
        self.path = path
        self.dom = dom
        self.image = image


class DomParser:
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

    def parse(self, html_path: str) -> DomInfo:
        path = pathlib.Path(html_path)

        if self.base_path:
            path = self.base_path / path

        self.driver.get(path.as_uri())
        dom = BeautifulSoup(self.driver.page_source(), "html5lib")
        screenshot_base64 = self.driver.get_screenshot_as_base64()
        screenshot_bytes = base64.b64decode(screenshot_base64)
        screenshot = Image.open(BytesIO(screenshot_bytes))

        return DomInfo(path, dom, screenshot)


def xpath(element) -> str:
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if len(siblings) == 1 else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)
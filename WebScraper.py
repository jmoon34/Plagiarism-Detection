from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        try:
            with closing(get(self.url, stream=True)) as resp:
                if self.is_good_response(resp):
                    raw_html = resp.content
                    return BeautifulSoup(raw_html, 'html.parser').find_all()
                else:
                    return None

        except RequestException as e:
            self.log_error("Error during requests to {0} : {1}".format(self.url, str(e)))

    def extract_text(self):
        soup = self.get_html()
        if soup is None:
            return ""
        text = ""
        for tag in soup:
            if tag.name == 'p' and tag.parent.name != 'p':
                text += (tag.text + "\n")
        return text.lower()



    @staticmethod
    def is_good_response(resp):
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    @staticmethod
    def log_error(e):
        print(e)

w = WebScraper("https://www.storyofmathematics.com/17th_fermat.html")
soup = w.get_html()

with open("Texts/paragraph.txt", 'w') as f:
    for tag in soup:
        if tag.name == 'p' and tag.parent.name != 'p':
            f.write(tag.text)
            f.write("\n")
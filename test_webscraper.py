from WebScraper import WebScraper
url = "https://arxiv.org/pdf/0801.1809"
w = WebScraper(url)
html = w.get_html()
print(w.extract_text())



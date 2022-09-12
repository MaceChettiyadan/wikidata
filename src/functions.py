import webbrowser
import wikipedia
import webbrowser
from bs4 import BeautifulSoup as bs

def get_page(name):
  return wikipedia.page(name)
  
def open_page(name):
  url = wikipedia.page(name).url
  webbrowser.open(url)

def extract_headers(html):
  # return headers from html string
  soup = bs(html, 'html.parser')
  try:
    dic = {}
    toc = soup.find(id="toc")
    lis = toc.find_all('li')
    for li in lis:
      #get child spans
      nums = li.find_all(class_ = "tocnumber")
      num = nums[0].text
      values = li.find_all(class_ = "toctext")
      value = values[0].text
      dic[num] = value
      
    treeview_data = []
    for key in dic:
      val = dic[key]
      parent = key.split(".")[0] if '.' in key else ''
      id = key
      treeview_data.append((parent, id, val, (key, val)))
    return treeview_data
  except:
    return [("", 0, "No headers found!", ("", "This article has no Headers"))]
    
    
      
    
  
  
  
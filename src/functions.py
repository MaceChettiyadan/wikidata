import webbrowser
import wikipedia
from bs4 import BeautifulSoup as bs

def get_page(name):
  try:
    return wikipedia.page(name)
  except:
    return False
  
def open_page(name):
  webbrowser.open(name)

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
    
    
def get_summary(string, chars):
  ##nearest sentence to chars
  val = ""
  if len(string) > chars:
    val = string[:chars]
  else:
    return string
  #find last period
  last_period = val.rfind('.')
  val = val[:last_period+1]
  return val
  
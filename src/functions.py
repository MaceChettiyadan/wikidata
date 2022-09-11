import webbrowser
import wikipedia
import webbrowser

def get_page(name):
  return wikipedia.page(name, auto_suggest=False, redirect=True, preload=False)
  
def open_page(name):
  url = wikipedia.page(name).url
  webbrowser.open(url)

import random

# Source - https://stackoverflow.com/a/44923103
# Posted by ntg, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-25, License - CC BY-SA 4.0

from IPython.display import display_html
from itertools import chain,cycle
def display_side_by_side(*args,titles=cycle([''])):
    html_str=''
    for df,title in zip(args, chain(titles,cycle(['</br>'])) ):
        html_str+='<th style="text-align:center"><td style="vertical-align:top">'
        html_str+=f'<h2 style="text-align: center;">{title}</h2>'
        html_str+=df.to_html().replace('table','table style="display:inline"')
        html_str+='</td></th>'
    display_html(html_str,raw=True)
  
seed = 8262026
def rand():
	global seed
	random.seed(seed)
	seed += 1
	return random.random()
def generate_random_color() :
    color = (rand(),rand(),rand())
    return color

def first(pair): return pair[0]
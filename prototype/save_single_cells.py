'''You probably don't want to run this script.'''
from mako.template import Template
import re
import BeautifulSoup as b

def find_cells(n):
    result = [div for div in n.findAll('div') if 'class' in dict(div.attrs) and re.match(r'^cell\ .*', dict(div.attrs)['class'])]
    return result

html_data = open('old-merge.html').read()
soup = b.BeautifulSoup(html_data)
first_bar = soup.find('div', id='first-bar')
second_bar = soup.find('div', id='second-bar')
third_bar = soup.find('div', id='third-bar')

first_cells = find_cells(first_bar)
second_cells = find_cells(second_bar)
third_cells = find_cells(third_bar)

first_cells.insert(4, '<div class="diff-spacer">{}</div>'.format(second_cells[3]))

for i, cell in enumerate(first_cells):
    with open('merge-cells/cell-1-{i:d}.html'.format(i=i), 'w') as w:
        assert type(cell) == b.Tag or type(cell) == str, str(type(cell)) + str(cell)
        w.write(str(cell))

for i, cell in enumerate(second_cells):
    with open('merge-cells/cell-2-{i:d}.html'.format(i=i), 'w') as w:
        w.write(str(cell))

for i, cell in enumerate(third_cells):
    with open('merge-cells/cell-3-{i:d}.html'.format(i=i), 'w') as w:
        w.write(str(cell))

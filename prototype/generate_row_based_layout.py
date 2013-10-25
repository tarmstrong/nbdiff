'''You probably don't want to run this script.'''
from mako.template import Template
import re
import BeautifulSoup as b

def find_cells(n):
    result = [div for div in n.findAll('div') if 'class' in dict(div.attrs) and re.match(r'^cell\ .*', dict(div.attrs)['class'])]
    return result

html_data = open('old-diff.html').read()
soup = b.BeautifulSoup(html_data)
first_bar = soup.find('div', id='first-bar')
soup = b.BeautifulSoup(html_data)
second_bar = soup.find('div', id='second-bar')

first_cells = find_cells(first_bar)
second_cells = find_cells(second_bar)
assert isinstance(first_bar, b.Tag, )
assert isinstance(second_bar, b.Tag, )

#first_cells.insert(3, '<div class="diff-spacer">spacer</div>')
first_cells.insert(3, '<div class="diff-spacer">{}</div>'.format(second_cells[3]))

print first_cells
print second_cells
zcells = zip(first_cells, second_cells)

rowfmt = "<div class='row'><div class='row-cell'>{}</div><div class='row-cell'>{}</div></div>"

rendered_cells = "\n".join([rowfmt.format(*c) for c in zcells])

rendered_full = Template(open('nbdiff-template.html').read()).render(cells=rendered_cells)

open('diff.html', 'w').write(rendered_full)

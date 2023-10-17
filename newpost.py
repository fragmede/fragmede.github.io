#!/usr/bin/env python
import datetime
import shutil

filename_date = datetime.datetime.now().strftime('%Y-%m-%d')
full_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%m:%d PST')

title = input("Title with spaces")

hyphened_title = '-'.join([x.lower() for x in title.split()])

with open('_posts/TEMPLATE.markdown', 'r') as file:
    lines = file.readlines()

for index, line in enumerate(lines):
    if line.startswith('date:'):
        lines[index] = 'date: {}\n'.format(full_date)
    elif line.startswith('title:'):
        lines[index] = 'title: {}\n'.format(title)

out_file_name = '_posts/{}-{}.markdown'.format(filename_date, hyphened_title)
with open(out_file_name, 'w') as file:
        file.writelines(lines)

print('wrote {}'.format(out_file_name))

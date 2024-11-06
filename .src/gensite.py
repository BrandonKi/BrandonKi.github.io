import sys
from pathlib import Path
from datetime import datetime
import os

import htmlmin  # Being lazy for right now

MINIFY = True
# MINIFY = False

articles = []

# Usage:
#   py gensite.py path/to/input/mds path/to/output/htmls
#   py gensite.py . ..
def main():
    if len(sys.argv) < 3:
        print('You forgot to tell me what directories to look at!!')
        print('Usage:\n\tpy gensite.py path/to/input/mds path/to/output/htmls')
        print('\t(usually you want to run this: py gensite.py . ..)')
        sys.exit(-1)

    if MINIFY:
        m = htmlmin.Minifier(remove_comments=True, remove_all_empty_space=True)

    in_directory = Path(sys.argv[1])
    out_directory = Path(sys.argv[2])
    blog_out_directory = Path(sys.argv[2]) / 'blog'
    css_out_directory = Path(sys.argv[2]) / 'css'

    out_directory.mkdir(exist_ok=True, parents=True)
    blog_out_directory.mkdir(exist_ok=True)
    css_out_directory.mkdir(exist_ok=True)

    template = open(in_directory / 'templates' / 'template.html').read()
    
    global articles

    # Convert blog markdown to html
    md_files = (in_directory / 'blog').glob('*.md')
    for file in md_files:
        output = convert2html(file)
        articles[-1]['filename'] = file.stem
        with open(Path(out_directory / 'blog' / file.stem).with_suffix('.html'), "w") as outfile:
            # if MINIFY: output = m.minify(output)
            if MINIFY: output = m.minify(template.replace('{{Content}}', output))
            else: output = template.replace('{{Content}}', output)
            outfile.write(output)
    
    articles = sorted(articles, key=lambda x: x['date'], reverse=True)
    articles.insert(1, None)

    # Main html
    html_files = in_directory.glob('*.html')
    for file in html_files:
        with open(file, "r") as output:
            with open(Path(out_directory / file.stem).with_suffix('.html'), "w") as outfile:
                if file.stem == 'index':
                    output = output.read()
                else:
                    result = output.read()
                    if file.stem == 'blog':
                        for a in articles:
                            if a is None:
                                result += '<h3 style="margin-top:4rem;">Work In Progress</h3>'
                            else:
                                tags = ''
                                for t in a['tags']:
                                    tags += f'&nbsp<div class="blog-tag">&nbsp{t}&nbsp</div>&nbsp'
                                result += f'<div>{a['date'].strftime("%b %d, %Y")} &#x2014 <a class="link" href="blog/{a['filename']}.html">{a['title']}</a>&nbsp{tags}</div>'
                        result += '</div></div>'

                    output = template.replace('{{Content}}', result)
                if MINIFY: output = m.minify(output)
                outfile.write(output)

    # Copy css
    css_files = (in_directory / 'css').glob('*.css')
    for file in css_files:
        with open(file, "r") as output:
            with open(Path(out_directory / 'css' / file.stem).with_suffix('.css'), "w") as outfile:
                outfile.write(output.read())
                # outfile.write(m.minify(output.read()))

# Converts markdown to html, nothing complicated.
# This is not a compliant markdown parser however.
# It only accepts a nonstandard subset of markdown useful for making this website.
def convert2html(filename: str) -> None:
# <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    output = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/gruvbox-dark-soft.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://unpkg.com/highlightjs-copy/dist/highlightjs-copy.min.js"></script>
<link rel="stylesheet" href="https://unpkg.com/highlightjs-copy/dist/highlightjs-copy.min.css">
<script defer>
    hljs.addPlugin(new CopyButtonPlugin());
    hljs.highlightAll();
</script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" integrity="sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" integrity="sha384-7zkQWkzuo3B5mTepMUcHkMB5jZaolc2xDwL6VFqjFALcbeS9Ggm/Yr2r3Dy4lfFg" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" integrity="sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTstBeZFe/+rCMvRwr4yROQP43s0Xk" crossorigin="anonymous"></script>
<script>
    document.addEventListener("DOMContentLoaded", function() {
        renderMathInElement(document.body, {
          delimiters: [
              {left: '$$', right: '$$', display: true},
              {left: '$', right: '$', display: false},
              {left: '\\\\(', right: '\\\\)', display: false},
              {left: '\\\\[', right: '\\\\]', display: true}
          ],
          throwOnError : false
        });
    });
</script>
"""

    in_meta = False
    meta = {}
    key = ""

    in_bulleted_list = False
    in_numbered_list = False

    in_code_block = False
    backref = None

    tags = {'p': False, 'em': False, 'code': False, 'pre': False, 'ul': False, 'li': False, 'ol': False}

    file = open(filename, "r")
    for raw_line in file:
        line = raw_line.lstrip()
        if line.rstrip() == '---':
            in_meta = not in_meta
        elif in_meta:
            if line[0] == '-':
                meta[key].append(line[1:])
                continue
            key = line[0:line.find(':')]
            if len(key)+1 == len(line.strip()):
                meta[key] = []
            elif line.count("'") == 2:    # string
                meta[key] = line[line.find("'")+1:line.rfind("'")]
            elif line.count("\"") == 2:    # string
                meta[key] = line[line.find("\"")+1:line.rfind("\"")]
            elif line.count("-") > 1:   # date
                meta[key] = datetime.strptime(line[line.find(":")+1:].strip(), '%Y-%m-%d')
            else:                       # number
                try:
                    meta[key] = int(line[line.find(":")+1:])
                except:                 # HACK
                    meta[key] = line[line.find(":")+1:]
        elif len(line.strip()) == 0:
            output += '\n'
        elif line.startswith('```'):
            t = 'pre'
            output += f'<{'/' if tags[t] else ''}{t}>'
            tags[t] = not tags[t]
            t = 'code'
            # language = line[line.find('```')+3:].strip()
            # if len(language) > 0:
            #     language = f'class="language-{language}"'
            # output += f'<{'/' if tags[t] else ''}{t}{language if not tags[t] else ''}>'
            output += f'<{'/' if tags[t] else ''}{t}>'
            tags[t] = not tags[t]
            in_code_block = not in_code_block
        else:
            first_char = line[0]
            if first_char == '-':
                if not in_bulleted_list:
                    t = 'ul'
                    output += f'<{'/' if tags[t] else ''}{t}>'
                    tags[t] = not tags[t]
                    in_bulleted_list = True
                t = 'li'
                output += f'<{'/' if tags[t] else ''}{t}>'
                tags[t] = not tags[t]
                line = line[line.find('-')+1:].lstrip()
            elif line.startswith('[^'):
                num = line[line.find('^')+1:line.find(']')]
                if not in_numbered_list:
                    t = 'ol'
                    output += f'<{'/' if tags[t] else ''}{t}>'
                    tags[t] = not tags[t]
                    in_numbered_list = True
                t = 'li'
                output += f'<{'/' if tags[t] else ''}{t} id="footnote{num}">'
                tags[t] = not tags[t]
                line = line[line.find(']:')+2:].lstrip()
                backref = f'{num}'
            else:
                if in_bulleted_list:
                    if len(line.strip()) == 0:
                        continue
                    in_bulleted_list = False
                    t = 'ul'
                    output += f'<{'/' if tags[t] else ''}{t}>'
                    tags[t] = False
                if in_numbered_list:
                    print('t', line, 't')
                    if len(line.strip()) == 0:
                        continue
                    in_numbered_list = False
                    t = 'ol'
                    output += f'<{'/' if tags[t] else ''}{t}>'
                    tags[t] = False

            if in_code_block:
                output += raw_line
                continue
            elif first_char == '#':
                cnt = line.count('#')
                output += f'<h{cnt} class="blog-header">'
                tags[f'h{cnt}'] = True
                line = line[cnt:].lstrip()
            elif first_char not in ('`', '!'):
                output += '<p>'
                tags['p'] = True
            
            backslash = False
            unconsumed_sup = False
            unconsumed_bang = False
            unconsumed_link = False
            in_link = False
            saved_link = ""
            in_href = False
            saved_href = ""
            in_image = False
            for c in line:
                if c == '\\':
                    if backslash:
                        output += '\\'
                    else:
                        backslash = True
                elif backslash:
                    backslash = False
                    output += c
                elif in_link and c == '^':
                    unconsumed_sup = True
                elif c == '[' and unconsumed_bang:
                    in_image = True
                    in_link = True
                    unconsumed_bang = False
                elif unconsumed_bang:
                    unconsumed_bang = False
                    output += '!' + c
                elif c == '[':    # TODO, footnotes [^1]: some text
                    in_link = True
                elif c == ']':
                    in_link = False
                    unconsumed_link = True
                    continue
                # elif unconsumed_link and c == ':' and unconsumed_sup and not in_numbered_list:
                #     in_numbered_list = True
                #     output += f'<ol>'
                elif unconsumed_link and c == '(':
                    in_href = True
                elif unconsumed_link and unconsumed_sup:
                    output += f'<sup><a class="link" id="backref{saved_link}" href="#footnote{saved_link}">{saved_link}</a></sup>'
                    unconsumed_link = False
                    unconsumed_sup = False
                    saved_link = ""
                elif in_image and in_href and c == ')':
                    in_image = False
                    in_href = False
                    output += f'<figure><img width="650px" src="{saved_href}"><figcaption>{saved_link}</figcaption></figure>'
                    saved_link = ""
                    saved_href = ""
                elif in_href and c == ')':
                    in_href = False
                    output += f'<a class="link" href="{saved_href}">{saved_link}</a>'
                    saved_link = ""
                    saved_href = ""
                elif in_href:
                    saved_href += c
                elif c == '*' or c == '_':  # TODO bold
                    t = 'em'
                    if in_link:
                        saved_link += f'<{'/' if tags[t] else ''}{t}>'
                    else:
                        output += f'<{'/' if tags[t] else ''}{t}>'
                    tags[t] = not tags[t]
                elif c == '`':
                    t = 'code'
                    output += f'<{'/' if tags[t] else ''}{t}{'' if tags[t] else ' class="hljs"'}>'
                    tags[t] = not tags[t]
                elif c == '\n': # HACK
                    if backref is not None:
                        output += f'&nbsp<a class="link" href="#backref{backref}">&#x21A9;</a>'
                        backref = None
                    for k, v in tags.items():
                        if v and k in ('p', 'h1', 'h2', 'h3', 'h4', 'li'):
                            output += f'<{'/' if tags[k] else ''}{k}>'
                            tags[k] = False
                elif in_link:
                    saved_link += c
                elif c == '!':
                    unconsumed_bang = True
                else:
                    output += c
                unconsumed_link = False

    if backref is not None:
        output += f'&nbsp<a class="link" href="#backref{backref}">&#x21A9;</a>'
        backref = None

    meta_prefix = f'<div class="blog-content"><header><h1 class="blog-title">{meta['title']}</h1></header><p class="blog-meta">{
        meta['author']} - {meta['date'].strftime("%B %d, %Y")}</p><div class="blog-body">'
    meta_suffix = '</div></div>'

    articles.append(meta)

    file.close()
    return meta_prefix + output + meta_suffix


if __name__ == '__main__':
    main()

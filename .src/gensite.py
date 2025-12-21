import sys
from pathlib import Path
from datetime import datetime
import os
import re

from minify_html import minify as m # Being lazy for right now

MINIFY = True
# MINIFY = False

def minify(src):
    if MINIFY:
        return m(src, minify_js=True, minify_css=True)
    else:
        return src

articles = []

# Usage:
#   py gensite.py path/to/input/mds path/to/output/htmls
#   py gensite.py . ..
def main():
    if len(sys.argv) < 3:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        in_directory = Path(script_directory)
        out_directory = Path(script_directory) / '..'
    else:
        in_directory = Path(sys.argv[1])
        out_directory = Path(sys.argv[2])

    blog_out_directory = out_directory / 'blog'
    blog_tags_out_directory = out_directory / 'blog' / 'tags'
    css_out_directory = out_directory / 'css'

    out_directory.mkdir(exist_ok=True, parents=True)
    blog_out_directory.mkdir(exist_ok=True)
    blog_tags_out_directory.mkdir(exist_ok=True)
    css_out_directory.mkdir(exist_ok=True)

    template = open(in_directory / 'templates' / 'template.html', encoding="utf-8").read()
    
    global articles

    # Convert blog markdown to html
    md_files = (in_directory / 'blog').glob('*.md')
    md_files = [file for file in md_files if not file.name.startswith('.')] # hack for emacs
    for file in md_files:
        html_output, article_sidebar = convert2html(file)
        articles[-1]['filename'] = file.stem
        with open(Path(out_directory / 'blog' / file.stem).with_suffix('.html'), "w", encoding="utf-8") as outfile:
            partial_template = template.replace('{{Sidebar}}', article_sidebar)
            output = minify(partial_template.replace('{{Content}}', html_output))
            outfile.write(output)
    
    articles = sorted(articles, key=lambda x: x['date'], reverse=True)

    deduped_tags = set()
    blog_copy = ""

    # Main html
    html_files = in_directory.glob('*.html')
    for file in html_files:
        with open(file, "r", encoding="utf-8") as infile:
            with open(Path(out_directory / file.stem).with_suffix('.html'), "w", encoding="utf-8") as outfile:
                if file.stem == 'index':
                    output = infile.read()
                else:
                    result = infile.read()
                    if file.stem == 'blog':
                        blog_copy = result
                        for a in articles:
                            if a is None:
                                result += '<h3 style="margin-top:4rem;">Work In Progress</h3>'
                            else:
                                tags = ''
                                for t in a['tags']:
                                    deduped_tags.add(t)
                                    tags += f'&nbsp<a href="/blog/tags/{t}" class="blog-tag">&nbsp{t}&nbsp</a>&nbsp'
                                result += f'<div style="margin-bottom: 0.5em"><div style="font-family: monospace;display:inline-block;font-size:90%;">{a['date'].strftime("%b %d, %Y")}&nbsp</div><div style="display:inline-block;"> &#x2014 <a class="link" href="blog/{a['filename']}.html">{a['title']}</a>&nbsp{tags}</div></div>'
                        result += '</div></div>'

                    output = template.replace('{{Sidebar}}', '')
                    output = output.replace('{{Content}}', result)
                output = minify(output)
                outfile.write(output)

    # Make the tag pages
    # NOTE: duplicated code from above ^^
    for dt in deduped_tags:
        with open(Path(blog_tags_out_directory / dt).with_suffix('.html'), "w", encoding="utf-8") as outfile:
            result = blog_copy
            result += f'<svg class="tag-icon" width="18" height="18" viewBox="0 0 50 50"><path fill="white" stroke="none" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2" d="M47,5.5  C47,4.119,45.881,3,44.5,3c-0.156,0-14.876,0.002-14.876,0.002c-1.33,0-2.603-0.07-3.341,0.668L3.554,26.398  c-0.739,0.738-0.739,1.936,0,2.674l17.374,17.374c0.738,0.738,1.936,0.738,2.674,0L46.33,23.717c0.738-0.737,0.668-1.98,0.668-3.34  C46.998,20.377,47,5.656,47,5.5z"/><circle cx="39" cy="11" fill="#252525" r="3" stroke="#000000" stroke-linecap="round" stroke-miterlimit="10" stroke-width="2"/></svg>Filter:&nbsp<a href="../../blog" class="blog-tag">&nbsp{dt} <div class="blog-tag-x">X</div>&nbsp</a>'
            for a in articles:
                if dt in a['tags']:
                    tags = ''
                    for t in a['tags']:
                        tags += f'&nbsp<a href="../../blog/tags/{t}" class="blog-tag">&nbsp{t}&nbsp</a>&nbsp'
                    result += f'<div style="margin-bottom: 0.5em"><div style="font-family: monospace;display:inline-block;font-size:90%;">{a['date'].strftime("%b %d, %Y")}&nbsp</div><div style="display:inline-block;"> &#x2014 <a class="link" href="blog/{a['filename']}.html">{a['title']}</a>&nbsp{tags}</div></div>'
            result += '</div></div>'
            output = template.replace('{{Sidebar}}', '')
            output = output.replace('{{Content}}', result)
            output = minify(output)
            outfile.write(output)

    # Copy css
    css_files = (in_directory / 'css').glob('*.css')
    for file in css_files:
        with open(file, "r", encoding="utf-8") as output:
            with open(Path(out_directory / 'css' / file.stem).with_suffix('.css'), "w", encoding="utf-8") as outfile:
                output = output.read()
                output = minify(output)
                outfile.write(output)

    # Copy images
    img_files = (in_directory / 'blog').glob('*.[jpg][png]*')
    for file in img_files:
        with open(file, "rb") as output:
            with open(Path(out_directory / 'blog' / file.stem).with_suffix(file.suffix), "wb") as outfile:
                outfile.write(output.read())

# Converts markdown to html, nothing complicated.
# This is not a compliant markdown parser however.
# It only accepts a nonstandard subset of markdown useful for making this website.
def convert2html(filename: str) -> None:
    output = """
<link rel="stylesheet" href="../third_party/gruvbox-dark-soft.min.css">
<script rel="preload" src="../third_party/highlight.min.js"></script>
<script rel="preload" src="../third_party/highlightjs-copy.min.js"></script>
<link rel="stylesheet" href="../third_party/highlightjs-copy.min.css">
<script>
    hljs.addPlugin(new CopyButtonPlugin());
    hljs.highlightAll();
</script>

<link rel="stylesheet" href="../third_party/katex.min.css">
<script rel="preload" src="../third_party/katex.min.js"></script>
<script rel="preload" src="../third_party/auto-render.min.js"></script>
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
<script>
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.blog-header').forEach(element => {
        element.id = encodeURI(element.textContent.trim().toLowerCase().replace(/ /g, '-'));
        element.addEventListener('click', () => {
            const url = "#" + element.id;
            if (url) {
                window.location.href = url;
            }
        });
    });
});
</script>

<script>
document.addEventListener('DOMContentLoaded', () => {
    let tocLinks = document.querySelectorAll('#toc a');
    if (tocLinks.length === 0) return;
    const sections = document.querySelectorAll('.blog-body h1, .blog-body h2, .blog-body h3, .blog-body h4');

    const visibleSections = new Set();
    let userClicked = false;

    const getTocLinkForId = (id) => {
        try {
            if (window.CSS && CSS.escape) {
                return document.querySelector(`#toc a[href="#${CSS.escape(id)}"]`);
            }
        } catch (e) {
        }
        tocLinks = document.querySelectorAll('#toc a');
        for (const a of tocLinks) {
            if (a.getAttribute('href') === `#${id}`) return a;
        }
        return null;
    };

    const tocContainer = document.getElementById('toc');

    const scrollSidebarTo = (link) => {
        if (!tocContainer || !link) return;
        try {
            const top = link.offsetTop - (tocContainer.clientHeight / 2) + (link.offsetHeight / 2);
            tocContainer.scrollTo({ top: top, behavior: 'smooth' });
        } catch (e) {}
    };

    const observerCallback = (entries) => {
        if (userClicked) return; // skip updating if user clicked

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                visibleSections.add(entry.target);
            } else {
                visibleSections.delete(entry.target);
            }
        });

        if (visibleSections.size > 0) {
            const lastSection = Array.from(visibleSections).reduce((a, b) =>
                a.offsetTop > b.offsetTop ? a : b
            );
            tocLinks.forEach(link => link.classList.remove('active'));
            const targetLink = getTocLinkForId(lastSection.id);
            if (targetLink) {
                targetLink.classList.add('active');
                scrollSidebarTo(targetLink);
            }
        }
    };

    const observerOptions = {
        root: null,
        rootMargin: '-50% 0px -50% 0px',
        threshold: 0
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);
    sections.forEach(section => {
        if (section.id) observer.observe(section);
    });

    tocLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            userClicked = true;

            tocLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            scrollSidebarTo(link);

            const onScroll = () => {
                userClicked = false;
                window.removeEventListener('scroll', onScroll);
            };
            window.addEventListener('scroll', onScroll);
        });
    });
});

observerCallback(
    sections.map(section => ({
        target: section,
        isIntersecting:
            section.getBoundingClientRect().top < window.innerHeight / 2 &&
            section.getBoundingClientRect().bottom > window.innerHeight / 2
    }))
);

</script>
<style>
body {
  display: flex;
  font-family: Arial, sans-serif;
  margin: 0;
}

#toc {
    position: sticky;
    top: 20px;
    height: 100vh;
    overflow-y: auto;
    flex: 0 0 200px;
    padding: 0px 0px 20px 8px;
    background: inherit;
    scroll-behavior: smooth;
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
}

#toc::-webkit-scrollbar { width: 0; height: 0; }

#toc a {
    display: block;
    margin: 5px 0;
    color: #b9b9b9;
    text-decoration: none;
}

#toc a.active {
    font-weight: bold;
    color: white;
}

#toc ul { list-style: none; margin: 0; padding-left: 0; }
#toc li { margin: 4px 0; }
#toc ul ul { padding-left: 1rem; }
#toc a { display: inline-block; }
</style>
"""
    headings = []

    in_meta = False
    meta = {}
    key = ""

    in_bulleted_list = False
    in_numbered_list = False

    in_code_block = False
    backref = None

    tags = {'p': False, 'em': False, 'code': False, 'pre': False, 'ul': False, 'li': False, 'ol': False}

    file = open(filename, "r", encoding="utf-8")
    for raw_line in file:
        line = raw_line.lstrip()
        if line.rstrip() == '---':
            in_meta = not in_meta
        elif in_meta:
            if line[0] == '-':
                meta[key].append(line[1:].strip())
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
            if in_bulleted_list:    # HACK, temp fix
               output += f'<{'/' if tags['ul'] else ''}{'ul'}>' 
               
            if tags['pre'] and tags['code']:
                ts = ['code', 'pre']
            else:
                ts = ['pre', 'code']
            for t in ts:
                language = line[line.find('```')+3:].strip()
                if t == 'code' and len(language) > 0:
                    language = f' class="language-{language}"'
                    output += f'<{'/' if tags[t] else ''}{t}{language if not tags[t] else ''}>'
                else:
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
                raw_line = raw_line.replace('<', '&lt;')
                raw_line = raw_line.replace('>', '&gt;')
                output += raw_line
                continue
            elif first_char == '#':
                cnt = line.count('#')
                output += f'<h{cnt} class="blog-header">'
                tags[f'h{cnt}'] = True
                line = line[cnt:].lstrip()
                headings.append((line.strip(), cnt))
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
                    output += f'<figure><img class="blog-image" src="{saved_href}"><figcaption>{saved_link}</figcaption></figure>'
                    # output += f'<figure><img width="650px" src="{saved_href}"><figcaption>{saved_link}</figcaption></figure>'
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
                        output += f'&nbsp<a class="link" style="font-family: monospace;" href="#backref{backref}">&#x21A9;</a>&nbsp'
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
        output += f'&nbsp<a class="link" style="font-family: monospace;" href="#backref{backref}">&#x21A9;</a>'
        backref = None

    for k, v in tags.items():
        if v and k in ('p', 'h1', 'h2', 'h3', 'h4', 'li', 'ol'):
            output += f'<{'/' if tags[k] else ''}{k}>'
            tags[k] = False

    meta_prefix = f'<div class="blog-content"><header><h1 class="blog-title">{meta['title']}</h1></header><p class="blog-meta">{meta['author']} - {meta['date'].strftime("%B %d, %Y")}</p><div class="blog-body">'
    meta_suffix = '</div></div>'

    articles.append(meta)

    file.close()

    def slugify(s: str) -> str:
        s = s.strip().lower()
        s = re.sub(r"\s+", "-", s)
        s = re.sub(r"[^a-z0-9\-\:\.\&,]", "", s)
        s = re.sub(r"-+", "-", s)
        return s

    if len(headings) > 0:
        root = {'level': 0, 'children': []}
        stack = [root]
        for text, level in headings:
            node = {'level': level, 'text': text, 'id': slugify(text), 'children': []}
            while stack and stack[-1]['level'] >= level:
                stack.pop()
            stack[-1]['children'].append(node)
            stack.append(node)

        def render_children(children):
            parts = ['<ul>']
            for child in children:
                parts.append('<li>')
                parts.append('<a href="#' + child['id'] + '">' + child['text'] + '</a>')
                if child['children']:
                    parts.append(render_children(child['children']))
                parts.append('</li>')
            parts.append('</ul>')
            return ''.join(parts)

        sidebar_html = '<nav id="toc">' + render_children(root['children']) + '</nav>'
    else:
        sidebar_html = ''

    return meta_prefix + output + meta_suffix, sidebar_html


if __name__ == '__main__':
    main()

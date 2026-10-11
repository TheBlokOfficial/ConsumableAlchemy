"""Lint WitcherScript (.ws) for two compiler pitfalls (README.md, "Pulapki kompilatora" 1 and 2).

python tools/lint_ws.py [path ...]

Paths are files or directories (searched recursively for *.ws); default is src/ of this repo.
Prints "path:line: message" per finding, exits 1 if there is any.

Rule A: inside a function annotated with @wrapMethod the identifier wrappedMethod may occur once.
Rule B: a local var declaration after any other statement of the function is a compile error.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.join(HERE, '..', 'src')
TOKEN_RE = re.compile(r'[A-Za-z_]\w*|\d[\w.]*|\S')


def read_text(path):
    with open(path, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        return raw.decode('utf-16', errors='replace')
    if raw.startswith(b'\xef\xbb\xbf'):
        return raw[3:].decode('utf-8', errors='replace')
    return raw.decode('utf-8', errors='replace')


def strip_text(text):
    """Remove comments, replace string/name literals by a placeholder; newlines are kept."""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        two = text[i:i + 2]
        if two == '//':
            while i < n and text[i] != '\n':
                i += 1
        elif two == '/*':
            end = text.find('*/', i + 2)
            end = n if end < 0 else end + 2
            out.append('\n' * text.count('\n', i, end))
            i = end
        elif c == '"' or c == "'":
            i += 1
            while i < n and text[i] != c and text[i] != '\n':
                i += 2 if text[i] == '\\' else 1
            if i < n and text[i] == c:
                i += 1
            out.append('0')
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def tokenize(text):
    toks = []
    for lineno, line in enumerate(strip_text(text).split('\n'), 1):
        for m in TOKEN_RE.finditer(line):
            toks.append((m.group(), lineno))
    return toks


def lint_text(text):
    """Returns a list of (line, message)."""
    toks = tokenize(text)
    found = []
    mode = 'top'            # top: outside function bodies, header: after "function name(", body
    wrap_pending = False    # @wrapMethod seen, function not started yet
    is_wrap = False
    wrapped_seen = 0
    depth = 0               # brace depth inside the function body
    seen_stmt = False
    in_decl = False
    i, n = 0, len(toks)
    while i < n:
        t, line = toks[i]
        if mode == 'top':
            if t == '@' and i + 1 < n and toks[i + 1][0] == 'wrapMethod':
                wrap_pending = True
            elif t in ('function', 'event') and i + 2 < n and re.match(r'[A-Za-z_]', toks[i + 1][0]) \
                    and toks[i + 2][0] == '(':
                mode, is_wrap, wrap_pending = 'header', wrap_pending, False
                i += 2
            elif t in (';', '{', '}'):
                wrap_pending = False
        elif mode == 'header':
            if t == ';':
                mode = 'top'
            elif t == '{':
                mode, depth, seen_stmt, in_decl, wrapped_seen = 'body', 1, False, False, 0
        else:
            if t == 'wrappedMethod' and is_wrap:
                wrapped_seen += 1
                if wrapped_seen > 1:
                    found.append((line, 'wrappedMethod used more than once in a @wrapMethod function'))
            if in_decl:
                if t == ';':
                    in_decl = False
            elif t == 'var':
                if seen_stmt:
                    found.append((line, 'local var declared after a statement'))
                in_decl = True
            else:
                seen_stmt = True
                if t == '{':
                    depth += 1
                elif t == '}':
                    depth -= 1
                    if depth == 0:
                        mode = 'top'
        i += 1
    return found


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                files += [os.path.join(root, x) for x in sorted(names) if x.lower().endswith('.ws')]
        else:
            files.append(p)
    return files


def main(argv):
    files = collect(argv or [os.path.normpath(DEFAULT_ROOT)])
    count = 0
    for path in files:
        for line, msg in lint_text(read_text(path)):
            print('%s:%d: %s' % (path, line, msg))
            count += 1
    print('lint_ws: %d file(s) scanned, %d finding(s)' % (len(files), count))
    return 1 if count else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

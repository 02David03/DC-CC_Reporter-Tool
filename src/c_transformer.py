import subprocess
import os
import re
from itertools import dropwhile

from pycparser import c_ast, c_parser, c_generator

CPP_INCLUDE_REGEX = re.compile(r'^# (\d+) "(.+?)"')

def cpp (filename):
    """
    File -> Text
    """
    script_dir = os.path.dirname(__file__)
    fake_libc_include = '-I' +  os.path.join(script_dir, 'fake_libc_include')

    process_result = subprocess.run(
        ['gcc', '-E', fake_libc_include, filename],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )
    return process_result.stdout

def analyze_includes (filename, txt):
    """
    Text -> [(Lineno, Text)]
    """
    header_lineno = 0
    lines_included = None
    result = [] # (header_lineno, lines_included[])

    def first_line_of_file_not_reached (line):
        match = CPP_INCLUDE_REGEX.match(line)
        return not (match and match[1] == "1" and match[2] == filename)

    capturing_included_source = False

    for line in dropwhile(first_line_of_file_not_reached, txt.splitlines()):
        line = line.strip()
        if not len(line):
            continue

        match = CPP_INCLUDE_REGEX.match(line)
        if match:
            if match[2] == filename:
                header_lineno = int(match[1])
                capturing_included_source = False
            elif not capturing_included_source:
                capturing_included_source = True
                lines_included = []
                result.append((header_lineno, lines_included))
        elif capturing_included_source:
            lines_included.append(line)
    return result

def compare_asts (ast1, ast2):
    if type(ast1) != type(ast2):
        return False

    # In the function block, calls of inline function may be expanded.
    # We shouldn't depend on the way they are expanded but only on the function name.
    # At least, the function call is added a new argument "namespace" then
    # we can't use pure equality of ASTs here.
    if isinstance(ast1, c_ast.FuncDef) and isinstance(ast2, c_ast.FuncDef):
        return ast1.decl.name == ast2.decl.name

    if isinstance(ast1, tuple) and isinstance(ast2, tuple):
        if ast1[0] != ast2[0]:
            return False
        ast1 = ast1[1]
        ast2 = ast2[1]
        return compare_asts(ast1, ast2)

    for attr in ast1.attr_names:
        if getattr(ast1, attr) != getattr(ast2, attr):
            return False

    if len(ast1.children()) != len(ast2.children()):
        return False

    for c1, c2 in zip(ast1.children(), ast2.children()):
        if compare_asts(c1, c2) == False:
            return False

    return True

class ASTDiff:
    def __init__ (self):
        self.asts_and_counts = [] # [[ast, count]]

    def inc (self, ast):
        for item in self.asts_and_counts:
            if compare_asts(item[0], ast):
                item[1] += 1
                return
        self.asts_and_counts.append([ast, 1])

    def dec (self, ast):
        """
        Return true if the ast exists (count > 0)
        """
        for item in self.asts_and_counts:
            if compare_asts(item[0], ast):
                if (item[1] > 0):
                    item[1] -= 1
                    return True
                else:
                    return False
        return False

def ast_delete (ast1, ast2):
    """
    AST-level deletion
    ast1 -= ast2

    Assumes that header directives are listed
    at the head of the target file.
    """
    diff = ASTDiff()

    for node in ast2.ext:
        diff.inc(node)

    nodes_to_delete = set([node for node in ast1.ext if diff.dec(node)])

    ast1.ext = [node for node in ast1.ext if node not in nodes_to_delete]

class CTransformer:
    """
    (AST -> AST) -> File -> Text

    "transformation" can be an AST node visitor.
    """
    def __init__ (self, transformation):
        self.transformation = transformation

    """
    The file of parameter "filename" can be before preprocessing.
    It can contains directives.
    """
    def transform (self, filepath):
        cpped_txt = cpp(filepath)

        includes = analyze_includes(filepath, cpped_txt)

        fp = open(filepath)
        orig_txt_lines = fp.readlines()
        fp.close()
        included_headers = []
        included_headers_srcs = []
        for lineno, header_src_lines in includes:
            included_headers.append(orig_txt_lines[lineno - 1])
            included_headers_srcs.extend(header_src_lines)

        parser = c_parser.CParser()
        ast_a = parser.parse(cpped_txt)
        ast_b = parser.parse('\n'.join(included_headers_srcs))

        ast_delete(ast_a, ast_b)
        self.transformation.visit(ast_a)

        contents =  '%s\n\n%s' % (
            ''.join(included_headers),
            c_generator.CGenerator().visit(ast_a)
        )

        return contents
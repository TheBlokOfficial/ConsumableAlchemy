"""python tools/test_lint_ws.py - sample checks for lint_ws.py"""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_ws import lint_text

WRAP_TWICE = """@wrapMethod(CR4Player)
function Foo() : bool
{
	var a, b : int;

	a = 1;
	if(wrappedMethod())
		return true;
	return wrappedMethod();
}
"""

LATE_VAR = """class A
{
	private var member : int;

	function Bar()
	{
		var x : int;
		x = 1; // var y : int;
		var z : name;
		z = 'var w : int; }';
	}

	import function Baz();
	timer function Tick(dt : float, id : int)
	{
		var q : int;
		q = 0;
	}
}
"""


class LintTest(unittest.TestCase):
    def test_wrapped_method_twice(self):
        self.assertEqual(lint_text(WRAP_TWICE), [(9, 'wrappedMethod used more than once in a @wrapMethod function')])

    def test_late_var(self):
        self.assertEqual(lint_text(LATE_VAR), [(9, 'local var declared after a statement')])

    def test_clean(self):
        src = "@wrapMethod(X)\nfunction F()\n{\n\tvar a : int;\n\n\treturn wrappedMethod();\n}\n"
        self.assertEqual(lint_text(src), [])


if __name__ == '__main__':
	unittest.main()

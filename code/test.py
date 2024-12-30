import sys
import tkinter as tk
from tkinter import scrolledtext
import io
from c_lexer import CLexer
from c_parser import CParser
from java_lexer import JavaLexer
from java_parser import JavaParser
from python_lexer import PythonLexer
from python_parser import PythonParser

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Static Code Analyzer - Automated Tests")
        self.root.geometry("800x600")
        self.test_cases = []
        self.create_widgets()

    def create_widgets(self):
        # Test cases text area
        self.test_cases_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier New", 12))
        self.test_cases_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Run Tests Button
        run_tests_button = tk.Button(self.root, text="Run Tests", command=self.run_tests)
        run_tests_button.pack(pady=5)

        # Results Area
        self.results_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, font=("Courier New", 12))
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load Test Cases
        self.load_test_cases()

    def load_test_cases(self):
        self.test_cases = [
            {
                "language": "Python",
                "code": "x = 10 + 20 * 3 - 5 / 2",
                "description": "Python - Simple Arithmetic Expression (No Errors)"
            },
            {
                "language": "Python",
                "code": "def multiply(a, b):\n    return a * b\n\nresult = multiply(4, 5",
                "description": "Python - Function Definition with Syntax Error"
            },
            {
                "language": "C",
                "code": "int a = 5;\nint b = a + 10;",
                "description": "C - Variable Declaration and Assignment (No Errors)"
            },
            {
                "language": "C",
                "code": "int x = 10;\nif (x > 5) {\n    x = x * 2;\n} else {\n    x = x / 2;",
                "description": "C - Conditional Statement with Syntax Error"
            },
            {
                "language": "Java",
                "code": '''public class Test {
    public int add(int x, int y) {
        return x + y;
    }
    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.add(5, 10));
    }
}''',
                "description": "Java - Method Declaration and Invocation (No Errors)"
            }
        ]
        for test_case in self.test_cases:
            self.test_cases_text.insert(tk.INSERT, f"Description: {test_case['description']}\n")
            self.test_cases_text.insert(tk.INSERT, f"Language: {test_case['language']}\n")
            self.test_cases_text.insert(tk.INSERT, f"Code:\n{test_case['code']}\n\n")

    def run_tests(self):
        self.results_text.delete('1.0', tk.END)
        for test_case in self.test_cases:
            self.results_text.insert(tk.INSERT, f"Running Test: {test_case['description']}\n")
            result = self.analyze_code(test_case['language'], test_case['code'])
            self.results_text.insert(tk.INSERT, f"Result:\n{result}\n\n")

    def analyze_code(self, language, code):
        lexer = None
        parser = None
        if language == "Python":
            lexer = PythonLexer()
            parser = PythonParser()
        elif language == "C":
            lexer = CLexer()
            parser = CParser()
        elif language == "Java":
            lexer = JavaLexer()
            parser = JavaParser()

        lexer.build()
        parser.build()

        # Redirect stdout to capture errors
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        try:
            lexer.input(code)
            tokens = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens.append(str(tok))

            result = parser.parse(code)
            output = "Tokens:\n" + "\n".join(tokens) + "\nParsed Result:\n" + str(result) + "\n"
        except Exception as e:
            output = f"Exception: {e}\n"
        finally:
            # Reset stdout
            sys.stdout = old_stdout
            errors = mystdout.getvalue()
            output += errors

        return output


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from python_lexer import PythonLexer
from python_parser import PythonParser
from c_lexer import CLexer
from c_parser import CParser
from java_lexer import JavaLexer
from java_parser import JavaParser
import io
import sys


class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Select Language")
        self.root.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        # Language Selection
        tk.Label(self.root, text="Select Language:").pack(pady=10)
        self.language_var = tk.StringVar(value="Python")
        tk.Radiobutton(self.root, text="Python", variable=self.language_var, value="Python").pack()
        tk.Radiobutton(self.root, text="C", variable=self.language_var, value="C").pack()
        tk.Radiobutton(self.root, text="Java", variable=self.language_var, value="Java").pack()

        tk.Button(self.root, text="Next", command=self.open_language_window).pack(pady=10)

    def open_language_window(self):
        selected_language = self.language_var.get()
        language_window = tk.Toplevel(self.root)
        LanguageWindow(language_window, selected_language)


class LanguageWindow:
    def __init__(self, root, language):
        self.root = root
        self.language = language
        self.root.title(f"Static Code Analyzer - {self.language}")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Text Area for Code
        self.code_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier New", 12))
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Analyze Button
        analyze_button = tk.Button(self.root, text="Analyze", command=self.analyze_code)
        analyze_button.pack(pady=5)

        # Results Area
        self.results_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, font=("Courier New", 12))
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def analyze_code(self):
        code = self.code_text.get('1.0', tk.END)

        if self.language == "Python":
            lexer = PythonLexer()
            parser = PythonParser()
        elif self.language == "C":
            lexer = CLexer()
            parser = CParser()
        elif self.language == "Java":
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
                tokens.append(tok)

            result = parser.parse(code)

            self.results_text.delete('1.0', tk.END)
            if result:
                self.results_text.insert(tk.INSERT, "Code Analysis Completed Successfully\n")
                self.results_text.insert(tk.INSERT, "Tokens:\n")
                for token in tokens:
                    self.results_text.insert(tk.INSERT, f"{token}\n")
                self.results_text.insert(tk.INSERT, "\nParsed Result:\n")
                self.results_text.insert(tk.INSERT, str(result) + "\n")
            else:
                self.results_text.insert(tk.INSERT, "Code Analysis Failed\n")
        except Exception as e:
            self.results_text.insert(tk.INSERT, f"Exception: {e}\n")
        finally:
            # Reset stdout
            sys.stdout = old_stdout
            errors = mystdout.getvalue()
            self.results_text.insert(tk.INSERT, errors)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()

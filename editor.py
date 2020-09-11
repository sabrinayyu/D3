class SimpleEditor:
    def __init__(self, document):
        self.document = document
        self.dictionary = set()
        # On windows, the dictionary can often be found at:
        # C:/Users/{username}/AppData/Roaming/Microsoft/Spelling/en-US/default.dic
        with open("/usr/share/dict/words") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.add(word)
        self.paste_text = ""


    def cut(self, i, j):
        self.paste_text = self.document[i:j]
        self.document = self.document[:i] + self.document[j:]

    def copy(self, i, j):
        self.paste_text = self.document[i:j]

    def paste(self, i):
        self.document = self.document[:i] + self.paste_text + self.document[i:]

    def get_text(self):
        return self.document

    def misspellings(self):
        result = 0
        for word in self.document.split(" "):
            if word not in self.dictionary:
                result = result + 1
        return result


class yuSimpleEditor(SimpleEditor):
    def __init__(self, document):
        super().__init__(document)
        self.document = bytearray(document, 'utf-8')
        
    def delete(self, i, j):
        del self.document[i:j]
        
    def cut(self, i, j):
        self.copy(i, j)
        self.delete(i, j)

    def get_text(self):
        return self.document.decode('utf-8')

    def misspellings(self):
        result = 0
        for word in self.get_text().split(" "):
            if word not in self.dictionary:
                result = result + 1
        return result

import timeit

class EditorBenchmarker:
    new_editor_case1 = """
from __main__ import SimpleEditor
s = SimpleEditor("{}")"""
    
    new_editor_case2 = """
from __main__ import yuSimpleEditor
s = yuSimpleEditor("{}")"""

    editor_cut_paste = """
for n in range({}):
    if n%2 == 0:
        s.cut(1, 3)
    else:
        s.paste(2)"""

    editor_copy_paste = """
for n in range({}):
    if n%2 == 0:
        s.copy(1, 3)
    else:
        s.paste(2)"""

    editor_get_text = """
for n in range({}):
    s.get_text()"""

    editor_mispellings = """
for n in range({}):
    s.misspellings()"""

    def __init__(self, cases, N):
        self.cases = cases
        self.N = N
        self.editor_cut_paste = self.editor_cut_paste.format(N)
        self.editor_copy_paste = self.editor_copy_paste.format(N)
        self.editor_get_text = self.editor_get_text.format(N)
        self.editor_mispellings = self.editor_mispellings.format(N)

    def benchmark(self):
        for case in self.cases:
            print("------------------Original Editor-------------")
            print("Evaluating case length: {}".format(len(case)))
            new_editor = self.new_editor_case1.format(case)
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor,number=1)
            print("{} cut paste operations took {} s".format(self.N, cut_paste_time))
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste,setup=new_editor,number=1)
            print("{} copy paste operations took {} s".format(self.N, copy_paste_time))
            get_text_time = timeit.timeit(stmt=self.editor_get_text,setup=new_editor,number=1)
            print("{} text retrieval operations took {} s".format(self.N, get_text_time))
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings,setup=new_editor,number=1)
            print("{} mispelling operations took {} s".format(self.N, mispellings_time))
            
            print("------------------Improved Editor-------------")
            print("Evaluating case length: {}".format(len(case)))
            new_editor = self.new_editor_case2.format(case)
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor,number=1)
            print("{} cut paste operations took {} s".format(self.N, cut_paste_time))
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste,setup=new_editor,number=1)
            print("{} copy paste operations took {} s".format(self.N, copy_paste_time))
            get_text_time = timeit.timeit(stmt=self.editor_get_text,setup=new_editor,number=1)
            print("{} text retrieval operations took {} s".format(self.N, get_text_time))
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings,setup=new_editor,number=1)
            print("{} mispelling operations took {} s".format(self.N, mispellings_time))
            

if __name__ == "__main__":
    b = EditorBenchmarker(["hello friends", "hello friends" * 1000, "hello friends" * 100000], 1000)
    b.benchmark()
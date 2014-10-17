# -*- coding: utf-8 -*-
from ctypes import byref, CDLL, c_char_p, c_wchar_p, c_void_p, POINTER

class FST(object):
    def __init__(self, libpath, fst_a_path, fst_g_path):
        self.__lib = CDLL(libpath)

        self.__lib.init.argtypes = [POINTER(c_char_p), c_char_p, c_char_p]
        self.__lib.init.restype = c_void_p

        self.__lib.terminate.argtypes = [c_void_p]
        self.__lib.terminate.restype = None

        self.__lib.analyse.argtypes = [c_void_p, c_wchar_p]
        self.__lib.analyse.restype = POINTER(c_wchar_p)

        self.__lib.generate.argtypes = [c_void_p, c_wchar_p]
        self.__lib.generate.restype = POINTER(c_wchar_p)

        error = c_char_p()
        self.__handle = self.__lib.init(byref(error), fst_a_path, fst_g_path)
        if error.value != None:
            self.__handle = 0
            raise Exception(u"Initialisation of fst failed: " + unicode(error.value, "UTF-8"))
    
    def __del__(self):
        if (self.__handle != 0):
            self.__handle = 0
            class DummyLib:
                def __getattr__(obj, name):
                    raise Exception("Attempt to use library after terminate() was called")
            self.__lib = DummyLib()
        
    def analyse(self, word):
        ana_p = self.__lib.analyse(self.__handle, word)
        if ana_p:
            analysis = ana_p.contents.value
        else:
            analysis = ""
        self.__lib.free_analyses(ana_p)
        return analysis

    def generate(self, word):
        ana_p = self.__lib.generate(self.__handle, word)
        if ana_p:
            analysis = ana_p.contents.value
        else:
            analysis = ""
        self.__lib.free_analyses(ana_p)
        return analysis

class Analyser:
    def __init__(self):
        self.fst = FST(b"./libltpy.so", b"en.analyser.bin", b"en.generator.bin")

    # Use: 
    # analyser.analyse("cats")
    # -> ("cat", ["n", "pl"])
    def analyse(self, word):
        analysed = self.fst.analyse(word)
        results = []
        if analysed[0] == '@':
            return [(analysed, ["?"])]
        for token in analysed.split("/"):
            toks = [t.rstrip(">") for t in token.split("<")]
            results.append((toks.pop(0), toks))
        return results

    # Use:
    # analyser.generate("cat", ["n", "pl"])
    # -> "cats"
    def generate(self, base, tokens):
        arg = base
        for t in tokens:
            arg += "<" + t + ">"
        return self.fst.generate(arg)
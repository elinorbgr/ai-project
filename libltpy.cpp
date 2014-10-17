#include <lttoolbox/fst_processor.h>
#include <lttoolbox/lt_locale.h>

class Analyser {
    public:
        Analyser(const std::string & analyserpath, const std::string & generatorpath) throw(exception);
        std::wstring analyse(std::wstring const &word);
        std::wstring generate(std::wstring const &word);
    private:
        FSTProcessor fst_analyser;
        FSTProcessor fst_generator;
};

Analyser::Analyser(const std::string & analyserpath, const std::string & generatorpath) throw(exception) {
    FILE * file = fopen(analyserpath.c_str(), "r");
    if (!file) {
        std::cerr << "Couldn't open analyser file " << analyserpath << std::endl;
        throw exception();
    }
    fst_analyser.load(file);
    fclose(file);
    fst_analyser.setCaseSensitiveMode(false);
    fst_analyser.setDictionaryCaseMode(true);
    fst_analyser.initBiltrans();

    file = fopen(generatorpath.c_str(), "r");
    if (!file) {
        std::cerr << "Couldn't open analyser file " << analyserpath << std::endl;
        throw exception();
    }
    fst_generator.load(file);
    fclose(file);
    fst_generator.setCaseSensitiveMode(false);
    fst_generator.setDictionaryCaseMode(true);
    fst_generator.initBiltrans();
}
    
std::wstring Analyser::analyse(std::wstring const &word) {
    std::pair <std::wstring,int> analysis = fst_analyser.biltransWithQueue(word, false);
    // The 'false' means we require no ^ or $ in input/output
    if (analysis.second == 0) {
        return analysis.first;
    }
    else {
        // a partial match:
        return L"@"+word;
    }
}

std::wstring Analyser::generate(std::wstring const &word) {
    std::pair <std::wstring,int> analysis = fst_generator.biltransWithQueue(word, false);
    // The 'false' means we require no ^ or $ in input/output
    if (analysis.second == 0) {
        return analysis.first;
    }
    else {
        // a partial match:
        return L"@"+word;
    }
}

extern "C" std::wstring * analyse(Analyser * a, const wchar_t * word) {
    // It seems Python can only send wchar_t*, but we need a wstring
    size_t wlen = wcslen(word);
    if (wlen == 0) {
        // avoid a bug in biltransWithQueue:
        return 0;
    }
    std::wstring inputString = L"";
    for (size_t i = 0; i < wlen; i++) {
        inputString.append(1, word[i]);
    }
    std::wstring * out = new wstring(a->analyse(inputString));
    return out;
}

extern "C" std::wstring * generate(Analyser * a, const wchar_t * word) {
    // It seems Python can only send wchar_t*, but we need a wstring
    size_t wlen = wcslen(word);
    if (wlen == 0) {
        // avoid a bug in biltransWithQueue:
        return 0;
    }
    std::wstring inputString = L"";
    for (size_t i = 0; i < wlen; i++) {
        inputString.append(1, word[i]);
    }
    std::wstring * out = new wstring(a->generate(inputString));
    return out;
}

extern "C" void free_analyses(std::wstring * analyses) {
    delete analyses;
}

extern "C" Analyser * init(const char ** error, const char * path_a, const char * path_b) {
    LtLocale::tryToSetLocale();
    Analyser * a = 0;
    try {
        a = new Analyser(path_a, path_b);
        
    }
    catch (exception & e) {
        delete a;
        a = 0;
        *error = e.what();
        return 0;
    }
    *error = 0;
    return a;
}

extern "C" void terminate(Analyser * a) {
    delete a;
}

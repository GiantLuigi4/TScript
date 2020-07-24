from python import method_builder

method_dictionary = {}


def load_or_get(name):
    if method_dictionary.get(name, "N\\A") == "N\\A":
        method_dictionary.update({name: method_builder.build_from_file("../"+name)})
    return method_dictionary.get(name, "N\\A")

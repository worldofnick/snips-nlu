from __future__ import unicode_literals

from builtins import object, str

from snips_nlu_ontology import (
    BuiltinEntityParser as _BuiltinEntityParser, get_all_builtin_entities,
    get_supported_entities)

from snips_nlu.utils import LimitedSizeDict


class BuiltinEntityParser(object):
    def __init__(self, language):
        self.language = language
        self.parser = _BuiltinEntityParser(language)
        self.supported_entities = get_supported_entities(language)
        self._cache = LimitedSizeDict(size_limit=1000)

    def parse(self, text, scope=None, use_cache=True):
        text = text.lower()  # Rustling only works with lowercase
        if not use_cache:
            return self.parser.parse(text, scope)
        cache_key = (text, str(scope))
        if cache_key not in self._cache:
            parser_result = self.parser.parse(text, scope)
            self._cache[cache_key] = parser_result
        return self._cache[cache_key]

    def supports_entity(self, entity):
        return entity in self.supported_entities


_RUSTLING_PARSERS = dict()


def get_builtin_entity_parser(language):
    global _RUSTLING_PARSERS
    if language not in _RUSTLING_PARSERS:
        _RUSTLING_PARSERS[language] = BuiltinEntityParser(language)
    return _RUSTLING_PARSERS[language]


def get_builtin_entities(text, language, scope=None, use_cache=True):
    parser = get_builtin_entity_parser(language)
    return parser.parse(text, scope=scope, use_cache=use_cache)


def is_builtin_entity(entity_label):
    return entity_label in get_all_builtin_entities()

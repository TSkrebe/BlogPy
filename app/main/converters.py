from werkzeug.routing import IntegerConverter as BaseIntegerConverter


class IntegerConverter(BaseIntegerConverter):
    regex = r'-?\d+'

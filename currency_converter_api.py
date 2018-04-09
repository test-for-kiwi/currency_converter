#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from currency_converter import Converter
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/currency_converter')
def currency_converter():
    """
    Function for web api via flask server. We use converter object from cli version, so we modify arguments from url to
    the same string as for command line
    :return: We return conversion from input currency to output currency/currencies in json format
    """
    amount = request.args.get('amount', type=float)
    input_currency = request.args.get('input_currency', type=str)
    output_currency = request.args.get('output_currency', type=str, default=None)

    converter = Converter()

    if output_currency:
        args = converter.parser_arguments(f'--amount {amount} --input_currency {input_currency} --output_currency {output_currency}'.split())
    else:
        args = converter.parser_arguments(f'--amount {amount} --input_currency {input_currency}'.split())

    return jsonify(converter.searching_conversion(args))


if __name__ == "__main__":
    app.run()

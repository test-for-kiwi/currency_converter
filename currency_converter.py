#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
from forex_python.converter import CurrencyRates, RatesNotAvailableError


class Converter(object):
    def parser_arguments(self, args=None):
        """
        Method parsing arguments from command line or from web api url. --output_currency is optional, others are mandatory
        :param args: In case we want make test from this program or call via web api
        :return: Namespace with arguments from command line
        """
        parser = argparse.ArgumentParser(description='Input for currency converter')
        parser.add_argument('--amount', help='Amount which you want to convert', dest='input_amount', required=True, type=float)
        parser.add_argument('--input_currency', help='Input currency - 3 letters name or currency symbol', required=True, type=str.upper)
        parser.add_argument('--output_currency', help='Requested/output currency - 3 letters name or currency symbol', type=str.upper)

        return parser.parse_args(args)

    def get_code_from_symbol(self, currency_symbol_test):
        """
        Find out if entered string for currency is symbol. If yes then return currency code, else return None
        :param currency_symbol_test: Is it really symbol?
        :return: currency code or None
        """
        file_path = os.path.dirname(os.path.abspath(__file__))

        with open(file_path + '/currencies.json') as f:
            currency_data = json.loads(f.read())

        currency_code = next((item.get('cc') for item in currency_data if item["symbol"] == currency_symbol_test), None)

        return currency_code

    def searching_conversion(self, args):
        """
        According to input parameters this method finds out exchange rate(s) between currency/currencies.
        :param args: Namespace with arguments from command line or from z web api url
        :return: We return conversion from input currency to output currency/currencies in string prepared for json
        """
        curr_rates = CurrencyRates()

        # Test if input currency is entered as symbol. If yes, we find out currency code
        transformed_input_code = self.get_code_from_symbol(args.input_currency)

        if transformed_input_code:
            args.input_currency = transformed_input_code

        # Is output currency entered?
        if args.output_currency:
            # Test if input currenci is entered as symbol. If yes, we find out currency code
            transformed_output_code = self.get_code_from_symbol(args.output_currency)

            if transformed_output_code:
                args.output_currency = transformed_output_code

            try:
                # We try to find out exchange rate. If currency not known, throw an error.
                output_amount = curr_rates.convert(args.input_currency, args.output_currency, args.input_amount)
            except RatesNotAvailableError:
                return f'{args.input_currency} or {args.output_currency} is not known currency.'

            adjusted_output_amount = {args.output_currency: round(output_amount, 3)}
        else:
            try:
                # We try to find out exchange rate. If currency not known, throw an error.
                output_amount_dict = curr_rates.get_rates(args.input_currency)
            except RatesNotAvailableError:
                return f'{args.input_currency} is not known currency.'

            adjusted_output_amount = {key: round(value * args.input_amount, 3) for key, value in output_amount_dict.items()}

        # Complete string with output data
        res = {
            'input':
                {
                    'amount': args.input_amount,
                    'currency': args.input_currency
                },
            'output': adjusted_output_amount
        }

        return res


def testcases(converter):
    """
    Testing function. We can check here, how parser evaluate arguments.
    :return: None. Print input parameters and result of currency conversion.
    """
    tests = ['--amount 100.0 --input_currency EUR --output_currency CZK',
             '--amount 100.0 --input_currency EUR',
             '--amount 0.9 --input_currency ¥ --output_currency AUD',
             '--amount 10.92 --input_currency £',
             '--amount 10.92 --input_currency $ --output_currency €'
            ]

    for test in tests:
        args = converter.parser_arguments(test.split())
        print(args)
        print(json.dumps(converter.searching_conversion(args), indent=4))


def main():
    converter = Converter()
    # Uncomment function when testing
    #testcases(converter)

    # Parsing arguments from command line
    args = converter.parser_arguments()

    # Print required conversion
    print(json.dumps(converter.searching_conversion(args), indent=4))


if __name__ == "__main__":
    main()

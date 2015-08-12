#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Brian Bugh
# Copyright (c) 2015 Brian Bugh
#
# License: MIT
#

"""This module exports the ElmLint plugin class."""

import json
import re
from SublimeLinter.lint import Linter, util


class ElmLint(Linter):

    """Provides an interface to elm-lint."""

    syntax = 'elm'
    cmd = 'elm-make --warn --report=json'
    executable = None
    version_args = '--version'
    version_re = r'Elm Platform (?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.15.0'
    regex = r'^(?:(?P<warning>warning)|(?P<error>error))\|(?P<line>\d+)\|(?P<col>\d+)\|(?P<message>.*?)\|(?P<near>.*?)$'
    multiline = False
    line_col_base = (1, 1)
    tempfile_suffix = 'elm'
    error_stream = util.STREAM_BOTH
    selectors = {}
    word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = None

    def run(self, cmd, code):
        """
        Runs the elm-make command with a json output and then transforms it
        into a simplified string that the regex can parse.
        """

        cmd_output = super().run(cmd, code)

        if re.match(r'^Successfully generated.*$', cmd_output) is not None:
            return cmd_output

        json_errors = json.loads(cmd_output)

        transformed_errors = []
        for error in json_errors:
            err_type = error['type'] # warning || error
            overview = error['overview']

            # Elm sometimes specifies two regions. The "subregion" is more
            # contextually relevant, so default to that if it's available.
            region = error.get('subregion') or error.get('region')

            # Type mismatch errors specify additional useful data in the
            # details element, but not in json format.
            details = error['details']
            type_mismatch = re.match(r'As I infer the type.*types:\s*(?P<expected>\w+)\s*(?P<actual>\w+)', details, re.DOTALL)
            if type_mismatch  is not None:
                overview += " Expected '" + type_mismatch.group('expected') + "', got '" + type_mismatch.group('actual') + "'"

            # SublimeLinter can highlight a larger area if the range is specified
            # using characters - Elm has lengthy meaningful errors so this will
            # highlight the full error location the same way Elm does.
            highlight = "x" * (region['end']['column'] - region['start']['column'])

            error_info = err_type + "|" + str(region['start']['line']) + "|" + str(region['start']['column']) + "|" + overview + "|" + highlight

            transformed_errors.append(error_info)

        return "\n".join(transformed_errors)
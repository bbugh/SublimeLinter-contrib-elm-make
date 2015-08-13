#
# linter.py
# Elm Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Brian Bugh
# Copyright (c) 2015 Brian Bugh
# Twitter: @brainbag
# Github: @bbugh
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
    version_re = r'elm-make (?P<version>[\.\d]+)'
    version_requirement = '>= 0.2.0'
    regex = r'^(?:(?P<warning>warning|warn)|(?P<error>error))@@@(?P<line>\d+)@@@(?P<col>\d+)@@@(?P<message>.*?)@@@(?P<near>.*?)?$'
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
        """Run elm-make, transform json into a string parseable by the regex."""
        cmd_output = super().run(cmd, code)

        # Package missing error does not come out in json, so give a useful error
        # and ignore everything else that happens.
        if re.match(r'Some new packages are needed.', cmd_output) is not None:
            return 'error@@@1@@@1@@@Missing required packages; please run "elm-package install".'

        elm_errors = re.match(r'\[\{.*\}\]', cmd_output, re.DOTALL)

        # If no json is found, it's a good build (or an unhandled exception)
        if elm_errors is None:
            return cmd_output

        json_errors = json.loads(elm_errors.group())

        transformed_errors = [self.transform_error(error) for error in json_errors]

        return "\n".join(transformed_errors)

    def transform_error(self, error):
        """Transform json error into a string for the regex matcher."""
        # Elm sometimes specifies two regions. The "subregion" is more
        # contextually relevant, so default to that if it's available.
        region = error.get('subregion') or error.get('region')

        # SublimeLinter can highlight a larger area if the range is specified
        # using characters - Elm has lengthy meaningful errors so this will
        # highlight the full error location the same way Elm does.
        highlight = "x" * (region['end']['column'] - region['start']['column'])

        return "@@@".join([
            error['type'],
            str(region['start']['line']),
            str(region['start']['column']),
            self.build_message(error),
            highlight
        ])

    def build_message(self, json_error):
        """
        Collect error message details.

        Elm includes extra useful content in the 'details' field, but
        it's in text form. This will extract useful info from error
        messages.
        """
        details = json_error['details']
        overview = json_error['overview']

        # Missing fields shows list of fields, extract them
        missing_fields = re.match(r'Looks like a record is missing fields (?P<fields>.*)\s*', details)
        if missing_fields is not None:
            overview += ' Maybe missing fields "{}"?'.format(missing_fields.group('fields'))

        # Type mismatch lists types, extract them
        type_mismatch = re.match(r'.*?As I infer the type.*types:\s+(?P<expected>[^\n]+)\n\s+(?P<actual>[^\n]+)\s*', details, re.DOTALL)
        if type_mismatch is not None:
            overview += ' Expected "{}", got "{}"'.format(
                type_mismatch.group('expected'), type_mismatch.group('actual'))

        return overview

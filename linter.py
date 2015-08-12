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

        json_data = json.loads(cmd_output)

        result = []
        for error in json_data:
            err_type = error['type']

            # Elm sometimes specifies two regions. The "subregion" is more
            # contextually relevant, so default to that if it's available.
            region = error.get('subregion') or error.get('region')
            overview = error['overview']

            # SublimeLinter can highlight a larger area if the range is specified
            # using characters - Elm has lengthy meaningful errors so this will
            # highlight the full error space the same way Elm does.
            highlight = "x" * (region['end']['column'] - region['start']['column'])

            error_info = err_type + "|" + str(region['start']['line']) + "|" + str(region['start']['column']) + "|" + overview + "|" + highlight

            result.append(error_info)

        return "\n".join(result)
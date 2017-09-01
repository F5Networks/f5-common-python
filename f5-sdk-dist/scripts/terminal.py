#!/usr/bin/env python
# Copyright 2017 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import subprocess

from collections import namedtuple

# used for terminal:
Result = namedtuple('Result', 'succeeded, cli, error')


class Hold(object):
    """Hold

A basic text caching object for later use of printing into the terminal,
storing into a return object, or mimicking the standard IO commands of a file
object.

This object is handy for reducing code size, but offering a transparent
functionality to a user using the terminal function.
    """
    def __init__(self):
        self.held = str()

    def __str__(self):
        return self.get_held()

    def __enter__(self):
        return self

    def __exit__(self):
        self.held = ''

    def writeline(self, addition):
        """writeline()

Functions like a file.writeline() call; however, it stores into the object's
cached memory rather than a file's IO.
        """
        addition = addition.strip()
        self.held = self.held + addition + "\n"

    def write(self, addition):
        """write()

Functions like a file.write() call; however, it stores into the object's cached
memory rather than a file's IO.
        """
        self.held = self.held + addition

    def output(self):
        """output()

Dumps the contents of the cache as a string into the terminal.
        """
        print(self.held)

    def get_held(self):
        """get_held()

Returns the cached contents as a str() object.
        """
        return self.held


def terminal(cmd, log=None, args=[], want_result=True, multi_stmt=False):
    """terminal

Usage:
    terminal(cmd, log=None, args=[], want_result=True, multi_stmt=False)

    Args:
        cmd - list or tuple(list) that contains the command with args
            commonly delimited by spaces
    Opts:
        log - string containing the log location where to store the CLI
            stdout result from running the command on the terminal
        args - list of arguments within the command statement that would
            normally be delimited by spaces.  Note that if the cmd argument
            is already a list, then it will be extended by this list.  If it
            is a str, then it will be put into a list with this list
            extended after it.
        want_result - boolean contaiining whether or not the result,
            namedtuple will be returned
        multi_stmt - boolean enabling there to be a multi-command stmt.  If
            this is left as False, then cmd statements in the arguments or
            as a part of the cmd argument will be ignored and not
            interpretted, or the OSError will be thrown over the fact that
            the cmd will not be allowed.
    Returns:
        result - A named tuple containing the following flags:
            succeeded - boolean on whether or not the command succeeded
            cli - the cli's stdout
            error - the exception that was thrown if one was over whether or
                not the command failed at the CLI

This function will attempt to execute a CLI command at the /bin/bash
terminal.
    """
    Error = None
    succeeded = False
    if log and isinstance(log, str) and os.access(log, os.W_OK):
        fh = open(log, 'w')
    else:
        fh = Hold()
    if args and isinstance(cmd, str):
        cmd = [cmd]
        cmd.extend(args)
    try:
        proc = subprocess.Popen(cmd, shell=multi_stmt, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        # fh.write(subprocess.check_output(cmd, shell=multi_stmt))
        out, err = proc.communicate()
        fh.write('Out:\n' + str(out))
        fh.write('Err:\n' + str(err))
        succeeded = True if proc.returncode == 0 else False
    except OSError as Error:
        fh.write(str(Error))
    except subprocess.CalledProcessError as Error:
        fh.write(str(Error))

    try:
        fh.close()
        result = Result(succeeded, None, Error)
    except Exception:
        if want_result:
            result = Result(succeeded, fh.get_held(), Error)
        elif not want_result:
            result = Result(succeeded, None, Error)
            fh.output()
    return result

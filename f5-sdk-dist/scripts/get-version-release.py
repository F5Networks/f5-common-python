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

import argparse
import re
import subprocess
import sys

releaseTagRe = re.compile("^v(\d+\.\d+\.\d+((a|rc|RC)\d+)?$)")
gitDescribeRe = re.compile("^v(\d+\.\d+\.\d+(?:a\d+)?)-(\d+)-g(.*)$")


def runCommand(cmd):
    output = ""

    try:
        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                             )
        (output) = p.communicate()[0]
    except OSError as e:
        print("Execution failed:", e)

    return (output, p.returncode)


def main(args):

    version = "0.0.0"
    releaseNumber = 1
    branch = ""

    # Is this a tagged commit?
    (output, status) = runCommand('git describe --tags --exact-match')

    if status == 0:
        # Yes.
        tag = output.rstrip()

        # Does this tag match the format of tagged releases?
        m = releaseTagRe.match(tag)
        if m:
            version = m.group(1)
        (output, status) = runCommand('git rev-parse --short HEAD')
        if status == 0:
            commit = output.rstrip()
    else:
        # No, use git describe to get information about this commit.
        (output, status) = runCommand('git describe --tags')
        if status == 0:

            m = gitDescribeRe.match(output)
            if m:
                version = m.group(1)
                release = m.group(2)
                commit = m.group(3)

                releaseNumber = releaseNumber + int(release)

    # Get the branch name.
    (output, status) = runCommand('git rev-parse --abbrev-ref HEAD')
    if status == 0:
        branch = output.rstrip()

    results = []
    if args.version:
        results.append(version)
    if args.release:
        results.append(releaseNumber)
    if args.commit:
        results.append(commit)
    if args.branch:
        results.append(branch)

    if len(results):
        print('%s' % ' '.join(map(str, results)))
    else:
        print(version, releaseNumber, commit, branch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action="store_true")
    parser.add_argument('--release', action="store_true")
    parser.add_argument('--branch', action="store_true")
    parser.add_argument('--commit', action="store_true")

    main(parser.parse_args(sys.argv[1:]))

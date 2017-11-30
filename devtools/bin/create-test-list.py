#!/usr/bin/env python

"""
Rules

for *.py files
  * if the changed file is __init__.py, and there is a side-band test/ dir, then test the entire test/functional directory
    the reason for this is that the init files are usually organizing collections
    and those can affect many different apis if they break
  * if the filename is test_*.py then include it
  * if the filename is *.py, then check to see if it has an associated test_FILENAME file
    and if so, include it in the test
  * summarize all of the above so that a test_FILENAME that is a subpath of the first bullet
    is not tested twice

for non-*.py files
  * if the file is in a test/functional directory, test the whole directory
"""

import subprocess
import os
import shutil
import argparse


def cleanup_tox_directory():
    if os.path.exists('.tox'):
        shutil.rmtree('.tox')


def examine_python_rules(line):
    fname, fext = os.path.splitext(line)
    filename = os.path.basename(line)
    dirname = os.path.dirname(line)
    test_filename = 'test_' + filename
    functional_test_file = '{0}/test/functional/{1}'.format(dirname, test_filename)
    functional_test_dir = '{0}/test/functional/'.format(dirname)

    if filename == '__init__.py' and os.path.exists(functional_test_dir):
        return functional_test_dir
    elif filename.startswith('test_') and filename.endswith('.py'):
        return line
    elif fext == '.py' and os.path.exists(functional_test_file):
        return functional_test_file
    elif 'test/functional' in line and filename == '__init__.py':
        print("  * Skipping {0} because it is not a test file".format(line))
    elif filename == '__init__.py' and not os.path.exists(functional_test_dir):
        print("  * {0} does not have a side-band test directory!".format(line))
    else:
        print("  * {0} did not match any rules!".format(line))


def examine_non_python_rules(line):
    if 'test/functional' in line:
        return os.path.dirname(line)


def determine_files_to_test(product, commit):
    results = []
    build_all = [
        'setup.py', 'f5/bigip/contexts.py', 'f5/bigip/mixins.py',
        'f5/bigip/resource.py', 'f5sdk_plugins/fixtures.py',
        'f5/bigip/__init__.py'
    ]
    output_file = "pytest.{0}.jenkins.txt".format(product)

    p1 = subprocess.Popen(
        ['git', '--no-pager', 'diff', '--name-only', 'origin/development', commit],
        stdout=subprocess.PIPE,
    )
    p2 = subprocess.Popen(
        ['egrep', '-v', '(^requirements\.|^setup.py)'],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
    )
    p3 = subprocess.Popen(
        ['egrep', '(^f5\/{0}\/)'.format(product)],
        stdin=p2.stdout,
        stdout=subprocess.PIPE,
    )
    out, err = p3.communicate()
    out = out.splitlines()
    out = filter(None, out)

    if not out:
        return

    for line in out:
        fname, fext = os.path.splitext(line)

        if not os.path.exists(line):
            print "{0} was not found. Maybe this is a rename?".format(line)
            continue

        if line in build_all:
            cleanup_tox_directory()
            results.append('f5/{0}'.format(product))
        elif fext == '.py':
            result = examine_python_rules(line)
            if result:
                results.append(result)
        else:
            result = examine_non_python_rules(line)
            if result:
                results.append(result)
    if results:
        results = set(results)
        results = compress_testable_files(results)
        fh = open(output_file, 'w')
        fh.writelines("%s\n" % l for l in results)
        fh.close()


def compress_testable_files(files):
    lines = sorted(files)

    for idx, item in enumerate(lines):
        file, ext = os.path.splitext(item)
        if not ext and not file.endswith('/'):
            item += '/'
        tmp = [x for x in lines if item in x and item != x]
        for _ in tmp:
            lines.remove(_)
    return lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--commit', help='Git commit to check', required=True)
    args = parser.parse_args()

    for product in ['iworkflow', 'bigip', 'bigiq']:
        determine_files_to_test(product, args.commit)

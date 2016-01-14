<!--
Copyright 2015 F5 Networks Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Contributing Guide for f5-common-python
If you have found this that means you you want to help us out. Thanks in advance for lending a hand! This guide should
get you up and running quickly and make it easy for you to contribute. If we don't answer your questions here and you
help or just want to say hi shoot us an email at f5-common-python@f5.com.

## Issues
Creating issues is good, creating good issues is even better. By filing meaningful bug reports will lots of information
 in them helps us figure out what to fix when and how it impacts our users. We like bugs because it means people are
 using our code, and we like fixing them even more.
 
### Bugs
TODO: What do we want in our bug reports and an example?

### Feature Requests and Enhancements
TODO: What do we want in our bug reports and an example?

## Pull Requests
If you are submitting a pull request you need to make sure that you have done a few things first.

* If an issue doesn't exist, file one.
* Make sure you have tested your code because we are going to do that when when you make your PR. You don't want 
_The Hat_ because your request fails unit tests.
* A reasonable set of unit tests is required, and the approver of the pull request is expecting to review them along with the product code.
* Functional tests are nice-to-have but not required to complete a pull request. Note that not having functional tests will make your pull request end up in an integration branch and be held out of the main develop branch until someone writes an appropriate set of tests.
* Clean up your git history because no one wants to see 75 commits for one issue
* Use our [commit template](.git-commit-template.txt).
* Use our pull request template.

```
@<reviewer_id>
#### What issues does this address?
Fixes #<issueid>
WIP #<issueid>
...

#### What's this change do?

#### Where should the reviewer start?

#### Any background context?
```

## Testing
Creating tests is pretty straightforward and we need you to help us keep ensure
the quality of our code. We write both our unit tests and functional tests
using [pytest](http://pytest.org). We know it is extra work to write these
tests but the maintainers and consumers of this code appreciate the effort and
writing the tests is pretty easy. Take a look at a few of the test directories 
like [f5/bigip/ltm/test](f5/bigip/ltm/test/) if you need help getting started.

Unit tests are located alongside the code, such as [f5/bigip/ltm/test](f5/bigip/ltm/test/).
Functional tests are located at the top level in [test/functional](test/functional/).
 
Running tests is easy. Here's an example of how to run unit tests.

```
shell
 $ py.test --cov ./f5 --cov-report=html --ignore=test/
 $ open htmlcov/index.html
```

If you are running our functional tests, you will need a real BIG-IP to run them against. You can get one of those pretty easily in [Amazon EC2](https://aws.amazon.com/marketplace/pp/B00JL3UASY/ref=srh_res_product_title?ie=UTF8&sr=0-10&qid=1449332167461).

Here's an example of how to run functional tests.

```
shell
 $ py.test --ignore=f5/ --bigip=1.2.3.4
```

## License
 
### Apache V2.0
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 
### Contributor License Agreement
Individuals or business entities who contribute to this project must have completed and submitted the [F5 Contributor License Agreement](http://f5networks.github.io/f5-openstack-docs/cla_landing/index.html) to Openstack_CLA@f5.com prior to their
code submission being included in this project.


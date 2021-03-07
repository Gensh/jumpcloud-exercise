# Jumpcloud QA Exercise

QA exercise for Senior QA Engineer, SaaS

## Process

### Planning

Initially, a shallow reading of the requirements led the developer to believe an automation framework was mandatory. While this was later identified to not be the case, initial planning was directed to that end. As such, initial goals were shallow.

- Set up test framework using boilerplate from prior frameworks.
- Write wrapper around the hash server to fluently run commands agnostic of OS.
- Write a basic test for GETting a hash since that will cover the bulk of functionality.
- Expand test coverage for POST, GET, and GET stats to cover basic cases.
- Extend the hash server wrapper to test parallel connection, including shutdown.
- Identify gaps in test coverage and expand.

Python was selected as the development language due to the developer's familiarity with the tools. A time limit was set between 3-5 hours to complete all tasks.

### Building the framework

The developer made a number of early mistakes due to time away from PyTest and the age of the boilerplate. Updating dependencies and other setup consumed at least an hour. Several hours were consumed by chasing the difference between running the hash server on its own vs through Python – the issue being a change in API since the developer had last used the `subprocess` module. The developer considered this time to be lost and so did not include it in the allotted limit. In an ordinary iteration, this would be result in delaying another work item.

Past this point, progress was more as expected. It's possible that the amount of time spent on refactoring and organization was undue for a project of this weight, but the developer is distracted by a messy code base. Around the three hour mark, the developer stopped for review of the code base. While a number of basic cases were lain out, distance to the final deliverable was unclear, especially given the 80:20 rule. The developer made the decision to stop work on the automation framework.

## Deliverables

### Tests

Test were written according to the requirements, even if the developer disagreed with them (example: returning 200 during shutdown). In lieu of more formal requirements and due to the simplicity of the tests written, all were described by job stories rather than just acceptance criteria. That was probably an abuse of the format, but it was easier to write. At present, test coverage is for basic cases only. More complete testing would largely require solving the issues discussed in results below.

### Results of automation

None of the test cases under automation are passing. This was an issue encountered immediately, as the example commands gave different output than expected. After resolving issues within the automation framework, however, test cases were still not passing. Ordinarily, the developer would have consulted with other QA team members and then developer team members after a short window of examination. As this ws not possible, the developer chose to expand test coverage as if the problem was resolved. This would make the best use of time.

### Bug reports

The developer chose not to write any bug reports. As failure is total, there is a greater underlying issue which would need to be resolved before even considering doing so. More importantly, internal bug reports are a tool to be used sparingly. In most cases, they indicate development process is broken and can strengthen silo walls. Bugs discovered internally should be scoped and worked as a normal ticket with QA providing guidance.

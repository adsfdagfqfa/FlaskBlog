# Assignment B3 Report Draft - Parts 1 to 4

Project under test: FlaskBlog  
Repository: `D:\CodeField\FlaskBlog`  
Selected component test framework: Python `unittest` with Flask `test_client` and isolated SQLite databases

> Note: Parts 5 and 6, "Use of Artificial Intelligence" and "Ethical Considerations", are intentionally left for later completion by the team.

## 1. Introduction to the Implemented Software Project

### 1.1 Project Background

FlaskBlog is a modern blog web application implemented with the Flask framework. It provides a complete blogging platform where users can register, log in, publish posts, browse posts, comment on posts, search content, and manage account settings. The project also includes administration functions for managing users, posts, and comments.

The system is suitable for a personal blog or a small content publishing platform. Its design is lightweight and practical: Flask is used as the web framework, SQLite is used for data persistence, WTForms is used for form definition, Jinja templates are used for server-side rendering, and TailwindCSS is used for styling the user interface.

### 1.2 General Goals of the Project

The general goals of FlaskBlog are:

- To provide a usable blog platform with user registration, authentication, post publishing, post reading, and comments.
- To support administrative management of users, posts, and comments.
- To provide a clean and responsive user interface with dark and light themes.
- To support multiple languages through translation files.
- To track basic post analytics, including post views and visitor information.
- To provide basic security controls such as password hashing, session management, CSRF protection, and optional reCAPTCHA.

### 1.3 Major Functional Requirements

| Functional area | Main requirements | Main source files |
|---|---|---|
| User authentication | Register, log in, log out, reset password, and verify user identity | `app/routes/signup.py`, `app/routes/login.py`, `app/routes/logout.py`, `app/routes/passwordReset.py`, `app/routes/verifyUser.py` |
| User account management | View profile pages, account settings, username changes, password changes, and profile-picture changes | `app/routes/user.py`, `app/routes/accountSettings.py`, `app/routes/changeUserName.py`, `app/routes/changePassword.py`, `app/routes/changeProfilePicture.py` |
| Blog content management | Home page, post creation, post viewing, post editing, post deletion, comments, and post URL ID / slug generation | `app/routes/index.py`, `app/routes/createPost.py`, `app/routes/post.py`, `app/routes/editPost.py`, `app/routes/dashboard.py`, `app/utils/delete.py`, `app/utils/generateUrlIdFromPost.py` |
| Search and categories | Search users and posts by keyword; browse posts by category | `app/routes/search.py`, `app/routes/searchBar.py`, `app/routes/category.py` |
| Administration | View and manage users, posts, and comments; change user roles | `app/routes/adminPanel.py`, `app/routes/adminPanelUsers.py`, `app/routes/adminPanelPosts.py`, `app/routes/adminPanelComments.py` |
| Analytics | Record post views, visitor usernames, countries, operating systems, continents, and time spent | `app/routes/postsAnalytics.py`, `app/routes/returnPostAnalyticsData.py`, `app/utils/getAnalyticsPageData.py` |

### 1.4 Major Non-Functional Requirements

| Quality characteristic | Requirement in this project | Related risk |
|---|---|---|
| Security | Passwords should be hashed; authenticated pages should require valid sessions; CSRF protection should be enabled; reCAPTCHA can be enabled for login and signup | Input validation and authorization checks are distributed across route functions, which increases the risk of missing checks |
| Reliability | Core user and post workflows should work consistently; database operations should not crash on normal inputs | Route functions directly perform database operations, so exceptions may interrupt main workflows |
| Usability | The web interface should be responsive, understandable, visually consistent, and easy to navigate | If backend validation and UI validation are inconsistent, users may receive confusing behavior |
| Internationalization and UI quality | The system should provide translated interface text, support multiple languages, support dark/light presentation, and keep templates, CSS, and JavaScript consistent across pages | Translation gaps, inconsistent theme behavior, or inconsistent layout may reduce usability for different users |
| Maintainability | Code should be modular and easy to test | Business logic, database access, and template rendering are mixed in route functions |
| Testability | Components should be testable with isolated test data | Global configuration and database paths must be patched during testing to avoid polluting production-like databases |
| Performance | Common pages such as home, search, post view, and admin pages should respond in acceptable time | Multiple SQLite queries and repeated database connections may affect scalability |

### 1.5 Software Architecture and Major Components

FlaskBlog follows a lightweight Flask architecture based on routes, templates, forms, utility modules, and SQLite databases.

| Component | Description |
|---|---|
| Application entry point | `app/app.py` creates the Flask application, configures CSRF protection, registers context processors, registers error handlers, and registers all Blueprints. |
| Configuration | `app/settings.py` stores application name, version, host, port, database paths, UI paths, SMTP settings, default administrator settings, and reCAPTCHA settings. |
| Routes / controllers | `app/routes/*.py` contains route functions for user actions, post actions, search, categories, administration, and analytics. |
| Forms | `app/utils/forms/*.py` defines WTForms form classes for signup, login, password reset, post creation, comments, and account changes. |
| Utility modules | `app/utils/*.py` provides helper functions for logging, timestamps, points, deletion, profile pictures, post URL IDs, analytics, and translations. |
| Data storage | `app/db/*.db` contains SQLite databases for users, posts, comments, and analytics. `app/utils/dbChecker.py` creates required database tables when the application starts. |
| Presentation layer | `app/templates/tailwindUI` contains Jinja templates. `app/static/tailwindUI` contains CSS and JavaScript assets. |

The architecture is simple and easy to understand, but many route functions combine request parsing, validation, authorization, database access, business logic, and response generation. This makes the system easy to build but also increases the chance of logic defects in complex workflows.

## 2. Risk Analysis Report

### 2.1 Objective and Scope of Risk Analysis

The objective of this risk analysis is to identify, assess, and prioritize the main product risks of FlaskBlog, so that the testing effort can focus on the most important and failure-prone areas. The risk analysis is also used as the basis for the high-level test plan and for selecting the two modules used in detailed component testing.

The scope of this risk analysis includes product quality risks that may affect the visible behavior, correctness, reliability, security, and maintainability of the FlaskBlog application. The analysis focuses on risks related to:

- User registration, login, and session handling.
- Post creation, post viewing, and post management.
- Database integrity for users, posts, comments, and analytics data.
- Authorization control for restricted pages and administrator functions.
- Search, category browsing, and analytics features.
- Web application concerns such as input validation, error handling, external service configuration, and usability.

The following items are not the main scope of this risk analysis:

- Project management risks such as team availability, schedule delay, or communication issues.
- Full penetration testing or formal security audit.
- Load testing, stress testing, and large-scale performance benchmarking.
- Full compatibility testing across all browsers and devices.
- Real external service reliability, such as live SMTP delivery or live Google reCAPTCHA availability.

### 2.2 Risk Identification Method

The risks were identified from several sources to avoid relying on only one viewpoint:

| Source | How it was used for risk identification |
|---|---|
| Project requirements and README features | The feature list was used to identify major user-visible functions such as registration, login, post creation, administration, search, themes, and analytics. |
| Software architecture | `app/app.py` and the Blueprint registration structure were reviewed to understand major components and dependencies. |
| Source code review | Route functions, form classes, utility functions, and database helper code were inspected to identify validation, authorization, database, and exception-handling risks. |
| Database structure | SQLite tables for users, posts, comments, and analytics were reviewed to identify data integrity and persistence risks. |
| User workflows | Typical workflows were traced, including signup, login, create post, view post, comment, search, and admin management. |
| Exploratory analysis | The application code was explored manually and with small route-level tests to find suspicious logic paths and failure-prone branches. |
| Web application checklist | Common web application risk areas were considered, including input validation, authentication, authorization, session state, CRUD operations, file upload, external services, error handling, and usability. |

This identification process produced a list of product risks that are directly connected to observable software quality and testable behavior.

### 2.3 Risk Assessment Method

The risk assessment uses a qualitative risk-based testing approach. Each risk item is assessed by two factors:

- Likelihood: the probability that the risk will occur.
- Impact: the seriousness of the consequence if the risk occurs.

Both factors are rated on a 1 to 5 scale:

| Score | Likelihood meaning | Impact meaning |
|---|---|---|
| 1 | Very unlikely | Very low impact |
| 2 | Unlikely | Low impact |
| 3 | Possible | Medium impact |
| 4 | Likely | High impact |
| 5 | Very likely | Very high impact |

Risk exposure is calculated as:

`Risk Exposure = Likelihood x Impact`

Risk levels:

| Risk exposure | Risk level |
|---|---|
| 1-6 | Low |
| 7-12 | Medium |
| 13-25 | High |

### 2.4 Product Risk Register

| ID | Risk category | Risk item | Affected area | Likelihood | Impact | Exposure | Level | Mitigation / test focus |
|---|---|---|---|---:|---:|---:|---|---|
| R1 | Signup input validation | The signup route may accept malformed or incomplete account data if WTForms rules are not enforced on the backend | `signup.py`, `SignUpForm.py`, users database | 4 | 4 | 16 | High | Apply equivalence partitioning and boundary value analysis to username, email, password, confirmation, and duplicate data |
| R2 | Post creation workflow reliability | Valid logged-in users may be unable to create posts, or invalid post data may be stored, due to missing validation, helper-call errors, or database insertion failures | `createPost.py`, `CreatePostForm.py`, `generateUrlIdFromPost.py`, posts database | 4 | 5 | 20 | High | Use white-box tests for unauthenticated access, empty content, valid content insertion, and helper/database paths |
| R3 | Access control | Restricted routes may rely on incomplete or inconsistent session and role checks, allowing unauthorized access or modification | Create post, dashboard, edit post, delete operations, admin panel | 3 | 5 | 15 | High | Test session-based access control for the selected create post workflow; record role-based admin and delete permissions as wider product risks |
| R4 | Data integrity | Duplicate users, duplicate emails, malformed accounts, or malformed posts may be persisted and affect later login, display, search, or administration behavior | Signup, login, posts, comments | 3 | 4 | 12 | Medium | Check database side effects after valid, invalid, and duplicate submissions |
| R5 | Login and session correctness | Valid users may fail to log in, wrong credentials may be accepted, or session state may not be established correctly | `login.py`, users database, Flask session | 4 | 4 | 16 | High | Apply black-box tests for valid login, wrong password, and unknown user behavior |
| R6 | Post view and comment-path reliability | Viewing an existing or missing post may fail, views may be updated incorrectly, or comment-related branches may crash due to route-level assumptions | `post.py`, posts database, comments database | 3 | 4 | 12 | Medium | Apply white-box tests for existing post, missing post, slug redirect, and comment insertion branches |
| R7 | Administration and destructive action safety | Admin, delete, and role-change operations may affect the wrong user or content if role checks or delete cascades are incomplete | Admin panel, dashboard delete, post delete, user delete | 2 | 5 | 10 | Medium | Record as a medium-priority follow-up area; deletion tests are not part of the current detailed execution |
| R8 | Usability and internationalization | Multi-language and theme features may display inconsistent UI text | Translation and templates | 2 | 2 | 4 | Low | Perform usability checks on selected languages and pages |
| R9 | External dependency | External services may fail or be misconfigured | SMTP, reCAPTCHA, profile picture service | 3 | 3 | 9 | Medium | Use configuration-based tests and mock external services where possible |
| R10 | Reliability and resource management | Routes that open SQLite connections directly may leave transactions or connections in an uncertain state when exceptions occur | Signup, login, create post, edit post, delete utilities | 3 | 3 | 9 | Medium | Consider through white-box review; direct automated resource assertions are outside the current execution |
| R11 | Credential security | Passwords may be stored in plaintext or in a format that violates security expectations | Signup, login, users database | 2 | 5 | 10 | Medium | Verify after signup that stored password values differ from raw passwords; deeper security testing is outside scope |
| R12 | Search functional correctness | Search results may be incomplete or inconsistent across title, tags, author, and username queries | Search route | 3 | 3 | 9 | Medium | Record for future functional tests outside the detailed component-test scope |
| R13 | Analytics correctness | Post analytics may record missing or incorrect visitor, country, operating-system, or time-spent data | Analytics routes and analytics database | 3 | 3 | 9 | Medium | Record for future API and database-state tests outside the detailed component-test scope |

### 2.5 Risk Prioritization

The highest risks are R1, R2, R3, and R5. They are prioritized because they affect the main user journey:

1. A user must be able to register with valid information, and invalid information must be rejected.
2. A logged-in user must be able to create a post successfully.
3. Restricted operations must not be available to unauthenticated or unauthorized users.
4. A registered user must be able to log in only with valid credentials and receive a correct session.

Risk level summary:

| Risk level | Exposure range | Number of risks | Risk IDs | Testing implication |
|---|---:|---:|---|---|
| High | 13-25 | 4 | R1, R2, R3, R5 | Must be prioritized by systematic test design and early representative execution |
| Medium | 7-12 | 8 | R4, R6, R7, R9, R10, R11, R12, R13 | Should be covered by representative functional, integration, or review-based tests |
| Low | 1-6 | 1 | R8 | Can be covered by checklist-based review and exploratory usability checks |

Therefore, the detailed component tests in this report focus on two high-risk functional areas and four representative route-level components:

- User Authentication as the black-box target area, with signup and login selected as representative workflows, addressing R1, R4, and credential/session risks.
- Blog Content Management as the white-box target area, with create post and post view/comment handling selected as representative workflows, addressing R2, R3, and post data integrity risks.

This prioritization also supports the test execution order. High-risk tests should be executed first because failures in registration, post creation, or access control would block the most important user workflows. The risk register covers the whole product, but the detailed component tests cover only the selected representative workflows. Login, post editing, post deletion, administration, search, and analytics are recorded as product risks or future regression-test candidates, but they are not claimed as fully tested in this report.

### 2.6 Risk-to-Test Traceability

| Risk ID | Risk focus | Selected module / component | Related test design | Coverage status in this report |
|---|---|---|---|---|
| R1 | Invalid signup input may be accepted | User Account and Authentication / signup workflow | BB-01 to BB-24; executed all designed signup cases | Covered by design and automated execution; defect found |
| R2 | Valid post creation may fail | Blog Content Management / create post workflow | WB-Create-01 to WB-Create-04 | Covered for main create-post branches; defect found |
| R3 | Unauthorized access to restricted functions | Blog Content Management / create post workflow | WB-Create-01 unauthenticated create-post access | Partially covered only for `/createpost`; admin, edit, and delete authorization are not fully tested |
| R4 | Duplicate or malformed data may be stored | Signup database state checks | BB duplicate and invalid-input cases | Partially covered through users database assertions |
| R5 | Login may accept wrong credentials or fail to establish a session | User Authentication / login workflow | BB-Login representative tests | Covered by black-box login tests |
| R6 | Post viewing may fail for missing posts or comment-related branches | Blog Content Management / post view workflow | WB-Post representative branch tests | Covered by white-box post route tests; defect risk recorded |
| R7 | Delete and administration operations may affect wrong records | Admin and delete-related routes | Not selected for detailed execution | Recorded as follow-up risk |
| R10 | Direct SQLite operations may have weak exception/resource handling | Signup and create-post routes | White-box review during component selection | Not directly automated |
| R11 | Password storage may be insecure | Signup/login workflow | Potential database assertion after valid signup | Recorded as follow-up check |

### 2.7 Risk Mitigation Strategy

| Risk level | Mitigation strategy |
|---|---|
| High | Design systematic test cases, execute component tests, check database side effects, and record defects immediately |
| Medium | Add functional tests for representative scenarios and include regression tests after fixes |
| Low | Use checklist-based review and exploratory testing |

The testing strategy is risk-based. More rigorous techniques are applied to high-risk areas. For the User Account and Authentication Module, the signup workflow uses equivalence partitioning and boundary value analysis. For the Blog Post Management Module, the create post workflow uses source-code-based control flow analysis and branch coverage thinking.

## 3. High-Level Test Plan

This section follows the general structure of an IEEE 829-style test plan.

### 3.1 Test Plan Identifier

Test Plan ID: `FlaskBlog-B3-TP-001`

### 3.2 Introduction

This test plan defines the high-level testing activities for the FlaskBlog project. The purpose is to verify important functional behavior, reduce product risks, and provide evidence for the final project report.

The scope of this test plan covers component-level and route-level tests for selected FlaskBlog modules. It also defines broader test items for the whole project based on the risk analysis.

### 3.3 Test Items

The main test items are:

- User registration module
- User login and logout module
- Account settings module
- Post creation module
- Post editing and post viewing module
- Comment module
- Search and category module
- Admin panel module
- Analytics module
- UI templates and translation files

The detailed component tests in this report focus on:

- `signup` module: `app/routes/signup.py`, `app/utils/forms/SignUpForm.py`
- `login` module: `app/routes/login.py`, `app/utils/forms/LoginForm.py`
- `createPost` module: `app/routes/createPost.py`, `app/utils/forms/CreatePostForm.py`, `app/utils/generateUrlIdFromPost.py`
- `post` module: `app/routes/post.py`, `app/utils/forms/CommentForm.py`, `app/utils/delete.py`

### 3.4 Features to Be Tested

The risk register covers the whole product. The detailed execution scope of this report is narrower and focuses on four selected representative route-level workflows from two high-risk functional areas.

Detailed component tests in this report:

| Feature | Priority | Related risks |
|---|---|---|
| Signup input validation | High | R1, R4 |
| Duplicate username and duplicate email handling | High | R1, R4 |
| Login credential and session behavior | High | R5, R11 |
| Access control for creating posts when the user is not logged in | High | R2, R3 |
| Successful post creation | High | R2 |
| Empty post content handling | Medium | R2 |
| Existing and missing post view behavior | Medium | R6 |
| Comment insertion path inside the post route | Medium | R6, R4 |

Recorded product risks not tested in detail in this report:

| Feature / risk area | Reason for recording | Scope status |
|---|---|---|
| Logout behavior | It affects session state after login but is lower risk than login acceptance/rejection | Future regression-test candidate |
| Post edit and post delete behavior | It affects content integrity and destructive operations | Future regression-test candidate |
| Search by title, tags, author, and username | It affects content discovery but is not part of the selected components | Outside detailed execution scope |
| Admin-only pages and role changes | They require broader role-based access-control testing | Outside detailed execution scope |
| Post analytics recording | It depends on analytics routes and analytics database state | Outside detailed execution scope |
| Basic UI rendering and translation | It is lower risk and better suited to checklist or exploratory testing | Outside detailed execution scope |

### 3.5 Features Not to Be Tested in Detail

The following items are not tested in detail in this report:

- Full browser-based UI compatibility across all devices.
- Logout, post editing, post deletion, and administration workflows beyond the selected access-control check for `/createpost`.
- Search, analytics, and full UI translation behavior.
- SMTP email delivery.
- Real Google reCAPTCHA verification.
- Load testing or stress testing.
- Security penetration testing.
- Complete testing of every language translation file.

These items are excluded because the assignment focuses on component tests for two selected major modules, and because several excluded items require external services or a larger testing environment.

### 3.6 Test Approach

The testing approach combines risk-based testing, black-box testing, and white-box testing.

For the User Authentication area:

- Black-box testing is applied to the signup workflow because it has clear input fields and observable external behavior.
- Black-box testing is also applied to the login workflow because credential acceptance/rejection is externally observable through redirects and session state.
- Equivalence partitioning is used to divide valid and invalid signup inputs and valid/invalid login credentials.
- Boundary value analysis is used for username length, email length, and password length in the signup workflow.
- Database state and Flask session state are checked after submissions.

For the Blog Content Management area:

- White-box testing is applied to the create post workflow because the source code contains clear conditional branches.
- White-box testing is also applied to `post.py` because the route contains post lookup, slug redirection, view-count update, comment insertion, comment deletion, post deletion, analytics, and not-found handling in one function.
- Control flow analysis is used to identify branches.
- The selected tests cover unauthenticated create-post access, logged-in empty content, logged-in valid content, post-view slug handling, existing-post rendering, missing-post behavior, and comment insertion.
- Database state and exceptions are checked to evaluate the result.

### 3.7 Item Pass / Fail Criteria

A test case passes if:

- The actual HTTP status code matches the expected status code.
- The actual redirect target matches the expected redirect target when applicable.
- The database side effect matches the expected state.
- No unexpected exception is raised.

A test case fails if:

- Invalid data is accepted when it should be rejected.
- Valid data is rejected when it should be accepted.
- The database contains incorrect records after test execution.
- An unexpected exception occurs.
- Access control behavior does not match the expected result.

### 3.8 Suspension Criteria and Resumption Requirements

Testing should be suspended if:

- The application cannot be imported or started.
- Required dependencies are unavailable.
- The database schema cannot be created.
- A blocking defect prevents most planned tests from executing.

Testing can resume when:

- Dependencies are installed and importable.
- The test database can be created.
- Blocking defects are fixed or isolated.
- A stable test environment is available again.

### 3.9 Test Deliverables

The test deliverables are:

- This report draft for Parts 1 to 4.
- Component test source code:
  - `app/tests/assignment_b3_bb_signup_tests.py`
  - `app/tests/assignment_b3_bb_login_tests.py`
  - `app/tests/assignment_b3_wb_createpost_tests.py`
  - `app/tests/assignment_b3_wb_post_tests.py`
- Test execution result summary.
- Defect records for discovered failures.

### 3.10 Testing Tasks

| Task | Description |
|---|---|
| Project analysis | Review the FlaskBlog project structure, major modules, configuration, database files, routes, forms, templates, and utilities |
| Risk analysis | Identify product risks, assess likelihood and impact, calculate risk exposure, and prioritize risks |
| Test planning | Define test scope, test items, features to be tested, features not to be tested, approach, environment, and responsibilities |
| Black-box test design | Design equivalence class and boundary value test cases for the User Account and Authentication Module, using the signup workflow as the representative component |
| White-box test design | Analyze source-code branches and design control-flow-based tests for the Blog Post Management Module, using the create post workflow as the representative component |
| Test implementation | Implement automated component tests with Python `unittest`, Flask `test_client`, and temporary SQLite databases |
| Test execution | Run the automated tests, collect pass/fail/error results, and inspect database side effects |
| Defect reporting | Record failed tests, observed behavior, expected behavior, affected source files, impact, and suggested fixes |
| Regression testing | Re-run relevant tests after defects are fixed to confirm that failures are removed and no related behavior is broken |
| Report preparation | Summarize project analysis, risk analysis, test plan, test design, execution results, and defect findings |

### 3.11 Environmental Needs

| Environment item | Requirement |
|---|---|
| Operating system | Windows environment used in this project |
| Python | Python version compatible with the project, as managed by `uv` |
| Dependencies | Flask, Flask-WTF, WTForms, Passlib, and other dependencies from `app/pyproject.toml` |
| Test database | Temporary SQLite databases created during test execution |
| Test command | Run the four focused test files from the `app` directory with `uv run python tests\<file>.py` |

### 3.12 Responsibilities

| Role | Responsibility |
|---|---|
| Test designer | Analyze risks, select test objects, design black-box and white-box tests |
| Test implementer | Implement automated component tests using Flask `test_client` |
| Test executor | Run the tests, collect results, and record failures |
| Defect analyst | Analyze failed tests and map failures to source code defects |

### 3.13 Staffing and Training Needs

| Need | Description |
|---|---|
| Testing knowledge | Testers should understand basic software testing concepts, including risk-based testing, equivalence partitioning, boundary value analysis, and white-box branch coverage |
| Python and Flask knowledge | Testers should be able to read Python code, understand Flask routes, sessions, requests, redirects, and Blueprint registration |
| Database knowledge | Testers should understand basic SQLite operations and how to verify database side effects after test execution |
| Test automation knowledge | Testers should know how to run Python `unittest` tests and interpret pass, fail, and error results |
| Additional training | No special external training is required, but team members should review the relevant lecture materials on risk-based testing, black-box techniques, white-box techniques, and test planning before finalizing the report |

### 3.14 Schedule

| Activity | Estimated order |
|---|---|
| Project structure analysis | Step 1 |
| Risk analysis | Step 2 |
| High-level test planning | Step 3 |
| Signup black-box test design | Step 4 |
| Create post white-box test design | Step 5 |
| Test program implementation | Step 6 |
| Test execution and defect recording | Step 7 |
| Report writing | Step 8 |

### 3.15 Risks and Contingencies

| Project risk | Contingency |
|---|---|
| Dependency installation or `uv` execution problem | Use the existing local virtual environment or install dependencies in a clean environment |
| Existing project databases contain unrelated data | Use temporary SQLite databases for component tests |
| Route functions depend on templates or flash messages | Replace template rendering and flash messages with simple test doubles during component tests |
| External services are unavailable | Disable reCAPTCHA and avoid SMTP delivery in component tests |

### 3.16 Approvals

| Approver | Approval responsibility |
|---|---|
| Project team members | Review whether the selected modules, risk analysis, test plan, test cases, and execution results are correct and complete for submission |
| Test lead / report owner | Confirm that the test plan follows the required structure and that the final report is internally consistent |
| Course instructor / examiner | Final acceptance is subject to the assignment grading process |

For this assignment report, the approval section records the intended review responsibilities. Formal signatures are not required unless requested by the course submission rules.

## 4. Detailed Test Design and Execution Report

### 4.1 Selected Modules

Two major functional areas were selected for detailed component testing. Each area is represented by two route-level workflows.

| Test type | Selected functional area | Selected representative component / workflow | Reason for selection |
|---|---|---|---|
| Black-box testing | User Authentication | Signup workflow; login workflow | Signup is the first point where external users create persistent account data. Login is the gate for authenticated behavior and session creation. Both workflows have clear external inputs and observable outcomes, so they are suitable for equivalence partitioning, boundary value analysis, and credential acceptance/rejection tests. |
| White-box testing | Blog Content Management | Create post workflow; post view/comment workflow | Create post is the core content-production workflow. The `post.py` route handles post lookup, slug redirection, view count update, comments, deletion buttons, analytics, and not-found behavior in one source-level control flow. These workflows directly affect whether users can publish, read, and interact with blog content. |

The assignment requires selected modules rather than exhaustive testing of the whole application. Therefore, this report selects two high-risk functional areas and tests four representative route-level components. Logout, post edit, post delete, administration, search, and analytics are important follow-up workflows, but they are not claimed as fully covered by the current execution.

### 4.2 Selected Test Framework

The selected test framework is Python `unittest` with Flask `test_client`.

Reasons:

- It can test Flask routes without starting a real HTTP server.
- It supports session manipulation, POST forms, redirects, and file uploads.
- It can run fast component tests.
- It works well with temporary SQLite databases.
- It is included in Python's standard library, which reduces additional dependency risk.

The tests are implemented in four focused files:

- `app/tests/assignment_b3_bb_signup_tests.py`
- `app/tests/assignment_b3_bb_login_tests.py`
- `app/tests/assignment_b3_wb_createpost_tests.py`
- `app/tests/assignment_b3_wb_post_tests.py`

The tests are executed with:

```powershell
cd D:\CodeField\FlaskBlog\app
uv run python tests\assignment_b3_bb_signup_tests.py
uv run python tests\assignment_b3_bb_login_tests.py
uv run python tests\assignment_b3_wb_createpost_tests.py
uv run python tests\assignment_b3_wb_post_tests.py
```

### 4.3 General Architecture of the Test Programs

The test program uses the following architecture:

1. Create temporary SQLite databases for the data stores needed by each component, including users, posts, comments, and analytics.
2. Patch the database paths in `settings.py` and the selected route modules.
3. Register only the target Blueprint in a small Flask test application.
4. Replace template rendering, flash messages, point updates, delete utilities, and external visitor-data lookup with test doubles where necessary.
5. Use Flask `test_client` to send GET and POST requests.
6. Inspect HTTP responses, redirects, exceptions, database state, and selected test-double call records.
7. Report passed, failed, and errored test cases through `unittest`.

This architecture isolates the component under test and avoids modifying the real project databases in `app/db`.

### 4.4 Black-Box Test Design and Execution: User Authentication

The User Authentication area is tested with black-box techniques because the main behavior can be observed through submitted form inputs, redirects, session state, and database side effects. Two representative workflows are covered: signup and login.

#### 4.4.1 Signup Workflow

##### Test Object

The selected major module is the User Account and Authentication Module. Within this module, the signup workflow is selected as the representative component for black-box testing because registration is the first step of the user account lifecycle and has clear input/output behavior.

The selected test object includes:

- Route: `app/routes/signup.py`
- Form definition: `app/utils/forms/SignUpForm.py`
- Route URL: `/signup`

Main external inputs:

- `userName`
- `email`
- `password`
- `passwordConfirm`

##### Input Conditions

Based on the form definition and route behavior, the main input conditions are:

- Username should be required and should have length 4 to 25.
- Email should be required and should have length 6 to 50.
- Password should be required and should have length at least 8.
- Password confirmation should be required, should have length at least 8, and should match password.
- Username should contain ASCII characters.
- Username and email should be unique.

For equivalence-class design, `passwordConfirm` is treated mainly as a dependent input whose key condition is whether it matches `password`. Its length requirement is indirectly covered when it is kept equal to the password value in password-length tests.

##### Equivalence Classes

The signup black-box design follows the single-fault assumption. One valid representative input is used as the baseline, and each negative test case changes one invalid input condition while keeping the other fields valid. Therefore, exhaustive Cartesian-product combination testing is not used.

| Input | Valid equivalence classes | Invalid equivalence classes |
|---|---|---|
| Username | ASCII username, length 4-25, not already used | Empty username; length < 4; length > 25; non-ASCII username; duplicate username |
| Email | Valid email format, length 6-50, not already used | Empty email; invalid email format; length < 6; length > 50; duplicate email |
| Password | Length >= 8 | Empty password; length < 8 |
| Password confirmation | Same as password | Different from password |

##### Boundary Values

| Field | Boundary values |
|---|---|
| Username length | 3, 4, 5, 24, 25, 26 |
| Email length | 5, 6, 7, 49, 50, 51 |
| Password length | 7, 8, 9 |
| Password confirmation | Same value as password; different value from password |

The final signup test design combines equivalence partitioning and boundary value analysis. Each negative or boundary-value test changes only one invalid class or one boundary condition while keeping the other fields at normal valid values. The design has 23 single-condition cases plus one fully valid representative case, so there are 24 signup black-box cases in total.

##### Black-Box Test Cases

| Test case ID | Objective | Input | Expected result |
|---|---|---|---|
| BB-01 | Test a valid representative signup | `validuser`, `valid@example.com`, normal valid password | User is inserted and response redirects to home page |
| BB-02 | Test empty username | Empty username with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-03 | Test username length below minimum | Username length 3 with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-04 | Test username length above maximum | Username length 26 with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-05 | Test non-ASCII username | Chinese username with otherwise valid fields | Signup is rejected and no user is inserted |
| BB-06 | Test duplicate username | Existing `validuser`, then submit another `validuser` with a new valid email | Signup is rejected and only one `validuser` exists |
| BB-07 | Test empty email | Empty email with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-08 | Test invalid email format | `bad-email` with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-09 | Test email length below minimum | Email length 5 with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-10 | Test email length above maximum | Email length 51 with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-11 | Test duplicate email | New valid username with an existing valid email | Signup is rejected and no new user is inserted |
| BB-12 | Test empty password | Empty password with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-13 | Test password length below minimum | Password length 7 with otherwise normal valid fields | Signup is rejected and no user is inserted |
| BB-14 | Test mismatched password confirmation | Valid password with different confirmation | Signup is rejected and no user is inserted |
| BB-15 | Test username length at minimum boundary | Username length 4 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-16 | Test username length just above minimum | Username length 5 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-17 | Test username length just below maximum | Username length 24 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-18 | Test username length at maximum boundary | Username length 25 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-19 | Test email length at minimum boundary | Email length 6 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-20 | Test email length just above minimum | Email length 7 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-21 | Test email length just below maximum | Email length 49 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-22 | Test email length at maximum boundary | Email length 50 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-23 | Test password length at minimum boundary | Password length 8 with otherwise valid fields | User is inserted and response redirects to home page |
| BB-24 | Test password length just above minimum | Password length 9 with otherwise valid fields | User is inserted and response redirects to home page |

##### Black-Box Execution Results

The signup black-box test program executed all 24 designed cases.

Execution command:

```powershell
uv run python tests\assignment_b3_bb_signup_tests.py
```

Overall result:

| Total cases | Passed | Failed | Errors | Pass rate |
|---:|---:|---:|---:|---:|
| 24 | 17 | 7 | 0 | 70.8% |

The passed cases are not listed individually in this section because they behaved as expected. The failed cases are shown below because they reveal the main defect in the signup route.

| Test case ID | Test focus | Expected result | Actual result | Verdict |
|---|---|---|---|---|
| BB-03 | Username length below minimum, length 3 | Signup should be rejected and no user should be inserted | User with username `abc` was inserted; assertion showed `1 != 0` | Fail |
| BB-04 | Username length above maximum, length 26 | Signup should be rejected and no user should be inserted | User with length-26 username was inserted; assertion showed `1 != 0` | Fail |
| BB-08 | Invalid email format | Signup should be rejected and no user should be inserted | User with email `bad-email` was inserted; assertion showed `1 != 0` | Fail |
| BB-09 | Email length below minimum, length 5 | Signup should be rejected and no user should be inserted | User with short email was inserted; assertion showed `1 != 0` | Fail |
| BB-10 | Email length above maximum, length 51 | Signup should be rejected and no user should be inserted | User with long email was inserted; assertion showed `1 != 0` | Fail |
| BB-12 | Empty password | Signup should be rejected and no user should be inserted | User with empty password was inserted; assertion showed `1 != 0` | Fail |
| BB-13 | Password length below minimum, length 7 | Signup should be rejected and no user should be inserted | User with short password was inserted; assertion showed `1 != 0` | Fail |

Failure analysis:

All seven failures have the same root cause. The tests expected invalid signup data to be rejected, but the route inserted the submitted user into the database. The failed assertions all compare the number of inserted users against the expected value `0`, but the actual count is `1`.

This indicates that the backend signup route does not enforce the validation rules defined in `SignUpForm.py`. In particular, username length, email format, email length, empty password, and password length rules are not checked before insertion. Some invalid cases, such as empty username, non-ASCII username, duplicate username, empty email, duplicate email, and mismatched password confirmation, were still rejected by other route-level checks or database constraints, but the WTForms validation rules were not consistently applied.

The execution output also shows several `ResourceWarning: unclosed database` messages. These warnings do not change the pass/fail count, but they suggest that some database connections in the route code are not closed consistently.

##### Defect Found by Black-Box Testing

Defect ID: `D-BB-01`

Title: Signup backend does not enforce WTForms validation.

Description:

The signup route creates `SignUpForm(request.form)`, but it does not call `form.validate()` before processing submitted data. As a result, backend validation rules defined in `SignUpForm.py`, such as username length, email length, email format, and password length, are not enforced by the route.

Observed evidence:

- Invalid inputs such as username length 3, username length 26, invalid email format, email length 5, email length 51, empty password, and password length 7 were accepted.
- Invalid users were inserted into the users database.
- The related single-fault tests, including `test_bb03_short_username_is_rejected`, `test_bb08_invalid_email_format_is_rejected`, and `test_bb13_short_password_is_rejected`, failed.

Impact:

Invalid account data can enter the database. This affects data quality, account management, and security assumptions. Frontend validation can also be bypassed, so backend validation is required.

Suggested fix:

Call form validation before inserting the user:

```python
form = SignUpForm(request.form)
if request.method == "POST":
    if not form.validate():
        flashMessage(...)
        return render_template(...)
```

#### 4.4.2 Login Workflow

##### Test Object

The second black-box target in the User Authentication area is the login workflow.

The selected test object includes:

- Route: `app/routes/login.py`
- Form definition: `app/utils/forms/LoginForm.py`
- Route URL: `/login/redirect=<direct>`

##### Input Conditions

The login workflow has two main external inputs:

- `userName`
- `password`

The key behavior is externally observable: valid credentials should create a session and redirect, while invalid credentials should keep the user on the login page without creating `session["userName"]`.

The form definition also includes length rules for username and password:

- Username should be required and should have length 4 to 25.
- Password should be required and should have length at least 5.

##### Login Equivalence Classes

The login black-box design follows the single-fault assumption. One valid existing account is used as the baseline, and each negative test case changes one main invalid input condition while keeping the other input condition valid where possible.

| Input | Valid equivalence classes | Invalid equivalence classes |
|---|---|---|
| Username | Existing username, length 4-25 | Empty username; length < 4; length > 25; unknown username |
| Password | Provided password, length >= 5, matching the account | Empty password; length < 5; wrong password |

The observable output condition is whether the login creates `session["userName"]`. Valid credentials should create the session and redirect, while invalid or incomplete credentials should not create a user session.

##### Login Invalid Boundary Values

| Field | Boundary values |
|---|---|
| Username length | 3, 4, 5, 20, 24, 25, 26 |
| Password length | 4, 5, 6, 10 |

The login test design uses one fully valid baseline case to cover a normal existing username with length 20 and a matching password with length 10. The remaining cases change one username or password equivalence class / boundary value at a time. Therefore, the login workflow has 14 black-box test cases in total: 1 valid baseline case, 8 additional username cases, and 5 additional password cases.

##### Black-Box Login Test Cases

| Test case ID | Objective | Input | Expected result |
|---|---|---|---|
| BB-Login-01 | Valid credentials baseline | Existing username with length 20, matching password with length 10 | Login succeeds, `session["userName"]` is set, and response redirects |
| BB-Login-02 | Empty username | Empty username with otherwise valid password | Login is rejected and no user session is created |
| BB-Login-03 | Username length below minimum | Username with length 3 and otherwise valid password | Login is rejected and no user session is created |
| BB-Login-04 | Username length at minimum boundary | Existing username with length 4 and matching password | Login succeeds, `session["userName"]` is set, and response redirects |
| BB-Login-05 | Username length just above minimum | Existing username with length 5 and matching password | Login succeeds, `session["userName"]` is set, and response redirects |
| BB-Login-06 | Username length just below maximum | Existing username with length 24 and matching password | Login succeeds, `session["userName"]` is set, and response redirects |
| BB-Login-07 | Username length at maximum boundary | Existing username with length 25 and matching password | Login succeeds, `session["userName"]` is set, and response redirects |
| BB-Login-08 | Username length above maximum | Username with length 26 and otherwise valid password | Login is rejected and no user session is created |
| BB-Login-09 | Unknown username | Non-existing username with otherwise valid password | Login is rejected and no user session is created |
| BB-Login-10 | Empty password | Existing username with empty password | Login is rejected and no user session is created |
| BB-Login-11 | Password length below minimum | Existing username with password length 4 | Login is rejected and no user session is created |
| BB-Login-12 | Password length at minimum boundary | Existing username with matching password length 5 | Login succeeds, `session["userName"]` is set, and response redirects |
| BB-Login-13 | Password length just above minimum | Existing username with matching password length 6 | Login succeeds, `session["userName"]` is set, and response redirects |
| BB-Login-14 | Wrong password | Existing username with wrong password | Login is rejected and no user session is created |

##### Black-Box Login Execution Results

The login black-box test program executed all 14 designed cases.

Execution command:

```powershell
uv run python tests\assignment_b3_bb_login_tests.py
```

Overall result:

| Total cases | Passed | Failed | Errors | Pass rate |
|---:|---:|---:|---:|---:|
| 14 | 14 | 0 | 0 | 100.0% |

Failed test cases:

No failed test cases were observed in the login black-box test execution. The passed cases are not listed individually here because all designed login inputs behaved as expected.

Failure analysis:

No login failure needed root-cause analysis in this execution. The result indicates that the tested login route correctly accepted valid existing credentials, rejected empty or invalid credentials, rejected unknown users and wrong passwords, and set `session["userName"]` only for successful login attempts.

### 4.5 White-Box Test Design and Execution: Blog Content Management

The Blog Content Management area is tested with white-box techniques because its route functions contain explicit source-level branches for authentication, request method, post lookup, redirects, database writes, and exceptional paths. Two representative workflows are covered: create post and post view/comment handling.

##### White-Box Design Method and Coverage Criteria

The white-box test cases were designed by reading the source code and constructing a control-flow view of each selected route function. The analysis focuses on executable statements, decision points, early returns, database writes, and exception-prone paths.

The main design principle is to identify feasible paths first, and then use those paths to cover important conditions. This is necessary because Flask routes often return immediately after redirects, deletion actions, not-found handling, or errors, so exhaustive path coverage would include many impossible or low-value combinations.

Therefore, the coverage target is representative feasible path coverage, supported by statement and branch coverage where practical. The tests cover key decisions such as authentication state, request method, post existence, slug correctness, delete-button handling, comment submission, analytics enabled/disabled behavior, session username presence, and visitor-data success or failure.

Based on this method, `createPost.py` is tested with four feasible paths, while `post.py` is tested with ten representative feasible paths covering its main control-flow responsibilities.

#### 4.5.1 Create Post Workflow

##### Test Object

The selected functional area is Blog Content Management. Within this area, the create post workflow is selected as a representative white-box component because it is a core post management operation and contains important conditional branches.

The selected test object includes:

- Route: `app/routes/createPost.py`
- Form definition: `app/utils/forms/CreatePostForm.py`
- URL ID helper: `app/utils/generateUrlIdFromPost.py`
- Route URL: `/createpost`

##### Control Flow Analysis

The `createPost()` function has the following main control flow:

1. Check whether `userName` exists in session.
2. If the user is not logged in, redirect to the login page.
3. If the user is logged in, create the post form.
4. If the request method is GET, render the create post page.
5. If the request method is POST, read title, tags, content, banner, and category.
6. If `postContent == ""`, show an error message and do not insert a post.
7. If `postContent != ""`, insert a new post into the posts database, add points, show a success message, and redirect to the home page.

##### Coverage Objective

The coverage objective for `createPost.py` is to cover the main feasible paths through the route and the key decisions that control whether a user can create a post. The tests focus on authentication, request method, and post-content validation:

- Not logged in branch.
- Logged in and GET rendering branch.
- Logged in and empty post content branch.
- Logged in and valid post content branch.

These four cases cover the main executable statements, both outcomes of the authentication decision (`"userName" in session`), both outcomes of the request-method decision (`request.method == "POST"`), and both outcomes of the content decision (`postContent == ""`). This gives branch coverage for the main business decisions and representative feasible path coverage for the whole route. The tests do not attempt to cover every invalid form-field combination, such as missing form keys or missing uploaded files, because the objective is route-level control-flow coverage rather than exhaustive form validation testing.

##### White-Box Test Cases

| Test case ID | Covered branch | Preconditions | Input | Expected result |
|---|---|---|---|---|
| WB-Create-01 | User not logged in | No `userName` in session | GET `/createpost` | Redirect to `/login/redirect=&createpost` |
| WB-Create-02 | Logged in, GET request | `userName=alice` in session | GET `/createpost` | Create post page is rendered |
| WB-Create-03 | Logged in, POST, empty content | `userName=alice` in session | POST with empty `postContent` | No post is inserted; create page is returned |
| WB-Create-04 | Logged in, POST, valid content | `userName=alice` in session | POST with valid title, tags, content, banner, and category | Post is inserted and response redirects to home page |

##### White-Box Execution Results

Representative white-box tests were executed using the implemented test program.

Execution command:

```powershell
uv run python tests\assignment_b3_wb_createpost_tests.py
```

Overall result:

| Total cases | Passed | Failed | Errors | Pass rate |
|---:|---:|---:|---:|---:|
| 4 | 3 | 0 | 1 | 75.0% |

The passed cases are not listed individually in this section because they behaved as expected. The error case is shown below because it reveals the main defect in the create-post route.

| Test case ID | Test focus | Expected result | Actual result | Verdict |
|---|---|---|---|---|
| WB-Create-04 | Logged-in user submits a valid post | The post should be inserted and the response should redirect to the home page | `TypeError: generateurlID() takes 0 positional arguments but 1 was given` | Error |

Failure analysis:

The failed execution has one direct cause. The successful create-post branch calls `generateurlID(postTitle)`, but the helper function is defined without parameters. Therefore, the route crashes before the database insertion and redirect can complete. This prevents a valid logged-in user from publishing a post through the tested path.

##### Defect Found by White-Box Testing

| Field | Detail |
|---|---|
| Defect ID | `D-WB-01` |
| Title | Valid create post workflow crashes because of incorrect `generateurlID` call |
| Description | In `app/routes/createPost.py`, the successful post creation branch calls `generateurlID(postTitle)`. However, in `app/utils/generateUrlIdFromPost.py`, the function is defined as `def generateurlID():` with no positional arguments. Therefore, a logged-in user submitting a valid post with non-empty content triggers a `TypeError`. |
| Observed evidence | Test case `test_wb_create_04_valid_input_inserts_post` raised `TypeError: generateurlID() takes 0 positional arguments but 1 was given`. The successful post creation branch could not complete. |
| Impact | Critical defect in the core post publishing workflow. A normal logged-in user cannot successfully publish a valid post through the tested path. |
| Suggested fix | Since `generateurlID()` currently generates a random unique ID and does not use the post title, change the call to `generateurlID()`. Alternatively, if the intended design is to generate an ID from the title, redesign the helper function to accept `postTitle` explicitly. Based on existing code, the direct fix is to remove the unnecessary argument. |

#### 4.5.2 Post View and Comment Workflow

##### Test Object

The second white-box target in the Blog Content Management area is the `post.py` route. Although the user-facing purpose is "view post", the route also contains slug normalization, view-count update, comment insertion, comment deletion, post deletion, analytics handling, and not-found handling. Therefore, it is a useful representative component for source-code-based control-flow testing.

The selected test object includes:

- Route: `app/routes/post.py`
- Form definition: `app/utils/forms/CommentForm.py`
- Deletion utility: `app/utils/delete.py`
- Route URLs: `/post/<urlID>` and `/post/<slug>-<urlID>`

##### Control Flow Analysis

The `post()` function has the following main control flow:

1. Read the `urlID` from the route and query the posts database.
2. If no post exists, render the not-found page. In the current implementation, this intended branch is exception-prone because `posts` can be `None`.
3. If the post exists but the slug is missing or incorrect, redirect to the canonical slug URL.
4. If the post exists and the slug is correct, load the full post record.
5. Increment the post view count.
6. If the request method is POST and contains `postDeleteButton`, delete the post and redirect.
7. If the request method is POST and contains `commentDeleteButton`, delete the comment and redirect.
8. If the request method is POST and contains a normal comment, insert the comment and redirect.
9. If the request method is GET, load comments.
10. If analytics is enabled, record visitor analytics when visitor data is available; otherwise skip analytics or log the failure.
11. Render the post page.

##### Coverage Objective

The coverage objective for `post.py` is to cover the main feasible paths through the route and the key conditions that control post viewing, canonical URL redirection, view updates, comment handling, deletion actions, and analytics recording. The route has more branches than `createPost.py`, and several branches return immediately. For this reason, exhaustive combination coverage is not practical or necessary for this component-level report. The selected design instead targets representative feasible path coverage, supported by statement, branch, and condition coverage for the most important decisions.

The ten designed paths cover:

- Both outcomes of post existence: existing post and missing post.
- Both outcomes of slug validation: missing/wrong slug and correct slug.
- Both outcomes of request method: GET and POST.
- POST sub-branches for post deletion, comment deletion, and normal comment insertion.
- Both outcomes of login-dependent comment behavior: logged-in user and missing session user.
- Both outcomes of analytics configuration: analytics disabled and analytics enabled.
- Analytics success and analytics failure behavior.

The ten cases do not cover every possible edge case. For example, they do not separately test a wrong non-empty slug versus a missing slug, a POST request with no delete button and no `comment` field, a comment-delete request with a missing `commentID`, empty comment text, or unauthorized deletion attempts. These are useful follow-up regression or robustness tests, but they are outside the selected representative path set.

##### White-Box Post Test Cases

| Test case ID | Covered branch | Preconditions | Input | Expected result |
|---|---|---|---|---|
| WB-Post-01 | Missing post path | No post with `urlID=missing` exists | GET `/post/missing` | Not-found page is rendered |
| WB-Post-02 | Existing post, missing or incorrect slug | Post with `urlID=abc123` exists | GET `/post/abc123` | Redirect to canonical slug URL |
| WB-Post-03 | Existing post, correct slug, normal GET, analytics disabled | Post with `urlID=abc123` exists; analytics disabled | GET `/post/valid-blog-title-abc123` | Post page is rendered and views increase |
| WB-Post-04 | Post deletion branch | Logged-in user; post exists; user is allowed to delete | POST with `postDeleteButton` | Delete utility is called and response redirects to home page |
| WB-Post-05 | Comment deletion branch | Logged-in user; post and comment exist | POST with `commentDeleteButton` and `commentID` | Comment delete utility is called and response redirects |
| WB-Post-06 | Logged-in normal comment submission | Logged-in user `alice`; post exists | POST with `comment` | Comment is inserted and response redirects |
| WB-Post-07 | Comment submission without logged-in user | No `userName` in session; post exists | POST with `comment` | Request should be rejected or handled safely; current code may raise a session-related error |
| WB-Post-08 | Analytics enabled, logged-in visitor, visitor data success | Logged-in user; analytics enabled; IP/user-agent data returns success | GET correct slug URL | Analytics row is inserted with the logged-in username |
| WB-Post-09 | Analytics enabled, anonymous visitor, visitor data success | No `userName` in session; analytics enabled; IP/user-agent data returns success | GET correct slug URL | Analytics row is inserted with `unsignedUser` |
| WB-Post-10 | Analytics enabled, visitor data failure | Analytics enabled; IP/user-agent data returns failure | GET correct slug URL | Analytics insertion is skipped and page rendering should still complete |

##### White-Box Post Execution Results

The automated execution now covers all ten designed post paths.

Execution command:

```powershell
uv run python tests\assignment_b3_wb_post_tests.py
```

Overall result:

| Total cases | Passed | Failed | Errors | Pass rate |
|---:|---:|---:|---:|---:|
| 10 | 8 | 0 | 2 | 80.0% |

The passed cases are not listed individually in this section because they behaved as expected. The error cases are shown below because they identify the main unsafe paths in `post.py`.

| Test case ID | Test focus | Expected result | Actual result | Verdict |
|---|---|---|---|---|
| WB-Post-01 | Missing post URL | The not-found page should be rendered | `TypeError: argument of type 'NoneType' is not iterable` | Error |
| WB-Post-07 | Anonymous comment submission | The request should be rejected or handled safely without inserting a comment | `KeyError: 'userName'` | Error |

Failure analysis:

The main failure reason is that `post.py` uses route data before checking whether the required object or session value exists. In `WB-Post-01`, the database query returns `None`, but the route still evaluates `str(urlID) in posts`, which raises a `TypeError`. In `WB-Post-07`, the route reads `session["userName"]` during comment insertion without first checking whether the user is logged in, which raises a `KeyError`. Both errors show that the route needs guard checks before using optional database results or session keys.

##### Defect Found by Post White-Box Testing

| Field | Detail |
|---|---|
| Defect ID | `D-WB-02` |
| Title | Missing post route crashes before rendering the not-found page |
| Description | In `app/routes/post.py`, the route queries `cursor.execute("select urlID, title from posts where urlID = ?", (urlID,))` and `posts = cursor.fetchone()`. If no matching post exists, `posts` is `None`. The next condition `if str(urlID) in posts:` attempts to iterate over `None` and raises a `TypeError`. |
| Observed evidence | Test case `test_wb_post_01_missing_post_renders_not_found_page` raised `TypeError: argument of type 'NoneType' is not iterable`. |
| Impact | Users who open a missing or invalid post URL receive a server error instead of the expected not-found page. This affects reliability and user-facing error handling for the blog content module. |
| Suggested fix | Check for `None` before testing membership: `if posts and str(urlID) in posts:` ... `else: return render_template("notFound.html")` |

##### Additional Defect Found by Post White-Box Testing

| Field | Detail |
|---|---|
| Defect ID | `D-WB-03` |
| Title | Comment submission without a logged-in user crashes with a session key error |
| Description | In the normal comment submission branch of `app/routes/post.py`, the route inserts the comment using `session["userName"]`. However, the route does not first check whether `"userName"` exists in the session. If an unauthenticated user submits a POST request with a `comment` field, the route raises `KeyError: 'userName'` instead of rejecting the request safely or redirecting the user to login. |
| Observed evidence | Test case `test_wb_post_07_comment_without_login_is_handled_safely` raised `KeyError: 'userName'`. No safe rejection or login redirect was returned. |
| Impact | An unauthenticated comment submission can crash the post route. This affects reliability and access-control behavior for comments. |
| Suggested fix | Check the session before inserting a comment: `if "userName" not in session:` → `flashMessage(...)`; `return redirect(url_for("login.login", direct="..."))` |

### 4.6 Test Execution Summary

The component test programs were executed with:

```powershell
cd D:\CodeField\FlaskBlog\app
uv run python tests\assignment_b3_bb_signup_tests.py
uv run python tests\assignment_b3_bb_login_tests.py
uv run python tests\assignment_b3_wb_createpost_tests.py
uv run python tests\assignment_b3_wb_post_tests.py
```

Execution summary:

| Total tests | Passed | Failed | Errors |
|---:|---:|---:|---:|
| 52 | 42 | 7 | 3 |

Detailed result:

| Test file | Result summary | Meaning |
|---|---|---|
| `assignment_b3_bb_signup_tests.py` | 24 tests; 17 passed, 7 failed | Signup accepts several invalid values because backend WTForms validation is not enforced; valid boundary values are accepted |
| `assignment_b3_bb_login_tests.py` | 14 tests; all passed | Login accepts valid credentials and rejects wrong, unknown, empty, and invalid-length credential inputs; username and password boundary values are covered |
| `assignment_b3_wb_createpost_tests.py` | 4 tests; 3 passed, 1 error | Valid create-post path crashes because `generateurlID` is called with an argument |
| `assignment_b3_wb_post_tests.py` | 10 tests; 8 passed, 2 errors | Missing-post path crashes because `posts` is `None`; unauthenticated comment submission crashes because `session["userName"]` is missing |

### 4.7 Conclusion for Parts 1 to 4

The first four required parts of the assignment have been completed for FlaskBlog. The project was analyzed in terms of background, goals, requirements, architecture, and components. A risk analysis was performed and used to prioritize high-risk areas. A high-level test plan was created using an IEEE 829-style structure. Finally, two major modules were selected for detailed component testing:

- User Authentication area for black-box testing, using signup and login as representative workflows.
- Blog Content Management area for white-box testing, using create post and post view/comment handling as representative workflows.

The testing process found important defects:

- The signup route does not enforce backend form validation.
- The create post route crashes on the valid post creation path because it calls `generateurlID` with an invalid argument.
- The post view route crashes on missing post URLs because it tests membership on `None` before rendering the not-found page.
- The post comment branch crashes when an unauthenticated request submits a comment because it reads `session["userName"]` without checking the session first.

These findings are directly related to high-priority product risks and should be included in the final defect discussion and regression testing plan.

## 5. Use of Artificial Intelligence

To be added by the team.

## 6. Ethical Considerations

To be added by the team.

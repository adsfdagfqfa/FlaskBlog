# Assignment B3

## 1 **Introduction to the Implemented Software Project**** \(高\)**

### 1\.1 **Project Background**

FlaskBlog is a blog web application built with Python's Flask framework\. It provides a complete blogging platform where users can register, log in, publish posts, browse posts, comment on posts, search content, and manage account settings\. The project also includes administration functions for managing users, posts, and comments\.

The project targets personal blogs or small content publishing platforms\. Its design is lightweight and practical: Flask for routing and request handling, SQLite for persistent storage, WTForms for form definition, Jinja2 templates for server\-side HTML rendering, and TailwindCSS for front\-end styling\.

### 1\.2 **General Goals of the Project**

FlaskBlog set out to cover:

- The full blogging cycle — user registration, authentication, post creation, post reading, and commenting\.

- Basic admin management of users, posts, and comments\.

- A clean, responsive interface with light and dark themes\.

- Multiple interface languages through translation files\.

- Basic post analytics — view counts, visitor information, operating systems, and reading duration\.

- Standard web security practices — password hashing, session\-based authentication, CSRF protection, and optional reCAPTCHA\.

### 1\.3 **Major Functional Requirements**

|Functional Area|Main Requirements|Key Source Files|
|---|---|---|
|User authentication|Register, log in, log out, reset password, verify identity|`app/routes/signup.py`, `app/routes/login.py`, `app/routes/logout.py`, `app/routes/passwordReset.py`, `app/routes/verifyUser.py`|
|User account management|Profile page, account settings, change username/password/profile picture|`app/routes/user.py`, `app/routes/accountSettings.py`, `app/routes/changeUserName.py`, `app/routes/changePassword.py`, `app/routes/changeProfilePicture.py`<br>|
|Blog content management|Home page, create/view/edit/delete posts, comments, post URL ID / slug generation|`app/routes/index.py`, `app/routes/createPost.py`, `app/routes/post.py`, `app/routes/editPost.py`, `app/routes/dashboard.py`, `app/utils/delete.py`, `app/utils/generateUrlIdFromPost.py`|
|Search and categories|Search posts and users by keyword; browse posts by category|`app/routes/search.py`, `app/routes/searchBar.py`, `app/routes/category.py`|
|Administration|View and manage users, posts, comments; change user roles|`app/routes/adminPanel.py`, `app/routes/adminPanelUsers.py`, `app/routes/adminPanelPosts.py`, `app/routes/adminPanelComments.py`|
|Analytics|Record post views, visitor info, operating systems, time spent|`app/routes/postsAnalytics.py`, `app/routes/returnPostAnalyticsData.py`, `app/utils/getAnalyticsPageData.py`|

### 1\.4 **Major Non\-Functional Requirements**

|Quality Area|Project Requirements|Related Risks|
|---|---|---|
|Security|Passwords should be hashed; authenticated pages should require valid sessions; CSRF protection should be enabled; reCAPTCHA can be enabled for login and signup|Validation and authorization are distributed across individual route functions — easy to miss a check|
|Reliability|Core user and post workflows should work consistently without crashing on normal inputs|Route functions directly perform database operations, so exceptions may interrupt main workflows|
|Usability|The web interface should be responsive, understandable, visually consistent, and easy to navigate|If backend validation and UI validation are inconsistent, users may receive confusing behavior |
|Internationalization and UI quality|The system should provide translated interface text, support multiple languages, support dark/light presentation, and keep templates, CSS, and JavaScript consistent across pages|Translation gaps, inconsistent theme behavior, or inconsistent layout may reduce usability for different users|
|Maintainability|Code should be modular and easy to test|Business logic, database access, and template rendering are mixed in route functions|
|Testability|Components should be testable with their isolated test data|Global configuration and database paths must be patched during testing to avoid polluting production\-like databases|
|Performance|Common pages should respond in acceptable time|Multiple SQLite queries and repeated connection opens per request may become a bottleneck|

### 1\.5 **Software Architecture and Major Components**

FlaskBlog follows a lightweight Flask architecture based on routes, templates, forms, utility modules, and SQLite databases\.

|Component|Description|
|---|---|
|Entry point|`app/app.py` creates the Flask application, sets up CSRF protection, registers context processors and error handlers, and mounts all Blueprints\.|
|Configuration|`app/settings.py` holds application name, version, host/port, database paths, SMTP settings, default admin credentials, and reCAPTCHA settings|
|Routes<br>|`app/routes/*.py` contains route functions for user actions, post actions, search, categories, administration, and analytics\.|
|Forms|`app/utils/forms/*.py` defines WTForms classes for signup, login, password reset, post creation, comments, account changes\.|
|Utility modules|`app/utils/*.py` provides helper functions for logging, timestamps, user points, deletion, profile pictures, post URL ID, analytics, and translations|
|Data storage<br>|`app/db/*.db` contains SQLite databases for users, posts, comments, and analytics\. `app/utils/dbChecker.py` creates required database tables when the application starts\.|
|Presentation layer|`app/templates/tailwindUI` for Jinja templates; `app/static/tailwindUI` for CSS and JavaScript assets|

The architecture is easy to follow but has a recurring structural pattern: many route functions combine request parsing, input validation, authorization, database access, business logic, and response rendering\. This makes the system easy to build but also increases the chance of logic defects in complex workflows\.



## 2 Risk Analysis Report** \(高\)**

### 2\.1 Objective and Scope

The objective of this risk analysis is to identify, assess, and prioritize the main product risks of FlaskBlog, so that the testing effort can focus on the most important and failure\-prone areas\. The risk analysis is also used as the basis for the high\-level test plan and for selecting the two modules used in detailed component testing\.

In scope:

- User registration, login, and session handling

- Post creation, viewing, and management

- Database integrity across users, posts, comments, and analytics

- Authorization on restricted pages and admin functions

- Search, category browsing, and analytics features

- Web application concerns: input validation, error handling, external services, and usability

Out of scope:

- Project management risks \(team availability, schedule delay, communication issues\)

- Full penetration testing or formal security auditing

- Load testing, stress testing, and large\-scale performance benchmarking

- Full compatibility testing across all browsers and devices

- Live external service reliability \(SMTP delivery, Google reCAPTCHA\)

### 2\.2 **Risk Identification Method**

Risks were identified from multiple overlapping sources to avoid single\-viewpoint blind spots:

|Source|How It Was Used|
|---|---|
|Requirements and README|The feature list was mapped to major user\-visible functions。|
|Architecture review<br>|`app.py` and Blueprint registration were reviewed to understand major components and dependencies。|
|Source code inspection<br>|Route functions, form classes, utility functions, and database helper code were inspected to identify validation, authorization, database, and exception\-handling risks\.|
|Database structure|SQLite table schemas were reviewed to identify data integrity and persistence risks\.|
|Workflow tracing|Typical workflows were traced, including signup, login, create post, view post, comment, search, and admin management\.|
|Exploratory analysis|Suspicious branches and failure\-prone paths were identified through manual code reading and small route\-level tests\.|
|Web application checklist|Common web application risk areas were considered, including input validation, authentication, authorization, session state, CRUD operations, file upload, external services, error handling, and usability\.|

### 2\.3 Assessment Method

The risk assessment uses a qualitative risk\-based testing approach\. Each risk is rated by two factors: **Likelihood** \(how probable the failure is\) and **Impact** \(how serious the consequence would be if it occurred\)\. Both factors are rated on a 1 to 5 scale\.

|Score|Likelihood|Impact|
|---|---|---|
|1|Very unlikely|Negligible|
|2|Unlikely|Minor|
|3|Possible|Moderate|
|4|Likely|Significant|
|5|Very likely|Severe|

Risk exposure is calculated as: `Risk Exposure = Likelihood x Impact`

|Exposure Range|Level|
|---|---|
|1–6|Low|
|7–12|Medium|
|13–25|High|

### 2\.4 Product Risk Register

|ID|Category|Risk|Affected Area|L|I|Level|Test Focus|
|---|---|---|---|---|---|---|---|
|R1|Input validation<br>|Signup may accept malformed or incomplete data if WTForms rules are not enforced on the backend|`signup.py`, `SignUpForm.py`,  users database<br>|4|4|High|Apply equivalence partitioning and boundary value analysis to username, email, password, confirmation, and duplicate data|
|R2|Core workflow|Valid logged\-in users may be unable to create posts due to validation gaps, helper errors, or database insertion failures|`createPost.py`, `CreatePostForm.py`, `generateUrlIdFromPost.py`, posts database|4|5|High|Use white\-box tests for unauthenticated access, empty content, valid content insertion, and helper/database paths|
|R3|Access control|Restricted routes may have incomplete session or role checks, allowing unauthorized access|Create post, dashboard, edit, delete, admin panel|3|5|High|Test session\-based access control for the create post workflow; Record role\-based admin and delete permissions as broader product risks for future testing|
|R4|Data integrity|Duplicate or malformed records of users or posts may affect later login, display, search, admin behavior|Signup, login, posts, comments<br>|3|4|Medium|Check database side effects after valid, invalid, and duplicate submissions|
|R5|Login and session|Valid users may fail to log in, wrong credentials may be accepted, or session may not be set correctly|`login.py`, users database, Flask session|4|4|High|Apply black\-box tests for valid login, wrong password, and unknown user behavior|
|R6|Post and comment reliability|Viewing an existing or missing post may fail, views may be updated incorrectly, or comment\-related branches may crash due to route\-level assumptions|`post.py`, posts database, comments database<br>|3|4|Medium|Apply white\-box tests for existing post, missing post, slug redirect, and comment insertion branches|
|R7|Destructive actions|Delete and role\-change operations may affect the wrong user or content if delete cascades or role checks are incomplete|Admin panel, dashboard, delete utilities|2|5|Medium|Record as a medium\-priority follow\-up area; Deletion tests are not part of the current detailed execution|
|R8|Usability and internationalization<br>|Multi\-language and theme features may show inconsistent UI text across pages<br>|Translation and templates|2|2|Low|Perform usability checks on selected languages and pages<br>|
|R9|External dependency|External services may fail or be misconfigured|SMTP, reCAPTCHA, profile picture service|3|3|Medium|Use configuration\-based tests and mock external services where possible|
|R10|Resource management|Routes that open SQLite connections directly may leave transactions or connections in an uncertain state when exceptions occur|Signup, login, create post, edit, delete|3|3|Medium|Consider through white\-box review; Direct automated resource assertions are outside the current execution |
|R11|Credential security|Passwords may be stored in a format that violates security expectations|Signup, login, users database|2|5|Medium|Check stored values differ from raw input after signup; Deeper security testing is outside scope|
|R12|Search correctness|Search results may be incomplete or inconsistent across title, tags, author, username queries|Search route|3|3|Medium|Record for future tests outside the detailed component\-test scope|
|R13|Analytics correctness|Post analytics may record incorrect visitor, country, operating\-system, or time\-spent data|Analytics routes and analytics database|3|3|Medium|Record for future tests outside the detailed component\-test scope|

### 2\.5 Risk Prioritization

The four highest\-priority risks are R1, R2, R3, and R5\. They rank at the top because they affect the main user journey end\-to\-end:

1. A user must be able to register with valid data, and invalid information must be rejected\.

2. A logged\-in user must be able to publish a post successfully\.

3. Unauthenticated or unauthorized users must not access restricted functions\.

4. A registered user must be able to log in only with correct credentials and receive a working session\.

|Level|Exposure Range|Count|IDs|Testing implication|
|---|---|---|---|---|
|High|13–25|4|R1, R2, R3, R5|Must be prioritized by systematic test design and early representative execution|
|Medium|7–12|8|R4, R6, R7, R9, R10, R11, R12, R13|Should be covered by representative functional, integration, or review\-based tests|
|Low|1–6|1|R8|Can be covered by checklist\-based review and exploratory usability checks|

The detailed component tests planned for this assignment therefore focus on: **User Authentication** \(signup and login, addressing R1, R4, R5, R11\) and **Blog Content Management** \(create post and post view/comment, addressing R2, R3, R6\)\.

### 2\.6 Risk\-to\-Test Traceability

|Risk|Focus|Selected Component|Test Design|Status|
|---|---|---|---|---|
|R1|Invalid signup accepted|Signup workflow|BB\-01 to BB\-14|Covered; defect found|
|R2|Post creation fails|Create post workflow|WB\-Create\-01 to WB\-Create\-04|Covered; defect found|
|R3|Unauthorized access|Create post access check|WB\-Create\-01|Partially covered for `/createpost`|
|R4|Duplicate/malformed data|Signup DB assertions|Duplicate and invalid\-input cases|Partially covered|
|R5|Login accepts wrong credentials|Login workflow|BB\-Login\-01 to BB\-Login\-03|Covered|
|R6|Post view crashes|Post view workflow|WB\-Post\-01 to WB\-Post\-04|Covered; defect found|
|R7|Destructive actions|Admin and delete routes|Not selected|Follow\-up|
|R10|SQLite connection leaks|Signup, create post routes|White\-box review|Not directly automated|
|R11|Password storage|Signup/login workflow|DB assertion after signup|Follow\-up|

### 2\.7 Mitigation Strategy

|Risk Level|Strategy|
|---|---|
|High|Design systematic test cases, execute component tests, verify DB side effects, record defects immediately|
|Medium|Cover representative scenarios with functional or integration tests; add regression tests after fixes|
|Low|Checklist\-based review and exploratory testing|



## 3 High\-Level Test Plan \(徐\)

### 3\.1 **Test Plan Identifier**

Test Plan ID: `FlaskBlog-B3-TP-001`

### 3\.2 **Introduction**

This test plan defines the high\-level testing activities for the FlaskBlog project\. The purpose is to verify important functional behavior, reduce product risks, and provide evidence for the final project report\.

The scope of this test plan covers component\-level and route\-level tests for selected FlaskBlog modules\. It also defines broader test items for the whole project based on the risk analysis\.

### 3\.3 **Test Items**

The main test items are:

1. User registration module

2. User login and logout module

3. Account settings module

4. Post creation module

5. Post editing and post viewing module

6. Comment module

7. Search and category module

8. Admin panel module

9. Analytics module

10. UI templates and translation files

The detailed component tests in this report focus on:

- `signup` module: `app/routes/signup.py`, `app/utils/forms/SignUpForm.py`

- `login` module: `app/routes/login.py`, `app/utils/forms/LoginForm.py`

- `createPost` module: `app/routes/createPost.py`, `app/utils/forms/CreatePostForm.py`, `app/utils/generateUrlIdFromPost.py`

- `post` module: `app/routes/post.py`, `app/utils/forms/CommentForm.py`, `app/utils/delete.py`

### 3\.4 **Features to Be Tested**

The risk register covers the whole product\. But the detailed execution scope of this report is narrower and focuses on four selected representative route\-level workflows from two high\-risk functional areas\.

Detailed component tests in this report:

|Feature|Priority|Related risks|
|---|---|---|
|Signup input validation|High|R1, R4|
|Duplicate username and duplicate email handling|High|R1, R4|
|Login credential and session behavior|High|R5, R11|
|Access control for creating posts when the user is not logged in|High|R2, R3|
|Successful post creation|High|R2|
|Empty post content handling|Medium|R2|
|Existing and missing post view behavior|Medium|R6|
|Comment insertion path inside the post route|Medium|R6, R4|

Recorded product risks not tested in detail in this report:

|Feature|Reason for recording|Scope status|
|---|---|---|
|Logout behavior|It affects session state after login but is lower risk than login acceptance/rejection\.|Future regression\-test candidate|
|Post edit and post delete behavior|It affects content integrity and destructive operations\.|Future regression\-test candidate|
|Search by title, tags, author, and username|It affects content discovery but is not part of the selected components\.|Outside detailed execution scope|
|Admin\-only pages and role changes|They require broader role\-based access\-control testing\.<br>|Outside detailed execution scope|
|Post analytics recording|It depends on analytics routes and analytics database state\.|Outside detailed execution scope|
|Basic UI rendering and translation|It is lower risk and better suited to checklist or exploratory testing|Outside detailed execution scope|

### 3\.5 **Features Not to Be Tested in Detail**

The following items are not tested in detail in this report:

1. Full browser\-based UI compatibility across all devices\.

2. Logout, post editing, post deletion, and administration workflows beyond the selected access\-control check for `/createpost`\.

3. Search, analytics, and full UI translation behavior\.

4. SMTP email delivery\.

5. Real Google reCAPTCHA verification\.

6. Load testing or stress testing\.

7. Security penetration testing\.

8. Complete testing of every language translation file\.

These items are excluded because the assignment focuses on component tests for two selected major modules, and because several excluded items require external services or a larger testing environment\.

### 3\.6 **Test Approach**

The testing approach combines risk\-based testing, black\-box testing, and white\-box testing\.

For the User Authentication area:

- Black\-box testing is applied to the signup workflow because it has clear input fields and observable external behavior\.

- Black\-box testing is also applied to the login workflow because credential acceptance/rejection is externally observable through redirects and session state\.

- Equivalence partitioning is used to divide valid and invalid signup inputs and valid/invalid login credentials\.

- Boundary value analysis is used for username length, email length, and password length in the signup workflow\.

- Database state and Flask session state are checked after submissions\.

For the Blog Content Management area:

- White\-box testing is applied to the create post workflow because the source code contains clear conditional branches\.

- White\-box testing is also applied to `post.py` because the route contains post lookup, slug redirection, view\-count update, comment insertion, comment deletion, post deletion, analytics, and not\-found handling in one function\.

- Control flow analysis is used to identify branches\.

- The selected tests cover unauthenticated create\-post access, logged\-in empty content, logged\-in valid content, post\-view slug handling, existing\-post rendering, missing\-post behavior, and comment insertion\.

- Database state and exceptions are checked to evaluate the result\.

### 3\.7 **Item Pass / Fail Criteria**

A test case passes if:

- The actual HTTP status code matches the expected status code\.

- The actual redirect target matches the expected redirect target when applicable\.

- The database side effect matches the expected state\.

- No unexpected exception is raised\.

A test case fails if:

- Invalid data is accepted when it should be rejected\.

- Valid data is rejected when it should be accepted\.

- The database contains incorrect records after test execution\.

- An unexpected exception occurs\.

- Access control behavior does not match the expected result\.

### 3\.8 **Suspension Criteria and Resumption Requirements**

Testing should be suspended if:

- The application cannot be imported or started\.

- Required dependencies are unavailable\.

- The database schema cannot be created\.

- A blocking defect prevents most planned tests from executing\.

Testing can resume when:

- Dependencies are installed and importable\.

- The test database can be created\.

- Blocking defects are fixed or isolated\.

- A stable test environment is available again\.

### 3\.9 **Test Deliverables**

The test deliverables are:

1. A risk analysis report, a high\-level test plan and a detailed test design and execution report

2. Component test source code:

    - `app/tests/assignment_b3_bb_signup_tests.py`

    - `app/tests/assignment_b3_bb_login_tests.py`

    - `app/tests/assignment_b3_wb_createpost_tests.py`

    - `app/tests/assignment_b3_wb_post_tests.py`

3. Test execution result summary

4. Defect records for discovered failures

### 3\.10 **Testing Tasks**

|Task|Description|
|---|---|
|Project analysis|Review the FlaskBlog project structure, major modules, configuration, database files, routes, forms, templates, and utilities|
|Risk analysis|Identify product risks, assess likelihood and impact, calculate risk exposure, and prioritize risks|
|Test planning|Define test scope, test items, features to be tested, features not to be tested, approach, environment, and responsibilities|
|Black\-box test design|Design equivalence class and boundary value test cases for the User Account and Authentication Module, using the signup workflow as the representative component|
|White\-box test design|Analyze source\-code branches and design control\-flow\-based tests for the Blog Post Management Module, using the create post workflow as the representative component|
|Test implementation|Implement automated component tests with Python `unittest`, Flask `test_client`, and temporary SQLite databases|
|Test execution<br>|Run the automated tests, collect pass/fail/error results, and inspect database side effects|
|Defect reporting|Record failed tests, observed behavior, expected behavior, affected source files, impact, and suggested fixes|
|Regression testing|Re\-run relevant tests after defects are fixed to confirm that failures are removed and no related behavior is broken|
|Report preparation|Summarize project analysis, risk analysis, test plan, test design, execution results, and defect findings|

### 3\.11 **Environmental Needs**

|Environment item|Requirement|
|---|---|
|Operating system|Windows environment used in this project|
|Python|Python version compatible with the project, as managed by `uv`|
|Dependencies|Flask, Flask\-WTF, WTForms, Passlib, and other dependencies from `app/pyproject.toml`|
|Test database|Temporary SQLite databases created during test execution|
|Test command|Run the four focused test files from the `app` directory with `uv run python tests\<file>.py`|

### 3\.12 **Responsibilities**

|Role|Responsibility|
|---|---|
|Test designer|Analyze risks, select test objects, design black\-box and white\-box tests|
|Test implementer|Implement automated component tests using Flask `test_client`|
|Test executor|Run the tests, collect results, and record failures|
|Defect analyst|Analyze failed tests and map failures to source code defects|

### 3\.13 **Staffing and Training Needs**

|Need|Description|
|---|---|
|Testing knowledge|Testers should understand basic software testing concepts, including risk\-based testing, equivalence partitioning, boundary value analysis, and white\-box branch coverage\.|
|Python and Flask knowledge|Testers should be able to read Python code, understand Flask routes, sessions, requests, redirects, and Blueprint registration\.|
|Database knowledge|Testers should understand basic SQLite operations and how to verify database side effects after test execution\.|
|Test automation knowledge|Testers should know how to run Python `unittest` tests and interpret pass, fail, and error results\.|
|Additional training|No special external training is required, but team members should review the relevant lecture materials on risk\-based testing, black\-box techniques, white\-box techniques, and test planning before finalizing the report\.|

### 3\.14 Schedule

1. Project structure analysis

2. Risk analysis

3. High\-level test planning

4. Signup black\-box test design

5. Create post white\-box test design

6. Test program implementation

7. Test execution and defect recording

8. Report writing

### 3\.15 **Risks and Contingencies**

|Project risk|Contingency|
|---|---|
|Dependency installation or `uv` execution problem|Use the existing local virtual environment or install dependencies in a clean environment|
|Existing project databases contain unrelated data|Use temporary SQLite databases for component tests|
|Route functions depend on templates or flash messages|Replace template rendering and flash messages with simple test doubles during component tests|
|External services are unavailable|Disable reCAPTCHA and avoid SMTP delivery in component tests|

### 3\.16 **Approvals**

|Approver|Approval responsibility|
|---|---|
|Project team members<br>|Review whether the selected modules, risk analysis, test plan, test cases, and execution results are correct and complete for submission\.|
|Test leader|Confirm that the test plan follows the required structure and that the final report is internally consistent\.|
|Course instructor|Final acceptance is subject to the assignment grading process\.|



## 4 Test Design and Execution Report \(薛\)

### 4\.1 **Selected Modules**



Two major functional areas were selected for detailed component testing\. Each area is represented by two route\-level workflows\.

|Test type|Selected functional area|Selected representative component / workflow|Reason for selection|
|---|---|---|---|
|Black\-box testing|User Authentication|Signup workflow; login workflow<br>|Signup is the first point where external users create persistent account data\. Login is the gate for authenticated behavior and session creation\. Both workflows have clear external inputs and observable outcomes, so they are suitable for equivalence partitioning, boundary value analysis, and credential acceptance/rejection tests\.|
|White\-box testing|Blog Content Management|Create post workflow; post view/comment workflow|Creating posts is the core content\-production workflow\. The `post.py` route handles post lookup, slug redirection, view count update, comments, deletion buttons, analytics, and not\-found behavior in one source\-level control flow\. These workflows directly affect whether users can publish, read, and interact with blog content\.|



The assignment requires selected modules rather than exhaustive testing of the whole application\. Therefore, this report selects two high\-risk functional areas and tests four representative route\-level components\. Logout, post edit, post delete, administration, search, and analytics are not claimed as fully covered by the current execution\.



### **4\.2 Selected Test Framework**



The selected test framework is Python `unittest` with Flask `test_client`\.

Reasons:

- It can test Flask routes without starting a real HTTP server\.

- It supports session manipulation, POST forms, redirects, and file uploads\.

- It can run fast component tests\.

- It works well with temporary SQLite databases\.

- It is included in Python's standard library, which reduces additional dependency risk\.



### **4\.3 General Architecture of the Test Programs**



The test program uses the following architecture:

1. Create temporary SQLite databases for the data stores needed by each component, including users, posts, comments, and analytics\.

2. Patch the database paths in `settings.py` and the selected route modules\.

3. Register only the target Blueprint in a small Flask test application\.

4. Replace template rendering, flash messages, point updates, delete utilities, and external visitor\-data lookup with test doubles where necessary\.

5. Use Flask `test_client` to send GET and POST requests\.

6. Inspect HTTP responses, redirects, exceptions, database state, and selected test\-double call records\.

7. Report passed, failed, and errored test cases through `unittest`\.

This architecture isolates the component under test and avoids modifying the real project databases in `app/db`\.



### **4\.4 Black\-Box Test Design and Execution: User Authentication**



The User Authentication area is tested with black\-box techniques because the main behavior can be observed through submitted form inputs, redirects, session state, and database side effects\. Two representative workflows are covered: signup and login\.

#### **4\.4\.1 Signup Workflow**

##### **Test Object**

The selected major modules are the User Account and Authentication Module\. Within this module, the signup workflow is selected as the representative component for black\-box testing because registration is the first step of the user account lifecycle and has clear input/output behavior\.



The selected test object includes:

- Route: `app/routes/signup.py`

- Form definition: `app/utils/forms/SignUpForm.py`

- Route URL: `/signup`



Main external inputs:

- `userName`

- `email`

- `password`

- `passwordConfirm`

##### **Input Conditions**



Based on the form definition and route behavior, the main input conditions are:

- Username should be required and should have length 4 to 25\.

- Email should be required and should have length 6 to 50\.

- Password should be required and should have length at least 8\.

- Password confirmation should be required, should have length at least 8, and should match password\.

- Username should contain ASCII characters\.

- Username and email should be unique\.

For equivalence\-class design, `passwordConfirm` is treated mainly as a dependent input whose key condition is whether it matches `password`\. Its length requirement is indirectly covered when it is kept equal to the password value in password\-length tests\.



##### **Equivalence Classes**



The signup black\-box design follows the single\-fault assumption\. One valid representative input is used as the baseline, and each negative test case changes one invalid input condition while keeping the other fields valid\. Therefore, exhaustive Cartesian\-product combination testing is not used\.

|Input|Valid equivalence classes|Invalid equivalence classes|
|---|---|---|
|Username|ASCII username, length 4\-25, not already used|Empty username; length \< 4; length \> 25; non\-ASCII username; duplicate username|
|Email|Valid email format, length 6\-50, not already used|Empty email; invalid email format; length \< 6; length \> 50; duplicate email|
|Password|Length \>= 8|Empty password; length \< 8|
|Password confirmation|Same as password|Different from password|



##### **Boundary Values**

The final signup test design combines equivalence partitioning and boundary value analysis\. BB\-01 to BB\-14 cover the main equivalence classes\. BB\-15 to BB\-24 add ten valid boundary\-value representatives for username and email length\. Password boundary values are covered by BB\-13 for length 7, BB\-01 for length 8, and selected valid boundary cases using password lengths 9 and 15\.

|Field|Boundary values|
|---|---|
|Username length|3, 4, 5, 20, 24, 25, 26|
|Email length|5, 6, 7, 28, 49, 50, 51|
|Password length|7, 8, 9, 15|

##### **Black\-Box Test Cases**



|Test case ID|Objective|Input|Expected result|
|---|---|---|---|
|BB\-01<br>|Test a valid representative signup|`validuser`, `valid@example.com`, normal valid password|User is inserted and response redirects to home page|
|BB\-02|Test empty username|Empty username with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-03|Test username length below minimum|Username length 3 with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-04|Test username length above maximum|Username length 26 with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-05|Test non\-ASCII username|Chinese username with otherwise valid fields|Signup is rejected and no user is inserted|
|BB\-06|Test duplicate username|Existing `validuser`, then submit another `validuser` with a new valid email|Signup is rejected and only one `validuser` exists|
|BB\-07|Test empty email|Empty email with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-08|Test invalid email format|`bad-email` with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-09|Test email length below minimum|Email length 5 with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-10|Test email length above maximum|Email length 51 with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-11|Test duplicate email|New valid username with an existing valid email|Signup is rejected and no new user is inserted|
|BB\-12|Test empty password|Empty password with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-13|Test password length below minimum|Password length 7 with otherwise normal valid fields|Signup is rejected and no user is inserted|
|BB\-14|Test mismatched password confirmation|Valid password with different confirmation|Signup is rejected and no user is inserted|
|BB\-15|Test username length at minimum boundary|Username length 4 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-16|Test username length just above minimum|Username length 5 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-17|Test username length just below maximum|Username length 24 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-18|Test username length at maximum boundary|Username length 25 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-19|Test email length at minimum boundary|Email length 6 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-20|Test email length just above minimum|Email length 7 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-21|Test email length just below maximum|Email length 49 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-22|Test email length at maximum boundary|Email length 50 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-23|Test password length at minimum boundary|Password length 8 with otherwise valid fields|User is inserted and response redirects to home page|
|BB\-24|Test password length just above minimum|Password length 9 with otherwise valid fields|User is inserted and response redirects to home page|





##### **Black\-Box Execution Results**

**Execution command:**

```PowerShell
uv run python tests\assignment_b3_bb_signup_tests.py
```

**Overall result**:

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGQwMDk5ZGI4YTQwNWNiYmFlNGJjNGVmY2Y0OGI3YmNfMDkwM2RlODMzYzIzNzYzYzdkOTM0Yjk3ODdjYmZhMjJfSUQ6NzY1MTU2OTkzODI0MzE0NDY1OF8xNzgxNTI5MjYzOjE3ODE2MTU2NjNfVjM)

|Total cases|Passed|Failed|Errors|Pass rate|
|---|---|---|---|---|
|24|17|7|0|70\.8%|

The passed cases are not listed individually in this section because they behaved as expected\. The failed cases are shown below because they reveal the main defect in the signup route\.

|Test case ID|Test focus|Expected result|Actual result|Verdict|
|---|---|---|---|---|
|BB\-03|Username length below minimum, length 3|Signup should be rejected and no user should be inserted|User with username `abc` was inserted; assertion showed `1 != 0`|Fail|
|BB\-04|Username length above maximum, length 26|Signup should be rejected and no user should be inserted|User with length\-26 username was inserted; assertion showed `1 != 0`|Fail|
|BB\-08|Invalid email format|Signup should be rejected and no user should be inserted|User with email `bad-email` was inserted; assertion showed `1 != 0`|Fail|
|BB\-09|Email length below minimum, length 5|Signup should be rejected and no user should be inserted|User with short email was inserted; assertion showed `1 != 0`|Fail|
|BB\-10|Email length above maximum, length 51|Signup should be rejected and no user should be inserted|User with long email was inserted; assertion showed `1 != 0`|Fail|
|BB\-12|Empty password|Signup should be rejected and no user should be inserted|User with empty password was inserted; assertion showed `1 != 0`|Fail|
|BB\-13|Password length below minimum, length 7|Signup should be rejected and no user should be inserted|User with short password was inserted; assertion showed `1 != 0`|Fail|



**Failure analysis**:

All seven failures have the same root cause\. The tests expected invalid signup data to be rejected, but the route inserted the submitted user into the database\. The failed assertions all compare the number of inserted users against the expected value `0`, but the actual count is `1`\.

This indicates that the backend signup route does not enforce the validation rules defined in `SignUpForm.py`\. In particular, username length, email format, email length, empty password, and password length rules are not checked before insertion\. Some invalid cases, such as empty username, non\-ASCII username, duplicate username, empty email, duplicate email, and mismatched password confirmation, were still rejected by other route\-level checks or database constraints, but the WTForms validation rules were not consistently applied\.

The execution output also shows several `ResourceWarning: unclosed database` messages\. These warnings do not change the pass/fail count, but they suggest that some database connections in the route code are not closed consistently\.



##### **Defect Found by Black\-Box Testing**

|Defect ID|`D-BB-01`|
|---|---|
|Title|Signup backend does not enforce WTForms validation|
|Description|The signup route creates `SignUpForm(request.form)`, but it does not call `form.validate()` before processing submitted data\. As a result, backend validation rules defined in `SignUpForm.py`, such as username length, email length, email format, and password length, are not enforced by the route\.|
|Observed evidence|Invalid inputs such as username length 3, username length 26, invalid email format, email length 5, email length 51, empty password, and password length 7 were accepted\. Invalid users were inserted into the users database\. The related single\-fault tests, including `test_bb03_short_username_is_rejected`, `test_bb08_invalid_email_format_is_rejected`, and `test_bb13_short_password_is_rejected`, failed\.|
|Impact|Invalid account data can enter the database\. This affects data quality, account management, and security assumptions\. Frontend validation can also be bypassed, so backend validation is required\.|
|Suggested fix|Call form validation before inserting the user\.|

#### **4\.4\.2 Login Workflow**



##### **Test Object**

The second black\-box target in the User Authentication area is the login workflow\.

The selected test object includes:

- Route: `app/routes/login.py`

- Form definition: `app/utils/forms/LoginForm.py`

- Route URL: `/login/redirect=<direct>`

##### **Input Conditions**



The login workflow has two main external inputs:

- `userName`

- `password`

The key behavior is externally observable: valid credentials should create a session and redirect, while invalid credentials should keep the user on the login page without creating `session["userName"]`\.



The form definition also includes length rules for username and password:

- Username should be required and should have length 4 to 25\.

- Password should be required and should have length at least 5\.

##### **Equivalence Classes**

|Input|Valid equivalence classes|Invalid equivalence classes|
|---|---|---|
|Username|Existing username, length 4\-25|Empty username; length \< 4; length \> 25; unknown username|
|Password|Provided password, length \>= 5, matching the account|Empty password; length \< 5; wrong password|

##### **Boundary Values**

|Field|Boundary values|
|---|---|
|Username length|3, 4, 5, 20, 24, 25, 26|
|Password length|4, 5, 6, 10|



##### **Black\-Box Test Cases**

|Test case ID|Objective|Input|Expected result|
|---|---|---|---|
|BB\-Login\-01|Valid credentials baseline|Existing username with length 20, matching password with length 10|Login succeeds, `session["userName"]` is set, and response redirects|
|BB\-Login\-02|Empty username|Empty username with otherwise valid password|Login is rejected and no user session is created|
|BB\-Login\-03|Username length below minimum|Username with length 3 and otherwise valid password|Login is rejected and no user session is created|
|BB\-Login\-04|Username length at minimum boundary|Existing username with length 4 and matching password|Login succeeds, `session["userName"]` is set, and response redirects|
|BB\-Login\-05|Username length just above minimum|Existing username with length 5 and matching password|Login succeeds, `session["userName"]` is set, and response redirects|
|BB\-Login\-06|Username length just below maximum|Existing username with length 24 and matching password|Login succeeds, `session["userName"]` is set, and response redirects|
|BB\-Login\-07|Username length at maximum boundary|Existing username with length 25 and matching password|Login succeeds, `session["userName"]` is set, and response redirects|
|BB\-Login\-08|Username length above maximum|Username with length 26 and otherwise valid password|Login is rejected and no user session is created|
|BB\-Login\-09|Unknown username|Non\-existing username with otherwise valid password|Login is rejected and no user session is created|
|BB\-Login\-10|Empty password|Existing username with empty password|Login is rejected and no user session is created|
|BB\-Login\-11|Password length below minimum|Existing username with password length 4|Login is rejected and no user session is created|
|BB\-Login\-12|Password length at minimum boundary|Existing username with matching password length 5|Login succeeds, `session["userName"]` is set, and response redirects|
|BB\-Login\-13|Password length just above minimum|Existing username with matching password length 6|Login succeeds, `session["userName"]` is set, and response redirects|
|BB\-Login\-14|Wrong password|Existing username with wrong password|Login is rejected and no user session is created|





##### **Black\-Box Execution Results**

**Execution command:**

```PowerShell
uv run python tests\assignment_b3_bb_login_tests.py
```

**Overall result**:

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NjdkZDZkZGRmYmQ2ZDcxOGE5ZjVjY2NhZTQ0MDU1YjJfZTAyNjA4NDE0MmE1NWI2NWE4MmU1MGVhODAzMmJkNTBfSUQ6NzY1MTU3OTM5ODAwNTA1MDU2NV8xNzgxNTI5MjYzOjE3ODE2MTU2NjNfVjM)

|Total cases|Passed|Failed|Errors|Pass rate|
|---|---|---|---|---|
|14|14|0|0|100\.0%|



### **4\.5 White\-Box Test Design and Execution: Blog Content Management**

The Blog Content Management area is tested with white\-box techniques because its route functions contain explicit source\-level branches for authentication, request method, post lookup, redirects, database writes, and exceptional paths\. Two representative workflows are covered: create post and post view/comment handling\.



#### **4\.5\.1 White\-Box Design Method and Coverage Criteria**



The white\-box test cases were designed by reading the source code and constructing a control\-flow view of each selected route function\. The analysis identifies important executable statements, decision points, nested branches, early returns, database write paths, and exception\-prone paths\.

The main design principle is to identify feasible paths first, and then use those paths to cover different important conditions\. This is especially important for Flask route functions because many branches return immediately after a redirect, deletion action, not\-found path, or error\-handling path\. As a result, some theoretical branch combinations cannot occur in one request, while other combinations add little value because an earlier branch already ends the route\.

The coverage target is therefore representative feasible path coverage rather than exhaustive path coverage\. Each selected test case should follow a complete practical route path from request input to response or exception\. On top of those feasible paths, the tests are designed to provide statement coverage for the main rendering, redirect, delete, comment, database\-write, and analytics statements where feasible\. They also provide decision / branch coverage for the major decisions, such as authentication state, request method, post existence, slug correctness, post\-delete button, comment\-delete button, comment submission, analytics enabled/disabled, session username present/absent, and visitor\-data success/failure\.

Based on this method, `createPost.py` is designed with four main feasible paths: unauthenticated access, logged\-in GET rendering, logged\-in POST with empty content, and logged\-in POST with valid content\. `post.py` is designed with ten representative feasible paths covering its main control\-flow responsibilities\. The design does not claim exhaustive path coverage; for example, a request that triggers `postDeleteButton` returns before comment insertion or analytics handling can occur, so those conditions should be covered by separate feasible paths instead of forced into one impossible combined path\.



#### **4\.5\.2 Create Post Workflow**



##### **Test Object**



The selected functional area is Blog Content Management\. Within this area, the create post workflow is selected as a representative white\-box component because it is a core post management operation and contains important conditional branches\.



The selected test object includes:



- Route: `app/routes/createPost.py`

- Form definition: `app/utils/forms/CreatePostForm.py`

- URL ID helper: `app/utils/generateUrlIdFromPost.py`

- Route URL: `/createpost`

##### **Control Flow Analysis**



The `createPost()` function has the following main control flow:



1. Check whether `userName` exists in session\.

2. If the user is not logged in, redirect to the login page\.

3. If the user is logged in, create the post form\.

4. If the request method is GET, render the create post page\.

5. If the request method is POST, read title, tags, content, banner, and category\.

6. If `postContent == ""`, show an error message and do not insert a post\.

7. If `postContent != ""`, insert a new post into the posts database, add points, show a success message, and redirect to the home page\.

##### **Coverage Objective**



The coverage objective for `createPost.py` is to cover the main feasible paths through the route and the key decisions that control whether a user can create a post\. The tests focus on authentication, request method, and post\-content validation:



- Not logged in branch\.

- Logged in and GET rendering branch\.

- Logged in and empty post content branch\.

- Logged in and valid post content branch\.

These four cases cover the main executable statements, both outcomes of the authentication decision \(`"userName" in session`\), both outcomes of the request\-method decision \(`request.method == "POST"`\), and both outcomes of the content decision \(`postContent == ""`\)\. This gives branch coverage for the main business decisions and representative feasible path coverage for the whole route\. The tests do not attempt to cover every invalid form\-field combination, such as missing form keys or missing uploaded files, because the objective is route\-level control\-flow coverage rather than exhaustive form validation testing\.



##### **White\-Box Test Cases**

|Test case ID|Covered branch|Preconditions|Input|Expected result|
|---|---|---|---|---|
|WB\-Create\-01|User not logged in|No `userName` in session|GET `/createpost`|Redirect to `/login/redirect=&createpost`|
|WB\-Create\-02|Logged in, GET request|`userName=alice` in session|GET `/createpost`|Create post page is rendered|
|WB\-Create\-03|Logged in, POST, empty content|`userName=alice` in session|POST with empty `postContent`|No post is inserted; create page is returned|
|WB\-Create\-04|Logged in, POST, valid content|`userName=alice` in session|POST with valid title, tags, content, banner, and category|Post is inserted and response redirects to home page|



##### **White\-Box Execution Results**

**Execution command:**

```PowerShell
uv run python tests\assignment_b3_wb_createpost_tests.py
```

**Overall result:**

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTIzNzRiMmExZDYwOTRhM2E3ZGVkYjE3MThiZjg4Y2RfNzg2M2M0ZWIyMDk5YTk4ZjhlNjQ2ZTcyMjhmMDlkYTBfSUQ6NzY1MTU4Mjc0OTM4MzU5MjkxOF8xNzgxNTI5MjYzOjE3ODE2MTU2NjNfVjM)

|Total cases|Passed|Failed|Errors|Pass rate|
|---|---|---|---|---|
|4|3|0|1|75\.0%|

The passed cases are not listed individually in this section because they behaved as expected\. The error case is shown below because it reveals the main defect in the create\-post route\.

|Test case ID|Test focus|Expected result|Actual result|Verdict|
|---|---|---|---|---|
|WB\-Create\-04|Logged\-in user submits a valid post|The post should be inserted and the response should redirect to the home page|`TypeError: generateurlID() takes 0 positional arguments but 1 was given`|Error|

**Failure analysis:**

The failed execution has one direct cause\. The successful create\-post branch calls `generateurlID(postTitle)`, but the helper function is defined without parameters\. Therefore, the route crashes before the database insertion and redirect can complete\. This prevents a valid logged\-in user from publishing a post through the tested path\.

##### **Defect Found by White\-Box Testing**

|Defect ID|`D-WB-01`|
|---|---|
|Title|Valid create post workflow crashes because of incorrect `generateurlID` call|
|Description|In `app/routes/createPost.py`, the successful post creation branch calls `generateurlID(postTitle)`\. However, in `app/utils/generateUrlIdFromPost.py`, the function is defined as `def generateurlID():` with no positional arguments\. |
|Observed evidence|Test case `test_wb_create_04_valid_input_inserts_post` raised `TypeError: generateurlID() takes 0 positional arguments but 1 was given`\. The successful post creation branch could not complete\.|
|Impact|Critical defect in the core post publishing workflow\. A normal logged\-in user cannot successfully publish a valid post through the tested path\.|
|Suggested fix|Since `generateurlID()` currently generates a random unique ID and does not use the post title, change the call to `generateurlID()`\. |

#### **4\.5\.3 Post View and Comment Workflow**



##### **Test Object**

The second white\-box target in the Blog Content Management area is the `post.py` route\. Although the user\-facing purpose is "view post", the route also contains slug normalization, view\-count update, comment insertion, comment deletion, post deletion, analytics handling, and not\-found handling\. Therefore, it is a useful representative component for source\-code\-based control\-flow testing\.



The selected test object includes:

- Route: `app/routes/post.py`

- Form definition: `app/utils/forms/CommentForm.py`

- Deletion utility: `app/utils/delete.py`

- Route URLs: `/post/<urlID>` and `/post/<slug>-<urlID>`



##### **Control Flow Analysis**



The `post()` function has the following main control flow:

1. Read the `urlID` from the route and query the posts database\.

2. If no post exists, render the not\-found page\. In the current implementation, this intended branch is exception\-prone because `posts` can be `None`\.

3. If the post exists but the slug is missing or incorrect, redirect to the canonical slug URL\.

4. If the post exists and the slug is correct, load the full post record\.

5. Increment the post view count\.

6. If the request method is POST and contains `postDeleteButton`, delete the post and redirect\.

7. If the request method is POST and contains `commentDeleteButton`, delete the comment and redirect\.

8. If the request method is POST and contains a normal comment, insert the comment and redirect\.

9. If the request method is GET, load comments\.

10. If analytics is enabled, record visitor analytics when visitor data is available; otherwise skip analytics or log the failure\.

11. Render the post page\.

##### **Coverage Objective**

The coverage objective for `post.py` is to cover the main feasible paths through the route and the key conditions that control post viewing, canonical URL redirection, view updates, comment handling, deletion actions, and analytics recording\. The route has more branches than `createPost.py`, and several branches return immediately\. For this reason, exhaustive combination coverage is not practical or necessary for this component\-level report\. The selected design instead targets representative feasible path coverage, supported by statement, branch, and condition coverage for the most important decisions\.



The ten designed paths cover:

- Both outcomes of post existence: existing post and missing post\.

- Both outcomes of slug validation: missing/wrong slug and correct slug\.

- Both outcomes of request method: GET and POST\.

- POST sub\-branches for post deletion, comment deletion, and normal comment insertion\.

- Both outcomes of login\-dependent comment behavior: logged\-in user and missing session user\.

- Both outcomes of analytics configuration: analytics disabled and analytics enabled\.

- Analytics success and analytics failure behavior\.

The ten cases do not cover every possible edge case\. For example, they do not separately test a wrong non\-empty slug versus a missing slug, a POST request with no delete button and no `comment` field, a comment\-delete request with a missing `commentID`, empty comment text, or unauthorized deletion attempts\. These are useful follow\-up regression or robustness tests, but they are outside the selected representative path set\.



##### **White\-Box Post Test Cases**

|Test case ID|Covered branch|Preconditions|Input|Expected result|
|---|---|---|---|---|
|WB\-Post\-01|Missing post path|No post with `urlID=missing` exists|GET `/post/missing`|Not\-found page is rendered|
|WB\-Post\-02|Existing post, missing or incorrect slug|Post with `urlID=abc123` exists|GET `/post/abc123`|Redirect to canonical slug URL|
|WB\-Post\-03|Existing post, correct slug, normal GET, analytics disabled|Post with `urlID=abc123` exists; analytics disabled|GET `/post/valid-blog-title-abc123`|Post page is rendered and views increase|
|WB\-Post\-04|Post deletion branch|Logged\-in user; post exists; user is allowed to delete|POST with `postDeleteButton`|Delete utility is called and response redirects to home page|
|WB\-Post\-05|Comment deletion branch|Logged\-in user; post and comment exist|POST with `commentDeleteButton` and `commentID`|Comment delete utility is called and response redirects|
|WB\-Post\-06|Logged\-in normal comment submission|Logged\-in user `alice`; post exists|POST with `comment`|Comment is inserted and response redirects|
|WB\-Post\-07|Comment submission without logged\-in user|No `userName` in session; post exists|POST with `comment`|Request should be rejected or handled safely; current code may raise a session\-related error|
|WB\-Post\-08|Analytics enabled, logged\-in visitor, visitor data success|Logged\-in user; analytics enabled; IP/user\-agent data returns success|GET correct slug URL|Analytics row is inserted with the logged\-in username|
|WB\-Post\-09|Analytics enabled, anonymous visitor, visitor data success|No `userName` in session; analytics enabled; IP/user\-agent data returns success|GET correct slug URL|Analytics row is inserted with `unsignedUser`|
|WB\-Post\-10|Analytics enabled, visitor data failure|Analytics enabled; IP/user\-agent data returns failure|GET correct slug URL|Analytics insertion is skipped and page rendering should still complete|



##### **White\-Box Post Execution Results**

**Execution command:**

```PowerShell
uv run python tests\assignment_b3_wb_post_tests.py
```

**Overall result:**

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZTJiNDk3ZDRhNmJjZTM0NTA3MjgyZGNlZWRkMGRiZjRfYWViM2U0MjRhOTdlNzFmZWUwNTQ2MDAyNjg5NjRlMjFfSUQ6NzY1MTU4NzM0NTE1Mzc0MDAxMV8xNzgxNTI5MjYzOjE3ODE2MTU2NjNfVjM)

|Total cases|Passed|Failed|Errors|Pass rate|
|---|---|---|---|---|
|10|8|0|2|80\.0%|

The passed cases are not listed individually in this section because they behaved as expected\. The error cases are shown below because they identify the main unsafe paths in `post.py`\.

|Test case ID|Test focus|Expected result|Actual result|Verdict|
|---|---|---|---|---|
|WB\-Post\-01<br>|Missing post URL|The not\-found page should be rendered|`TypeError: argument of type 'NoneType' is not iterable`|Error|
|WB\-Post\-07|Anonymous comment submission|The request should be rejected or handled safely without inserting a comment|`KeyError: 'userName'`|Error|

**Failure analysis:**

The main failure reason is that `post.py` uses route data before checking whether the required object or session value exists\. In `WB-Post-01`, the database query returns `None`, but the route still evaluates `str(urlID) in posts`, which raises a `TypeError`\. In `WB-Post-07`, the route reads `session["userName"]` during comment insertion without first checking whether the user is logged in, which raises a `KeyError`\. Both errors show that the route needs guard checks before using optional database results or session keys\.



##### **Defect Found by Post White\-Box Testing**

|Defect ID|`D-WB-02`|
|---|---|
|Title|Missing post route crashes before rendering the not\-found page|
|Description|In `app/routes/post.py`, the route queries `cursor.execute("select urlID, title from posts where urlID = ?", (urlID,))` and `posts = cursor.fetchone()`\. If no matching post exists, `posts` is `None`\. The next condition `if str(urlID) in posts:` attempts to iterate over `None` and raises a `TypeError`\.|
|Observed evidence|Test case `test_wb_post_01_missing_post_renders_not_found_page` raised `TypeError: argument of type 'NoneType' is not iterable`\.|
|Impact|Users who open a missing or invalid post URL receive a server error instead of the expected not\-found page\. This affects reliability and user\-facing error handling for the blog content module\.|
|Suggested fix|Check for `None` before testing membership: `if posts and str(urlID) in posts:` \.\.\. `else: return render_template("notFound.html")`|

|Defect ID|`D-WB-03`|
|---|---|
|Title|Comment submission without a logged\-in user crashes with a session key error|
|Description|In the normal comment submission branch of `app/routes/post.py`, the route inserts the comment using `session["userName"]`\. However, the route does not first check whether `"userName"` exists in the session\. If an unauthenticated user submits a POST request with a `comment` field, the route raises `KeyError: 'userName'` instead of rejecting the request safely or redirecting the user to login\.|
|Observed evidence|Test case `test_wb_post_07_comment_without_login_is_handled_safely` raised `KeyError: 'userName'`\. No safe rejection or login redirect was returned\.|
|Impact|An unauthenticated comment submission can crash the post route\. This affects reliability and access\-control behavior for comments\.|
|Suggested fix|Check the session before inserting a comment: `if "userName" not in session:` → `flashMessage(...)`; `return redirect(url_for("login.login", direct="..."))`|



## 5 **Use of Artificial Intelligence ****\(薛\)**

Artificial intelligence was used as an auxiliary tool during this project\. It was mainly used in the following ways:

1. **Project understanding and module analysis**
AI was used to help read and summarize the FlaskBlog repository structure\. It helped identify the major functional areas of the system, such as user authentication, signup, login, post creation, post viewing, comments, administration, search/category browsing, and analytics\.

2. **Risk analysis support**
AI was used to suggest possible product risks for a Flask\-based blog system, such as invalid user input being accepted, login/session errors, failed post creation, unsafe comment handling, incorrect post view behavior, database inconsistency, and analytics recording errors\. The final risk list, risk levels, and selected test targets were reviewed and adjusted manually\.

3. **Black\-box test design**
AI was used to help derive equivalence classes and boundary values for the signup and login workflows\. For example, it helped identify valid and invalid classes for username, email, password, password confirmation, existing users, unknown users, and wrong passwords\. These suggestions were then checked against the actual form definitions, route behavior, and executed test results\.

4. **White\-box test design**
AI and coding\-agent\-style tools were used to help inspect the source code of `createPost.py` and `post.py`\. They helped identify feasible control\-flow paths, branch conditions, early returns, database write operations, redirect paths, comment\-related branches, deletion branches, and analytics branches\. The final white\-box test cases were selected based on representative feasible path coverage\.

5. **Test code implementation**
AI was used to draft initial Python `unittest` test code using Flask `test_client` and isolated SQLite databases\. The code was then manually reviewed, modified, and executed\. Configuration patching, temporary database setup, expected results, and actual execution results were checked before being included in the report\.

6. **Report writing support**
AI was used to help organize the report structure and improve English expression for sections such as project analysis, risk analysis, test design, execution summaries, and defect descriptions\. However, the final report content was manually checked to ensure that it matched the actual repository, implemented tests, and observed execution results\.

AI was not used as a replacement for human judgment\. All important decisions, including module selection, risk ratings, test case design, expected results, defect analysis, and final conclusions, were reviewed manually\. No real user data or sensitive information was used when interacting with AI tools\.

## 6 **Ethical Considerations ****\(徐\)**




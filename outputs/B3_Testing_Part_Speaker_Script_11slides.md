# Speaker Script - B3 Testing Part: Setup and Post Components

## Slide 1 - Opening
Good morning. This section presents the detailed component test design and execution report for FlaskBlog. I will focus on the setup or authentication component and the post component. These are the two selected areas for the assignment's detailed testing requirement.

## Slide 2 - Contents
The section has five parts: testing scope, setup component testing, setup execution and defect, post component testing, and final defect summary with regression direction.

## Slide 3 - Testing Scope
The testing scope was selected from the risk analysis. For setup, the main concerns were invalid signup data, malformed account records, login behavior, and session state. For post, the main concerns were failed post creation, unsafe access control, missing post handling, comment behavior, and route-level exceptions. The tests were route-level component tests using isolated SQLite databases and Flask test_client.

## Slide 4 - Setup Component: Black-box Design
For setup testing, we used black-box techniques because signup and login have clear external inputs and observable outputs. Signup inputs include username, email, password, and password confirmation. We derived valid and invalid equivalence classes, then added boundary values for username length, email length, and password length. Login was tested through valid credentials, unknown users, empty fields, short fields, and wrong password cases.

## Slide 5 - Setup Component: Execution Results
The setup tests were implemented with Python unittest and Flask test_client. This choice allowed us to submit requests without a browser, inspect Flask session state, and check database side effects directly. Signup had 24 cases: 17 passed and 7 failed, with a pass rate of 70.8 percent. Login had 14 cases and all passed. This difference is important because login behavior was stable, while signup backend validation was not consistently enforced.

## Slide 6 - Setup Defect
The main setup defect is D-BB-01. The signup route creates a SignUpForm object, but it does not call form.validate before inserting the user. Therefore, invalid inputs such as short usernames, overly long usernames, invalid email formats, empty passwords, and short passwords were accepted. The fix is to enforce WTForms validation on the backend before database insertion, not only on the frontend.

## Slide 7 - Post Component: White-box Design
For the post component, we used white-box testing because the internal branch structure is important. In createPost.py, the route checks session state, handles GET rendering, rejects empty post content, and should insert valid posts. In post.py, the route handles post lookup, slug normalization, view count update, delete actions, comment submission, analytics branches, and final rendering. We selected feasible paths rather than impossible branch combinations.

## Slide 8 - Create Post Workflow
For createPost.py, we designed four paths: unauthenticated access, logged-in GET rendering, logged-in POST with empty content, and logged-in POST with valid content. Three cases passed, but the valid post case produced a TypeError. The route calls generateurlID with postTitle as an argument, while the helper is defined without parameters. This prevents a normal logged-in user from publishing a valid post through the tested path.

## Slide 9 - Post View and Comment Workflow
For post.py, we designed ten representative paths. These include missing post, canonical slug redirect, normal GET with view update, post deletion, comment deletion, logged-in comment submission, anonymous comment submission, and analytics enabled or disabled paths. Eight cases passed and two produced errors. The errors show that the route uses optional data before checking whether the post exists or whether the user is logged in.

## Slide 10 - Defect Summary and Regression Direction
In total, the detailed testing found one black-box defect and three white-box defects. D-BB-01 is missing backend validation in signup. D-WB-01 is the helper-call mismatch in createPost. D-WB-02 is the missing-post crash in post.py. D-WB-03 is the anonymous-comment session KeyError. After fixes, the same test suites should be reused as regression tests to confirm invalid signup data is rejected, valid posts can be published, missing posts render safely, and anonymous comments are handled correctly.

## Slide 11 - Closing
To conclude, the tests followed the assignment requirement by selecting two major modules, using black-box and white-box techniques, implementing executable test programs, and reporting concrete evidence. The key lesson is that route-level tests are effective for FlaskBlog because many risks happen at the boundary between request data, session state, validation, and SQLite side effects. Thank you.
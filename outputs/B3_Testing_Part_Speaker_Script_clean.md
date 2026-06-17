# Speaker Script - Clean Layout Version

## Slide 1
Good morning. This part presents the detailed component testing work for FlaskBlog. I will focus on the setup component and the post component, which are the two selected areas for detailed test design and execution.

## Slide 2
The structure is straightforward. First, I will explain the scope. Then I will cover setup testing, including black-box design, test execution, and the defect found. After that I will cover post testing, including white-box design, execution results, and regression direction.

## Slide 3
The testing scope follows the risk analysis. Setup testing targets signup validation, login behavior, database side effects, and session state. Post testing targets create post, post viewing, comment behavior, and unsafe route branches. The tests were route-level component tests using isolated SQLite databases and Flask test_client.

## Slide 4
For setup testing, black-box design is suitable because the inputs and outputs are clear. Signup was tested through username, email, password, and confirmation. We used equivalence partitioning and boundary value analysis. Login was tested through credential classes, including valid credentials, unknown users, empty fields, short fields, and wrong passwords.

## Slide 5
The setup test suite contains 24 signup cases and 14 login cases. The boundary values cover username length, email length, and password length. Assertions check response behavior, redirects, session state, and database insertion or non-insertion.

## Slide 6
The setup execution result shows an important contrast. Login passed all 14 cases. Signup passed 17 out of 24 cases, so the pass rate was 70.8 percent. This means login behavior was stable, but signup backend validation had a clear weakness.

## Slide 7
The setup defect is D-BB-01. The signup route creates a SignUpForm object but does not call form.validate before inserting user data. Invalid inputs such as short usernames, invalid email formats, empty passwords, and short passwords were accepted. The fix is to enforce backend WTForms validation before database insertion.

## Slide 8
For the post component, white-box testing is appropriate because the routes contain important branches. createPost.py has session checks, GET rendering, empty-content rejection, and valid-post insertion. post.py includes post lookup, slug normalization, view count update, deletion branches, comment branches, analytics branches, and final rendering.

## Slide 9
The create post workflow had four cases. Three passed, but the valid post submission produced an error. The route calls generateurlID with postTitle as an argument, while the helper takes no parameters. This prevents a normal logged-in user from publishing a valid post.

## Slide 10
The post view and comment workflow had ten representative paths. Eight passed and two produced errors. The missing post path raises a TypeError because the route checks membership on None. The anonymous comment path raises a KeyError because session userName is used without checking login state.

## Slide 11
Overall, the detailed tests found one black-box defect and three white-box defects. The regression plan is to rerun the same suites after fixes, confirming invalid signup data is rejected, valid posts can be published, missing posts render safely, and anonymous comments are handled without server errors. Thank you.
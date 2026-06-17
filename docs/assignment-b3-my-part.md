# Assignment B3 - FlaskBlog Project Analysis and Component Test Design

## 1. FlaskBlog 项目模块分析

### 1.1 项目背景与目标

FlaskBlog 是一个基于 Flask 的现代博客系统，项目目标是提供一个可运行的博客应用，使用户能够注册、登录、发布文章、浏览文章、评论文章，并通过后台管理功能维护用户、文章和评论数据。项目同时支持深色/浅色主题、多语言界面、分类浏览、搜索、文章访问分析等功能。

从 `README.md` 和源码结构看，该项目主要面向个人博客或小型内容发布场景。系统强调以下目标：

- 提供完整的用户系统，包括注册、登录、用户主页、头像和账户设置。
- 提供文章管理能力，包括创建、编辑、分类、搜索和阅读文章。
- 提供管理员面板，用于管理用户、文章和评论。
- 提供可用性和展示层支持，包括 TailwindCSS UI、响应式页面、主题切换、多语言翻译。
- 提供基础安全能力，包括密码哈希、CSRF 保护、可配置 reCAPTCHA、登录状态控制。
- 提供运行监控能力，包括日志记录、文章浏览量和访问分析。

### 1.2 主要功能性需求

| 功能领域 | 主要需求 | 相关代码位置 |
|---|---|---|
| 用户认证与账户 | 用户注册、登录、登出、修改用户名、修改密码、修改头像、账户设置 | `app/routes/signup.py`, `app/routes/login.py`, `app/routes/logout.py`, `app/routes/changePassword.py`, `app/routes/changeUserName.py`, `app/routes/changeProfilePicture.py` |
| 内容发布与管理 | 创建文章、编辑文章、查看文章、删除文章、文章 URL ID/slug 生成 | `app/routes/createPost.py`, `app/routes/editPost.py`, `app/routes/post.py`, `app/utils/generateUrlIdFromPost.py` |
| 评论功能 | 在文章详情页发表评论、删除评论 | `app/routes/post.py`, `app/routes/adminPanelComments.py`, `app/utils/delete.py` |
| 搜索与分类 | 按标题、标签、作者、用户搜索；按分类浏览文章 | `app/routes/search.py`, `app/routes/searchBar.py`, `app/routes/category.py` |
| 管理后台 | 管理用户、文章和评论，切换用户角色 | `app/routes/adminPanel.py`, `app/routes/adminPanelUsers.py`, `app/routes/adminPanelPosts.py`, `app/routes/adminPanelComments.py` |
| 分析统计 | 记录文章访问量、访问者国家、操作系统和停留时间 | `app/routes/postsAnalytics.py`, `app/routes/returnPostAnalyticsData.py`, `app/utils/getAnalyticsPageData.py` |
| 国际化与界面 | 多语言翻译、主题切换、模板渲染、静态资源 | `app/translations/*.json`, `app/templates/tailwindUI`, `app/static/tailwindUI` |

### 1.3 主要非功能性需求

| 质量属性 | 项目中的体现 | 风险点 |
|---|---|---|
| 安全性 | 使用 `sha512_crypt` 哈希密码，启用 Flask-WTF CSRFProtect，可选 reCAPTCHA | 配置文件中存在 SMTP 密码；部分路由权限检查较分散；表单验证未必实际调用 |
| 可用性 | TailwindCSS 页面、响应式截图、多语言、主题切换 | UI 与后端校验不一致时，用户可能提交异常数据 |
| 可维护性 | 路由按功能拆分，表单类和工具函数单独放置 | 业务逻辑、数据库访问和视图渲染混在同一路由函数中，单元测试隔离成本较高 |
| 可靠性 | SQLite 持久化、日志记录、默认管理员初始化 | 异常路径中数据库连接可能无法及时关闭；缺少自动化测试 |
| 可测试性 | Flask 路由可用 `test_client` 测试，表单类独立 | 直接导入全局配置和数据库路径，需要测试时进行隔离或 monkeypatch |

### 1.4 软件架构与主要组件

项目采用典型 Flask MVC/分层风格，但实现上更接近“路由函数 + 模板 + SQLite + 工具函数”的轻量架构。

| 层次/组件 | 说明 |
|---|---|
| 应用入口 | `app/app.py` 创建 Flask 实例，注册 CSRF、上下文处理器、错误处理器、请求日志和所有 Blueprint。 |
| 配置层 | `app/settings.py` 保存端口、模板路径、数据库路径、登录/注册开关、SMTP、reCAPTCHA、默认管理员等配置。 |
| 路由层 | `app/routes/*.py` 每个文件对应一个页面或业务功能，如注册、登录、创建文章、后台管理等。 |
| 表单层 | `app/utils/forms/*.py` 使用 WTForms 定义输入字段和校验规则，例如用户名长度、密码长度、文章标题长度等。 |
| 工具层 | `app/utils/*.py` 包含日志、时间戳、积分、删除、URL ID/slug 生成、数据分析等辅助逻辑。 |
| 数据层 | `app/db/*.db` 使用 SQLite 分别存储用户、文章、评论和分析数据；`app/utils/dbChecker.py` 负责建表和默认管理员初始化。 |
| 表现层 | `app/templates/tailwindUI` 保存 HTML/Jinja 模板，`app/static/tailwindUI` 保存 CSS 和 JS。 |

整体结构的优点是功能边界直观、适合小型应用快速开发；主要不足是路由函数承担了输入读取、权限判断、数据库操作、业务判断和页面跳转等多种职责，导致缺陷容易集中在分支逻辑和表单校验衔接处。

## 2. 两个模块的选择

根据项目结构和风险分析，本部分选择两个主要模块中的高风险代表性工作流进行组件测试。风险登记表可以覆盖整个系统，但本部分的详细测试范围只覆盖两个选定工作流，不声称完整测试登录、删除、后台、搜索和分析等所有功能。

| 测试类型 | 被测模块 | 选择理由 |
|---|---|---|
| 黑盒测试 | 用户注册模块 `signup` | 注册是用户数据进入系统的第一道入口，涉及用户名、邮箱、密码、确认密码、重复账号、ASCII 检查、密码哈希、session 创建和用户表插入。如果后端校验缺失，异常账号数据会影响后续登录、展示和管理逻辑，因此适合使用等价类划分和边界值分析。 |
| 白盒测试 | 文章创建模块 `createPost` | 创建文章是博客系统的核心内容生产流程，涉及登录状态判断、GET/POST 判断、空内容判断、文件上传、URL ID 生成、数据库插入、积分增加和重定向。该流程一旦失败，合法用户无法发布文章，因此适合基于源码进行控制流和分支覆盖分析。 |

风险与测试选择的对应关系如下：

| 风险点 | 选择的测试对象 | 覆盖情况 |
|---|---|---|
| 注册输入校验缺失导致非法用户数据入库 | `signup` 黑盒测试 | 通过 BB-01 至 BB-14 设计覆盖，自动化执行覆盖代表性子集并发现缺陷 |
| 重复用户名或邮箱破坏用户数据完整性 | `signup` 数据库状态检查 | 通过重复用户名/邮箱设计用例覆盖，自动化执行覆盖重复用户名 |
| 合法用户无法创建文章 | `createPost` 白盒测试 | 通过正常创建分支发现 `generateurlID(postTitle)` 参数错误缺陷 |
| 未登录用户访问受限功能 | `/createpost` 未登录分支 | 当前只覆盖创建文章的 session 访问控制，不代表后台、编辑、删除等权限均已测试 |
| 登录、文章编辑、文章删除和后台管理风险 | 登录、编辑、删除、后台相关路由 | 记录为后续回归测试候选项，本报告不做详细执行 |

测试框架选择 Flask 自带的 `test_client`，并配合临时 SQLite 数据库执行组件级测试。选择原因如下：

- 能直接调用 Flask 路由，不需要启动真实服务器，执行速度快。
- 支持 session 设置、POST 表单提交和文件上传，适合测试注册和文章创建模块。
- 可使用临时数据库隔离测试数据，避免污染项目自带的 `app/db/*.db`。
- 可与 `unittest` 或 `pytest` 集成，便于后续扩展成自动化测试程序。

## 3. 黑盒测试设计：用户注册模块

### 3.1 测试对象

测试对象为 `/signup` 路由，对应源码 `app/routes/signup.py`，表单定义位于 `app/utils/forms/SignUpForm.py`。

该模块的外部输入包括：

- `userName`
- `email`
- `password`
- `passwordConfirm`

根据表单定义和注册业务逻辑，可得到以下主要输入约束：

- 用户名长度应为 4-25，且不能为空。
- 邮箱长度应为 6-50，且不能为空。
- 密码长度至少为 8，且不能为空。
- 确认密码长度至少为 8，且必须与密码一致。
- 用户名应只包含 ASCII 字符。
- 用户名和邮箱不能与数据库中已有记录重复。

### 3.2 等价类划分

本注册模块的黑盒测试设计采用单缺陷假设：先设置一个全合法输入作为基准，每个无效测试用例只改变一个非法输入条件，其他字段保持合法。因此，本测试不采用所有输入项的全组合方式。

其中，`passwordConfirm` 主要作为依赖输入处理，核心条件是是否与 `password` 一致；当密码长度类测试中确认密码与密码保持相同时，确认密码的长度要求也被间接覆盖。

| 输入项 | 有效等价类 | 无效等价类 |
|---|---|---|
| 用户名 | 长度 4-25，ASCII，未被占用 | 为空；长度 < 4；长度 > 25；非 ASCII；已存在用户名 |
| 邮箱 | 长度 6-50，格式合理，未被占用 | 为空；格式错误；长度 < 6；长度 > 50；已存在邮箱 |
| 密码 | 长度 >= 8 | 为空；长度 < 8 |
| 确认密码 | 与密码相同 | 与密码不一致 |

### 3.3 边界值分析

| 字段 | 边界值 |
|---|---|
| 用户名长度 | 3、4、25、26 |
| 邮箱长度 | 5、6、50、51 |
| 密码长度 | 7、8 |
| 确认密码 | 与密码相同、与密码不同 |

### 3.4 黑盒测试用例

| 用例编号 | 测试目的 | 输入数据 | 预期结果 |
|---|---|---|---|
| BB-01 | 有效注册 | `validuser`, `valid@example.com`, `abcdefgh`, `abcdefgh` | 注册成功，写入用户表，重定向首页 |
| BB-02 | 用户名为空 | ``, `valid@example.com`, `abcdefgh`, `abcdefgh` | 注册失败，不写入用户表 |
| BB-03 | 用户名长度小于 4 | `abc`, `valid@example.com`, `abcdefgh`, `abcdefgh` | 注册失败，不写入用户表 |
| BB-04 | 用户名长度大于 25 | `abcdefghijklmnopqrstuvwxyz`, `valid@example.com`, `abcdefgh`, `abcdefgh` | 注册失败，不写入用户表 |
| BB-05 | 非 ASCII 用户名 | `测试用户`, `cn@example.com`, `abcdefgh`, `abcdefgh` | 注册失败，不写入用户表 |
| BB-06 | 重复用户名 | 已存在 `validuser`，再次使用 `validuser` 和新的合法邮箱注册 | 注册失败，用户表中仍只有一个 `validuser` |
| BB-07 | 邮箱为空 | `validuser`, ``, `abcdefgh`, `abcdefgh` | 注册失败，不写入用户表 |
| BB-08 | 邮箱格式错误 | `validuser`, `bad-email`, `abcdefgh`, `abcdefgh` | 注册失败，不写入用户表 |
| BB-09 | 邮箱长度小于 6 | `validuser`, `a@b.c`, `abcdefgh`, `abcdefgh` | 注册失败，不写入用户表 |
| BB-10 | 邮箱长度大于 50 | `validuser`, 长度为 51 的邮箱地址, `abcdefgh`, `abcdefgh` | 注册失败，不写入用户表 |
| BB-11 | 重复邮箱 | 使用新的合法用户名和已存在邮箱注册 | 注册失败，不写入新用户 |
| BB-12 | 密码为空 | `validuser`, `valid@example.com`, ``, `` | 注册失败，不写入用户表 |
| BB-13 | 密码长度小于 8 | `validuser`, `valid@example.com`, `abcdefg`, `abcdefg` | 注册失败，不写入用户表 |
| BB-14 | 密码确认不一致 | `validuser`, `valid@example.com`, `abcdefgh`, `abcdefgi` | 注册失败，不写入用户表 |

### 3.5 黑盒测试执行结果

使用 Flask `test_client` 和临时 `users.db` 执行了代表性用例。自动化测试程序覆盖了重新设计后的部分黑盒用例，并保留了一个综合非法输入代表用例，用于暴露后端校验缺陷。

| 执行测试重点 | 预期结果 | 实际结果 | 结论 |
|---|---|---|---|
| 有效注册代表用例，对应 BB-01 | 有效输入注册成功并插入用户 | HTTP 302，`validuser` 被插入数据库 | 通过 |
| 综合非法输入代表用例，关联 BB-03、BB-08 和 BB-13 | 无效输入应被拒绝 | HTTP 302，`ab / bad-email / short` 仍被插入数据库 | 失败 |
| 重复用户名，对应 BB-06 | 重复用户名应被拒绝 | HTTP 200，数据库中 `validuser` 仍只有 1 条 | 通过 |

### 3.6 黑盒测试发现的缺陷

缺陷编号：D-BB-01

缺陷描述：注册模块创建了 `SignUpForm(request.form)`，但在 `signup()` 中没有调用 `form.validate()` 或 `form.validate_on_submit()`，因此 WTForms 中定义的长度、必填和邮箱格式校验没有真正参与后端判断。测试中，用户名长度为 2、邮箱格式错误、密码长度为 5 的输入仍被写入数据库并登录成功。

影响：无效账户数据可能进入数据库，影响数据质量和后续登录、展示、管理逻辑；同时前端校验若被绕过，后端无法提供有效保护。

建议修复：在处理 POST 请求时先执行表单校验，例如：

```python
form = SignUpForm(request.form)
if request.method == "POST":
    if not form.validate():
        flashMessage(...)
        return render_template(...)
```

## 4. 白盒测试设计：文章创建模块

### 4.1 测试对象

测试对象为 `/createpost` 路由，对应源码 `app/routes/createPost.py`。该模块负责在用户登录后创建文章，并向 `posts` 数据库插入文章记录。

### 4.2 控制流分析

根据源码，`createPost()` 的主要控制流如下：

1. 判断 session 中是否存在 `userName`。
2. 若未登录，则提示需要登录并重定向到登录页。
3. 若已登录，则创建 `CreatePostForm`。
4. 若请求方法为 GET，则渲染创建文章页面。
5. 若请求方法为 POST，则读取标题、标签、内容、封面和分类。
6. 若 `postContent == ""`，则提示内容为空，不插入数据库。
7. 若 `postContent != ""`，则连接文章数据库，插入文章，增加用户积分，提示成功并重定向首页。

### 4.3 覆盖目标

依据白盒测试课件中语句覆盖和分支覆盖的思想，本模块测试目标为：

- 覆盖未登录分支。
- 覆盖已登录 GET 渲染分支。
- 覆盖已登录 POST 但内容为空分支。
- 覆盖已登录 POST 且内容非空的成功创建分支。

由于该函数分支较少，目标为尽可能达到 100% 主要业务分支覆盖。

### 4.4 白盒测试用例

| 用例编号 | 覆盖目标 | 前置条件 | 输入 | 预期结果 |
|---|---|---|---|---|
| WB-01 | 未登录分支 | session 中无 `userName` | GET `/createpost` | 重定向到 `/login/redirect=&createpost` |
| WB-02 | 已登录 + 空内容分支 | session 中 `userName=alice` | POST，`postContent=""` | 不插入文章，返回创建页面 |
| WB-03 | 已登录 + 正常创建分支 | session 中 `userName=alice` | POST，标题、标签、内容、封面、分类均有效 | 插入文章并重定向首页 |
| WB-04 | 已登录 GET 分支 | session 中 `userName=alice` | GET `/createpost` | 渲染创建文章页面 |

### 4.5 白盒测试执行结果

使用 Flask `test_client` 和临时 `posts.db` 执行代表性白盒测试，结果如下：

| 用例编号 | 预期结果 | 实际结果 | 结论 |
|---|---|---|---|
| WB-01 | 未登录时重定向到登录页 | HTTP 302，Location 为 `/login/redirect=&createpost` | 通过 |
| WB-02 | 已登录但内容为空时不插入文章 | HTTP 200，文章表记录数为 0 | 通过 |
| WB-03 | 已登录且输入有效时插入文章并重定向首页 | 抛出 `TypeError: generateurlID() takes 0 positional arguments but 1 was given` | 失败 |

### 4.6 白盒测试发现的缺陷

缺陷编号：D-WB-01

缺陷描述：在 `app/routes/createPost.py` 中，成功创建文章分支调用了：

```python
generateurlID(postTitle)
```

但 `app/utils/generateUrlIdFromPost.py` 中函数定义为：

```python
def generateurlID():
```

该函数不接收任何参数。因此，当用户已登录且提交非空文章内容时，程序进入数据库插入分支，在计算 `urlID` 时触发 `TypeError`，导致文章无法成功创建。

影响：这是文章创建模块的主流程缺陷，会直接阻断核心功能。普通用户即使输入合法文章，也无法完成发布。

建议修复：将调用改为无参数调用：

```python
generateurlID()
```

或修改工具函数定义，使其接收标题并基于标题生成 URL ID。但从当前实现看，`getSlugFromPostTitle(postTitle)` 已负责标题 slug，`generateurlID()` 负责生成随机唯一 ID，因此更直接的修复是删除多余参数。

## 5. 小结

本部分先从项目结构出发，将 FlaskBlog 划分为用户认证、内容发布、评论、搜索分类、管理后台、分析统计、配置、数据库、模板静态资源等主要模块。随后根据风险和测试技术适配性，选择用户注册模块中的 `signup` 工作流进行黑盒测试，选择内容发布模块中的 `createPost` 工作流进行白盒测试。登录、文章编辑、文章删除和后台管理同样存在测试价值，但由于本次作业范围有限，作为后续回归测试候选项记录，而不在本报告中声称已完整覆盖。

黑盒测试采用等价类划分和边界值分析，发现注册路由没有实际调用 WTForms 校验，导致无效输入仍可注册成功。白盒测试采用控制流和分支覆盖思想，发现文章创建成功路径中函数调用参数不匹配，导致核心发布功能抛出异常。这两个缺陷分别对应输入校验风险和主业务流程可靠性风险，建议作为本项目测试报告中的重点缺陷记录。

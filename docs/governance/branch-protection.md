# 分支保护建议

分支保护是防止误操作进入 `main` 的关键设置。第一阶段已经建立基础检查，第二阶段建议在 GitHub 仓库中启用分支保护。

## 用途

分支保护用于确保：

- 所有修改必须经过 Pull Request。
- 自动检查通过后才能合并。
- 至少一名维护者完成审核。
- `main` 不被直接推送覆盖。

## 建议规则

在 GitHub 仓库页面进入：

```text
Settings -> Branches -> Branch protection rules -> Add rule
```

建议配置：

- Branch name pattern: `main`
- Require a pull request before merging: 开启
- Required approvals: `1`
- Dismiss stale pull request approvals when new commits are pushed: 开启
- Require review from Code Owners: 开启
- Require status checks to pass before merging: 开启
- Required status checks: `Markdown and MkDocs`
- Require conversation resolution before merging: 开启
- Do not allow bypassing the above settings: 根据社团维护方式决定
- Restrict who can push to matching branches: 推荐开启，只允许维护者

## 为什么不在仓库里自动完成

分支保护属于 GitHub 仓库设置，不适合直接写进普通代码文件。它也会影响所有维护者的权限和合并方式，因此应由仓库管理员在 GitHub 设置页面确认后开启。

## CODEOWNERS 关系

本仓库使用 `.github/CODEOWNERS` 指定默认审核责任人。只有在分支保护中开启 `Require review from Code Owners` 后，CODEOWNERS 才会成为阻塞合并的规则。

如果后续有多个教学负责人，可以把 CODEOWNERS 改成更细粒度：

```text
/docs/web/ @web-reviewer
/labs/ @lab-reviewer
/scripts/ @automation-reviewer
```

当前仓库先使用 `@QXMRX` 作为默认维护者，保持流程简单。

## 如何测试

开启后，可以用一个测试 Pull Request 验证：

- 直接向 `main` 推送应被拒绝。
- 未通过 `Basic Checks` 时不能合并。
- 没有维护者审核时不能合并。
- 新提交推送后旧审核会失效。

## 如何维护

每次新增 GitHub Actions 检查后，都应评估是否把对应 job 加入 required status checks。不要一次性把不稳定检查设为必需，否则会阻塞正常教学资料更新。

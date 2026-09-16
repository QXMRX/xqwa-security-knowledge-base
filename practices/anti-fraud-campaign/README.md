# 反诈宣传活动

面向校园场景的反诈宣传单页活动。本目录既是活动资产，也是这次活动的实践记录：记录页面内容怎么组织、为什么最后选了这条发布链路、以及投放前如何核验。

## 当前状态

| 项目 | 内容 |
| --- | --- |
| 活动状态 | 宣传页已完成，等待正式投放 |
| 页面源文件 | `practices/anti-fraud-campaign/index.html` |
| 页面类型 | 单文件静态页，内联样式与脚本，不收集任何个人信息 |
| 发布方式 | 并入 GitHub Pages 站点，构建时发布到 `/practices/anti-fraud-campaign/` |

## 活动目标

面向计算机系新生和还不熟悉网络安全的同学，把“遇到陌生信息先停下来核验”变成当场就能执行的动作，而不是泛泛提醒“注意防骗”。

页面只承担三件事：给出三不原则、给出一条可执行的核验路径、给出已经造成损失时的求助方向。

## 页面内容结构

1. 首屏：主张“先停一秒，再做决定”，配三不原则摘要。
2. 三不原则：不扫描陌生二维码、不轻信自称客服或官方的来电私信、不透露验证码与身份与银行卡信息。
3. 风险提示位：说明已公开高危漏洞（常称 1day）的现实风险，并明确要求发布前由负责老师或技术人员从厂商安全公告、国家信息安全漏洞库或 CISA KEV 目录核验受影响产品、补丁版本和更新时间，不转发未证实的“紧急漏洞”消息。
4. 核验动作：中断操作、从应用商店或官网自行进入官方入口、保留聊天与转账记录并联系银行与公安机关。
5. 求助入口：按钮展开提示，引导拨打 110 或前往就近公安机关报案，并提示不要把验证码、密码或远程控制权限交给任何人。

页面不出现学校、社团或其他组织名称，这在个人备案或纯静态投放场景下可以减少额外的主体审核要求。

## 为什么最后没有用对象存储默认域名

最初的方案是把页面放进对象存储，拿默认域名当二维码地址。实测发现这条路走不通：

- 默认域名访问 HTML 时返回 `Content-Disposition: attachment` 和 `x-oss-force-download: true`，浏览器按下处理，扫码结果是“下载文件”而不是打开网页。
- 这两个响应头不随客户端变化：用微信 UA（`MicroMessenger`）请求，结果与普通浏览器完全一致。
- `x-oss-force-download` 是厂商保留的响应头，无法通过对象元数据设置或清除。
- 即使配置了默认首页让根地址返回 200，根地址仍然带强制下载标记，所以“指向目录根”也绕不过去。
- 绑定自定义域名可以解决，但要求域名已完成 ICP 备案；备案还要求账号下有符合条件的云服务器、周期以周计，且备案期间域名不能对外提供访问。

改并入现有 GitHub Pages 站点后，返回 `text/html` 且没有强制下载标记，扫码直接渲染页面。

## 发布链路

- 页面源文件放在本目录，由 `scripts/build_pages_site.py` 在构建时发布到 `_site/practices/anti-fraud-campaign/`。
- 页面文件缺失时构建直接失败，不会静默发布一个缺少该页的站点。
- `.github/workflows/deploy-pages.yml` 的 `paths` 包含 `practices/**`，改动本目录会触发重新部署。
- 对外地址：`https://qxmrx.github.io/xqwa-security-knowledge-base/practices/anti-fraud-campaign/`

## 投放前核验

```bash
URL=https://qxmrx.github.io/xqwa-security-knowledge-base/practices/anti-fraud-campaign/

# 1. 能直接打开，且不是下载
curl -sS -D - -o /dev/null "$URL" | grep -iE '^HTTP/|content-type|content-disposition|force-download'

# 2. 线上内容与仓库源文件逐字节一致（改完忘记部署会被这一步抓到）
curl -sS "$URL" | shasum -a 256
shasum -a 256 practices/anti-fraud-campaign/index.html

# 3. 用微信实测：把地址发到“文件传输助手”，点开后应直接渲染页面
```

判定标准：返回 `200`；`Content-Type` 为 `text/html; charset=utf-8`；**不出现** `Content-Disposition` 与 `x-oss-force-download`；两侧 SHA-256 相同。任何一条不满足，就不要把地址印到二维码上。

## 合规与安全清单

- 页面不收集任何个人信息，无表单、无后端、无统计脚本。
- 唯一外部链接是 CISA 已知在野利用漏洞目录，使用 `rel="noreferrer"` 且在新标签打开。
- 页脚保留免责声明：本页面用于反诈宣传，不替代执法机关、金融机构或软件厂商的正式公告。
- 若后续改用自有域名并启用备案，需注意备案主体与内容性质的一致性；页面一旦加入学校或社团名称，个人备案可能被要求转为单位备案。
- 不把登录 Cookie、AccessKey、SSH 私钥或控制台密码放进仓库、聊天记录或二维码文案。

## 维护方式

1. 改文案：编辑 `practices/anti-fraud-campaign/index.html`。
2. 本地验证：`python scripts/check_all.py` 与 `mkdocs build --strict`。
3. 合并到 `main` 后自动触发 Pages 部署。
4. 按“投放前核验”重新确认地址可用，再更新二维码。

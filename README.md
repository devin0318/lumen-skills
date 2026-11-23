# Lumen Skills

无需 GitHub 账号即可从 Releases 下载安装包，公开仓库支持匿名 HTTPS 克隆和拉取。Lumen 团队的项目技能。当前发布 **Lumen CBSA 2.0.0**，业务依据为 **Lumen CBSA 业务知识库 v2.0**。装好后选中技能，直接聊球房办赛、业务规则、产品需求、进度或研发工作；输入 `help` 查看示例和实际加载的版本。

[下载团队安装包和说明](https://github.com/devin0318/lumen-skills/releases/tag/lumen-cbsa-v2.0.0) · [各客户端安装、更新与旧版卸载](使用指南.md) · [打开业务知识库首页](<plugins/lumen-cbsa/skills/lumen-cbsa/references/00 首页 · Lumen CBSA v2.0.md>)

## 发到群里

> Lumen CBSA 更新了，附件是安装包和说明。这版用的是 CBSA 业务知识库 v2.0。装好后在对话里选 lumen-cbsa，直接说你手头的事就行，比如“球房中途换台，前面打的比分怎么算？”也可以把需求文档交给它一起看。输入 help 能看到版本，应该是 Skill 2.0.0、知识库 v2.0。以前装过 lumen 的，确认新版能用后，按说明最后一节把旧版移走。

## 维护和发布

- Obsidian 中的项目知识库保存业务原稿。这个仓库保存团队可以分发的版本。工作区知识库管理员按发布日期选定首页和专题；编辑 `plugins/lumen-cbsa/skills/lumen-cbsa/` 中的发布副本，使用包内相对链接。保留上游资料名和章节号，内部飞书原件链接只留在团队知识库。发布前扫描整个仓库与 ZIP，检查私有文档链接和凭据。
- **术语只有一个入口**，即 [术语](plugins/lumen-cbsa/skills/lumen-cbsa/references/术语.md)。这版在 v2.0 条目中补上旧称，将旧字典里仍有用的对接词放回同一页。下次拿到新版术语时逐条对齐：已覆盖的并入现行条目，别名放在同一行，新增词注明业务场景；遇到冲突查专题、决策和待确认事项。保留旧编号只是为了读懂历史材料。不要用整页复制覆盖已合并词条。
- 保持 `lumen-cbsa` 名称稳定。发布时统一更新技能入口、Claude 和 Codex 的插件清单版本、使用指南里的版本与下载链接，并标明本次知识依据。维护多个项目时，每个项目占用 `plugins/lumen-项目简称/` 下的独立目录，分别登记到两个市场清单。
- 从新包试问“人工续赛的胜负能否晋级，C 档比分能否计战力”，再问一个待确认问题，例如提前公布签表后的种子档位。核对答案引用的专题以及 `help` 版本；从新目录验证 ZIP 可打开、市场可发现技能。
- 运行 `python3 tools/package.py <仓库外的输出目录>` 生成可发群的 ZIP 和 Markdown 指南。发布已核对的内容到 `main`，在同一版本创建 `lumen-cbsa-v版本号` 标签与 GitHub Release，上传两个附件。团队市场跟踪 `main`，具体同步时机见使用指南；安装 ZIP 的同事可从 Releases 换版。

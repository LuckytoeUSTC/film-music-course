# 制作源文件

`slides.json`保存23页内容、讲者、讲稿、时间预算和来源编号，`sources.json`保存链接。文本可直接修改，PPT文字也可在PowerPoint中编辑。

制作流程：

1. `build_media.py`提取书签与静帧，`extra_frames.py`补充对照画面。
2. `make_clips.py`从D盘资源截取带余量样片和对应SRT，`prepare_portable.py`生成720p/SDR、英语原声、字幕烧录的交付视频。
3. `build_deck.mjs`用Artifact Tool导出候选PPT与预览，`embed_media.py`加入原生嵌入媒体，`finalize.mjs`执行结构、几何、字体和重新导入检查。
4. `verify_powerpoint.ps1`只读打开本次PPT并导出逐页PNG与PDF，`verify_media.py`完整解码媒体。
5. `build_delivery.py`生成讲稿与离线HTML，`contact.py`、`slide_contact.py`仅生成检查用总览。

当前脚本使用本机依赖与D盘原片路径，需要按使用环境调整。不是安装包，不建议不看内容直接批量重跑。PPT最终输出不覆盖已有文件，修改后应另用修订文件名。

`signal_match.py`是探索性频谱候选检索，存在错误匹配。其结果不作为配乐署名、旋律一致性或音乐起止的证据。

所有构建缓存留在本地build目录。制作过程中未更改D盘电影、原声、字幕或PBF原件。整理脚本仅是本次操作记录，不是日常清理命令。

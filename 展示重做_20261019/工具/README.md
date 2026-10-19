# 重做版制作源文件

slides.json保存28页文字、讲稿notes、排练备忘prep、媒体文件名、来源编号与时间预算。sources.json保存来源。

- author_content.py是本次重构的内容快照生成脚本，使用上一版源稿作为部分语料；日常修订直接编辑slides.json，勿无意覆盖手工修改。
- build_deck.mjs通过Artifact Tool构建候选PPT和PNG；embed_media.py添加12个原生嵌入媒体；finalize.mjs检查后发布新文件，不覆盖已有文件。
- build_delivery.py生成双人讲稿、标题大纲、离线HTML和媒体回放页。
- verify_powerpoint.ps1通过PowerPoint只读打开、导出PDF和逐页图片。

build是本地中间目录，不上传。D盘原片和原声只读。重复配乐图片用于对应音频比较；没有生成影片画面。新提取音频为01、02、03、06各曲开头35/30/30/30秒；AAC192k，仅取音轨，原封面与原件保留。

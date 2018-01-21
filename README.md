<h1 align=center><img src="./Resource/Banner.png" alt="CDrawDemoView"></h1>

<p align="center">
    <a href="./CHANGELOG"><img alt="Version" src="https://img.shields.io/badge/version-0.4.0-brightgreen.svg"/></a>
    <a href="https://lucka.moe"><img alt="Author" src="https://img.shields.io/badge/author-Lucka-5880C8.svg"/></a>
    <a href="https://python.org"><img alt="Python" src="https://img.shields.io/badge/python-3.5-ffDE57.svg"/></a>
    <a href="./LICENSE"><img alt="Author" src="https://img.shields.io/badge/licence-MIT-A31F34.svg"/></a>
</p>
<p align="center">
    iTunes 音乐库分析工具
</p>

## Functions
扫描 XML 格式的 iTunes 音乐库文件，生成 `.data` 数据，对比历史数据，生成报告。

歌曲的下列信息将被记录：

| Key Name      | Description
| :------------ | :----------
| `trackID`     | 歌曲唯一序列号
| `totalTime`   | 歌曲时长
| `discNumber`  | 光盘序号
| `trackNumber` | 音轨序号
| `year`        | 歌曲发行年份
| `dateAdded`   | 加入音乐库的时间
| `playCount`   | 播放次数
| `name`        | 歌曲标题
| `artist`      | 艺术家
| `albumArtist` | 专辑艺术家<sup>`0.3.0`</sup>
| `album`       | 专辑名称
| `genre`       | 音乐类型<sup>`0.2.0`</sup>
| `location`    | 音频文件路径<sup>`0.2.0`</sup>

专辑的下列信息将被记录：

| Key Name     | Description
| :----------- | :----------
| `albumID`    | 专辑唯一序列号
| `totalTime`  | 专辑总时长
| `name`       | 专辑
| `artist`     | 专辑艺术家<sup>`0.3.0`</sup>
| `trackCount` | 音轨数量
| `dateAdded`  | 加入音乐库的时间
| `playCount`  | 总播放次数
| `playTime`   | 总播放时长<sup>`0.2.1`</sup>

单个音乐库的报告内容包括以下内容：

* 歌曲总数、专辑总数、总时长
* 总播放次数、总播放时长
* 播放次数和播放时长的 TOP 10 列表（分歌曲和专辑）

两个音乐库对比的报告内容包括以下内容：

* 新增歌曲数、新增专辑数
* 期间播放次数、期间播放时长
* 期间播放次数和播放时长的 TOP 10 列表（分歌曲和专辑）

对于旧的数据可进行版本和基本信息如歌曲名称的更新。

## Requirements
### Environment
  * Python 3.5

### Files
| Filename                 | Note
| :----------------------- | :---
| iTunes Music Library.xml | iTunes 音乐库文件

## Useage
本工具需要通过命令行参数使用。

生成的 `.data` 数据储存在 `./Library` 文件夹中。

### Command Line Option List
| Opt / Long Opt   | Args / Opt   | Note
| :--------------- | :----------- | :---
| `-a` `--add`     |              | 扫描新的 iTunes 音乐库 XML 文件并保存数据
| `-r` `--report`  | `<filename>` | 生成指定音乐库记录的报告
| `-c` `--compare` | `<filename>` | 比较当前音乐库和过去指定音乐库记录并生成报告
| `-u` `--update`  | `<filename>` | 更新制定记录的数据文件
|                  | `--force`    | 强制升级<sup>`0.3.1`</sup>
|                  | `--auto`     | 对于疑似相同歌曲进行自动确认<sup>`0.3.1`</sup>
| `-h` `--help`    |              | 显示帮助文本

## Licence
本工具基于 [MIT 协议](./LICENSE)。

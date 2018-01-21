# Changelog
## [0.4.0] - 2018-01-19
### Version
| File    | Version
| :------ | :------
| `.data` | 0.3.0

### Changed
- 从 [lucka-me/toolkit](https://github.com/lucka-me/toolkit) 分离
- 更名为 LiAna
- 代码模块化，整合数据升级工具

### Fixed
- 对比记录时歌曲匹配可能会中断

## [0.3.1] - 2018-01-14
### Version
| Tool / File      | Version
| :--------------- | :------
| Data Update Tool | 0.3.1
| `.data`          | 0.3.0

### Added
- 数据更新工具在匹配歌曲时将提示疑似相同歌曲，由供用户决定是否作为相同歌曲更新
  - 自动确认命令 `--auto`
- 数据更新工具增加强制更新命令 `--force`

### Changed
- 优化代码
- 清除测试代码

## [0.3.0] - 2018-01-13
### Version
| Tool / File      | Version
| :--------------- | :------
| Data Update Tool | 0.3.0
| `.data`          | 0.3.0

### Added
- 音乐记录中增加以下项目：

| Key Name      | Description
| :------------ | :----------
| `albumArtist` | 专辑艺术家

- 专辑记录中增加以下项目：

| Key Name | Description
| :------- | :----------
| `artist` | 专辑艺术家

### Changed
- 因为 `trackID` 存在问题，暂时用歌曲名称和专辑名称作为匹配的要素
- 暂时取消 `trackID` 的偏差检测

### Fixed
- 被删除歌曲的 `trackID` 可能被新添加歌曲使用，造成对比记录时出现严重的统计错误
- 被删除又重新加入的歌曲在对比记录时会被统计两次
- 当发生变化的歌曲和专辑少于10个时会出现错误

## [0.2.2] - 2018-01-13
### Version
| Tool / File      | Version
| :--------------- | :------
| Data Update Tool | 0.2.2
| `.data`          | 0.2.1

### Changed
- 专辑添加时间取其歌曲添加时间中最早的一个
- 对比音乐库记录时偏差检测的次数增加为5次

## [0.2.1] - 2018-01-12
### Version
| Tool / File      | Version
| :--------------- | :------
| Data Update Tool | 0.2.1
| `.data`          | 0.2.1

### Added
- 专辑记录中增加以下项目：

| Key Name   | Description
| :--------- | :----------
| `playTime` | 总播放时长

### Fixed
- 专辑总播放时长计算错误

## [0.2.0] - 2018-01-12
### Version
| Tool / File      | Version
| :--------------- | :------
| Data Update Tool | 0.2.0
| `.data`          | 0.2.0

### Added
- 歌曲记录中增加以下项目：

| Key Name   | Description
| :--------- | :----------
| `genre`    | 音乐类型
| `location` | 音频文件路径

- 对记录进行版本管理
- 独立的数据更新工具，用于将较旧的记录更新为新版 LibraryAnaly 可读的格式
- 主函数

### Changed
- 更新注释和代码内文档

## [0.1.1] - 2018-01-12
### Fixed
- 对比记录时未将新增歌曲和专辑的播放次数和总播放时间计算在内

## [0.1.0] - 2018-01-03
- 首个基础功能完整的版本

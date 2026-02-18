# 数据库清理计划

## 总结
- **总表数**: 31个
- **空表数**: 10个
- **可安全删除的表**: 7个
- **可安全删除的字段**: 20个

## 一、可以安全删除的空表

### Culture应用（4个表）
1. **culture_interactiveexercise** (0条记录)
   - 原因：互动练习功能未实现
   - 影响：无，小程序不使用此功能

2. **culture_exerciseattempt** (0条记录)
   - 原因：依赖于互动练习表
   - 影响：无

3. **culture_userprogress** (0条记录)
   - 原因：进度追踪未使用
   - 影响：无，小程序不使用

4. **culture_favorite** (0条记录)
   - 原因：小程序使用本地存储(wx.getStorageSync)而非API
   - 影响：无

### Question应用（1个表）
5. **question_examcomment** (0条记录)
   - 原因：考试评论功能未实现
   - 影响：无

### User应用（2个表）
6. **user_user_groups** (0条记录)
   - 原因：Django自带的用户组功能，未使用
   - 影响：无

7. **user_user_user_permissions** (0条记录)
   - 原因：Django自带的用户权限功能，未使用
   - 影响：无

## 二、不存在的表（模型定义但未创建表）

以下模型在user/study_models.py中定义，但表不存在：
- user_studygoal
- user_studystatistics  
- user_studysession
- user_achievementbadge
- user_userachievement
- user_studyreport

**处理方案**：删除study_models.py文件，或者运行makemigrations创建表

## 三、可以删除的字段

### Question应用
1. **question_questioncategory表**
   - `parent_category` - 未使用（0/17）
   - `level_range` - 未使用（0/17）

2. **question_questionset表**
   - `listening_audio_duration` - 未使用（0/16）

3. **question_question表**
   - `audio_file` - 未使用（0/547）
   - `audio_duration` - 未使用（0/547）
   - `image_file` - 未使用（0/547）

### University应用
4. **university_university表**
   - `logo_url` - 未使用（0/10）
   - `campus_image_url` - 未使用（0/10）

### Culture应用
5. **culture_category表**
   - `description_en` - 未使用（0/6）

6. **culture_content表**
   - `audio_url` - 未使用（0/13）
   - `like_count` - 未使用（0/13）

### User应用
7. **user_user表**
   - `first_name` - 未使用（0/7）
   - `last_name` - 未使用（0/7）
   - `english_name` - 未使用（0/7）
   - `phone` - 未使用（0/7）
   - `avatar` - 未使用（0/7）
   - `total_correct_count` - 未使用（0/7）
   - `total_score` - 未使用（0/7）

### HSK_INFO应用
8. **hsk_info_studyguide表**
   - `resources` - 未使用（0/1）

9. **hsk_info_faq表**
   - `related_links` - 未使用（0/2）
   - `view_count` - 未使用（0/2）

## 四、清理执行顺序

### 阶段1：删除未使用的模型和空表
1. 删除culture应用中的4个空表模型
2. 删除question应用中的examcomment模型
3. 删除或修复user应用中的study_models

### 阶段2：删除未使用的字段
1. 从模型中移除未使用的字段
2. 创建并执行迁移

### 阶段3：验证
1. 运行测试确保系统正常
2. 检查前端功能是否正常

## 五、预期效果
- 减少数据库表：从31个到24个
- 清理未使用字段：约20个字段
- 简化模型定义，提高代码可维护性
- 加快数据库查询速度

## 六、风险评估
- ✅ 低风险：删除空表和未使用字段
- ⚠️ 中风险：确保前端代码不依赖这些字段
- ✅ 已验证：小程序收藏使用本地存储，不使用API

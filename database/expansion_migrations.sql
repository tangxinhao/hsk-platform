-- HSK备考系统扩展 - 数据库迁移脚本
-- 执行前请确保已备份数据库
-- 执行: mysql -u root -p hsk_learning < expansion_migrations.sql

USE hsk_learning;

-- ============================================
-- 1. 扩展用户表字段
-- ============================================

ALTER TABLE user_user 
ADD COLUMN IF NOT EXISTS learning_goal VARCHAR(50) DEFAULT '' COMMENT '学习目标',
ADD COLUMN IF NOT EXISTS target_hsk_level INT DEFAULT 1 COMMENT '目标HSK等级',
ADD COLUMN IF NOT EXISTS preferred_regions JSON COMMENT '偏好地区',
ADD COLUMN IF NOT EXISTS preferred_majors JSON COMMENT '偏好专业',
ADD COLUMN IF NOT EXISTS budget DECIMAL(10,2) COMMENT '学费预算',
ADD COLUMN IF NOT EXISTS study_time_per_day INT DEFAULT 30 COMMENT '每日学习时长(分钟)';

-- ============================================
-- 2. 学习统计相关表
-- ============================================

-- 学习目标表
CREATE TABLE IF NOT EXISTS user_study_goal (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    target_hsk_level INT NOT NULL COMMENT '目标HSK等级',
    target_date DATE NOT NULL COMMENT '目标日期',
    daily_practice_count INT DEFAULT 10 COMMENT '每日练习目标',
    current_progress INT DEFAULT 0 COMMENT '当前进度',
    is_completed BOOLEAN DEFAULT FALSE COMMENT '是否完成',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_target_date (target_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学习目标表';

-- 学习统计表（按日期聚合）
CREATE TABLE IF NOT EXISTS user_study_statistics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    date DATE NOT NULL COMMENT '统计日期',
    practice_count INT DEFAULT 0 COMMENT '练习次数',
    correct_count INT DEFAULT 0 COMMENT '正确次数',
    study_time INT DEFAULT 0 COMMENT '学习时长(分钟)',
    points_earned INT DEFAULT 0 COMMENT '获得积分',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_date (user_id, date),
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户学习统计表';

-- ============================================
-- 3. 题目和考试相关表
-- ============================================

-- 扩展套卷表
ALTER TABLE question_questionset
ADD COLUMN IF NOT EXISTS is_official BOOLEAN DEFAULT FALSE COMMENT '是否官方试卷',
ADD COLUMN IF NOT EXISTS year INT COMMENT '年份',
ADD COLUMN IF NOT EXISTS attempt_count INT DEFAULT 0 COMMENT '尝试次数',
ADD COLUMN IF NOT EXISTS average_score DECIMAL(5,2) DEFAULT 0 COMMENT '平均分';

-- 音频文件表
CREATE TABLE IF NOT EXISTS question_audio (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question_id INT NULL COMMENT '关联题目',
    question_set_id INT NULL COMMENT '关联套卷',
    file_name VARCHAR(200) NOT NULL COMMENT '文件名',
    file_url VARCHAR(500) NOT NULL COMMENT '文件URL',
    duration INT DEFAULT 0 COMMENT '时长(秒)',
    file_size INT DEFAULT 0 COMMENT '文件大小(字节)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES question_question(id) ON DELETE CASCADE,
    FOREIGN KEY (question_set_id) REFERENCES question_questionset(id) ON DELETE CASCADE,
    INDEX idx_question_id (question_id),
    INDEX idx_question_set_id (question_set_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='音频文件表';

-- 试卷导入记录表
CREATE TABLE IF NOT EXISTS question_paper_import (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '试卷标题',
    hsk_level INT NOT NULL COMMENT 'HSK等级',
    file_path VARCHAR(500) NOT NULL COMMENT '文件路径',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending/processing/completed/failed',
    total_questions INT DEFAULT 0 COMMENT '总题目数',
    imported_questions INT DEFAULT 0 COMMENT '已导入题目数',
    error_log TEXT COMMENT '错误日志',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_hsk_level (hsk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='试卷导入记录表';

-- 考试记录表
CREATE TABLE IF NOT EXISTS question_exam_attempt (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_set_id INT NOT NULL,
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME NULL COMMENT '结束时间',
    score DECIMAL(5,2) DEFAULT 0 COMMENT '得分',
    status VARCHAR(20) DEFAULT 'in_progress' COMMENT '状态: in_progress/completed/abandoned',
    answers JSON COMMENT '答案JSON',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    FOREIGN KEY (question_set_id) REFERENCES question_questionset(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_question_set_id (question_set_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='考试记录表';

-- 考试报告表
CREATE TABLE IF NOT EXISTS question_exam_report (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exam_attempt_id INT NOT NULL UNIQUE,
    total_questions INT NOT NULL COMMENT '总题目数',
    correct_count INT NOT NULL COMMENT '正确数量',
    accuracy_rate DECIMAL(5,2) NOT NULL COMMENT '正确率',
    time_spent INT NOT NULL COMMENT '用时(秒)',
    category_performance JSON COMMENT '分类表现',
    weak_points JSON COMMENT '薄弱知识点',
    suggestions TEXT COMMENT '学习建议',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exam_attempt_id) REFERENCES question_exam_attempt(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='考试报告表';

-- ============================================
-- 4. 院校相关表
-- ============================================

-- 扩展院校表
ALTER TABLE university_university
ADD COLUMN IF NOT EXISTS application_deadline DATE COMMENT '申请截止日期',
ADD COLUMN IF NOT EXISTS dormitory_fee DECIMAL(10,2) COMMENT '住宿费',
ADD COLUMN IF NOT EXISTS living_cost DECIMAL(10,2) COMMENT '生活费预估',
ADD COLUMN IF NOT EXISTS success_rate DECIMAL(5,2) COMMENT '录取成功率(%)',
ADD COLUMN IF NOT EXISTS employment_rate DECIMAL(5,2) COMMENT '就业率(%)';

-- 院校推荐记录表
CREATE TABLE IF NOT EXISTS university_recommendation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    university_id INT NOT NULL,
    match_score DECIMAL(5,2) NOT NULL COMMENT '匹配分数(0-100)',
    reason TEXT COMMENT '推荐理由',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES university_university(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_match_score (match_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='院校推荐记录表';

-- 院校收藏表
CREATE TABLE IF NOT EXISTS university_favorite (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    university_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_university (user_id, university_id),
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES university_university(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='院校收藏表';

-- 申请记录表
CREATE TABLE IF NOT EXISTS university_application (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    university_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'preparing' COMMENT '状态: preparing/submitted/admitted/rejected',
    notes TEXT COMMENT '备注',
    submitted_at DATETIME NULL COMMENT '提交时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES university_university(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='申请记录表';

-- ============================================
-- 5. 文化学习相关表
-- ============================================

-- 文化测验表
CREATE TABLE IF NOT EXISTS culture_quiz (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '测验标题',
    description TEXT COMMENT '描述',
    category_id INT NOT NULL,
    difficulty INT DEFAULT 3 COMMENT '难度(1-5)',
    time_limit INT DEFAULT 30 COMMENT '时间限制(分钟)',
    pass_score INT DEFAULT 60 COMMENT '及格分数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES culture_category(id) ON DELETE CASCADE,
    INDEX idx_category_id (category_id),
    INDEX idx_difficulty (difficulty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文化测验表';

-- 测验尝试记录表
CREATE TABLE IF NOT EXISTS culture_quiz_attempt (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    quiz_id INT NOT NULL,
    score INT NOT NULL COMMENT '得分',
    is_passed BOOLEAN DEFAULT FALSE COMMENT '是否通过',
    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES culture_quiz(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_quiz_id (quiz_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测验尝试记录表';

-- 学习证书表
CREATE TABLE IF NOT EXISTS culture_certificate (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    certificate_number VARCHAR(50) UNIQUE NOT NULL COMMENT '证书编号',
    issue_date DATE NOT NULL COMMENT '颁发日期',
    certificate_url VARCHAR(500) COMMENT '证书图片URL',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES culture_category(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_certificate_number (certificate_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学习证书表';

-- ============================================
-- 6. 系统管理相关表
-- ============================================

-- 系统通知表
CREATE TABLE IF NOT EXISTS system_notification (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '通知标题',
    content TEXT NOT NULL COMMENT '通知内容',
    type VARCHAR(20) DEFAULT 'info' COMMENT '类型: info/warning/important',
    target_users VARCHAR(20) DEFAULT 'all' COMMENT '目标用户: all/specific_level/specific_users',
    target_filter JSON COMMENT '目标筛选条件',
    is_published BOOLEAN DEFAULT FALSE COMMENT '是否已发布',
    published_at DATETIME NULL COMMENT '发布时间',
    created_by INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES user_user(id) ON DELETE CASCADE,
    INDEX idx_is_published (is_published),
    INDEX idx_published_at (published_at),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统通知表';

-- 用户通知阅读记录表
CREATE TABLE IF NOT EXISTS user_notification_read (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    notification_id INT NOT NULL,
    read_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_notification (user_id, notification_id),
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE CASCADE,
    FOREIGN KEY (notification_id) REFERENCES system_notification(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户通知阅读记录表';

-- 系统操作日志表
CREATE TABLE IF NOT EXISTS system_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NULL,
    action VARCHAR(50) NOT NULL COMMENT '操作',
    module VARCHAR(50) NOT NULL COMMENT '模块',
    details TEXT COMMENT '详情',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent VARCHAR(500) COMMENT 'User Agent',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_module (module),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统操作日志表';

-- ============================================
-- 7. 插入示例数据（可选）
-- ============================================

-- 插入一些分类数据
INSERT IGNORE INTO question_questioncategory (name, description) VALUES
('vocabulary', '词汇'),
('reading', '阅读'),
('listening', '听力'),
('writing', '写作'),
('grammar', '语法'),
('comprehensive', '综合')
ON DUPLICATE KEY UPDATE name=name;

-- ============================================
-- 8. 创建视图（用于统计查询）
-- ============================================

-- 用户学习统计视图
CREATE OR REPLACE VIEW v_user_statistics AS
SELECT 
    u.id AS user_id,
    u.username,
    u.hsk_level,
    u.total_practice_count,
    u.total_correct_count,
    CASE 
        WHEN u.total_practice_count > 0 
        THEN ROUND(u.total_correct_count * 100.0 / u.total_practice_count, 2)
        ELSE 0 
    END AS accuracy_rate,
    COUNT(DISTINCT DATE(ar.created_at)) AS study_days,
    COUNT(DISTINCT wb.id) AS wrong_count
FROM user_user u
LEFT JOIN question_answerrecord ar ON u.id = ar.user_id
LEFT JOIN question_wrongbook wb ON u.id = wb.user_id
GROUP BY u.id;

-- 题目统计视图
CREATE OR REPLACE VIEW v_question_statistics AS
SELECT 
    q.id AS question_id,
    q.type,
    q.level,
    q.difficulty,
    qc.name AS category_name,
    COUNT(ar.id) AS attempt_count,
    SUM(CASE WHEN ar.is_correct THEN 1 ELSE 0 END) AS correct_count,
    CASE 
        WHEN COUNT(ar.id) > 0 
        THEN ROUND(SUM(CASE WHEN ar.is_correct THEN 1 ELSE 0 END) * 100.0 / COUNT(ar.id), 2)
        ELSE 0 
    END AS correct_rate
FROM question_question q
LEFT JOIN question_answerrecord ar ON q.id = ar.question_id
LEFT JOIN question_questioncategory qc ON q.category_id = qc.id
GROUP BY q.id;

-- 院校热度统计视图
CREATE OR REPLACE VIEW v_university_popularity AS
SELECT 
    u.id AS university_id,
    u.name,
    u.region,
    u.ranking_national,
    COUNT(DISTINCT uf.user_id) AS favorite_count,
    COUNT(DISTINCT ur.user_id) AS recommend_count,
    COUNT(DISTINCT ua.user_id) AS application_count
FROM university_university u
LEFT JOIN university_favorite uf ON u.id = uf.university_id
LEFT JOIN university_recommendation ur ON u.id = ur.university_id
LEFT JOIN university_application ua ON u.id = ua.university_id
GROUP BY u.id
ORDER BY favorite_count DESC, recommend_count DESC;

-- ============================================
-- 9. 创建存储过程（用于复杂操作）
-- ============================================

-- 更新用户学习统计的存储过程
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS update_user_study_statistics(
    IN p_user_id INT,
    IN p_date DATE,
    IN p_practice_count INT,
    IN p_correct_count INT,
    IN p_study_time INT,
    IN p_points_earned INT
)
BEGIN
    INSERT INTO user_study_statistics 
        (user_id, date, practice_count, correct_count, study_time, points_earned)
    VALUES 
        (p_user_id, p_date, p_practice_count, p_correct_count, p_study_time, p_points_earned)
    ON DUPLICATE KEY UPDATE
        practice_count = practice_count + p_practice_count,
        correct_count = correct_count + p_correct_count,
        study_time = study_time + p_study_time,
        points_earned = points_earned + p_points_earned,
        updated_at = CURRENT_TIMESTAMP;
END //

DELIMITER ;

-- ============================================
-- 10. 数据完整性检查
-- ============================================

-- 检查新表是否创建成功
SELECT 
    TABLE_NAME, 
    TABLE_COMMENT,
    TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'hsk_learning'
AND TABLE_NAME IN (
    'user_study_goal',
    'user_study_statistics',
    'question_audio',
    'question_paper_import',
    'question_exam_attempt',
    'question_exam_report',
    'university_recommendation',
    'university_favorite',
    'university_application',
    'culture_quiz',
    'culture_quiz_attempt',
    'culture_certificate',
    'system_notification',
    'user_notification_read',
    'system_log'
)
ORDER BY TABLE_NAME;

-- ============================================
-- 迁移完成提示
-- ============================================

SELECT '========================================' AS '';
SELECT '数据库迁移完成！' AS 'Status';
SELECT '请执行以下命令以应用Django模型迁移：' AS 'Next Step';
SELECT 'cd backend && python manage.py makemigrations && python manage.py migrate' AS 'Command';
SELECT '========================================' AS '';

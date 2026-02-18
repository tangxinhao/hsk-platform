-- HSK 用户表
CREATE TABLE user_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(254),
    hsk_level INT DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 题目表
CREATE TABLE question_question (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(20) NOT NULL, -- listening/character
    level INT NOT NULL, -- HSK1-6
    content TEXT NOT NULL,
    audio_url VARCHAR(255),
    image_url VARCHAR(255),
    options JSON NOT NULL,
    answer VARCHAR(255) NOT NULL,
    explanation TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 答题记录表
CREATE TABLE question_answerrecord (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    user_answer VARCHAR(255),
    is_correct BOOLEAN,
    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id),
    FOREIGN KEY (question_id) REFERENCES question_question(id)
);

-- 错题本表
CREATE TABLE question_wrongbook (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id),
    FOREIGN KEY (question_id) REFERENCES question_question(id)
);

-- 院校表
CREATE TABLE university_university (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    ranking INT,
    majors JSON,
    description TEXT
);

-- 文化分类表
CREATE TABLE culture_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    level VARCHAR(10) NOT NULL -- 初级/中级/高级
);

-- 文化内容表
CREATE TABLE culture_content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    cover_image VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES culture_category(id)
);

-- 文化内容收藏表
CREATE TABLE culture_favorite (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content_id INT NOT NULL,
    favorited_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_user(id),
    FOREIGN KEY (content_id) REFERENCES culture_content(id)
);

-- 用户
INSERT INTO user_user (username, password, email, hsk_level, is_active, is_admin) VALUES
('admin', 'pbkdf2_sha256$260000$test$testhash', 'admin@test.com', 6, 1, 1),
('test', 'pbkdf2_sha256$260000$test$testhash', 'test@test.com', 3, 1, 0);

-- 题目
INSERT INTO question_question (type, level, content, audio_url, image_url, options, answer, explanation) VALUES
('listening', 1, '请听音频，选择正确答案', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3', NULL, '["A","B","C"]', 'A', '正确答案是A'),
('character', 2, '请看图片，选择正确汉字', NULL, 'https://img2.baidu.com/it/u=1234567890,1234567890&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500', '["你","我","他"]', '你', '图片内容是"你"');

-- 院校
INSERT INTO university_university (name, region, ranking, majors, description) VALUES
('北京大学', '北京', 1, '["中文","计算机"]', '中国顶尖高校'),
('复旦大学', '上海', 3, '["经济","法学"]', '著名综合性大学');

-- 文化分类
INSERT INTO culture_category (name, description, level) VALUES
('历史', '中国历史相关内容', '初级'),
('文学', '中国文学相关内容', '中级'),
('艺术', '中国艺术相关内容', '高级'),
('节日', '中国传统节日', '初级');

-- 文化内容
INSERT INTO culture_content (category_id, title, content, cover_image) VALUES
(1, '秦始皇与长城', '<p>秦始皇统一中国，修建了著名的长城。</p>', 'https://img2.baidu.com/it/u=2718888888,1234567890&fm=253&fmt=auto&app=138&f=JPEG?w=600&h=400'),
(2, '唐诗宋词', '<p>唐诗宋词是中国文学的瑰宝。</p>', 'https://img2.baidu.com/it/u=2718888888,987654321&fm=253&fmt=auto&app=138&f=JPEG?w=600&h=400'); 
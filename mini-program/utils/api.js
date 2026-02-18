/**
 * API接口定义
 * 统一管理所有API端点
 */

// 不在这里写死完整地址，统一通过 app.globalData.apiBaseUrl 和 request.js 来拼接 /api 前缀
const API_BASE = '/api'

export default {
  // ========== 用户相关 ==========
  USER_LOGIN: '/user/login/',
  USER_REGISTER: '/user/register/',
  USER_INFO: '/user/me/',
  USER_PROGRESS: '/user/progress/',
  USER_DASHBOARD: '/user/dashboard/',
  
  // ========== 题目相关 ==========
  QUESTION_LIST: '/question/questions/',           // GET 获取题目列表
  QUESTION_DETAIL: '/question/questions/{id}/',    // GET 获取题目详情
  QUESTION_CATEGORIES: '/question/categories/',     // GET 获取题目分类
  
  // ========== 试卷相关 ==========
  PAPER_LIST: '/question/question-sets/',           // GET 获取试卷列表
  PAPER_DETAIL: '/question/question-sets/{id}/',   // GET 获取试卷详情
  PAPER_QUESTIONS: '/question/question-sets/{id}/questions/', // GET 获取试卷题目
  
  // ========== 考试相关 ==========
  EXAM_START: '/exam/start/',                       // POST 开始考试
  EXAM_SUBMIT: '/exam/submit/',                     // POST 提交答卷
  EXAM_RESULT: '/exam/attempts/{id}/',              // GET 获取考试结果
  EXAM_HISTORY: '/exam/attempts/',                  // GET 获取考试历史
  
  // ========== 学习辅助 ==========
  WRONG_BOOK: '/user/wrong-book/',                  // GET/POST 错题本
  FAVORITES: '/user/favorites/',                    // GET/POST 收藏夹
  STUDY_HISTORY: '/user/study-history/',            // GET 学习历史
  
  // ========== 大学相关 ==========
  UNIVERSITY_LIST: '/university/',                  // GET 获取大学列表
  UNIVERSITY_DETAIL: '/university/{id}/',           // GET 获取大学详情
  
  // ========== 文化相关 ==========
  CULTURE_LIST: '/culture/',                        // GET 获取文化内容列表
  CULTURE_DETAIL: '/culture/{id}/',                // GET 获取文化内容详情
  
  // ========== HSK信息 ==========
  HSK_LEVELS: '/hsk-info/levels/',                 // GET 获取HSK等级信息
  HSK_OUTLINE: '/hsk-info/outline/',               // GET 获取考试大纲
}

/**
 * 构建完整URL
 * @param {string} path - API路径
 * @param {object} params - 路径参数 {id: 1} => /api/university/1/
 */
export function buildUrl(path, params = {}) {
  let url = path
  Object.keys(params).forEach(key => {
    url = url.replace(`{${key}}`, params[key])
  })
  return url
}

/**
 * 格式化日期时间
 * @param {string} dateStr - ISO格式的日期字符串
 * @returns {string} 格式化后的日期字符串
 */
export function formatDateTime(dateStr) {
  if (!dateStr) return '暂无数据';

  try {
    const date = new Date(dateStr);

    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      return '日期格式无效';
    }

    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    });
  } catch (error) {
    console.error('日期格式化错误:', error);
    return '日期格式化错误';
  }
}

/**
 * 格式化日期（不含时间）
 * @param {string} dateStr - ISO格式的日期字符串
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(dateStr) {
  if (!dateStr) return '暂无数据';

  try {
    const date = new Date(dateStr);

    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      return '日期格式无效';
    }

    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  } catch (error) {
    console.error('日期格式化错误:', error);
    return '日期格式化错误';
  }
} 
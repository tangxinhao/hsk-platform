<template>
  <div class="dashboard-container">
    <h1 class="page-title">管理员Dashboard</h1>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon user-icon">
              <i class="el-icon-user"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboardData.user_stats?.total_users || 0 }}</div>
              <div class="stat-label">总用户数</div>
              <div class="stat-trend">
                <span class="trend-text">最近7天新增: {{ dashboardData.user_stats?.new_users_7d || 0 }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon question-icon">
              <i class="el-icon-document"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboardData.question_stats?.total_questions || 0 }}</div>
              <div class="stat-label">题目总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon practice-icon">
              <i class="el-icon-edit"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboardData.practice_stats?.practice_7d || 0 }}</div>
              <div class="stat-label">最近7天练习</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon exam-icon">
              <i class="el-icon-files"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboardData.exam_stats?.total_exams || 0 }}</div>
              <div class="stat-label">考试总数</div>
              <div class="stat-trend">
                <span class="trend-text">平均分: {{ dashboardData.exam_stats?.average_score || 0 }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <!-- 系统活跃度趋势 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统活跃度趋势</span>
            </div>
          </template>
          <div ref="activityChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      
      <!-- 用户HSK等级分布 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>用户HSK等级分布</span>
            </div>
          </template>
          <div ref="levelChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="charts-row">
      <!-- 题目数量分布 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>题目数量分布</span>
            </div>
          </template>
          <div ref="questionChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      
      <!-- 热门文化内容 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>热门文化内容 Top 10</span>
            </div>
          </template>
          <el-table :data="popularContent" style="width: 100%" max-height="300">
            <el-table-column prop="title" label="标题" width="200" />
            <el-table-column prop="view_count" label="浏览量" width="100" />
            <el-table-column prop="like_count" label="点赞数" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 热门套卷 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>热门套卷 Top 10</span>
            </div>
          </template>
          <el-table :data="popularSets" style="width: 100%">
            <el-table-column prop="title" label="套卷标题" />
            <el-table-column prop="level" label="HSK等级" width="100">
              <template #default="scope">
                <el-tag>HSK{{ scope.row.level }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="attempt_count" label="尝试次数" width="120" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'DashboardPage',
  data() {
    return {
      dashboardData: {},
      loading: true
    };
  },
  computed: {
    popularContent() {
      return this.dashboardData.culture_stats?.popular_content || [];
    },
    popularSets() {
      return this.dashboardData.exam_stats?.popular_sets || [];
    }
  },
  mounted() {
    this.loadDashboardData();
  },
  beforeUnmount() {
    // 清理事件监听器
    if (this._chartResizeHandler) {
      window.removeEventListener('resize', this._chartResizeHandler);
    }
  },
  methods: {
    async loadDashboardData() {
      try {
        this.loading = true;
        
        // 验证token是否存在
        const token = localStorage.getItem('token');
        if (!token) {
          this.$message.error('请先登录');
          this.$router.push('/login');
          return;
        }
        
        const response = await axios.get('/user/admin-dashboard/', {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          timeout: 30000  // 30秒超时
        });
        
        // 验证响应数据
        if (!response.data) {
          throw new Error('响应数据为空');
        }
        
        this.dashboardData = response.data;
        
        // 渲染图表
        this.$nextTick(() => {
          this.renderActivityChart();
          this.renderLevelChart();
          this.renderQuestionChart();
        });
      } catch (error) {
        console.error('加载Dashboard数据失败:', error);
        
        // 根据错误类型显示不同提示
        if (error.response) {
          // 服务器返回错误
          if (error.response.status === 401) {
            this.$message.error('登录已过期，请重新登录');
            this.$router.push('/login');
          } else if (error.response.status === 403) {
            this.$message.error('没有访问权限');
          } else if (error.response.status >= 500) {
            this.$message.error('服务器错误，请稍后重试');
          } else {
            this.$message.error('加载数据失败');
          }
        } else if (error.request) {
          // 请求发送但没有收到响应
          this.$message.error('网络错误，请检查网络连接');
        } else {
          // 其他错误
          this.$message.error('加载数据失败');
        }
      } finally {
        this.loading = false;
      }
    },
    
    renderActivityChart() {
      if (!this.$refs.activityChart) {
        return;
      }
      
      const chart = echarts.init(this.$refs.activityChart);
      const activityData = this.dashboardData.activity_data || [];
      
      // 数据验证
      if (!Array.isArray(activityData) || activityData.length === 0) {
        chart.showLoading();
        return;
      }
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: ['练习次数', '考试次数', '活跃用户']
        },
        xAxis: {
          type: 'category',
          data: activityData.map(item => item.date)
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '练习次数',
            type: 'line',
            data: activityData.map(item => item.practice_count),
            smooth: true
          },
          {
            name: '考试次数',
            type: 'line',
            data: activityData.map(item => item.exam_count),
            smooth: true
          },
          {
            name: '活跃用户',
            type: 'line',
            data: activityData.map(item => item.active_users),
            smooth: true
          }
        ]
      };
      
      chart.setOption(option);
      chart.hideLoading();
      
      // 响应式（防止重复绑定）
      const resizeHandler = () => {
        if (chart && !chart.isDisposed()) {
          chart.resize();
        }
      };
      
      // 移除旧的监听器（如果存在）
      window.removeEventListener('resize', this._chartResizeHandler);
      this._chartResizeHandler = resizeHandler;
      window.addEventListener('resize', resizeHandler);
    },
    
    renderLevelChart() {
      const chart = echarts.init(this.$refs.levelChart);
      const levelData = this.dashboardData.user_stats?.users_by_level || [];
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'HSK等级',
            type: 'pie',
            radius: '50%',
            data: levelData.map(item => ({
              name: item.level,
              value: item.count
            })),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      
      chart.setOption(option);
      
      window.addEventListener('resize', () => {
        chart.resize();
      });
    },
    
    renderQuestionChart() {
      const chart = echarts.init(this.$refs.questionChart);
      const questionData = this.dashboardData.question_stats?.questions_by_level || [];
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: questionData.map(item => item.level)
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '题目数量',
            type: 'bar',
            data: questionData.map(item => item.count),
            itemStyle: {
              color: '#1a1f2e'
            }
          }
        ]
      };
      
      chart.setOption(option);
      
      window.addEventListener('resize', () => {
        chart.resize();
      });
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333333;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  margin-right: 15px;
}

.user-icon {
  background: #6699CC;
  color: #FFFFFF;
}

.question-icon {
  background: #FF9966;
  color: #FFFFFF;
}

.practice-icon {
  background: #6699CC;
  color: #FFFFFF;
}

.exam-icon {
  background: #99CC99;
  color: #FFFFFF;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333333;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.stat-trend {
  font-size: 12px;
}

.trend-text {
  color: #67C23A;
}

.charts-row {
  margin-bottom: 20px;
}

.card-header {
  font-size: 16px;
  font-weight: bold;
  color: #333333;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #EBEEF5;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>

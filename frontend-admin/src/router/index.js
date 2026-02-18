import { createRouter, createWebHistory } from 'vue-router';
import { ElMessage } from 'element-plus';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue'),
    meta: { title: '登录', public: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage.vue'),
    meta: { title: '首页', requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/DashboardPage.vue'),
    meta: { title: '数据统计', requiresAuth: true }
  },
  {
    path: '/questions',
    name: 'Questions',
    component: () => import('../views/QuestionPage.vue'),
    meta: { title: '题目管理', requiresAuth: true }
  },
  {
    path: '/universities',
    name: 'Universities',
    component: () => import('../views/UniversityPage.vue'),
    meta: { title: '院校管理', requiresAuth: true }
  },
  {
    path: '/culture',
    name: 'Culture',
    component: () => import('../views/CulturePage.vue'),
    meta: { title: '文化管理', requiresAuth: true }
  },
  {
    path: '/exam-sets',
    name: 'ExamSets',
    component: () => import('../views/ExamSetsPage.vue'),
    meta: { title: '套卷管理', requiresAuth: true }
  },
  {
    path: '/mock-exam-questions',
    name: 'MockExamQuestions',
    component: () => import('../views/MockExamQuestionsPage.vue'),
    meta: { title: '模拟考试题目', requiresAuth: true }
  },
  {
    path: '/exam-set/:id/questions',
    name: 'ExamSetQuestions',
    component: () => import('../views/ExamSetQuestionsPage.vue'),
    meta: { title: '题目管理', requiresAuth: true }
  },
  {
    path: '/listening-groups',
    name: 'ListeningGroups',
    component: () => import('../views/ListeningGroupsManagePage.vue'),
    meta: { title: '听力题组管理', requiresAuth: true }
  },
  {
    path: '/listening-group/add',
    name: 'AddListeningGroup',
    component: () => import('../views/ListeningGroupPage.vue'),
    meta: { title: '批量添加听力题组', requiresAuth: true }
  },
  {
    path: '/listening-group/edit/:id',
    name: 'EditListeningGroup',
    component: () => import('../views/ListeningGroupEditPage.vue'),
    meta: { title: '编辑听力题组', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
];

const router = createRouter({
  // 管理端部署在 Nginx 的 /admin-panel/ 子路径下，history base 需要同步设置
  history: createWebHistory('/admin-panel/'),
  routes
});

// 路由守卫 - 检查登录状态
router.beforeEach((to, from, next) => {
  console.log('路由跳转:', from.path, '->', to.path);
  document.title = to.meta.title ? `${to.meta.title} - HSK管理系统` : 'HSK管理系统';

  const token = localStorage.getItem('token');
  
  // 如果需要认证但没有token
  if (to.meta.requiresAuth && !token) {
    ElMessage.warning('请先登录');
    next('/login');
    return;
  }
  
  // 如果已登录且访问登录页，重定向到首页
  if (to.path === '/login' && token) {
    next('/');
    return;
  }
  
  next();
});

export default router; 
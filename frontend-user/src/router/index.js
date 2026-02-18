import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage.vue'),
    meta: { public: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue'),
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterPage.vue'),
    meta: { public: true }
  },
  {
    path: '/about-hsk',
    name: 'AboutHSK',
    component: () => import('../views/AboutHSKPage.vue'),
    meta: { public: true }
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('../views/NewPracticePage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/listening-practice',
    name: 'ListeningPractice',
    component: () => import('../views/ListeningGroupPracticePage.vue'),
    meta: { public: true }
  },
  {
    path: '/exam',
    name: 'Exam',
    component: () => import('../views/ExamPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/:examId',
    name: 'ExamDetail',
    component: () => import('../views/ExamDetailPageNew.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/:examId/old',
    name: 'ExamDetailOld',
    component: () => import('../views/ExamDetailPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/result',
    name: 'ExamResult',
    component: () => import('../views/ExamResultPageNew.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/result/old',
    name: 'ExamResultOld',
    component: () => import('../views/ExamResultPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/progress',
    name: 'Progress',
    component: () => import('../views/ProgressPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wrong-book',
    name: 'WrongBook',
    component: () => import('../views/WrongBookPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/universities',
    name: 'Universities',
    component: () => import('../views/UniversitiesPage.vue'),
    meta: { public: true }
  },
  {
    path: '/university/:id',
    name: 'UniversityDetail',
    component: () => import('../views/UniversityDetailPage.vue'),
    meta: { public: true }
  },
  {
    path: '/culture',
    name: 'Culture',
    component: () => import('../views/CulturePage.vue'),
    meta: { public: true }
  },
  {
    path: '/culture/detail/:id?',
    name: 'CultureDetail',
    component: () => import('../views/CultureDetailPage.vue'),
    meta: { public: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
})

export default router

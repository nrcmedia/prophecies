import Dashboard from '@/views/Dashboard.vue'
import Error from '@/views/Error.vue'
import Login from '@/views/Login.vue'
import HistoryList from '@/views/HistoryList.vue'
import TaskRecordReviewList from '@/views/TaskRecordReviewList.vue'
import TaskRecordReviewRetrieve from '@/views/TaskRecordReviewRetrieve.vue'
import TipList from '@/views/TipList.vue'
import TipRetrieve from '@/views/TipRetrieve.vue'

export const router = {
  routes: [
    {
      name: 'dashboard',
      path: '/',
      component: Dashboard,
      meta: {
        title: ({ i18n }) => i18n.t('dashboard.title')
      }
    },
    {
      name: 'login',
      path: '/login',
      component: Login,
      meta: {
        title: ({ i18n }) => i18n.t('login.title')
      }
    },
    {
      name: 'history-list',
      path: '/history',
      component: HistoryList,
      props: true
    },
    {
      name: 'task-record-review-list',
      path: '/task-record-reviews/:taskId',
      component: TaskRecordReviewList,
      props: true
    },
    {
      name: 'task-record-review-retrieve',
      path: '/task-record-reviews/:taskId/:taskRecordReviewId',
      component: TaskRecordReviewRetrieve,
      props: true
    },
    {
      name: 'tip-list',
      path: '/tips',
      component: TipList,
      props: true
    },
    {
      name: 'tip-retreive',
      path: '/tips/:tipId',
      component: TipRetrieve,
      props: true
    },
    {
      name: 'error',
      path: '*',
      props: true,
      component: Error,
      meta: {
        title: ({ i18n }) => i18n.t('error.title')
      }
    }
  ]
}

export default router

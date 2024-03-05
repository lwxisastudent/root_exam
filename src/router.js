import { createRouter, createWebHistory } from 'vue-router';
import InputPage from './components/InputPage.vue';
import ExamPage from './components/ExamPage.vue';

const routes = [
  { path: '/', component: InputPage },
  { path: '/exam', component: ExamPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

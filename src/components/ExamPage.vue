<template>
  <div>
    <div v-if="examType === 'word'">
      <p>题目：{{ currentProblem + 1 }} / {{ totalProblems }}</p>
      <h1 :class="{ 'word': true, 'correct': problemFinished && isCorrect, 'incorrect': problemFinished && !isCorrect }">{{ currentWord }}</h1>
      <p>所在页码：{{ currentPage }}</p>
      <input type="text" v-model="answer" @keyup.enter="checkAnswer">
      <p v-if="problemFinished">正确答案：{{ correctAnswer }}</p>
      <p v-if="problemFinished">{{ meaning }}</p>
      <div class="button-container">
          <button @click="checkAnswer" :disabled="problemFinished">检查</button>
          <button v-if="problemFinished" @click="nextQuestion" :disabled="examFinished">进入下一题</button>
      </div>
    </div>
    
    <div v-else-if="examType === 'root'">
      <p>题目：{{ currentProblem + 1 }} / {{ totalProblems }}</p>
      <h1>{{ currentRoot }}</h1>
      <p>所在页码：{{ currentPage }} - {{ currentIndex }}</p>
      <input type="text" v-model="answer" @keyup.enter="checkAnswer">
      <p v-if="problemFinished">正确答案：{{ correctAnswer }}</p>
      <div class="button-container">
          <button @click="checkAnswer" :disabled="problemFinished">检查</button>
          <button v-if="problemFinished" @click="nextQuestion" :disabled="examFinished">进入下一题</button>
      </div>
    </div>

    <p v-if="examFinished">考试结束！</p>
    <p v-if="examFinished">正确率：{{ correctCount }}/{{ totalCount }}</p>
      <button @click="goHome" class="home-button">返回主页</button>
    <FooterLink />
  </div>
</template>

<script>
import axios from 'axios';
import FooterLink from './FooterLink.vue';

export default {
  components: {
    FooterLink
  },
  data() {
    return {
      words: [],
      roots: [],
      totalProblems: 0,
      currentProblem: 0,
      currentPage: 0,
      currentIndex: 0,
      currentWord: '',
      currentRoot: '',
      meaning: '',
      answer: '',
      correctAnswer: '',
      isCorrect: false,
      problemFinished: false,
      examFinished: false,
      correctCount: 0,
      totalCount: 0,
      examType: '',
      examMode: '',
      examSize: 5 //仅随机模式下使用
    };
  },
  mounted() {
  const pageRange = this.$route.query.pageRange;
    this.examType = this.$route.query.examType;
    this.examMode = this.$route.query.examMode;
    if(this.examMode === 'random'){
        this.examSize = this.$route.query.examSize;
    }
  this.fetchWordsAndRoots(pageRange);
  },
  methods: {
     fetchWordsAndRoots(pageRange) {
         
      if (this.examType === 'word') {
      axios.get('/api/words', { params: { pageRange } })
        .then(response => {
          this.words = response.data;
            if (this.examMode === 'random') {
              const randomIndexes = this.getRandomIndexes(this.words.length, this.examSize);
              this.words = randomIndexes.map(index => this.words[index]);
            }
        this.totalProblems = this.words.length;
          this.loadQuestion();
        })
        .catch(error => {
          console.log(error);
        });
      }else{

      axios.get('/api/roots', { params: { pageRange } })
        .then(response => {
          this.roots = response.data;
            if (this.examMode === 'random') {
              const randomIndexes = this.getRandomIndexes(this.roots.length, this.examSize);
              this.roots = randomIndexes.map(index => this.roots[index]);
            }
        this.totalProblems = this.roots.length;
          this.loadQuestion();
        })
        .catch(error => {
          console.log(error);
        });
      }
    },
    getRandomIndexes(maxIndex, count) {
      const indexes = [];
      while (indexes.length < count) {
        const randomIndex = Math.floor(Math.random() * maxIndex);
        if (!indexes.includes(randomIndex)) {
          indexes.push(randomIndex);
        }
      }
      return indexes;
    },
nextQuestion() {
    
      const maxProblem = this.examType === 'word' ? this.words.length : this.roots.length;

      if (this.currentProblem + 1 < maxProblem) {
          this.currentProblem++;
        this.answer = '';
        this.problemFinished = false;
        this.isCorrect = false;
        
        this.loadQuestion();
      }else{
          this.examFinished = true;
      }
    
},
     fetchWordRoot(rootId) {
      axios.get(`/api/roots/${rootId}`)
        .then(response => {
      this.correctAnswer = response.data.root;
        })
        .catch(error => {
          console.log(error);
        });
    },
    loadQuestion() {
        
      if (this.examType === 'word') {
        this.currentWord = this.words[this.currentProblem].word;
        this.currentPage = this.words[this.currentProblem].page;
        this.fetchWordRoot(this.words[this.currentProblem].root);
        
        this.meaning = this.words[this.currentProblem].meaning;
        
      } else {
        this.currentRoot = this.roots[this.currentProblem].root;
        this.currentPage = this.roots[this.currentProblem].page;
        this.currentIndex = this.roots[this.currentProblem].idx;
        this.correctAnswer = this.roots[this.currentProblem].meaning;
      }
    },
    checkAnswer() {
        
    if (!this.problemFinished) {
      this.problemFinished = true;
      this.totalCount++;

      if (this.examType === 'word') {
        const userAnswer = this.answer.trim().toLowerCase();
        const correctAnswers = this.correctAnswer.split(',');
        this.isCorrect = correctAnswers.some(answer => answer.trim().toLowerCase().replace('-', '') === userAnswer);
        
      } else {
        const userAnswer = this.answer.trim().toLowerCase().replace(/\s/g, '');
        const correctAnswer = this.correctAnswer.trim().toLowerCase().replace(/\s/g, '').replace('，', ',');
        this.isCorrect = userAnswer === correctAnswer;
      }

      if (this.isCorrect) {
        this.correctCount++;
      }
    }
    },
    goHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style src="@/assets/styles.css" scoped></style>
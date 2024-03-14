<template>
  <div>
      <h1>词根考查</h1>
    <label for="pageInput">输入页码范围：</label>
    <input type="text" v-model="pageRange" id="pageInput"><br>

    <input type="radio" id="word" value="word" v-model="examType">
    <label for="word">词</label>
    <input type="radio" id="root" value="root" v-model="examType">
    <label for="root">词根</label><br>

    <input type="radio" id="sequential" value="sequential" v-model="examMode">
    <label for="sequential">顺序考查</label>
    <input type="radio" id="random" value="random" v-model="examMode">
    <label for="random">随机考查</label><br>

    <div v-if="examMode === 'random'">
      <label for="examSize">自定义数量：</label>
      <input type="number" v-model="examSize" id="examSize" @keyup.enter="startExam">
    </div><br>

    <button @click="startExam">开始考试</button>
    <FooterLink />
  </div>
</template>

<script>
import FooterLink from './FooterLink.vue';
export default {
  components: {
    FooterLink
  },
  data() {
    return {
      pageRange: '',
      examType: 'word',
      examMode: 'sequential',
      examSize: 5
    };
  },
  methods: {
    startExam() {
      const page = parseInt(this.pageRange);
      if (!isNaN(page)) {
        this.pageRange = `${page}-${page}`;
      }
      
      if(this.examMode == 'random'){
      this.$router.push({ path: '/exam', query: { pageRange: this.pageRange, examType: this.examType, examMode: this.examMode, examSize: this.examSize }});
      }else{
      this.$router.push({ path: '/exam', query: { pageRange: this.pageRange, examType: this.examType, examMode: this.examMode}});
      }
    }
  }
}
</script>
<style src="@/assets/styles.css" scoped></style>
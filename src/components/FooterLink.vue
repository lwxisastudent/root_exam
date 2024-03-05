<template>
  <div>
    <p class="page-description">当前仅录入了前20页</p>
    <a :href="pdf" class="footer-link">查看 PDF</a>
  </div>
</template>

<script>
import pdf from '@/assets/Roots, Prefixes and Suffixes（2024.2）.pdf';
export default {
  name: 'FooterLink',
  data() {
    return {
      pdf: pdf
    };
  }
};
</script>

<style src="@/assets/styles.css" scoped></style>
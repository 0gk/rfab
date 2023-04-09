<script>
import RfabJbod from './RfabJbod.vue'

export default {

  components: {
    RfabJbod,
  },

  props: {
    model: {
      type: Object,
      default: {owner: 'Object model for CustomerPlant was not provided',},
    },
    view: {
      type: Object,
      default: {},
    },
  },

  data() {
    return {}
  },
}
</script>

<template>
  <h1>Plant owns by {{model.owner}}</h1>
  <el-row v-for="jbod in model.jbods">
    <el-col :span="24"><RfabJbod :model="jbod" :view="view" /></el-col>
  </el-row>
</template>

<style scoped>
</style>

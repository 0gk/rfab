<script>
import RfabJbod from './RfabJbod.vue'

export default {

  components: {
    RfabJbod,
  },

  props: {
    model: {
      type: Object,
      default: {},
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
  <div class="container">
    <RfabJbod class="jbod" v-for="jbod in model.jbods" :model="jbod" :view="view" />
  </div>
</template>

<style scoped>
.jbod {
  margin-bottom: 20px;
}
.container {
}
</style>

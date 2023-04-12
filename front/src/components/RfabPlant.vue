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
  <div v-for="jbod in model.jbods">
    <RfabJbod class="jbod" :model="jbod" :view="view" />
  </div>
</template>

<style scoped>
.jbod {
  margin-bottom: 20px;
}

</style>

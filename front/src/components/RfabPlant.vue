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
    <RfabJbod v-for="jbod in model.jbods" :model="jbod" :view="view" />
</template>

<style scoped>
</style>

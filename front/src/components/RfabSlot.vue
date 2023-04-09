<script>

export default {

  props: {
    model: {
      type: Object,
      default: {},
    },
  },

  data() {
    return {}
  }
}
</script>

<template>
  <div class="slot">
      <div>({{model.idx}}) {{model.sn}} | {{model.mdl}}</div>
      <div>{{model.status}}</div>
      <div>State: {{model.state}} Statuscode: {{model.scode}} Progress: {{model.progress/100}}% Grade: {{model.grade}}</div>
  </div>
</template>

<style scoped>
.slot {
    background: #ccffdc;
    width: 400px;
   /* border: 1px solid #000066; */
    padding: 5px;
    font-family: monospace;
}

</style>


<script>

export default {

  props: {
    model: {
      type: Object,
      default: {},
    },
    isSelected: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {}
  }
}
</script>

<template>
  <div class="slot" :class="{'slot-selected': isSelected}">
      <div class="row1">({{(model.idx < 10 ? '0' : '') + model.idx}})&nbsp;{{model.sn}}&nbsp;|&nbsp;{{model.mdl}}</div>
      <div class="row2">{{model.status}}</div>
      <div class="row3">
        <div class="col">State: {{model.state}}</div>
	<div class="col">Statuscode: {{model.scode}}</div>
	<div class="col">Progress: {{model.progress/100}}%</div>
	<div class="col">Grade: {{model.grade}}</div>
      </div>
  </div>
</template>

<style scoped>
</style>


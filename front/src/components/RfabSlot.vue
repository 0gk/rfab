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
      <div class="row1">({{model.idx}})&nbsp;{{model.sn}}&nbsp;|&nbsp;{{model.mdl}}</div>
      <div class="row2">{{model.status}}</div>
      <div class="row3">
        <div class="row3col">State: {{model.state}}</div>
	<div class="row3col">Statuscode: {{model.scode}}</div>
	<div class="row3col">Progress: {{model.progress/100}}%</div>
	<div class="row3col">Grade: {{model.grade}}</div>
      </div>
  </div>
</template>

<style scoped>
.slot {
    background: #ccffdc;
    width: 400px;
   /* border: 1px solid #000066; */
    padding: 5px;
    font-family: "Lucida Console";
    font-size: 12px; 
}
.row1 {
  text-align: center;
}
.row2 {
  text-align: center;
}
.row3 {
  display: flex;
}
.row3col {
    flex-grow: 1;
    text-align: center;
}

</style>


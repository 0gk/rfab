<script>
import RfabSlot from './RfabSlot.vue'

export default {

  components: {
    RfabSlot,
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

  computed: {
    gridStyle() { 
      return {
        background: '#3b3d3c',
        padding: '5px',
        display: 'grid',
        width: 'fit-content',
        gridTemplateColumns: `repeat(${this.view.rowLen}, 420px)`,
      }
    },
    jbodTitle() {
      return `WWN: ${this.model.wwn0}:${this.model.wwn1} Model: ${this.model.mdl} S/N: ${this.model.sn}`
    },
  },

}
</script>


<template>

      <div class="unit" :class="{'fit-content': !view.unlimColumnViewOn}">

        <div class="title-box">
          <span class="title">{{jbodTitle}}</span>
        </div>

        <div v-if="view.unlimColumnViewOn" class="autogrid" >
          <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" />
        </div>
        <div v-else :style="gridStyle" >
          <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" />
        </div>

      </div>

</template>


<style scoped>
.title{
  color: white;
  font-weight: normal;
  font-size: 120%;
}
.title-box{
  text-align: center;
  padding: 5px;
}
.unit {
  margin: auto;
  background: #6b6d6c;
  padding: 10px;
}
.fit-content {
  width: fit-content;
}
.autogrid {
  background: #3b3d3c;
  padding: 5px;
  display: grid;
  grid-template-columns: repeat(auto-fit, 420px);
}
.slot {
  margin: 5px;
}
</style>

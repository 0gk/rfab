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
    slotRows() {
      let obj = this.model.slots
      let lenght = Object.keys(obj).length
      let rowLen = Number(this.view.rowLen) || 4 
      let rowArr = [];
      for (let i=0; i<lenght; i++) {
        let colArr = [];
        let border = i + rowLen < lenght ? i + rowLen : lenght;
        for (; i <border; i++) {
          colArr.push(obj[String(i)]);
        }
        rowArr.push(colArr)
        i--;
      }
      return rowArr
    },
  },

}
</script>


<template>

    <div class="jbod">
      <div><span class="title">WWN:&nbsp;{{model.wwn0}}:{{model.wwn1}} Model:&nbsp;{{model.mdl}} S/N:&nbsp;{{model.sn}}</span>
      </div>
      <div class="line-container" v-if="view.unlimColumnViewOn" >
        <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" />
      </div>
      <div v-else >
        <div class="line-container" v-for="slotRow in slotRows">
          <RfabSlot class="slot" v-for="slot in slotRow" :model="slot" />
        </div>
      </div>
    </div>

</template>


<style scoped>
.title{
    font-weight: normal;
    font-size: 120%;
    color: white;
    align: center;
}
.jbod {
  background: #3b3d3c;
  margin: 5px;
  padding: 5px;
}
.line-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: stretch;
}
.slot {
  margin: 5px;
}
</style>

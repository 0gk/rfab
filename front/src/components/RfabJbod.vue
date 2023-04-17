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
        margin: 'auto',
        width: 'fit-content',
        gridTemplateColumns: `repeat(${this.view.rowLen}, var(--slot-width))`,
      }
    },
    jbodTitle() {
      return `(IDX) WWN: ${this.model.wwn0}:${this.model.wwn1} Model: ${this.model.mdl} S/N: ${this.model.sn}`
    },
  },

}
</script>


<template>

      <div class="jbod" :class="{'fit-content': !view.unlimColumnViewOn}">

        <div class="title-box">
          <span class="title">{{jbodTitle}}</span>
        </div>

        <div v-if="view.unlimColumnViewOn" class="grid autogrid" >
          <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" />
        </div>
        <div v-else class="grid" :style="gridStyle" >
          <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" />
        </div>

      </div>

</template>


<style scoped>

.autogrid {
  grid-template-columns: repeat(auto-fill, var(--slot-width));
}

.fit-content {
  width: fit-content;
}

</style>

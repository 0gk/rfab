<script>
import RfabSlot from './RfabSlot.vue'
import {apiPost} from '../api.js'

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
    return {
      selectedSlotsIdx: new Set(), 
      isSelectModeOn: false,
      slotDetails: null,
      actionsList: [
        {value: "abort", label: "Abort"},
        {value: "reset", label: "Reset"},
      ],
      chosenAction: '',
    }
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
      return `(${this.model.idx}) WWN: ${this.model.wwn0}:${this.model.wwn1} Model: ${this.model.mdl} S/N: ${this.model.sn}`
    },
  },

  methods: {

    onClickSlot(idx) {
      if (this.isSelectModeOn) {

        if (this.selectedSlotsIdx.has(idx)) {
          this.selectedSlotsIdx.delete(idx);
        } else {
          this.selectedSlotsIdx.add(idx);
        }

      } else {

        if (this.selectedSlotsIdx.has(idx)) {
	  this.selectedSlotsIdx.clear();
          this.slotDetails = null
        } else {
	  this.selectedSlotsIdx.clear();
          this.selectedSlotsIdx.add(idx);
          this.slotDetails = { waitingText: "Loading ..." }
        }

      }
    },

    onSelectModeChange() {
      this.selectedSlotsIdx.clear()
      this.slotDetails = null
    },

    sendAction() {
      if (this.chosenAction) {
        apiPost('/action/1', {action: this.chosenAction, data: { [this.model.idx]: this.selectedSlotsIdx } })
        var msg = `Action "${this.chosenAction}" was sent`;
	this.chosenAction = "";
      } else {
        var msg = `Choose action to sent`;
      }
      console.log(msg);
    },

  },

}
</script>


<template>

      <div class="jbod" :class="{'fit-content': !view.isUnlimColumnViewOn}">

        <div class="title-box">
	  <div class="title">
            {{jbodTitle}}
	  </div>
	  <div class="controls">
	    <div class="switch">
	      <el-switch v-model="isSelectModeOn" @change="onSelectModeChange" />
	    </div>
	    <div class="select">
	      <el-select v-model="chosenAction" class="m-2" placeholder="Action">
                <el-option
                  v-for="action in actionsList"
                  :key="action.value"
                  :label="action.label"
                  :value="action.value"
                />
              </el-select>
	    </div>
	    <div class="button">
              <el-button type="primary" plain @click="sendAction">Send</el-button> 
	    </div>
          </div>
        </div>


        <div v-if="view.isUnlimColumnViewOn" class="grid autogrid" >
          <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" :is-selected="selectedSlotsIdx.has(slot.idx)"  @click="onClickSlot(slot.idx)"/>
        </div>
        <div v-else class="grid" :style="gridStyle" >
          <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" :is-selected="selectedSlotsIdx.has(slot.idx)"  @click="onClickSlot(slot.idx)"/>
        </div>

        <div class="dutinfo-box" v-if="slotDetails">
	  <pre class="dutinfo" v-if="slotDetails.waitingText">{{slotDetails.waitingText}}</pre>
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

<script>
import RfabSlot from './RfabSlot.vue'
import {apiGet} from '../api.js'
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
      isМultiSelectModeOn: false,
      dutinfo: null,
      jbodstat: null,
      actionsList: [
        {value: "abort", label: "Abort"},
        {value: "reset", label: "Reset"},
      ],
      chosenAction: null,
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
      return `[${(this.model.idx < 10 ? '0' : '') + this.model.idx}] WWN: ${this.model.wwn0}:${this.model.wwn1} Model: ${this.model.mdl} S/N: ${this.model.sn}`
    },
  },

  methods: {

    cearSelection() {
      this.selectedSlotsIdx.clear();
      this.dutinfo = null;
    },

    async onClickSlot(idx) {
      if (this.isМultiSelectModeOn) {

        if (this.selectedSlotsIdx.has(idx)) {
          this.selectedSlotsIdx.delete(idx);
        } else {
          this.selectedSlotsIdx.add(idx);
        }

      } else {

        if (this.selectedSlotsIdx.has(idx)) {
	  this.cearSelection();
        } else {
	  this.cearSelection();
          this.selectedSlotsIdx.add(idx);
          this.dutinfo = 'Loading ...';
          try {
	    this.dutinfo = await apiGet(`/dutinfo/${window.plid}/${this.model.idx}/${idx}`);
          } catch (error) {
            this.displayMessage(`${error.message} while requesting about selected slot #${idx}`, 'error');
          }
        }

      }
    },

    async onClickJbodTitle() {
      if (this.jbodstat) {
        this.jbodstat = null;
      } else {
        this.jbodstat = 'Loading ...';
        try {
          this.jbodstat = await apiGet(`/jbodstat/${window.plid}/${this.model.idx}`);
        } catch (error) {
          this.displayMessage(`${error.message} while requesting statistic for jbod #${this.model.idx}`, 'error');
        }
      }
    },

    onSelectModeChange() {
      this.cearSelection();
    },

    async sendAction() {
      try {
        await apiPost('/action/' + window.plid, {action: this.chosenAction, data: { [this.model.idx]: Array.from(this.selectedSlotsIdx) } })
        this.displayMessage(`Action "${this.chosenAction}" was sent`, 'success');
        this.chosenAction = null;
        this.cearSelection();
      } catch (error) {
        this.displayMessage(`${error.message} while trying to dispatch action "${this.chosenAction}"`, 'error');
      }
    },

  },

}
</script>


<template>

      <div class="jbod" :class="{'fit-content': !view.isUnlimColumnViewOn}">

        <div class="title-box">
	  <div class="title" @click="onClickJbodTitle">
            {{jbodTitle}}
	  </div>
	  <div class="controls">
	    <div class="switch">
	      <el-switch v-model="isМultiSelectModeOn" @change="onSelectModeChange" />
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
	    <div class="button" >
              <el-button type="primary" plain @click="sendAction" :disabled="!chosenAction || this.selectedSlotsIdx.size == 0">Send</el-button> 
	    </div>
          </div>
        </div>

        <div class="jbodstat-box" v-if="jbodstat">
	  <pre class="jbodstat" >{{jbodstat}}</pre>
        </div>


        <div v-if="view.isUnlimColumnViewOn" class="grid autogrid" >
          <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" :is-selected="selectedSlotsIdx.has(slot.idx)"  @click="onClickSlot(slot.idx)"/>
        </div>
        <div v-else class="grid" :style="gridStyle" >
          <RfabSlot class="slot" v-for="slot in model.slots" :model="slot" :is-selected="selectedSlotsIdx.has(slot.idx)"  @click="onClickSlot(slot.idx)"/>
        </div>

        <div class="dutinfo-box" v-if="dutinfo">
	  <pre class="dutinfo" >{{dutinfo}}</pre>
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

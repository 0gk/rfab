<script>
import RfabJbod from './RfabJbod.vue'
import {apiPost} from '../api.js'

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
    return {
      chosenTest: null,
    }
  },

  computed: {
    currentTestLabel() {
      if (this.model && this.model.testoptions) {
        return this.model.testoptions[this.model.chosentest]
      } else {
        return ''
      }

    },
  },

  methods: {
    async sendChosenTest() {
      try {
        await apiPost('/action/' + window.plid, {action: 'chosentest', data: this.chosenTest })
        this.displayMessage(`Chosen test "${this.model.testoptions[this.chosenTest]}" id was sent`, 'success');
        this.chosenTest = null;
      } catch (error) {
        this.displayMessage(`${error.message} while trying to send chosen test "${this.model.testoptions[this.chosenTest]}" id`, 'error');
      }
    },

  },

  
}
</script>

<template>
  <div class="plant">

    <div class="panel">
      <div class="controls">
        <div class="select">
          <el-select v-model="chosenTest" class="m-2" placeholder="Test">
            <el-option
                v-for="(label, id) in model.testoptions"
                :key="id"
                :label="label"
                :value="id"
            />
          </el-select>
        </div>
        <div class="button" >
          <el-button type="primary" plain @click="sendChosenTest" :disabled="!chosenTest">Send</el-button>
        </div>
      </div>
      <div class="chosentest">
        Established testing procedure: "{{ currentTestLabel }}"
      </div>
    </div>

    <div>
      <RfabJbod v-for="jbod in model.jbods" :model="jbod" :view="view" />
    </div>

  </div>
</template>

<style scoped>
</style>

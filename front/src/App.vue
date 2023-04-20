<script>
import {apiGet} from './api.js'
import RfabPlant from './components/RfabPlant.vue'

export default {

  components: {
    RfabPlant,
  },

  data() {
    return {
      model: {},
      view: {
        isUnlimColumnViewOn: false,
	rowLen: 4,
      },
      rowLengths: [1, 2, 4, 5, 8, 10],
    }
  },

  async created() {
    this.model = await apiGet('/plant/1');

    function updateModel(model, newData) {
      for (let key in newData) {
        if(typeof(newData[key]) === 'object') {
          updateModel(model[key], newData[key])
	} else {
          model[key] = newData[key]
	}
      }
    }

    const sse = new EventSource('//fab.rlab.ru:9000/sse/1');
    sse.onmessage = event => {
        console.log('%c Event received:', 'color: green');
        console.log(event)
        const eventData = JSON.parse(event.data)
        console.log(eventData)
	if (eventData.type == 'update') {
	  updateModel(this.model, eventData.data);
	  console.log('Model updated');
	} else if (eventData.type == 'state') {
	  this.model = eventData.data;
	  console.log('Model overwrited');
	} else {
	  console.error('Unknown object type received');
	}

    }

    /*
    let pn = 1
    const carousel = async () => {
      pn = pn > 10 ? 1 : pn;
      this.model = await apiGet('/plant/' + pn);
      pn++;
    }
    setInterval(carousel,100); */
  },

}


</script>

<template>
      <header>
        <el-radio-group v-model="view.rowLen" size="large">
          <el-radio-button v-for="i in rowLengths" :key="i" :label="i" />
        </el-radio-group>
        <div class="header-block"><el-switch v-model="view.isUnlimColumnViewOn" /></div>
      </header>
      <main>
        <RfabPlant :model="this.model" :view="view"/>
      </main>
      <footer></footer>
</template>

<style scoped>

  header {
    display: flex;
    flex-direction: row;
    justify-content: right;
  }

  .header-block {
    margin: 5px;
    padding: 5px;
  }

</style>

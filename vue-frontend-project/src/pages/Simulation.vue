<template>
  <div>
      <h1>Satellite Simulation</h1>

    <button @click="startSSE();runRandomStatusUpdate();">Start</button>
    <button @click="stopSSE()">Stop</button>
    <div style="display: none;" class="alert-success" v-if="updateStatusMsg">{{updateStatusMsg}}</div>
    <table  class="table">
      <tr>
        <td>Name</td>
        <td>Status</td>
        <td></td>
      </tr>
      <tr v-for="s in satellites" data-id="{{s.id}}">
        <td>{{s.name}}</td>
        <td>{{s.status}}</td>
        <td data-id="{{s.id}}"><button v-if="s.status =='MALFUNCTIONING'" @click="updateStatus(s.slug)">Set to Nominal</button></td>
      </tr>
    </table>
    <div style="display: none;" class="alert-success" v-if="sseLastUpdated">{{sseLastUpdated.name}} updated to {{sseLastUpdated.status}}</div>
  </div>
</template>
<script>
import { useRouter } from 'vue-router'
import {getCSRFToken} from "../store/auth.js";

export default {
  setup() {
    const router = useRouter()

    return {
      router
    }
  },
  data() {
    return {
      eventSource: new EventSource('http://localhost:8000/stream/'),
      satellites: [{
        id: "",
        name: "",
        slug: "",
        updated: "",
        status: "" // NOMINAL, MALFUNCTIONING
      }],
      sseDataLog: [],
      sseLastUpdated: "",
      error: "",
      updateStatusMsg: "",
      sseMessage: "",
      simulationOn: false,
    }
  },
  methods: {
    async getSpacecrafts(){
      try {
        const response = await fetch('http://localhost:8000/api/spacecrafts', {
          method: 'GET',
           headers: {
                    'Content-Type': 'application/json',
                },
        })
        const data = await response.json()
        if (response.ok) {
          this.satellites = data
        } else {
          this.error = data.error || 'Error getting data'
        }
      } catch (err) {
        this.error = 'An error occurred mounting spacecraft data' + err
      }
    },
    async startSSE() {
        this.eventSource.onmessage = event => {
          this.sseDataLog.push(JSON.parse(event.data));
          this.sseLastUpdated = JSON.parse(event.data);
          this.satellites.forEach((s, index) =>{
            if(this.sseLastUpdated.slug === s.slug){
              this.satellites[index].status = this.sseLastUpdated.status;
            }
          });
        }
    },
    async stopSSE() {
      if (this.eventSource) {
          this.eventSource.close();
        }
      this.simulationOn = false;
    },
    async runRandomStatusUpdate(){
      let i = 0;
      this.simulationOn = true;
      while (i < 10 || !this.simulationOn){
        await this.sendRandomStatusUpdate();
      }
    },
    async sendRandomStatusUpdate(){
        const min = 1, max = 10;
        const rand_time = Math.floor(Math.random() * (max - min + 1) + min);
        const statusList = ["NOMINAL", "MALFUNCTIONING"];
        const randomStatus = Math.floor(Math.random() * statusList.length);
        await new Promise(resolve => setTimeout(resolve, rand_time * 1000));

        const randomSpaceCraft = Math.floor(Math.random() * this.satellites.length);
        console.log(this.satellites[randomSpaceCraft].slug);
        console.log(statusList[randomStatus])
        await this.updateStatus(this.satellites[randomSpaceCraft].slug, statusList[randomStatus]);
      },
    async updateStatus(slug, newStatus='NOMINAL'){
        try {
          const response = await fetch('http://localhost:8000/api/spacecrafts/' + slug + '/update-status', {
            method: 'PUT',
             headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCSRFToken()
                  },
            body: JSON.stringify({
              status: newStatus
            }),
          })
          const data = await response.json()
          if (response.ok) {
            this.updateStatusMsg = slug + " set to " + newStatus + " - updates will show if simulation started"

          } else {
            this.error = data.error || 'Update failed'
          }
        } catch (err) {
          this.error = 'An error occurred during sateillite update for: ' + err
        }
    }
  },
  async mounted() {
    await this.getSpacecrafts()
  }
}
</script>

<template>
  <div>
      <h1>Satellite Simulation</h1>

    <button @click="startSSE()">Start</button>
    <button @click="stopSSE()" disabled>Stop</button>
    <div class="alert-success" v-if="updateStatusMsg">{{updateStatusMsg}}</div>
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

    <div id="sse-data">{{sseData}}</div>
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
      sseData: [],
      error: "",
      updateStatusMsg: "",
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
        this.eventSource.onmessage = event => this.sseData = event.data;
    },
    async stopSSE() {
      if (this.eventSource) {
          this.eventSource.close();
        }
    },
    async updateStatus(slug){
        try {
          const response = await fetch('http://localhost:8000/api/spacecrafts/' + slug + '/update-status', {
            method: 'POST',
             headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCSRFToken()
                  },
            body: JSON.stringify({
              status: "NOMINAL"
            }),
          })
          const data = await response.json()
          if (response.ok) {
            this.updateStatus = slug + "set to NOMINAL"
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

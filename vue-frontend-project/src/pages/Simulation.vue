<template>
  <div>
      <h1>Satellite Simulation</h1>

    <button @click="startSSE()">Start</button>
    <button @click="stopSSE()" disabled>Stop</button>
    <table  class="table">
      <tr>
        <td>Name</td>
        <td>Status</td>
        <td></td>
      </tr>
      <tr v-for="s in satellites" data-id="{{s.id}}">
        <td>{{s.name}}</td>
        <td>{{s.status}}</td>
        <td data-id="{{s.id}}"><a @click="updateStatus()">update</a></td>
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
      error: ""
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
    async updateStatus(){
        // try {
        //   const response = await fetch('http://localhost:8000/api/register', {
        //     method: 'POST',
        //      headers: {
        //               'Content-Type': 'application/json',
        //               'X-CSRFToken': getCSRFToken()
        //           },
        //     body: JSON.stringify({
        //       email: this.email,
        //       password: this.password
        //     }),
        //     credentials: 'include'
        //   })
        //   const data = await response.json()
        //   if (response.ok) {
        //     this.success = 'Registration successful! Please log in.'
        //     setTimeout(() => {
        //       this.$router.push('/login')
        //     }, 1000)
        //   } else {
        //     this.error = data.error || 'Registration failed'
        //   }
        // } catch (err) {
        //   this.error = 'An error occurred during registration: ' + err
        // }
    }
  },
  async mounted() {
    await this.getSpacecrafts()
  }
}
</script>

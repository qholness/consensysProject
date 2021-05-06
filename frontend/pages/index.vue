<template>
  <div class="container">
    <!-- Swap users for debug purposes -->
    <select v-model="userId">
      <option
        v-for="user of users"
        :key="user.id"
        >{{ user.id }}</option>
    </select>
    <b-tabs
      active-nav-item-class="font-weight-bold text-uppercase text-primary"
      active-tab-class="font-weight-bold text-success"
      content-class="mt-3">
      <b-tab title="Bookings" active>
        <MyBookings :userId="userId" />
      </b-tab>
    <b-tab title="Book your room">
      <BookARoom :userId="userId" />
    </b-tab>
    <!-- <b-tab title="Disabled" disabled><p>I'm a disabled tab!</p></b-tab> -->
    </b-tabs>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from '@nuxtjs/axios';
import data from '~/store/bookings';
import MyBookings from '~/components/mybookings.vue';
import BookARoom from '~/components/bookaroom.vue';


export default Vue.extend({
  components: {
    BookARoom,
    MyBookings
  },
  data() {
    return {
      bookingsData: data,
      users: [],
      userId: null
    }
  },
  mounted: async function() {
    this.userId = 0;
    this.users = await this.$axios.$get("http://localhost:5000/get-users");
  }
  
})
</script>

<style>
.container {
  text-align: center;
}

.title {
  font-family:
    'Quicksand',
    'Source Sans Pro',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>

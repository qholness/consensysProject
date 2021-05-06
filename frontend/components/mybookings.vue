<template>
    <div>
        <div>
        <table class="table table-striped">
            <thead>
            <tr>
                <th>Room</th>
                <th>Date</th>
                <th>Time</th>
            </tr>
            </thead>
            <tbody>
            <tr
                v-for="row of bookingsData.myBookings"
                :key="row.eventId">
                <td>{{ row.name }}</td>
                <td>{{ `${row.year}.${row.month}.${row.day}` }}</td>
                <td>{{ row.starttime }}</td>
                <td><button
                    @click="cancelBooking(row.eventId)"
                    class="btn btn-danger">Cancel</button></td>
            </tr>
            </tbody>
        </table>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from '@nuxtjs/axios';
import data from '~/store/bookings';


export default Vue.extend({
    name: "MyBookings",
    props: ['userId'],
    data() {
        return {
            bookingsData: data
        }
    },
    methods: {
        cancelBooking: async function(id) {
            // Cancel booking
            confirm("Would you like to cancel this booking?")
            
            const data = await this.$axios.$get("http://localhost:5000/cancel-booking", {
                params: {
                    eventId: id
                }
            });
            this.getMyBookings();
        },
        getMyBookings: async function() {
            if(this.userId !== "") {
                const data = await this.$axios.$get("http://localhost:5000/my-bookings", {
                    params: {
                        userId: this.userId
                    }
                });
                this.bookingsData.myBookings = data;
            }
        },
    },
    mounted: async function() {
        this.getMyBookings();
    },
    watch: {
        userId: function(val) {
            if(val) {
                this.getMyBookings();
            }
        }
    }

})
</script>
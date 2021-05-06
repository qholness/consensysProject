<template>
    <div>
        <select
            class="form-control"
            v-model="selectedRoomId">
            <option value="">Select a room</option>
            <option 
            v-for="room of bookingsData.rooms"
            :key="room.id"
            :title="room.id"
            :value="room.id">{{ room.name }}</option>
        </select>
        <br>
        <DatePicker
            v-if="roomSelected"
            v-model="selectedDate" />
        <br>
        <div
            v-if="
            roomSelected &&
            dateSelected &&
            bookingsData.roomAvailability.length">
            <h3>Available blocks</h3>
            <div>
                <button
                    v-for="row, id  of bookingsData.roomAvailability"
                    :class="assignButtonClass(row)"
                    @click="bookRoom(row.starttime)"
                    :key="id"
                    :disabled="!row.isAvailable">
                    {{ row.starttime }}</button>
            </div>
            <br>
            <input
                type="number"
                v-model="premium">
        </div>
    </div>
</template>


<script lang="ts">
import Vue from 'vue'
import DatePicker from 'v-calendar/lib/components/date-picker.umd'
import data from '~/store/bookings';
import { AvailabilityRequest } from '~/store/bookings';


export default Vue.extend({
    name: "BookARoom",
    props: ['userId'],
    components: {
        DatePicker,
    },
    computed: {
        dateSelected: function(): boolean {
            return this.selectedDate !== "";
        },
        roomSelected: function(): boolean {
            return this.selectedRoomId !== "";
        },
        timeSelected: function(): boolean {
            return this.selectedtime !== "";
        },
    },
    data() {
        return {
            bookingsData: data,
            premium: 0,
            selectedDate: "",
            selectedTime: "",
            selectedRoomId: "",
        }
    },
    methods: {
        assignButtonClass: function(row) {
            if(row.isAvailable) {
                return "btn btn-success"
            }
            return "btn btn-secondary"
        },
        getListOfRooms: async function(){
            const data = await this.$axios.$get("http://localhost:5000/get-rooms");
            this.bookingsData.rooms = data;
        },
        getRoomAvailability: async function(){
            if(this.roomSelected) {
                if(this.dateSelected) {
                const data = await this.$axios.$get("http://localhost:5000/get-availability", {
                        params: {
                            userId: this.userId,
                            roomId: this.selectedRoomId,
                            year: this.selectedDate.getFullYear(),
                            month: this.selectedDate.getMonth() + 1, // getMonth is 0-indexed
                            day: this.selectedDate.getDate()
                        } as AvailabilityRequest
                    });
                this.bookingsData.roomAvailability = data;
                }
            }
        },
        getAvailableTokens: async function() {
            // Get user's token balance
        },
        bookRoom: async function(starttime){
            // Book the room
            confirm("Would you like to book for this time?")
            const data = await this.$axios.$get("http://localhost:5000/book-room", {
                params: {
                    userId: this.userId,
                    roomId: this.selectedRoomId,
                    year: this.selectedDate.getFullYear(),
                    month: this.selectedDate.getMonth() + 1, // getMonth is 0-indexed
                    day: this.selectedDate.getDate(),
                    starttime: starttime
                } as RoomAvailability
            });
        }
    },
    mounted: async function() {
        this.getListOfRooms();
    },
    watch: {
        selectedDate: function(val) {
            if(val) {
                this.getRoomAvailability();
            }
        },
        selectedRoomId: function(val) {
            if(val) {
                if(this.selectedDate !== "") {
                this.getRoomAvailability();
                }
            }
        }
    }
})
</script>
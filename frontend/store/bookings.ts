export interface AvailabilityRequest {
  userId: Number
  roomId: Number
  year: Number
  month: Number
  day: Number
}

export interface RoomAvailability {
  roomId: Number
  userId: Number
  year: Number
  month: Number
  day: Number
  name: string
  starttime?: string
  isAvailable?: boolean
}

const data = {
  roomAvailability: [] as RoomAvailability[],
  myBookings: [] as RoomAvailability[],
  rooms: []
}

export default data;
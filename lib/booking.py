class Booking():
    def __init__(self, id, date_booked, booking_status, user_id, space_id) -> None:        
        self.id = id
        self.date_booked = date_booked
        self.booking_status = self.is_valid(booking_status)        
        self.user_id = user_id
        self.space_id = space_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __str__(self) -> str:
        return f"Booking({self.id}, {self.date_booked}, {self.booking_status}, {self.user_id}, {self.space_id})"
    
    def is_valid(self, booking_status):
        if booking_status == "pending" or booking_status == "confirmed":
            return booking_status
        else: 
            raise Exception("Incorrect value: please enter either 'pending' or 'confirmed'")


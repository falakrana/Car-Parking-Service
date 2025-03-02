from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'car_parking_system_secret_key'

# Node class for Circular Linked List (Parking Slots)
class ParkingSlot:
    def __init__(self, slot_id):
        self.slot_id = slot_id
        self.is_occupied = False
        self.vehicle = None
        self.next = None

# Node class for Queue (Waitlist)
class WaitlistNode:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.next = None

# Vehicle class
class Vehicle:
    def __init__(self, license_plate, owner_name, contact, entry_time=None):
        self.license_plate = license_plate
        self.owner_name = owner_name
        self.contact = contact
        self.entry_time = entry_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Circular Linked List for Parking Slots
class ParkingSlotManager:
    def __init__(self, total_slots):
        self.head = None
        self.total_slots = total_slots
        self.available_slots = total_slots
        self.initialize_slots()
    
    def initialize_slots(self):
        if total_slots <= 0:
            return
        
        # Create first node
        self.head = ParkingSlot(1)
        current = self.head
        
        # Create remaining nodes in circular fashion
        for i in range(2, self.total_slots + 1):
            current.next = ParkingSlot(i)
            current = current.next
        
        # Complete the circle
        current.next = self.head
    
    def find_available_slot(self):
        if self.available_slots == 0:
            return None
        
        current = self.head
        for _ in range(self.total_slots):
            if not current.is_occupied:
                return current
            current = current.next
        
        return None
    
    def park_vehicle(self, vehicle):
        slot = self.find_available_slot()
        if not slot:
            return False
        
        slot.is_occupied = True
        slot.vehicle = vehicle
        self.available_slots -= 1
        return slot.slot_id
    
    def remove_vehicle(self, license_plate):
        if not self.head:
            return False
        
        current = self.head
        for _ in range(self.total_slots):
            if current.is_occupied and current.vehicle.license_plate == license_plate:
                current.is_occupied = False
                vehicle = current.vehicle
                current.vehicle = None
                self.available_slots += 1
                return vehicle
            current = current.next
        
        return False
    
    def get_all_slots(self):
        slots = []
        if not self.head:
            return slots
        
        current = self.head
        for _ in range(self.total_slots):
            slot_info = {
                'slot_id': current.slot_id,
                'is_occupied': current.is_occupied,
                'vehicle': current.vehicle.__dict__ if current.vehicle else None
            }
            slots.append(slot_info)
            current = current.next
        
        return slots

# Queue for Waitlist
class WaitlistQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, vehicle):
        new_node = WaitlistNode(vehicle)
        
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            return None
        
        vehicle = self.front.vehicle
        self.front = self.front.next
        
        if self.front is None:
            self.rear = None
        
        self.size -= 1
        return vehicle
    
    def get_all_waitlisted(self):
        waitlist = []
        current = self.front
        
        while current:
            waitlist.append(current.vehicle.__dict__)
            current = current.next
        
        return waitlist

# Hash Table for Vehicle Lookup
class VehicleHashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, license_plate):
        # Simple hash function
        return sum(ord(char) for char in license_plate) % self.size
    
    def insert(self, vehicle):
        index = self._hash(vehicle.license_plate)
        for i, (key, val) in enumerate(self.table[index]):
            if key == vehicle.license_plate:
                self.table[index][i] = (key, vehicle)
                return
        self.table[index].append((vehicle.license_plate, vehicle))
    
    def search(self, license_plate):
        index = self._hash(license_plate)
        for key, val in self.table[index]:
            if key == license_plate:
                return val
        return None
    
    def remove(self, license_plate):
        index = self._hash(license_plate)
        for i, (key, val) in enumerate(self.table[index]):
            if key == license_plate:
                del self.table[index][i]
                return val
        return None

# Initialize the parking system
total_slots = 6
parking_manager = ParkingSlotManager(total_slots)
waitlist_queue = WaitlistQueue()
vehicle_hash = VehicleHashTable()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cars')
def cars_info():
    slots = parking_manager.get_all_slots()
    waitlist = waitlist_queue.get_all_waitlisted()
    return render_template('cars.html', slots=slots, waitlist=waitlist)

@app.route('/park', methods=['POST'])
def park_vehicle():
    license_plate = request.form.get('license_plate')
    owner_name = request.form.get('owner_name')
    contact = request.form.get('contact')
    
    # Check if vehicle already exists
    if vehicle_hash.search(license_plate):
        flash('Vehicle with this license plate already parked!', 'danger')
        return redirect(url_for('cars_info'))
    
    vehicle = Vehicle(license_plate, owner_name, contact)
    
    # Try to park the vehicle
    slot_id = parking_manager.park_vehicle(vehicle)
    
    if slot_id:
        vehicle_hash.insert(vehicle)
        flash(f'Vehicle parked successfully in slot {slot_id}!', 'success')
    else:
        # Add to waitlist if no slots available
        waitlist_queue.enqueue(vehicle)
        flash('No parking slots available. Added to waitlist!', 'warning')
    
    return redirect(url_for('cars_info'))

@app.route('/remove', methods=['POST'])
def remove_vehicle():
    license_plate = request.form.get('license_plate')
    
    # Remove vehicle from parking
    vehicle = parking_manager.remove_vehicle(license_plate)
    
    if vehicle:
        vehicle_hash.remove(license_plate)
        flash('Vehicle removed successfully!', 'success')
        
        # Check waitlist and park the next vehicle if available
        if not waitlist_queue.is_empty():
            next_vehicle = waitlist_queue.dequeue()
            slot_id = parking_manager.park_vehicle(next_vehicle)
            if slot_id:
                vehicle_hash.insert(next_vehicle)
                flash(f'Vehicle from waitlist parked in slot {slot_id}!', 'info')
    else:
        flash('Vehicle not found in parking!', 'danger')
    
    return redirect(url_for('cars_info'))

@app.route('/search', methods=['POST'])
def search_vehicle():
    license_plate = request.form.get('license_plate')
    
    vehicle = vehicle_hash.search(license_plate)
    
    if vehicle:
        # Find which slot the vehicle is in
        slots = parking_manager.get_all_slots()
        slot_id = None
        
        for slot in slots:
            if slot['is_occupied'] and slot['vehicle']['license_plate'] == license_plate:
                slot_id = slot['slot_id']
                break
        
        return jsonify({
            'found': True,
            'vehicle': vehicle.__dict__,
            'slot_id': slot_id
        })
    else:
        # Check if in waitlist
        waitlist = waitlist_queue.get_all_waitlisted()
        for i, v in enumerate(waitlist):
            if v['license_plate'] == license_plate:
                return jsonify({
                    'found': True,
                    'vehicle': v,
                    'waitlist_position': i + 1
                })
        
        return jsonify({'found': False})

if __name__ == '__main__':
    app.run(debug=True)

    import os
    port = int(os.environ.get("PORT", 5000))  # Get PORT from Render environment
    app.run(host="0.0.0.0", port=port)

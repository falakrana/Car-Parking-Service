# Car Parking Simulation

## Overview
Car Parking Simulation is a project developed using Flask for backend operations and incorporates Data Structures and Algorithms (DSA) concepts such as **Queues, Doubly Linked Lists, and Hash Tables**. This system allows users to efficiently manage parking slots, search for vehicles, and maintain a waitlist queue when slots are full.

## Features
- **Parking Slot Management** (Circular Linked List)
- **Waitlist Queue** (Queue Data Structure)
- **Vehicle Lookup System** (Hash Table)
- **User Interaction Pages**:
  - Home Page
  - About Us Page
  - Contact Us Page
  - Cars Information Page
- **Search Vehicles by License Plate**
- **Dynamic Slot Availability**
- **Waitlist System for Overflow Parking**

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Structures**: Queue, Doubly Linked List, Hash Table

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/falakrana/Car-Parking-Service.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Car-Parking-Service
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python app.py
   ```
5. Open your browser and visit:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure
```
Car-Parking-Service/
│── templates/          # HTML Pages (index, about, contact, cars)
│── static/             # CSS, JS, Images
│── app.py              # Flask Application
│── requirements.txt    # Required dependencies
│── README.md           # Project Documentation
```

## How It Works
1. **Parking Slots Management**:
   - Uses **Circular Linked List** to efficiently track available and occupied parking slots.
2. **Waitlist Queue**:
   - If parking is full, the vehicle is added to a queue using the **Queue Data Structure**.
3. **Vehicle Search System**:
   - A **Hash Table** is used to store and retrieve vehicle information quickly.
4. **Dynamic UI**:
   - Users can interact with the system via an intuitive interface to park or retrieve vehicles.

## Pages
- **Home Page**: Introduction to the system.
- **About Us**: Information about the project.
- **Contact Us**: Users can reach out via a contact form.
- **Cars Information**: Displays parked cars, waitlist, and allows vehicle searches.

## Future Enhancements
- Integration with a **database** for persistent storage.
- Mobile-friendly **responsive design**.
- Additional **security features** like authentication.
- **AI-based parking recommendations**.

## Contact
For any queries, feel free to reach out:
- Email: [ranafalak18@gmail.com](mailto:ranafalak18@gmail.com)
- LinkedIn: [Falak Rana](https://www.linkedin.com/in/falak-rana-125520221/)
- GitHub: [FalakRana](https://github.com/falakrana)


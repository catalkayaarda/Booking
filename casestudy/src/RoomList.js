import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Navigate} from "react-router-dom";



const RoomList = () => {
  const [startDate, setStartDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endDate, setEndDate] = useState('');
  const [endTime, setEndTime] = useState('');
  const [availableRooms, setAvailableRooms] = useState([]);



  function Logout() {
  localStorage.clear();
      window.location.reload();

  return <Navigate to="/logout" />;
}

  useEffect(() => {
    fetchAvailableRooms();
  }, [startDate, startTime, endDate, endTime]);

  const fetchAvailableRooms = async () => {
    try {
      const startDateTime = `${startDate} ${startTime}`;
      const endDateTime = `${endDate} ${endTime}`;

      const response = await axios.get(`http://localhost:8000/api/availablerooms?start_date=${startDateTime}&end_date=${endDateTime}`);
      setAvailableRooms(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleBooking = async (roomId) => {
    try {
      const startDateTime = `${startDate} ${startTime}`;

      const endDateTime = `${endDate} ${endTime}`;

      await axios.post('http://localhost:8000/api/bookroom', {
        room: roomId,
        start_time: startDateTime,
        end_time: endDateTime,
      });

      fetchAvailableRooms();
      alert('Booking successful!');
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to book the room. Please try again.');
    }
  };


  return (
      <div>

        <div className="container mt-5">
          <div className="row">
            <div className="col">
              <div className="form-group">
                <label htmlFor="start-date">Start Date:</label>
                <input
                    type="date"
                    id="start-date"
                    className="form-control"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
                <input
                    type="time"
                    id="start-time"
                    className="form-control mt-2"
                    value={startTime}
                    onChange={(e) => setStartTime(e.target.value)}
                />
              </div>
            </div>
            <div className="col">
              <div className="form-group">
                <label htmlFor="end-date">End Date:</label>
                <input
                    type="date"
                    id="end-date"
                    className="form-control"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
                <input
                    type="time"
                    id="end-time"
                    className="form-control mt-2"
                    value={endTime}
                    onChange={(e) => setEndTime(e.target.value)}
                />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col">
              <button className="btn btn-primary" onClick={fetchAvailableRooms}>Refresh Available Rooms</button>
            </div>
          </div>
          <div className="row mt-3">
            <div className="col">
              <h2>Available Rooms</h2>
              <ul className="list-group">
                {availableRooms.map(room => (
                    <li key={room.id} className="list-group-item">
                      <div>Name: {room.name}</div>
                      <div>Capacity: {room.capacity}</div>
                      <button className="btn btn-success mt-2" onClick={() => handleBooking(room.id)}>Book Room</button>
                    </li>
                ))}
              </ul>
            </div>
          </div>


        </div>

      </div>
  );
};

export default RoomList;

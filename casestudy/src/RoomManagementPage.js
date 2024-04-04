import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Navigate } from 'react-router-dom';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;
const RoomManagementPage = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRooms();
  }, []);

  const token = localStorage.getItem('access_token');

  const fetchRooms = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/rooms',{
      headers: {
        Authorization: `Bearer ${token}`
      }});
      setRooms(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching rooms:', error);
      setLoading(false);
    }
  };
const getCookie = (name) => {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
};
  const deleteRoom = async (roomId) => {
  try {
    // Get the CSRF token from the cookies
    const csrftoken = getCookie('csrftoken');

    // Set the CSRF token in the request headers
    const headers = {
      'X-CSRFToken': csrftoken
    };

    // Send the DELETE request with the CSRF token included in the headers
    await axios.delete(`http://localhost:8000/api/rooms/${roomId}/`, { headers });

    // Remove the deleted room from the state
    setRooms((prevRooms) => prevRooms.filter((room) => room.id !== roomId));
  } catch (error) {
    console.error('Error deleting room:', error);
  }
};

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Room Management</h1>

      <ul className="list-group mt-3">
        {rooms.map((room) => (
          <li key={room.id} className="list-group-item">
            <div>Name: {room.name}</div>
            <div>Capacity: {room.capacity}</div>
            <button
              className="btn btn-danger mt-2"
              onClick={() => deleteRoom(room.id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RoomManagementPage;

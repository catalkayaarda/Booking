import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import RoomList from "./RoomList";
import Register from "./Register";
import RoomManagementPage from "./RoomManagementPage";
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from "axios";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [userrole, setUserRole] = useState(null);

  useEffect(() => {


    client.get("/api/user")
      .then(response => {
        setCurrentUser(response.data);
        setUserRole(response.data.user.userrole); // Assuming userRole is stored in user object as userRole
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching user data:", error);
        setCurrentUser(null);
        setLoading(false);
      });
  }, []);

  function submitLogin(e) {
    e.preventDefault();
    client.post("/api/login", { username, password })
      .then(response => {
        setCurrentUser(response.data);
         // Additional API call to fetch user details (including role)
      client.get("/api/user") // Adjust endpoint if needed
        .then(userResponse => {
          setUserRole(userResponse.data.user.userrole); // Assuming userrole is in user object
          setError(null);
        })
        .catch(error => {
          console.error("Error fetching user data:", error);
          setError("Failed to retrieve user details."); // More specific error message
        });
    })
      .catch(error => {
        console.error("Error logging in:", error);
        setError("Invalid username or password");
      });
  }

  function submitLogout(e) {
    e.preventDefault();
    client.post("/api/logout", { withCredentials: true })
      .then(() => setCurrentUser(null))
      .catch(error => console.error("Error logging out:", error));
  }

  if (loading) {
    return <div>Loading...</div>;
  }


  return (
    <BrowserRouter>
      <div>
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand>Room Booking App</Navbar.Brand>
            {currentUser ? (
              <Navbar.Text>
                <Button onClick={submitLogout} variant="light">Logout</Button>
              </Navbar.Text>
            ) : null}
          </Container>
        </Navbar>
        <Routes>
          <Route path="/" element={currentUser ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
          <Route path="/login" element={currentUser ? <Navigate to="/dashboard" /> :
            <div className="center">
              <Form onSubmit={submitLogin}>
                <h2>Login</h2>
                {error && <p className="text-danger">{error}</p>}
                <Form.Group className="mb-3" controlId="formBasicUsername">
                  <Form.Label>Username</Form.Label>
                  <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3" controlId="formBasicPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form>
            </div>
          } />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={currentUser ? (userrole === "superuser" ? <RoomManagementPage /> : <RoomList />) : <Navigate to="/login" />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;

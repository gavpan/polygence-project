import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../App.css";

function Profile() {
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(function () {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/signin");
      return;
    }

    fetch("http://127.0.0.1:5000/profile", {
      headers: {
        Authorization: "Bearer " + token
      }
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Invalid or expired token");
        }
        return response.json();
      })
      .then(function (data) {
        setProfile(data);
        setLoading(false);
      })
      .catch(function () {
        // Token missing/invalid/expired — clear it and send them to sign in
        localStorage.removeItem("token");
        navigate("/signin");
      });
  }, [navigate]);

  if (loading) {
    return (
      <div className="signin-page">
        <p>Loading your profile...</p>
      </div>
    );
  }

  return (
    <div className="signin-page">
      <div className="signin-card">
        <h1>Your Profile</h1>

        <p className="signin-text">
          Account details tied to your login.
        </p>

        <label>Username</label>
        <input type="text" value={profile.username} disabled />

        <label>User ID</label>
        <input type="text" value={profile.user_id} disabled />

        <label>Joined</label>
        <input type="text" value={profile.created_at} disabled />

        <Link to="/main">
          <button className="back-home-btn">Back to Chat</button>
        </Link>
      </div>
    </div>
  );
}

export default Profile;
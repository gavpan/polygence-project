import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../App.css";

const API_BASE = "http://127.0.0.1:5000";

function SignIn() {
  const navigate = useNavigate();

  const [mode, setMode] = useState("login"); // "login" or "register"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    const endpoint = mode === "login" ? "/login" : "/register";

    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.message || "Something went wrong");
        setLoading(false);
        return;
      }

      if (mode === "login") {
        // Save the JWT so future requests can prove who's logged in
        localStorage.setItem("token", data.token);
        navigate("/main");
      } else {
        // After registering, switch to login mode so they can sign in
        setMode("login");
        setError("Account created! Sign in below.");
        setPassword("");
      }
    } catch (err) {
      setError("Could not reach the server. Is Flask running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="signin-page">
      <div className="signin-card">
        <h1>{mode === "login" ? "Sign In" : "Sign Up"}</h1>

        <p className="signin-text">
          {mode === "login"
            ? "Sign in to save your tasks and schedules."
            : "Create an account to get started."}
        </p>

        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && <p className="signin-text">{error}</p>}

          <button type="submit" className="signin-submit-btn" disabled={loading}>
            {loading ? "Please wait..." : mode === "login" ? "Sign In" : "Sign Up"}
          </button>
        </form>

        <p className="signup-text">
          {mode === "login" ? (
            <>
              Do not have an account?{" "}
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  setMode("register");
                  setError("");
                }}
              >
                Create one
              </a>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  setMode("login");
                  setError("");
                }}
              >
                Sign in
              </a>
            </>
          )}
        </p>

        <Link to="/">
          <button className="back-home-btn">Back Home</button>
        </Link>
      </div>
    </div>
  );
}

export default SignIn;
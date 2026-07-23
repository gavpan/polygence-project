import { Link } from "react-router-dom";
import "../App.css";

function SignIn() {
  return (
    <div className="signin-page">
      <div className="signin-card">
        <h1>Sign In</h1>

        <p className="signin-text">
          Sign in to save your tasks and schedules.
        </p>

        <label>Email</label>
        <input
          type="email"
          placeholder="Enter your email"
        />

        <label>Password</label>
        <input
          type="password"
          placeholder="Enter your password"
        />

        <button className="signin-submit-btn">
          Sign In
        </button>

        <p className="signup-text">
          Do not have an account?{" "}
          <a href="#">Create one</a>
        </p>

        <Link to="/">
          <button className="back-home-btn">
            Back Home
          </button>
        </Link>
      </div>
    </div>
  );
}

export default SignIn;
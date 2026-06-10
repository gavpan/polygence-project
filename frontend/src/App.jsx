import "./App.css";

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <h2>SchedZen</h2>

        <div className="nav-links">
          <a href="#">Home</a>
          <a href="#">About Us</a>
          <a href="#">How It Works</a>
          <a href="#">Roadmap</a>
          <a href="#">Contact</a>
        </div>

        <button className="signin-btn">Sign In</button>
      </nav>

      <main className="hero">
        <h1>Plan Your Time Smarter</h1>

        <h2>Stay Organized, Stress Less</h2>

        <p>
          SchedZen is a web app that helps students organize their
          schoolwork and responsibilities through a chatbot. This
          project gives students a simple way to plan their time.
        </p>

        <button className="start-btn">
          Get Started
        </button>
      </main>
    </div>
  );
}

export default App;

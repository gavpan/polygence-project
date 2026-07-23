import { useState } from "react";
import { Link } from "react-router-dom";
import "../App.css";

function MainPage() {
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! Tell me your tasks, deadlines, estimated times, and available hours."
    }
  ]);

  const [schedule] = useState([]);

  async function sendMessage() {
    if (message.trim() === "") {
      return;
    }

    const currentMessage = message;

    const userMessage = {
      sender: "user",
      text: currentMessage
    };

    setMessages(function (oldMessages) {
      return [...oldMessages, userMessage];
    });

    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: currentMessage
        })
      });

      const data = await response.json();

      const botMessage = {
        sender: "bot",
        text: data.reply
      };

      setMessages(function (oldMessages) {
        return [...oldMessages, botMessage];
      });
    } catch (error) {
      const errorMessage = {
        sender: "bot",
        text: "Sorry, I could not connect to the backend."
      };

      setMessages(function (oldMessages) {
        return [...oldMessages, errorMessage];
      });
    }
  }

  function checkEnter(event) {
    if (event.key === "Enter") {
      sendMessage();
    }
  }

  return (
    <div className="main-chat-page">
      <div className="top-bar">
        <Link to="/">
          <button className="home-button">
            Back Home
          </button>
        </Link>

        <p className="small-logo">
          SchedZen
        </p>
      </div>

      <div className="main-layout">
        <section className="chat-area">
          <div className="chat-title">
            <h1>How can I help you plan today?</h1>

            <p>
              Enter your tasks, deadlines, estimated times, and available hours.
            </p>
          </div>

          <div className="message-area">
            {messages.map(function (item, index) {
              if (item.sender === "user") {
                return (
                  <div className="chat-row user-chat-row" key={index}>
                    <div className="user-chat-message">
                      {item.text}
                    </div>
                  </div>
                );
              }

              return (
                <div className="chat-row bot-chat-row" key={index}>
                  <div className="bot-chat-message">
                    {item.text}
                  </div>
                </div>
              );
            })}
          </div>

          <div className="bottom-input-area">
            <div className="chat-input-box">
              <input
                type="text"
                placeholder="Message SchedZen..."
                value={message}
                onChange={function (event) {
                  setMessage(event.target.value);
                }}
                onKeyDown={checkEnter}
              />

              <button onClick={sendMessage}>
                Send
              </button>
            </div>

            <p className="input-note">
              SchedZen may make mistakes, so check important information.
            </p>
          </div>
        </section>

        <aside className="schedule-panel">
          <div className="schedule-heading">
            <p className="schedule-label">
              YOUR PLAN
            </p>

            <h2>Generated Schedule</h2>
          </div>

          {schedule.length === 0 ? (
            <div className="empty-schedule">
              <div className="schedule-icon">
                ✓
              </div>

              <h3>No schedule yet</h3>

              <p>
                Your generated schedule will appear here.
              </p>
            </div>
          ) : (
            <div className="schedule-list">
              {schedule.map(function (scheduleItem, index) {
                return (
                  <div className="schedule-item" key={index}>
                    {scheduleItem}
                  </div>
                );
              })}
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

export default MainPage;
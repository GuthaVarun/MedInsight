import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "http://127.0.0.1:5000";

function App() {
  const [city, setCity] = useState("");
  const [rating, setRating] = useState("");
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const searchHospitals = async () => {
    setLoading(true);
    setError("");

    try {
      const params = {};

      if (city.trim()) {
        params.city = city.trim();
      }

      if (rating) {
        params.min_rating = rating;
      }

      const response = await axios.get(`${API_BASE}/api/hospitals`, {
        params,
      });

      setHospitals(response.data.hospitals || []);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the hospital service.");
      setHospitals([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>MedInsight</h1>
        <p>Find hospitals using location and rating</p>
      </header>

      <main>
        <section className="search-box">
          <h2>Hospital Search</h2>

          <div className="filters">
            <input
              type="text"
              placeholder="Enter city"
              value={city}
              onChange={(event) => setCity(event.target.value)}
            />

            <select
              value={rating}
              onChange={(event) => setRating(event.target.value)}
            >
              <option value="">Any rating</option>
              <option value="4">4+ rating</option>
              <option value="4.5">4.5+ rating</option>
            </select>

            <button onClick={searchHospitals} disabled={loading}>
              {loading ? "Searching..." : "Search Hospitals"}
            </button>
          </div>

          {error && <p className="error">{error}</p>}
        </section>

        <section className="results">
          <h2>Results</h2>

          {!loading && hospitals.length === 0 && !error && (
            <p>Enter a city and click Search Hospitals.</p>
          )}

          {hospitals.map((hospital) => (
            <div className="hospital-card" key={hospital.id}>
              <h3>{hospital.id}</h3>

              <p>
                <strong>Location:</strong>{" "}
                {hospital.city}, {hospital.state}
              </p>

              <p>
                <strong>District:</strong> {hospital.district}
              </p>

              <p>
                <strong>Rating:</strong> ⭐ {hospital.rating}
              </p>

              <p>
                <strong>Reviews:</strong>{" "}
                {hospital.number_of_reviews}
              </p>

              <p>
                <strong>Coordinates:</strong>{" "}
                {hospital.latitude}, {hospital.longitude}
              </p>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}

export default App;

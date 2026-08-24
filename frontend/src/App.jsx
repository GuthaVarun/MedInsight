import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "http://127.0.0.1:5000";

function App() {
  // =========================
  // Hospital Search
  // =========================

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

  // =========================
  // Doctor Search
  // =========================

  const [doctorName, setDoctorName] = useState("");
  const [specialization, setSpecialization] = useState("");
  const [hospital, setHospital] = useState("");
  const [minExperience, setMinExperience] = useState("");

  const [doctors, setDoctors] = useState([]);
  const [doctorLoading, setDoctorLoading] = useState(false);
  const [doctorError, setDoctorError] = useState("");

  const searchDoctors = async () => {
    setDoctorLoading(true);
    setDoctorError("");

    try {
      const params = {};

      if (doctorName.trim()) {
        params.name = doctorName.trim();
      }

      if (specialization.trim()) {
        params.specialization = specialization.trim();
      }

      if (hospital.trim()) {
        params.hospital = hospital.trim();
      }

      if (minExperience) {
        params.min_experience = minExperience;
      }

      const response = await axios.get(`${API_BASE}/api/doctors`, {
        params,
      });

      setDoctors(response.data.doctors || []);
    } catch (err) {
      console.error(err);
      setDoctorError("Unable to connect to the doctor service.");
      setDoctors([]);
    } finally {
      setDoctorLoading(false);
    }
  };

  // =========================
  // Emergency Search
  // =========================

  const [emergencyCity, setEmergencyCity] = useState("");
  const [emergencyState, setEmergencyState] = useState("");
  const [emergencyRating, setEmergencyRating] = useState("");

  const [emergencyHospitals, setEmergencyHospitals] = useState([]);
  const [emergencyNotice, setEmergencyNotice] = useState("");
  const [emergencyLoading, setEmergencyLoading] = useState(false);
  const [emergencyError, setEmergencyError] = useState("");

  const searchEmergencyHospitals = async () => {
    setEmergencyLoading(true);
    setEmergencyError("");
    setEmergencyNotice("");

    try {
      const params = {};

      if (emergencyCity.trim()) {
        params.city = emergencyCity.trim();
      }

      if (emergencyState.trim()) {
        params.state = emergencyState.trim();
      }

      if (emergencyRating) {
        params.min_rating = emergencyRating;
      }

      const response = await axios.get(`${API_BASE}/api/emergency`, {
        params,
      });

      setEmergencyHospitals(response.data.hospitals || []);
      setEmergencyNotice(response.data.notice || "");
    } catch (err) {
      console.error(err);
      setEmergencyError(
        "Unable to connect to the emergency hospital service."
      );
      setEmergencyHospitals([]);
    } finally {
      setEmergencyLoading(false);
    }
  };

  return (
    <div className="app">
      {/* =========================
          Header
      ========================= */}

      <header className="header">
        <h1>MedInsight</h1>
        <p>Find hospitals, doctors and emergency hospitals</p>
      </header>

      <main>
        {/* =========================
            Hospital Search
        ========================= */}

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

        {/* =========================
            Hospital Results
        ========================= */}

        <section className="results">
          <h2>Hospital Results</h2>

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

        {/* =========================
            Doctor Search
        ========================= */}

        <section className="search-box">
          <h2>Doctor Search</h2>

          <div className="filters">
            <input
              type="text"
              placeholder="Doctor name"
              value={doctorName}
              onChange={(event) => setDoctorName(event.target.value)}
            />

            <input
              type="text"
              placeholder="Specialization"
              value={specialization}
              onChange={(event) =>
                setSpecialization(event.target.value)
              }
            />

            <input
              type="text"
              placeholder="Hospital"
              value={hospital}
              onChange={(event) => setHospital(event.target.value)}
            />

            <input
              type="number"
              min="0"
              placeholder="Minimum experience"
              value={minExperience}
              onChange={(event) =>
                setMinExperience(event.target.value)
              }
            />

            <button onClick={searchDoctors} disabled={doctorLoading}>
              {doctorLoading ? "Searching..." : "Search Doctors"}
            </button>
          </div>

          {doctorError && <p className="error">{doctorError}</p>}
        </section>

        {/* =========================
            Doctor Results
        ========================= */}

        <section className="results">
          <h2>Doctor Results</h2>

          {!doctorLoading &&
            doctors.length === 0 &&
            !doctorError && (
              <p>
                Enter search criteria and click Search Doctors.
              </p>
            )}

          {doctors.map((doctor) => (
            <div
              className="hospital-card"
              key={doctor.doctor_id}
            >
              <h3>
                {doctor.first_name} {doctor.last_name}
              </h3>

              <p>
                <strong>Specialization:</strong>{" "}
                {doctor.specialization}
              </p>

              <p>
                <strong>Experience:</strong>{" "}
                {doctor.years_experience} years
              </p>

              <p>
                <strong>Hospital:</strong>{" "}
                {doctor.hospital_branch}
              </p>

              <p>
                <strong>Phone:</strong>{" "}
                {doctor.phone_number}
              </p>

              <p>
                <strong>Email:</strong>{" "}
                {doctor.email}
              </p>
            </div>
          ))}
        </section>

        {/* =========================
            Emergency Hospital Search
        ========================= */}

        <section className="search-box emergency-section">
          <h2>🚨 Emergency Hospital Search</h2>

          <p>
            Find highly rated hospitals by city or state for
            emergency-care reference.
          </p>

          <div className="filters">
            <input
              type="text"
              placeholder="Enter city"
              value={emergencyCity}
              onChange={(event) =>
                setEmergencyCity(event.target.value)
              }
            />

            <input
              type="text"
              placeholder="Enter state"
              value={emergencyState}
              onChange={(event) =>
                setEmergencyState(event.target.value)
              }
            />

            <select
              value={emergencyRating}
              onChange={(event) =>
                setEmergencyRating(event.target.value)
              }
            >
              <option value="">Any rating</option>
              <option value="4">4+ rating</option>
              <option value="4.5">4.5+ rating</option>
            </select>

            <button
              onClick={searchEmergencyHospitals}
              disabled={emergencyLoading}
            >
              {emergencyLoading
                ? "Searching..."
                : "Find Emergency Hospitals"}
            </button>
          </div>

          {emergencyError && (
            <p className="error">{emergencyError}</p>
          )}

          {emergencyNotice && (
            <p className="notice">
              ⚠️ {emergencyNotice}
            </p>
          )}
        </section>

        {/* =========================
            Emergency Results
        ========================= */}

        <section className="results">
          <h2>Emergency Hospital Results</h2>

          {!emergencyLoading &&
            emergencyHospitals.length === 0 &&
            !emergencyError && (
              <p>
                Enter a city or state and click Find Emergency
                Hospitals.
              </p>
            )}

          {emergencyHospitals.map((hospital) => (
            <div className="hospital-card" key={hospital.id}>
              <h3>{hospital.id}</h3>

              <p>
                <strong>Location:</strong>{" "}
                {hospital.city}, {hospital.state}
              </p>

              <p>
                <strong>District:</strong>{" "}
                {hospital.district}
              </p>

              <p>
                <strong>Rating:</strong> ⭐{" "}
                {hospital.rating}
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

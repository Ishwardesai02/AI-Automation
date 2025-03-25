import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  // Handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handle form submission
  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Send file to FastAPI backend
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze-code",
        formData
      );
      setResult(response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to analyze file.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "50px" }}>
      <h2>🚀 AI Code Quality Analyzer</h2>
      <input type="file" onChange={handleFileChange} />
      <br />
      <button
        onClick={handleSubmit}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          backgroundColor: "#4caf50",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Analyze Code
      </button>

      {result && (
        <div style={{ marginTop: "30px", textAlign: "left" }}>
          <h3>✅ Analysis Results:</h3>
          <pre
            style={{
              backgroundColor: "#f4f4f4",
              padding: "10px",
              borderRadius: "5px",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;


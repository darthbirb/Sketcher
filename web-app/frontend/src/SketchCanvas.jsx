import React, { useRef, useState } from "react";
import CanvasDraw from "react-canvas-draw";
import axios from "axios";

const SketchCanvas = () => {
  const canvasRef = useRef(null);
  const [predictions, setPredictions] = useState([]);

  const handleClear = () => {
    canvasRef.current.clear();
    setPredictions([]);
  };

  const handlePredict = async () => {
    const canvas = canvasRef.current.canvas.drawing;
    const imageData = canvas.toDataURL("image/png").split(",")[1];

    try {
      const response = await axios.post("/predict", { image: imageData });
      setPredictions(response.data.predictions);
    } catch (error) {
      console.error("Prediction error:", error);
    }
  };

  return (
    <div>
      <h1>Sketcher <span style={{ fontSize: "16px" }}>(not the shoes!)</span></h1>
      <CanvasDraw ref={canvasRef} brushRadius={3} />
      <button onClick={handleClear}>Clear</button>
      <button onClick={handlePredict}>Predict</button>
      <div>
        {predictions.length > 0 && (
          <ul>
            {predictions.map((pred, index) => (
              <li key={index}>
                {pred[0]} - {Math.round(pred[1] * 100)}%
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default SketchCanvas;

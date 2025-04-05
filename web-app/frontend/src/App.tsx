import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
// @ts-ignore
import SketchCanvas from "./components/SketchCanvas";

type SketchCanvasHandle = {
  clearCanvas: () => void;
  exportImage: () => Promise<string>;
};

function App() {
  const canvasRef = useRef<SketchCanvasHandle | null>(null);
  const [predictions, setPredictions] = useState<[string, number][]>([]);

  const handleClear = () => {
    canvasRef.current?.clearCanvas();
  };

  const handleSubmit = async () => {
    const base64 = await canvasRef.current?.exportImage();
    if (!base64) return;
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: base64.split(",")[1] }), // remove "data:image/..."
    });
    const result = await response.json();
    setPredictions(result.predictions);
  };

  return (
    <div className="min-h-screen bg-[#212121] text-white font-sans">
      {/* Header */}
      <header className="p-6">
        <h1 className="text-4xl font-bold text-white inline">Sketcher</h1>
        <span className="text-orange-400 text-md ml-3">(not the shoes)</span>
      </header>

      {/* Main layout */}
      <main className="flex justify-center items-start p-8 gap-10">
        {/* Canvas and Buttons */}
        <div className="flex flex-col items-center">
          <SketchCanvas ref={canvasRef} />

          <div className="flex gap-4 mt-4">
            <Button variant="outline" onClick={handleClear}>
              Clear
            </Button>
            <Button onClick={handleSubmit}>Submit</Button>
          </div>
        </div>

        {/* Prediction Table */}
        <div className="bg-[#2c2c2c] rounded-xl p-6 shadow-lg w-64">
          <h2 className="text-xl font-semibold mb-4">Predictions</h2>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-400">
                <th>Label</th>
                <th className="text-right">Confidence</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map(([label, value], index) => (
                <tr key={index}>
                  <td className="py-1">{label}</td>
                  <td className="py-1 text-right">{(value * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

export default App;

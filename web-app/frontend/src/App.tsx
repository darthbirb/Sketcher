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
  const [hasDrawn, setHasDrawn] = useState(false);

  const handleClear = () => {
    canvasRef.current?.clearCanvas();
    setPredictions([]);
    setHasDrawn(false);
  };

  const handleSubmit = async () => {
    const base64 = await canvasRef.current?.exportImage();
    if (!base64) return;
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: base64.split(",")[1] }),
    });
    const result = await response.json();
    setPredictions([...result.predictions]);
  };

  return (
    <div className="min-h-screen bg-[#212121] text-white font-sans flex flex-col items-center px-4 py-8">
      <h1 className="text-5xl font-bold text-center mb-2">Sketcher</h1>
      <p className="text-center text-lg text-gray-400 mb-8">
        Not the shoe! – Draw something for the model to recognize
      </p>

      <div className="relative">
        {!hasDrawn && (
          <div className="absolute z-10 w-full h-full flex items-center justify-center pointer-events-none">
            <p className="text-gray-400 text-lg">Draw something here</p>
          </div>
        )}
        <div
          onPointerDown={() => setHasDrawn(true)}
          className="bg-white rounded-xl"
          style={{ boxShadow: 'none', border: 'none' }}
        >
          <SketchCanvas ref={canvasRef} />
        </div>
      </div>

      {/* Buttons with fade-in effect */}
      <div
        className={`flex gap-4 mt-4 transition-opacity duration-500 ${
          hasDrawn ? "opacity-100" : "opacity-0"
        }`}
      >
        <Button
          variant={"destructive"}
          onClick={handleClear}
          disabled={!hasDrawn}
          className="w-32"
        >
          Clear
        </Button>
        <Button
          onClick={handleSubmit}
          disabled={!hasDrawn}
          className="w-32"
        >
          Predict
        </Button>
      </div>

      {predictions.length > 0 && (
        <div className="mt-8 w-[400px]">
          <div className="grid grid-cols-3 gap-2 text-center text-sm text-gray-400">
            {predictions.map(([label], index) => (
              <div key={index}>{label}</div>
            ))}
          </div>
          <div className="grid grid-cols-3 gap-2 text-center text-lg font-medium mt-1">
            {predictions.map(([_, confidence], index) => (
              <div key={index}>{(confidence * 100).toFixed(1)}%</div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-12 text-center text-sm text-gray-500 opacity-50">
        <p className="mb-1">
          Want to build an app like this? Fork it on{" "}
          <a href="https://github.com" className="underline text-white">
            GitHub
          </a>
        </p>
        <p>Powered by TensorFlow and React</p>
      </div>
    </div>
  );
}

export default App;
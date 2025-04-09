import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
// @ts-ignore
import SocialSidebar from "./components/ui/SocialSidebar";
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
    <div className="min-h-screen bg-[#0f0f0f] text-white font-sans flex flex-col items-center px-4 py-8">
      <SocialSidebar />

      <img
        src="/sketcher.png"
        alt="Sketcher"
        className="h-18 mb-2 invert"
      />

      <p className="text-center text-lg text-gray-400 mb-4">
        Sketch something for the model to identify
      </p>

      <div className="relative">
        {!hasDrawn && (
          <div className="absolute z-10 w-full h-full flex items-center justify-center pointer-events-none">
            <p className="text-gray-400 text-lg">Draw something here!</p>
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
        <div className="mt-8 w-[400px] max-w-full">
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

      <div className="mt-6 text-center text-sm text-gray-400">
        <p className="mb-1">
          Not to be confused with the shoes! Check out the code on{" "}
          <a
            href="https://github.com/darthbirb/Sketcher"
            className="underline text-white"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </p>
        <p>
          Based on the{" "}
          <a
            href="https://github.com/googlecreativelab/quickdraw-dataset"
            className="underline text-white"
            target="_blank"
            rel="noopener noreferrer"
          >
            Google Quick, Draw! Dataset
          </a>
        </p>
      </div>
    </div>
  );
}

export default App;
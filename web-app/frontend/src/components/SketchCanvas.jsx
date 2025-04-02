import React, { useRef } from "react";
import { ReactSketchCanvas } from "react-sketch-canvas";

const SketchCanvas = () => {
  const canvasRef = useRef(null);

  return (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-2">Draw Here</h2>
      <ReactSketchCanvas
        ref={canvasRef}
        width="400px"
        height="400px"
        strokeWidth={4}
        strokeColor="black"
        className="border-2 border-gray-300 rounded-lg"
      />
      <div className="mt-2 space-x-2">
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded"
          onClick={() => canvasRef.current?.clearCanvas()}
        >
          Clear
        </button>
        <button
          className="px-4 py-2 bg-green-500 text-white rounded"
          onClick={async () => {
            const data = await canvasRef.current?.exportPaths();
            console.log("Sketch Data:", data);
          }}
        >
          Export
        </button>
      </div>
    </div>
  );
};

export default SketchCanvas;

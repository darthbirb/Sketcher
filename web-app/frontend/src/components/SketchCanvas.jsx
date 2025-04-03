import React, { useEffect, useRef } from "react";
import { ReactSketchCanvas } from "react-sketch-canvas";

const SketchCanvas = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    // Firefox Bug Fix: Remove the 'mask' attribute from the first stroke group
    const removeMask = () => {
      document
        .querySelector("#react-sketch-canvas__stroke-group-0")
        ?.removeAttribute("mask");
    };

    // Try removing mask every time the canvas updates (ensures fix persists)
    const interval = setInterval(removeMask, 500);

    return () => clearInterval(interval); // Cleanup interval when component unmounts
  }, []);

  return (
    <div className="canvas-wrapper">
      <ReactSketchCanvas
        ref={canvasRef}
        width="600px"
        height="400px"
        strokeWidth={4}
        strokeColor="black"
      />
    </div>
  );
};

export default SketchCanvas;

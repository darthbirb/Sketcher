import React, { useEffect, useRef, forwardRef, useImperativeHandle } from "react";
import { ReactSketchCanvas } from "react-sketch-canvas";

const SketchCanvas = forwardRef((props, ref) => {
  const canvasRef = useRef(null);

  useImperativeHandle(ref, () => ({
    clearCanvas: () => canvasRef.current?.clearCanvas(),
    exportImage: () => canvasRef.current?.exportImage("png"),
  }));

  useEffect(() => {
    const removeMask = () => {
      document
        .querySelector("#react-sketch-canvas__stroke-group-0")
        ?.removeAttribute("mask");
    };

    const interval = setInterval(removeMask, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white rounded-xl p-2 shadow-md">
      <ReactSketchCanvas
        ref={canvasRef}
        width="400px"
        height="400px"
        strokeWidth={4}
        strokeColor="black"
        style={{ borderRadius: "1rem" }}
      />
    </div>
  );
});

export default SketchCanvas;

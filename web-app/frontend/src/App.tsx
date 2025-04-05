import React from 'react';
// @ts-ignore
import SketchCanvas from './components/SketchCanvas';
import { Button } from "@/components/ui/button";

function App() {
  return (
    <div className="app-container">
      {/* Sidebar (for future tabs/buttons) */}
      <div className="sidebar">
        <h2>Menu</h2>
        <ul>
          <li>Tab 1</li>
          <li>Tab 2</li>
          <li>Tab 3</li>
        </ul>
        <Button variant="outline" className="mt-4">Click Me</Button>
      </div>

      {/* Main content area */}
      <div className="main-content">
        <SketchCanvas />
      </div>
    </div>
  );
}

export default App;
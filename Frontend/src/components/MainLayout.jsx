import React, { useState } from "react";

import Sidebar from "./Sidebar";
import MobileHeader from "./MobileHeader";

function MainLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div
      className="
h-screen
bg-[#f8f5ef]
flex
overflow-hidden
"
    >
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div
        className="
flex-1
flex
flex-col
min-w-0
"
      >
        <MobileHeader onMenu={() => setSidebarOpen(true)} />

        <main
          className="
flex-1
overflow-y-auto

p-4
sm:p-6
lg:p-8

"
        >
          {children}
        </main>
      </div>
    </div>
  );
}

export default MainLayout;

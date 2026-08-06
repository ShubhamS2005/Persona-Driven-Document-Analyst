import React, { useState } from "react";

import Sidebar from "./Sidebar";
import MobileHeader from "./MobileHeader";

function MainLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div
      className="
        min-h-screen
        flex

        bg-gradient-to-br
        from-stone-50
        via-amber-50
        to-orange-50
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
            overflow-auto

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

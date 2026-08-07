import React from "react";

import { Menu, Brain, UserCircle2 } from "lucide-react";

import { useLocation } from "react-router-dom";
import logo from "../assets/logo.png";

const pageTitles = {
  "/dashboard": "Dashboard",
  "/ask": "Ask Assistant",
  "/documents": "Documents",
  "/history": "History",
  "/settings": "Settings",
};

function MobileHeader({ onMenu }) {
  const location = useLocation();

  const title = pageTitles[location.pathname] || "Persona RAG";

  return (
    <header
      className="
        lg:hidden

        sticky
        top-0
        z-40

        h-16

        px-4

        flex
        items-center
        justify-between

        bg-white/90
        backdrop-blur-xl

        border-b
        border-stone-200

        shadow-sm
      "
    >
      {/* Left */}

      <div className="flex items-center gap-3">
        <button
          onClick={onMenu}
          className="
            p-2

            rounded-xl

            hover:bg-stone-100

            active:scale-95

            transition
          "
        >
          <Menu size={24} className="text-stone-700" />
        </button>

        <div className="flex items-center gap-3">
          <div
            className="
              p-2

              rounded-xl

              bg-amber-100

              border
              border-amber-200
            "
          >
            <img src={logo} className="w-6 h-6 object-contain" />
          </div>

          <div>
            <h1 className="font-bold text-stone-900">Persona RAG</h1>

            <p className="text-xs text-stone-500">{title}</p>
          </div>
        </div>
      </div>

      {/* Right */}

      <button
        className="
          rounded-full

          p-1

          hover:bg-stone-100

          transition
        "
      >
        <UserCircle2 size={34} className="text-amber-700" />
      </button>
    </header>
  );
}

export default MobileHeader;

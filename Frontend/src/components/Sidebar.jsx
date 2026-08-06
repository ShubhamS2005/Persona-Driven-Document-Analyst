import React from "react";

import { NavLink } from "react-router-dom";

import {
  LayoutDashboard,
  MessageSquare,
  FileText,
  History,
  Settings,
  Brain,
  X,
} from "lucide-react";

const menuItems = [
  {
    title: "Dashboard",
    path: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Ask Assistant",
    path: "/ask",
    icon: MessageSquare,
  },
  {
    title: "Documents",
    path: "/documents",
    icon: FileText,
  },
  {
    title: "History",
    path: "/history",
    icon: History,
  },
  {
    title: "Settings",
    path: "/settings",
    icon: Settings,
  },
];

function Sidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Overlay */}

      {isOpen && (
        <div
          className="
            fixed
            inset-0
            z-40

            bg-black/30
            backdrop-blur-sm

            lg:hidden
          "
          onClick={onClose}
        />
      )}

      <aside
        className={`
          fixed
          lg:relative

          top-0
          left-0

          z-50

          h-screen
          w-72

          bg-white

          border-r
          border-stone-200

          flex
          flex-col
          justify-between

          transition-transform
          duration-300

          ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
        `}
      >
        <div>
          {/* Header */}

          <div
            className="
              px-6
              py-6

              border-b
              border-stone-200
            "
          >
            <div className="flex justify-end lg:hidden mb-4">
              <button
                onClick={onClose}
                className="
                  p-2

                  rounded-lg

                  hover:bg-stone-100

                  transition
                "
              >
                <X size={22} className="text-stone-700" />
              </button>
            </div>

            <div className="flex items-center gap-3">
              <div
                className="
                  p-3

                  rounded-xl

                  bg-amber-100

                  border
                  border-amber-200
                "
              >
                <Brain size={28} className="text-amber-700" />
              </div>

              <div>
                <h1 className="text-xl font-bold text-stone-900">
                  Persona RAG
                </h1>

                <p className="text-xs text-stone-500">Document Intelligence</p>
              </div>
            </div>
          </div>

          {/* Navigation */}

          <nav className="px-4 mt-6">
            {menuItems.map((item) => (
              <NavLink
                key={item.title}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) => `
                  flex
                  items-center
                  gap-4

                  px-4
                  py-3

                  mb-2

                  rounded-xl

                  transition

                  ${
                    isActive
                      ? "bg-amber-100 text-amber-800 font-semibold"
                      : "text-stone-600 hover:bg-stone-100 hover:text-stone-900"
                  }
                `}
              >
                <item.icon size={20} />

                <span>{item.title}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Footer */}

        <div
          className="
            p-5

            border-t
            border-stone-200
          "
        >
          <div
            className="
              rounded-xl

              bg-stone-50

              border
              border-stone-200

              p-4
            "
          >
            <div className="flex justify-between items-center">
              <span className="text-sm text-stone-500">API Status</span>

              <span
                className="
                  h-3
                  w-3

                  rounded-full

                  bg-green-500
                "
              />
            </div>

            <p className="mt-2 font-semibold text-green-700">Operational</p>

            <p className="mt-1 text-xs text-stone-500">
              Connected to Flask API
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;

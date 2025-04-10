import { useState } from "react";

const links = [
  { name: "GitHub", src: "/github.svg", href: "https://github.com/darthbirb/Sketcher" },
  { name: "LinkedIn", src: "/linkedin.svg", href: "https://www.linkedin.com/in/amr-m-fawzy/" },
  { name: "Quick, Draw!", src: "/quickdraw.svg", href: "https://quickdraw.withgoogle.com/" },
];

const SocialSidebar = () => {
  const [hovered, setHovered] = useState<string | null>(null);

  return (
    <div className="hidden md:flex fixed left-4 top-1/2 -translate-y-1/2 flex-col items-center gap-6 z-50">
      {links.map(({ name, src, href }) => (
        <a
          key={name}
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          onMouseEnter={() => setHovered(name)}
          onMouseLeave={() => setHovered(null)}
          className="flex flex-col items-center group"
        >
          <img
            src={src}
            alt={name}
            className={`w-10 h-10 transition-all duration-300 
              grayscale hover:grayscale-0
              ${hovered === name ? "scale-125" : "scale-100"}`}
          />
          <span
            className={`text-sm text-gray-400 mt-2 transition-opacity duration-300 
              ${hovered === name ? "opacity-100" : "opacity-0"}`}
          >
            {name}
          </span>
        </a>
      ))}
    </div>
  );
};

export default SocialSidebar;
